from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..config import get_settings
from ..database import get_db
from ..models import User
from ..rate_limiter import login_rate_limiter
from ..schemas import LoginRequest, LogoutResponse, RegisterRequest, RegisterResponse, TokenResponse
from ..security import (
    clear_refresh_cookie,
    create_access_token,
    create_refresh_token,
    get_user_from_token,
    hash_password,
    set_refresh_cookie,
    verify_password,
)

router = APIRouter(prefix='/api/auth', tags=['auth'])
RATE_LIMIT_MESSAGE = 'Too many login attempts. Try again later.'
INVALID_CREDENTIALS_MESSAGE = 'Invalid email or password'
settings = get_settings()


def _email_lookup_key(email: str) -> str:
    return f'email:{email.lower()}'


def _ip_lookup_key(request: Request) -> str:
    client_host = request.client.host if request.client else 'unknown'
    return f'ip:{client_host}'


@router.post('/register', response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> RegisterResponse:
    normalized_email = payload.email.lower()
    existing_user = db.scalar(select(User).where(User.email == normalized_email))
    if existing_user is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already registered')

    user = User(
        email=normalized_email,
        hashed_password=hash_password(payload.password),
        name=payload.name,
        course=payload.course,
        year_level=payload.year_level,
    )
    db.add(user)

    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already registered') from exc

    return RegisterResponse(message='Registration successful. Please log in.')


@router.post('/login', response_model=TokenResponse)
def login(payload: LoginRequest, request: Request, db: Session = Depends(get_db)) -> Response:
    normalized_email = payload.email.lower()
    ip_key = _ip_lookup_key(request)
    email_key = _email_lookup_key(normalized_email)

    if login_rate_limiter.is_blocked(ip_key) or login_rate_limiter.is_blocked(email_key):
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=RATE_LIMIT_MESSAGE)

    user = db.scalar(select(User).where(User.email == normalized_email))
    if user is None or not verify_password(payload.password, user.hashed_password):
        login_rate_limiter.register_failure(ip_key)
        login_rate_limiter.register_failure(email_key)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=INVALID_CREDENTIALS_MESSAGE)

    login_rate_limiter.reset(ip_key)
    login_rate_limiter.reset(email_key)

    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    response = JSONResponse(content=TokenResponse(access_token=access_token).model_dump())
    set_refresh_cookie(response, refresh_token)
    return response


@router.post('/refresh', response_model=TokenResponse)
def refresh(request: Request, db: Session = Depends(get_db)) -> TokenResponse:
    refresh_token = request.cookies.get(settings.refresh_cookie_name)
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized')

    user = get_user_from_token(db, token=refresh_token, token_type='refresh')
    access_token = create_access_token(user)
    return TokenResponse(access_token=access_token)


@router.post('/logout', response_model=LogoutResponse)
def logout() -> Response:
    response = JSONResponse(content=LogoutResponse(message='Logged out').model_dump())
    clear_refresh_cookie(response)
    return response
