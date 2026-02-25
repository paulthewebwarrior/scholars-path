from __future__ import annotations

import logging
from functools import lru_cache
from pathlib import Path

import joblib
import pandas as pd

from .models import HabitsAssessment, User

logger = logging.getLogger(__name__)

MODEL_PATH = Path(__file__).resolve().parents[1] / 'artifacts' / 'linear_regression_best_model.pkl'
DEFAULT_AGE = 20
DEFAULT_GENDER = 'Other'
COFFEE_MG_PER_CUP = 95.0

YEAR_LEVEL_TO_AGE = {
    'freshman': 18,
    'first year': 18,
    'sophomore': 19,
    'second year': 19,
    'junior': 20,
    'third year': 20,
    'senior': 21,
    'fourth year': 21,
    'graduate': 23,
}


@lru_cache(maxsize=1)
def _load_pipeline():
    if not MODEL_PATH.exists():
        logger.warning('productivity.model.not_found path=%s', MODEL_PATH)
        return None
    try:
        return joblib.load(MODEL_PATH)
    except Exception:
        logger.exception('productivity.model.load_failed path=%s', MODEL_PATH)
        return None


def _infer_age(year_level: str | None) -> int:
    if not year_level:
        return DEFAULT_AGE
    normalized = year_level.strip().lower()
    return YEAR_LEVEL_TO_AGE.get(normalized, DEFAULT_AGE)


def _model_input(assessment: HabitsAssessment, user: User) -> dict[str, object]:
    final_grade = assessment.final_grade if assessment.grade_opt_in else None

    return {
        'age': _infer_age(user.year_level),
        'gender': DEFAULT_GENDER,
        'study_hours_per_day': float(assessment.study_hours),
        'sleep_hours': float(assessment.sleep_hours),
        'phone_usage_hours': float(assessment.phone_usage_hours),
        'social_media_hours': float(assessment.social_media_hours),
        'youtube_hours': float(assessment.social_media_hours),
        'gaming_hours': float(assessment.gaming_hours),
        'breaks_per_day': float(assessment.breaks_per_day),
        'coffee_intake_mg': float(assessment.coffee_intake) * COFFEE_MG_PER_CUP,
        'exercise_minutes': float(assessment.exercise_minutes),
        'assignments_completed': float(assessment.assignments_completed_per_week),
        'attendance_percentage': float(assessment.attendance_percentage),
        'stress_level': float(assessment.stress_level),
        'focus_score': float(assessment.focus_score),
        'final_grade': final_grade,
    }


def predict_productivity_score(assessment: HabitsAssessment, user: User) -> float | None:
    pipeline = _load_pipeline()
    if pipeline is None:
        return None

    try:
        features = _model_input(assessment, user)
        frame = pd.DataFrame([features])
        prediction = float(pipeline.predict(frame)[0])
        return round(prediction, 2)
    except Exception:
        logger.exception('productivity.predict.failed assessment_id=%s user_id=%s', assessment.assessment_id, user.id)
        return None
