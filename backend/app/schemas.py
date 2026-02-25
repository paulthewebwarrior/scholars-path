import re
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator

YEAR_LEVELS = ('Freshman', 'Sophomore', 'Junior', 'Senior')
PASSWORD_POLICY_MESSAGE = (
    'Password must be at least 8 characters with uppercase, lowercase, and numbers'
)


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str
    course: str
    year_level: Literal['Freshman', 'Sophomore', 'Junior', 'Senior']
    career_goal: str = ''

    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError(PASSWORD_POLICY_MESSAGE)
        if not re.search(r'[A-Z]', value):
            raise ValueError(PASSWORD_POLICY_MESSAGE)
        if not re.search(r'[a-z]', value):
            raise ValueError(PASSWORD_POLICY_MESSAGE)
        if not re.search(r'\d', value):
            raise ValueError(PASSWORD_POLICY_MESSAGE)
        return value

    @field_validator('name', 'course')
    @classmethod
    def validate_non_empty_profile_fields(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError('All fields are required')
        return cleaned

    @field_validator('career_goal')
    @classmethod
    def normalize_career_goal(cls, value: str) -> str:
        return value.strip()


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class RegisterResponse(BaseModel):
    message: str


class LogoutResponse(BaseModel):
    message: str


class ProfileUpdateRequest(BaseModel):
    name: str
    course: str
    year_level: Literal['Freshman', 'Sophomore', 'Junior', 'Senior']
    career_goal: str

    @field_validator('name')
    @classmethod
    def validate_name(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError('All fields are required')
        if len(cleaned) > 100:
            raise ValueError('Name too long (max 100 characters)')
        return cleaned

    @field_validator('course')
    @classmethod
    def validate_course(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError('All fields are required')
        return cleaned

    @field_validator('career_goal')
    @classmethod
    def clean_career_goal(cls, value: str) -> str:
        return value.strip()


class CareerSummaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str


class UserProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    name: str
    course: str
    year_level: str
    career_id: int | None = None
    career_goal: str
    career: CareerSummaryResponse | None = None
    created_at: datetime
    updated_at: datetime


class CareerSelectionRequest(BaseModel):
    career_id: int


class CareerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str


class CareerSkillAreaResponse(BaseModel):
    id: int
    name: str
    description: str
    importance_level: Literal['critical', 'high', 'moderate']


class CareerSubjectResponse(BaseModel):
    id: int
    name: str
    field_of_study: str
    description: str
    relevance_indicator: Literal['critical', 'high', 'moderate']


class SubjectResourceResponse(BaseModel):
    id: int
    title: str
    url: str
    provider: str


class CareerAlignedRecommendationResponse(BaseModel):
    subject_id: int
    subject_name: str
    field_of_study: str
    description: str
    relevance_indicator: Literal['critical', 'high', 'moderate']
    weakness_score: float
    baseline_weakness_score: float
    gap_closure_percent: float
    career_relevance_context: str
    supporting_skills: list[str]
    resources: list[SubjectResourceResponse]


class CareerAlignedRecommendationsListResponse(BaseModel):
    career: CareerResponse | None = None
    items: list[CareerAlignedRecommendationResponse]


class HabitsAssessmentBase(BaseModel):
    study_hours: float
    sleep_hours: float
    phone_usage_hours: float
    social_media_hours: float
    gaming_hours: float
    breaks_per_day: float
    coffee_intake: float
    exercise_minutes: float
    stress_level: float
    focus_score: float
    attendance_percentage: float
    assignments_completed_per_week: float
    final_grade: float | None = None
    grade_opt_in: bool = False

    @field_validator(
        'study_hours',
        'sleep_hours',
        'phone_usage_hours',
        'social_media_hours',
        'gaming_hours',
        'breaks_per_day',
        'coffee_intake',
        'exercise_minutes',
        'assignments_completed_per_week',
    )
    @classmethod
    def validate_non_negative(cls, value: float) -> float:
        if value < 0:
            raise ValueError('Value cannot be negative')
        return value

    @field_validator('stress_level')
    @classmethod
    def validate_stress_level(cls, value: float) -> float:
        if value < 1 or value > 10:
            raise ValueError('Stress level must be between 1 and 10')
        return value

    @field_validator('focus_score')
    @classmethod
    def validate_focus_score(cls, value: float) -> float:
        if value < 0 or value > 100:
            raise ValueError('Focus score must be between 0 and 100')
        return value

    @field_validator('attendance_percentage')
    @classmethod
    def validate_attendance_percentage(cls, value: float) -> float:
        if value < 0 or value > 100:
            raise ValueError('Attendance percentage must be between 0 and 100')
        return value

    @field_validator('final_grade')
    @classmethod
    def validate_final_grade(cls, value: float | None) -> float | None:
        if value is None:
            return value
        if value < 0 or value > 100:
            raise ValueError('Final grade must be between 0 and 100')
        return value


class HabitsAssessmentCreate(HabitsAssessmentBase):
    pass


class HabitsAssessmentResponse(HabitsAssessmentBase):
    model_config = ConfigDict(from_attributes=True)

    assessment_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime


class HabitsAssessmentHistoryResponse(BaseModel):
    items: list[HabitsAssessmentResponse]
    page: int
    page_size: int
    total: int


class HabitsCorrelationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    metric_name: str
    performance_metric: str
    correlation_coefficient: float
    sample_size: int
    confidence_interval_low: float
    confidence_interval_high: float
    confidence_level: float
    p_value: float
    calculation_timestamp: datetime


class HabitsRecommendationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    assessment_id: int
    user_id: int
    recommendation_text: str
    priority_rank: int
    supporting_metric: str
    correlation_strength: float
    status: Literal['pending', 'attempted', 'completed', 'not_applicable']
    status_updated_at: datetime | None
    created_at: datetime


class HabitsRecommendationsListResponse(BaseModel):
    items: list[HabitsRecommendationResponse]
