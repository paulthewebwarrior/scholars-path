"""Interactive tester for the linear regression productivity model.

Run with:
    python test_model.py

You will be prompted for each feature the model expects. The script
loads `artifacts/linear_regression_best_model.pkl` and prints the
predicted productivity score.
"""

from pathlib import Path
import sys

import joblib
import pandas as pd


MODEL_PATH = Path("artifacts/linear_regression_best_model.pkl")


# Schema that mirrors the training features used in `main.py`
FEATURES = [
    {"name": "age", "prompt": "Age in years", "type": "numeric", "min": 10, "max": 100, "cast": int},
    {"name": "gender", "prompt": "Gender (Male/Female/Other)", "type": "categorical"},
    {"name": "study_hours_per_day", "prompt": "Study hours per day", "type": "numeric", "min": 0, "max": 24},
    {"name": "sleep_hours", "prompt": "Sleep hours per day", "type": "numeric", "min": 0, "max": 24},
    {"name": "phone_usage_hours", "prompt": "Phone usage hours per day", "type": "numeric", "min": 0, "max": 24},
    {"name": "social_media_hours", "prompt": "Social media hours per day", "type": "numeric", "min": 0, "max": 24},
    {"name": "youtube_hours", "prompt": "YouTube hours per day", "type": "numeric", "min": 0, "max": 24},
    {"name": "gaming_hours", "prompt": "Gaming hours per day", "type": "numeric", "min": 0, "max": 24},
    {"name": "breaks_per_day", "prompt": "Number of breaks per day", "type": "numeric", "min": 0, "max": 50, "cast": int},
    {"name": "coffee_intake_mg", "prompt": "Coffee intake (mg caffeine per day)", "type": "numeric", "min": 0, "max": 2000, "cast": int},
    {"name": "exercise_minutes", "prompt": "Exercise minutes per day", "type": "numeric", "min": 0, "max": 300, "cast": int},
    {"name": "assignments_completed", "prompt": "Assignments completed per week", "type": "numeric", "min": 0, "max": 100, "cast": int},
    {"name": "attendance_percentage", "prompt": "Attendance percentage (0-100)", "type": "numeric", "min": 0, "max": 100},
    {"name": "stress_level", "prompt": "Stress level (1-10)", "type": "numeric", "min": 1, "max": 10, "cast": int},
    {"name": "focus_score", "prompt": "Focus score (0-100)", "type": "numeric", "min": 0, "max": 100, "cast": int},
    {"name": "final_grade", "prompt": "Final grade (0-100)", "type": "numeric", "min": 0, "max": 100},
]


def load_model(path: Path):
    """Load the persisted sklearn pipeline."""
    if not path.exists():
        sys.exit(f"Model file not found at {path}")
    return joblib.load(path)


def ask_numeric(prompt: str, min_val: float | None, max_val: float | None, cast=None) -> float:
    while True:
        raw = input(f"- {prompt}: ").strip()
        try:
            val = float(raw)
        except ValueError:
            print("  Please enter a numeric value.")
            continue

        if min_val is not None and val < min_val:
            print(f"  Value must be at least {min_val}.")
            continue
        if max_val is not None and val > max_val:
            print(f"  Value must be at most {max_val}.")
            continue

        if cast is int:
            val = int(round(val))
        return val


def ask_categorical(prompt: str) -> str:
    while True:
        val = input(f"- {prompt}: ").strip()
        if val:
            return val.title()
        print("  Please enter a value.")


def collect_inputs() -> dict:
    print("Provide the following details (Ctrl+C to quit):")
    answers: dict[str, float | str] = {}
    for feat in FEATURES:
        if feat["type"] == "numeric":
            answers[feat["name"]] = ask_numeric(
                prompt=feat["prompt"],
                min_val=feat.get("min"),
                max_val=feat.get("max"),
                cast=feat.get("cast"),
            )
        else:
            answers[feat["name"]] = ask_categorical(feat["prompt"])
    return answers


def predict_productivity(pipeline, features: dict) -> float:
    df = pd.DataFrame([features])
    prediction = pipeline.predict(df)[0]
    return float(prediction)


def main():
    model = load_model(MODEL_PATH)
    try:
        user_features = collect_inputs()
    except KeyboardInterrupt:
        print("\nAborted by user.")
        sys.exit(0)

    score = predict_productivity(model, user_features)
    print("\nPredicted productivity score:", round(score, 2))


if __name__ == "__main__":
    main()
