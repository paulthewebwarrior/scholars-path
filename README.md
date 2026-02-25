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

## Weighted Productivity Score (interactive)

You can now compute a weighted score for yourself using an interactive questionnaire.

### Formula

1. Model predicts grade `G3` from your answers + dataset defaults for non-asked fields.
2. Convert predicted grade to grade score:

\[
	ext{grade\_score} = \text{clip}\left(\frac{\hat{G3}}{20}, 0, 1\right) \times 100
\]

3. Compute behavior score from selected lifestyle/study factors:

\[
	ext{behavior\_score} =
0.30\cdot s_{studytime} +
0.25\cdot s_{absences} +
0.20\cdot s_{failures} +
0.10\cdot s_{goout} +
0.10\cdot s_{Walc} +
0.05\cdot s_{health}
\]

where each component score `s` is normalized to `[0, 100]` (with reverse scaling for negative factors like absences/failures/goout/Walc).

4. Final weighted score:

\[
	ext{weighted\_productivity} = 0.60\cdot\text{grade\_score} + 0.40\cdot\text{behavior\_score}
\]

### Questions you will answer

1. Subject focus (`math` / `portuguese`)
2. Sex (`F` / `M`)
3. Age (15-22)
4. Weekly study time level (1-4)
5. Past failures (0-4)
6. School absences (0-93)
7. Internet access at home (`yes` / `no`)
8. Higher education intention (`yes` / `no`)
9. Family relationship quality (1-5)
10. Going out with friends level (1-5)
11. Weekend alcohol consumption level (1-5)
12. Current health status (1-5)

The model fills all non-asked required fields using training-data defaults (median/mode), so you only answer the most important questions.

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

## Interactive self-test

```bash
/home/nytri/Projects/hackathon-project/.venv/bin/python main.py --interactive-score
```

After answering, you will see:
- Predicted `G3`
- Grade score component
- Behavior score component
- Final weighted productivity score and productivity band

Detailed output is saved to:
- `artifacts/latest_interactive_score.json`

## Inference usage

If you already have the trained model artifact:

- Use `load_model_and_predict(model_path, single_record)` in `main.py`.
- Build `single_record` with the same feature columns used in training (excluding `G1`, `G2`, `G3`).
- Convert the predicted grade to Productivity Score with `grade_to_productivity_score(...)`.

## Notes on significance and limitations

- This scoring is a normalized view of performance proxy (`G3`) rather than a causal productivity measurement.
- If you need domain-specific productivity, you can extend the score formula with weighted behavioral factors (e.g., attendance, study time), but that should be validated with stakeholders and ground-truth outcomes.
