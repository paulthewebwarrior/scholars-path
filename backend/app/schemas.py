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
    career_goal: str

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

    @field_validator('name', 'course', 'career_goal')
    @classmethod
    def validate_non_empty_profile_fields(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError('All fields are required')
        return cleaned


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


class UserProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    name: str
    course: str
    year_level: str
    career_goal: str
    created_at: datetime
    updated_at: datetime
