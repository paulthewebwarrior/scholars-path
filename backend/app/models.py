from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    LargeBinary,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import TypeDecorator

from .database import Base
from .encryption import decrypt_number, encrypt_number


class EncryptedFloat(TypeDecorator[float]):
    impl = LargeBinary
    cache_ok = True

    def process_bind_param(self, value: float | None, dialect) -> bytes | None:  # type: ignore[override]
        if value is None:
            return None
        return encrypt_number(float(value))

    def process_result_value(self, value: bytes | None, dialect) -> float | None:  # type: ignore[override]
        if value is None:
            return None
        return decrypt_number(value)


class Career(Base):
    __tablename__ = 'careers'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)


class SkillArea(Base):
    __tablename__ = 'skill_areas'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    importance_level: Mapped[str] = mapped_column(String(20), nullable=False, default='moderate')


class CareerSkill(Base):
    __tablename__ = 'career_skills'
    __table_args__ = (
        UniqueConstraint('career_id', 'skill_area_id', name='uq_career_skills_career_skill'),
        Index('ix_career_skills_career_id', 'career_id'),
        Index('ix_career_skills_skill_area_id', 'skill_area_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    career_id: Mapped[int] = mapped_column(ForeignKey('careers.id', ondelete='CASCADE'), nullable=False)
    skill_area_id: Mapped[int] = mapped_column(ForeignKey('skill_areas.id', ondelete='CASCADE'), nullable=False)


class Subject(Base):
    __tablename__ = 'subjects'
    __table_args__ = (
        Index('ix_subjects_field_of_study', 'field_of_study'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    field_of_study: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)


class SkillSubject(Base):
    __tablename__ = 'skill_subjects'
    __table_args__ = (
        UniqueConstraint('skill_area_id', 'subject_id', name='uq_skill_subjects_skill_subject'),
        Index('ix_skill_subjects_skill_area_id', 'skill_area_id'),
        Index('ix_skill_subjects_subject_id', 'subject_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    skill_area_id: Mapped[int] = mapped_column(ForeignKey('skill_areas.id', ondelete='CASCADE'), nullable=False)
    subject_id: Mapped[int] = mapped_column(ForeignKey('subjects.id', ondelete='CASCADE'), nullable=False)
    relevance_indicator: Mapped[str] = mapped_column(String(20), nullable=False, default='moderate')


class SubjectResource(Base):
    __tablename__ = 'subject_resources'
    __table_args__ = (
        Index('ix_subject_resources_subject_id', 'subject_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    subject_id: Mapped[int] = mapped_column(ForeignKey('subjects.id', ondelete='CASCADE'), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(String(512), nullable=False)
    provider: Mapped[str] = mapped_column(String(100), nullable=False)


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    course: Mapped[str] = mapped_column(String(100), nullable=False)
    year_level: Mapped[str] = mapped_column(String(50), nullable=False)
    career_id: Mapped[int | None] = mapped_column(
        ForeignKey('careers.id', ondelete='SET NULL'),
        nullable=True,
        index=True,
    )
    career_goal: Mapped[str] = mapped_column(String(255), nullable=False, default='')
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class HabitsAssessment(Base):
    __tablename__ = 'habits_assessment'
    __table_args__ = (
        Index('ix_habits_assessment_user_id_created_at', 'user_id', 'created_at'),
    )

    assessment_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    study_hours: Mapped[float] = mapped_column(EncryptedFloat, nullable=False)
    sleep_hours: Mapped[float] = mapped_column(EncryptedFloat, nullable=False)
    phone_usage_hours: Mapped[float] = mapped_column(EncryptedFloat, nullable=False)
    social_media_hours: Mapped[float] = mapped_column(EncryptedFloat, nullable=False)
    gaming_hours: Mapped[float] = mapped_column(EncryptedFloat, nullable=False)
    breaks_per_day: Mapped[float] = mapped_column(EncryptedFloat, nullable=False)
    coffee_intake: Mapped[float] = mapped_column(EncryptedFloat, nullable=False)
    exercise_minutes: Mapped[float] = mapped_column(EncryptedFloat, nullable=False)
    stress_level: Mapped[float] = mapped_column(EncryptedFloat, nullable=False)
    focus_score: Mapped[float] = mapped_column(EncryptedFloat, nullable=False)
    attendance_percentage: Mapped[float] = mapped_column(EncryptedFloat, nullable=False)
    assignments_completed_per_week: Mapped[float] = mapped_column(EncryptedFloat, nullable=False)
    final_grade: Mapped[float | None] = mapped_column(EncryptedFloat, nullable=True)
    grade_opt_in: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class HabitsCorrelation(Base):
    __tablename__ = 'habits_correlations'
    __table_args__ = (Index('ix_habits_correlations_metric_performance', 'metric_name', 'performance_metric'),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    metric_name: Mapped[str] = mapped_column(String(100), nullable=False)
    performance_metric: Mapped[str] = mapped_column(String(100), nullable=False)
    correlation_coefficient: Mapped[float] = mapped_column(Float, nullable=False)
    sample_size: Mapped[int] = mapped_column(Integer, nullable=False)
    confidence_interval_low: Mapped[float] = mapped_column(Float, nullable=False)
    confidence_interval_high: Mapped[float] = mapped_column(Float, nullable=False)
    confidence_level: Mapped[float] = mapped_column(Float, nullable=False, default=95.0)
    p_value: Mapped[float] = mapped_column(Float, nullable=False)
    calculation_timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class HabitsRecommendation(Base):
    __tablename__ = 'habits_recommendations'
    __table_args__ = (
        Index('ix_habits_recommendations_assessment_priority', 'assessment_id', 'priority_rank'),
        Index('ix_habits_recommendations_user_id_created_at', 'user_id', 'created_at'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    assessment_id: Mapped[int] = mapped_column(
        ForeignKey('habits_assessment.assessment_id', ondelete='CASCADE'),
        nullable=False,
        index=True,
    )
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    recommendation_text: Mapped[str] = mapped_column(Text, nullable=False)
    priority_rank: Mapped[int] = mapped_column(Integer, nullable=False)
    supporting_metric: Mapped[str] = mapped_column(String(100), nullable=False)
    correlation_strength: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default='pending')
    status_updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )


class HabitsNormalizedExport(Base):
    __tablename__ = 'habits_normalized_exports'
    __table_args__ = (Index('ix_habits_normalized_exports_assessment_id', 'assessment_id'),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    assessment_id: Mapped[int] = mapped_column(
        ForeignKey('habits_assessment.assessment_id', ondelete='CASCADE'),
        nullable=False,
        unique=True,
    )
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    study_hours: Mapped[float] = mapped_column(Float, nullable=False)
    sleep_hours: Mapped[float] = mapped_column(Float, nullable=False)
    phone_usage_hours: Mapped[float] = mapped_column(Float, nullable=False)
    social_media_hours: Mapped[float] = mapped_column(Float, nullable=False)
    gaming_hours: Mapped[float] = mapped_column(Float, nullable=False)
    breaks_per_day: Mapped[float] = mapped_column(Float, nullable=False)
    coffee_intake: Mapped[float] = mapped_column(Float, nullable=False)
    exercise_minutes: Mapped[float] = mapped_column(Float, nullable=False)
    stress_level: Mapped[float] = mapped_column(Float, nullable=False)
    focus_score: Mapped[float] = mapped_column(Float, nullable=False)
    attendance_percentage: Mapped[float] = mapped_column(Float, nullable=False)
    assignments_completed_per_week: Mapped[float] = mapped_column(Float, nullable=False)
    final_grade: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
