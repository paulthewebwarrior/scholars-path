import os
import tensorflow as tf
import numpy as np
import pandas as pd
from keras import Sequential
from keras.src.callbacks import EarlyStopping
from keras.src.layers import InputLayer, Dense
from keras.src.losses import mean_absolute_error
from matplotlib import pyplot as plt
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from xgboost import XGBRegressor

# Define file paths
dataset_path = "dataset/productivity_dataset.csv"
out_dir = "artifacts"

if not os.path.exists(out_dir):
    os.makedirs(out_dir)


def tensorflow_train_model(x: pd.DataFrame, y: pd.Series):
    callback = EarlyStopping(monitor="loss", patience=5)
    print("Training Tensorflow model...")
    scaler = StandardScaler()
    gender_dummies = pd.get_dummies(x["gender"])
    x = pd.concat([x, gender_dummies], axis=1)
    x.drop(columns=["gender"], inplace=True)
    scaler.fit_transform(x)
    x_train, x_test, y_train_, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    # Convert to tensor
    x_train_tensor = tf.convert_to_tensor(x_train, dtype=tf.float32)
    y_train_tensor = tf.convert_to_tensor(y_train_, dtype=tf.float32)
    x_test_tensor = tf.convert_to_tensor(x_test, dtype=tf.float32)
    y_test_tensor = tf.convert_to_tensor(y_test, dtype=tf.float32)
    model = Sequential([
        InputLayer(x_train_tensor.shape[1:]),
        Dense(32, activation="relu"),
        Dense(16, activation="relu"),
        Dense(1, activation="linear")
    ])
    model.compile(optimizer="adam", loss="mean_squared_error")
    model.fit(x_train_tensor, y_train_tensor, epochs=100, callbacks=[callback])
    model.evaluate(x_test_tensor, y_test_tensor)
    model.save("artifacts/tensorflow_model.keras")

    # Test the model and create graphs
    predictions = model.predict(x_test_tensor)
    plt.scatter(y_test, predictions)
    plt.xlabel("Actual Values")
    plt.ylabel("Predictions")
    plt.title("Actual vs Predictions")
    plt.savefig("artifacts/actual_vs_predictions.png")

    # Create the mean absolute error graph
    print("Mean Absolute Error: ", mean_absolute_error(y_test, predictions))
    print("Finished training Tensorflow model.")


def create_preprocessor(x: pd.DataFrame) -> ColumnTransformer:
    # Identify column types
    numerical_features = x.select_dtypes(include=[np.number]).columns.tolist()
    cat_features = [col for col in x.columns if col not in numerical_features]

    # Build numeric pipeline
    numerical_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    # Build categorical pipeline
    cat_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore"))
    ])

    # Combine into a ColumnTransformer
    return ColumnTransformer(transformers=[
        ("num", numerical_pipeline, numerical_features),
        ("cat", cat_pipeline, cat_features)
    ])


def main():
    # 1. Load data and separate features from the target
    df = pd.read_csv(dataset_path)

    # Remove identifier columns
    df.drop(columns=["student_id"], inplace=True)

    target_col = "productivity_score"

    x = df.drop(columns=[target_col])
    y = df[target_col]

    # 2. Initialize the preprocessor
    preprocessor = create_preprocessor(x)

    # 3. Define candidate models and their grids
    model_candidates = {
        "random_forest": {
            "model": RandomForestRegressor(random_state=42),
            "params": {
                "model__n_estimators": [50, 100, 150, 200],
                "model__max_depth": [1, 2, 4, 5]
            }
        },
        "linear_regression": {
            "model": LinearRegression(),
            "params": {
            }
        },
        "xgboost": {
            "model": XGBRegressor(random_state=42),
            "params": {
                "model__n_estimators": [50, 100, 150, 200],
                "model__learning_rate": [0.01, 0.05, 0.1, 0.2],
                "model__max_depth": [1, 2, 4, 5]
            }
        }
    }

    best_score = -np.inf
    best_model = None
    best_model_name = ""

    # 4. Iterate through candidates and perform Grid Search
    for name, config in model_candidates.items():
        # Combine preprocessor and model into a full pipeline
        full_pipeline = Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("model", config["model"])
        ])

        search = GridSearchCV(
            estimator=full_pipeline,
            param_grid=config["params"],
            cv=5,
            n_jobs=-1
        )

        print(f"Training {name}...")
        search.fit(x, y)
        print(f"Finished training {name}.")
        print(f"Best Score for {name}: {search.best_score_:.4f}")
        print()

        # Save the best model for this candidate
        model_path = os.path.join(out_dir, f"{name}_best_model.pkl")
        pd.to_pickle(search.best_estimator_, model_path)

        # Update best model tracking
        if search.best_score_ > best_score:
            best_score = search.best_score_
            best_model = search.best_estimator_
            best_model_name = name

    # 5. Output results
    if best_model is not None:
        print(f"Best Model: {best_model_name}")
        print(f"Best Score: {best_score:.4f}")

    # Train Tensorflow model
    tensorflow_train_model(x, y)


if __name__ == '__main__':
    main()
