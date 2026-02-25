from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import (
    ExtraTreesRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

RANDOM_STATE = 42
TARGET_COLUMN = "G3"
LEAKAGE_COLUMNS = ["G1", "G2"]


def load_student_data(student_dir: Path) -> pd.DataFrame:
    math_df = pd.read_csv(student_dir / "student-mat.csv", sep=";")
    math_df["subject"] = "math"

    portuguese_df = pd.read_csv(student_dir / "student-por.csv", sep=";")
    portuguese_df["subject"] = "portuguese"

    data = pd.concat([math_df, portuguese_df], ignore_index=True)
    data = data.drop_duplicates().reset_index(drop=True)

    numeric_cols = [
        "age",
        "Medu",
        "Fedu",
        "traveltime",
        "studytime",
        "failures",
        "famrel",
        "freetime",
        "goout",
        "Dalc",
        "Walc",
        "health",
        "absences",
        "G1",
        "G2",
        "G3",
    ]
    for col in numeric_cols:
        data[col] = pd.to_numeric(data[col], errors="coerce")

    data = data.dropna(subset=[TARGET_COLUMN]).reset_index(drop=True)
    return data


def build_preprocessor(features: pd.DataFrame) -> ColumnTransformer:
    numeric_features = features.select_dtypes(include=[np.number]).columns.tolist()
    categorical_features = [
        col for col in features.columns if col not in numeric_features
    ]

    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
        ]
    )
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, numeric_features),
            ("cat", categorical_pipeline, categorical_features),
        ]
    )


def tune_and_select_model(
    features_train: pd.DataFrame,
    target_train: pd.Series,
    preprocessor: ColumnTransformer,
) -> RandomizedSearchCV:
    candidates = {
        "random_forest": {
            "model": RandomForestRegressor(random_state=RANDOM_STATE, n_jobs=-1),
            "params": {
                "model__n_estimators": [300, 500, 700],
                "model__max_depth": [None, 10, 20, 30],
                "model__min_samples_leaf": [1, 2, 4],
                "model__max_features": ["sqrt", "log2", None],
            },
        },
        "extra_trees": {
            "model": ExtraTreesRegressor(random_state=RANDOM_STATE, n_jobs=-1),
            "params": {
                "model__n_estimators": [300, 500, 700],
                "model__max_depth": [None, 10, 20, 30],
                "model__min_samples_leaf": [1, 2, 4],
                "model__max_features": ["sqrt", "log2", None],
            },
        },
        "gradient_boosting": {
            "model": GradientBoostingRegressor(random_state=RANDOM_STATE),
            "params": {
                "model__n_estimators": [150, 250, 400],
                "model__learning_rate": [0.03, 0.05, 0.1],
                "model__max_depth": [2, 3, 4],
                "model__subsample": [0.8, 1.0],
            },
        },
    }

    best_search = None
    best_score = -np.inf

    for name, config in candidates.items():
        pipeline = Pipeline(
            steps=[
                ("preprocess", preprocessor),
                ("model", config["model"]),
            ]
        )

        search = RandomizedSearchCV(
            estimator=pipeline,
            param_distributions=config["params"],
            n_iter=12,
            scoring="neg_root_mean_squared_error",
            cv=5,
            random_state=RANDOM_STATE,
            n_jobs=-1,
            verbose=0,
        )
        search.fit(features_train, target_train)

        if search.best_score_ > best_score:
            best_score = search.best_score_
            best_search = search

        print(
            f"[{name}] best CV RMSE: {-search.best_score_:.3f} | params: {search.best_params_}"
        )

    if best_search is None:
        raise RuntimeError("Model search did not produce a valid trained model.")

    return best_search


def create_relationship_reports(data: pd.DataFrame, output_dir: Path) -> None:
    numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
    if TARGET_COLUMN in numeric_cols:
        corr = (
            data[numeric_cols]
            .corr(numeric_only=True)[TARGET_COLUMN]
            .sort_values(ascending=False)
        )
        corr.rename("correlation_with_G3").to_csv(
            output_dir / "numeric_relationships.csv"
        )

    categorical_cols = [
        c for c in data.columns if c not in numeric_cols and c not in [TARGET_COLUMN]
    ]
    categorical_summary_rows = []
    for col in categorical_cols:
        grouped = (
            data.groupby(col, dropna=False)[TARGET_COLUMN]
            .agg(["mean", "count"])
            .sort_values("mean", ascending=False)
            .reset_index()
        )
        grouped["feature"] = col
        grouped = grouped.rename(columns={col: "category", "mean": "target_mean"})
        categorical_summary_rows.append(
            grouped[["feature", "category", "target_mean", "count"]]
        )

    if categorical_summary_rows:
        pd.concat(categorical_summary_rows, ignore_index=True).to_csv(
            output_dir / "categorical_relationships.csv", index=False
        )


def train_pipeline(project_root: Path) -> dict:
    student_dir = project_root / "student"
    output_dir = project_root / "artifacts"
    output_dir.mkdir(parents=True, exist_ok=True)

    data = load_student_data(student_dir)

    features = data.drop(columns=[TARGET_COLUMN] + LEAKAGE_COLUMNS)
    target = data[TARGET_COLUMN]

    features_train, features_test, target_train, target_test = train_test_split(
        features,
        target,
        test_size=0.2,
        random_state=RANDOM_STATE,
    )

    preprocessor = build_preprocessor(features_train)
    best_search = tune_and_select_model(features_train, target_train, preprocessor)

    best_model = best_search.best_estimator_
    predictions = best_model.predict(features_test)

    metrics = {
        "mae": float(mean_absolute_error(target_test, predictions)),
        "rmse": float(np.sqrt(mean_squared_error(target_test, predictions))),
        "r2": float(r2_score(target_test, predictions)),
        "best_cv_rmse": float(-best_search.best_score_),
    }

    model_path = output_dir / "student_grade_predictor.joblib"
    joblib.dump(best_model, model_path)

    create_relationship_reports(data, output_dir)

    metadata = {
        "target": TARGET_COLUMN,
        "dropped_columns": LEAKAGE_COLUMNS,
        "train_rows": int(len(features_train)),
        "test_rows": int(len(features_test)),
        "model_path": str(model_path),
        "best_params": best_search.best_params_,
        "metrics": metrics,
    }

    with (output_dir / "training_summary.json").open("w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=2)

    return metadata


def load_model_and_predict(model_path: Path, single_record: dict) -> float:
    model = joblib.load(model_path)
    inference_df = pd.DataFrame([single_record])
    prediction = model.predict(inference_df)[0]
    return float(prediction)


if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    summary = train_pipeline(root)

    print("\nFinal evaluation metrics:")
    for key, value in summary["metrics"].items():
        print(f"- {key}: {value:.4f}")

    print(f"\nModel artifact: {summary['model_path']}")
    print("Training summary: artifacts/training_summary.json")
