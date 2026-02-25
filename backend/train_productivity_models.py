"""Train the productivity detection model using Linear Regression only."""

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

DATASET_PATH = Path('dataset/productivity_dataset.csv')
ARTIFACTS_DIR = Path('artifacts')
LINEAR_MODEL_PATH = ARTIFACTS_DIR / 'linear_regression_best_model.pkl'
DETECTION_MODEL_PATH = ARTIFACTS_DIR / 'productivity_detection_model.pkl'


def create_preprocessor(x: pd.DataFrame) -> ColumnTransformer:
    numerical_features = x.select_dtypes(include=[np.number]).columns.tolist()
    categorical_features = [col for col in x.columns if col not in numerical_features]

    numerical_pipeline = Pipeline(
        steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler()),
        ]
    )
    categorical_pipeline = Pipeline(
        steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('onehot', OneHotEncoder(handle_unknown='ignore')),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ('num', numerical_pipeline, numerical_features),
            ('cat', categorical_pipeline, categorical_features),
        ]
    )


def main() -> None:
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(DATASET_PATH)
    df = df.drop(columns=['student_id'])

    target_col = 'productivity_score'
    x = df.drop(columns=[target_col])
    y = df[target_col]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    pipeline = Pipeline(
        steps=[
            ('preprocessor', create_preprocessor(x_train)),
            ('model', LinearRegression()),
        ]
    )

    print('Training linear regression model for productivity detection...')
    pipeline.fit(x_train, y_train)

    predictions = pipeline.predict(x_test)
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    joblib.dump(pipeline, LINEAR_MODEL_PATH)
    joblib.dump(pipeline, DETECTION_MODEL_PATH)

    print('Training complete.')
    print(f'MAE: {mae:.4f}')
    print(f'R2:  {r2:.4f}')
    print(f'Saved model to: {LINEAR_MODEL_PATH}')
    print(f'Saved detection model to: {DETECTION_MODEL_PATH}')


if __name__ == '__main__':
    main()
