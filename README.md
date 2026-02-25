# Student Productivity Scoring (ML Pipeline)

This project trains a machine learning model to predict student final grade (`G3`) and converts the grade into a standardized **Productivity Score**.

## What was implemented

- Data ingestion from:
  - `student/student-mat.csv`
  - `student/student-por.csv`
- Feature engineering:
  - Adds `subject` feature (`math` / `portuguese`)
  - Removes duplicates after merge
- Leakage-safe modeling:
  - Target: `G3`
  - Dropped leakage columns: `G1`, `G2`
- Preprocessing:
  - Numeric imputation (`median`)
  - Categorical imputation (`most_frequent`) + one-hot encoding
- Model selection:
  - `RandomForestRegressor`, `ExtraTreesRegressor`, `GradientBoostingRegressor`
  - `RandomizedSearchCV` (5-fold, RMSE)
- Artifacts:
  - Trained model, metrics, relationships, and productivity outputs

## Productivity Score definition

The dataset target (`G3`) is on a 0-20 scale. We convert it to a 0-100 score:

\[
\text{Productivity Score} = \text{clip}\left(\frac{G3 - 0}{20 - 0},\ 0,\ 1\right) \times 100
\]

Equivalent implementation in code:

- `grade_to_productivity_score(...)` in `main.py`

### Why this conversion

- Preserves ranking of students (monotonic transformation)
- Makes output easier to interpret as a percentage-like score
- Keeps score bounded to `[0, 100]`
- Works for both **actual** and **predicted** grades

## Productivity bands

The score is also categorized:

- `low`: `[0, 40)`
- `moderate`: `[40, 70)`
- `high`: `[70, 85)`
- `excellent`: `[85, 100]`

Implementation:

- `productivity_band(...)` in `main.py`

## Output files

After running `main.py`, you get:

- `artifacts/student_grade_predictor.joblib`
- `artifacts/training_summary.json`
- `artifacts/numeric_relationships.csv`
- `artifacts/categorical_relationships.csv`
- `artifacts/productivity_scores.csv`
- `artifacts/productivity_score_summary.json`

### `productivity_scores.csv` columns

- `record_id`
- `subject`
- `actual_g3`
- `predicted_g3`
- `actual_productivity_score`
- `predicted_productivity_score`
- `score_error`
- `predicted_productivity_band`

## How to run

```bash
/home/nytri/Projects/hackathon-project/.venv/bin/python main.py
```

## Inference usage

If you already have the trained model artifact:

- Use `load_model_and_predict(model_path, single_record)` in `main.py`.
- Build `single_record` with the same feature columns used in training (excluding `G1`, `G2`, `G3`).
- Convert the predicted grade to Productivity Score with `grade_to_productivity_score(...)`.

## Notes on significance and limitations

- This scoring is a normalized view of performance proxy (`G3`) rather than a causal productivity measurement.
- If you need domain-specific productivity, you can extend the score formula with weighted behavioral factors (e.g., attendance, study time), but that should be validated with stakeholders and ground-truth outcomes.
