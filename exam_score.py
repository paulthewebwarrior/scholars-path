import numpy as np
import pandas as pd
import tensorflow as tf
from keras import Sequential
from keras.src.layers import Dense, InputLayer
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

out_dir = "artifacts"
in_dir = "student"


def build_preprocessor(features: pd.DataFrame):
    numeric_features = features.select_dtypes(include=[np.number]).columns.tolist()
    cat_features = [
        col for col in features.columns if col not in numeric_features
    ]

    numeric_pipe = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="mean"))
        ]
    )
    cat_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore"))
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("num", numeric_pipe, numeric_features),
            ("cat", cat_pipeline, cat_features)
        ]
    )


def read_data():
    df = pd.read_csv(in_dir + "/Exam_Score_Prediction.csv")
    df.drop(columns=["student_id"], axis=0)
    return df


def get_x_y_tensors(x_train, y_train, x_test, y_test):
    x_train = x_train.to_numpy()
    x_test = x_test.to_numpy()
    y_train = y_train.to_numpy()
    y_test = y_test.to_numpy()

    x_train_tensor = tf.convert_to_tensor(x_train, dtype=tf.float32)
    y_train_tensor = tf.convert_to_tensor(y_train, dtype=tf.float32)
    x_test_tensor = tf.convert_to_tensor(x_test, dtype=tf.float32)
    y_test_tensor = tf.convert_to_tensor(y_test, dtype=tf.float32)
    # Convert to tensors
    return x_train_tensor, y_train_tensor, x_test_tensor, y_test_tensor


def train_tensorflow_model(x, y):
    # Convert categorical features and scale them


    model = Sequential([
        InputLayer(input_shape=(tensors[0].shape[1],)),
        Dense(128, activation="relu"),
        Dense(64, activation="relu"),
        Dense(32, activation="relu"),
        Dense(1)
    ])
    model.compile(optimizer="adam", loss="mse")
    model.fit(tensors[0], tensors[1], epochs=100)
    model.save(out_dir + "/model.h5")


def train_pipeline():
    best_score = -np.inf
    best_model = None
    data = read_data()
    features = data.drop(columns=["exam_score"])
    target = data["exam_score"]
    preprocessor = build_preprocessor(features)
    x_train, x_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
    candidates = {
        "random_forest": {
            "model": RandomForestRegressor(random_state=42),
            "params": {
                "model__n_estimators": [100, 200, 300],
                "model__max_depth": [None, 5, 10, 20],
                "model__min_samples_leaf": [1, 2, 4]
            }
        }
    }

    for model_name, config in candidates.items():
        pipeline = Pipeline(steps=[("preprocessor", preprocessor), ("model", config["model"])])
        pipeline.fit(x_train, y_train)
        search = RandomizedSearchCV(
            pipeline,
            config["params"],
            n_iter=5,
            cv=3,
            verbose=1
        )
        search.fit(x_train, y_train)
        print(f"Best score for {model_name}: {search.best_score_:.3f}")
        if search.best_score_ > best_score:
            best_score = search.best_score_
            best_model = search.best_estimator_

        print(f"Test score for {model_name}: {search.score(x_test, y_test):.3f}")

    if best_model is not None:
        print(f"Best model: {best_model}")
        print(f"Best score: {best_score:.3f}")

    train_tensorflow_model(features, target)


if __name__ == "__main__":
    train_pipeline()
