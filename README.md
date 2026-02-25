# Student Productivity System

This repository now includes an end-to-end authentication and profile system for the `auth-profile-system` OpenSpec change.

## Auth Features Implemented

- User registration with strong-password and profile validation
- Login with JWT access token and HTTP-only refresh token cookie
- Login rate limiting (IP + email based)
- Token refresh endpoint
- Protected profile endpoints (`GET /api/profile/me`, `PUT /api/profile/me`)
- Angular login/register/profile pages and protected routes
- HTTP interceptor for token injection and automatic refresh/retry

## Backend Setup

1. Install dependencies:

```bash
cd backend
pip install -r requirements.txt
```

2. Configure environment variables (optional defaults shown below):

```bash
AUTH_DATABASE_URL=sqlite:///./auth.db
AUTH_JWT_SECRET_KEY=change-me-in-production
AUTH_JWT_ALGORITHM=HS256
AUTH_ACCESS_TOKEN_EXPIRE_MINUTES=15
AUTH_REFRESH_TOKEN_EXPIRE_DAYS=7
AUTH_REFRESH_COOKIE_NAME=refresh_token
AUTH_COOKIE_SECURE=false
AUTH_COOKIE_SAMESITE=lax
AUTH_ALLOWED_ORIGINS=http://localhost:4200
```

3. Create the users table:

```bash
cd backend
python scripts/create_users_table.py
```

4. Seed local test users (optional):

```bash
cd backend
python scripts/seed_test_users.py
```

5. Run the API:

```bash
cd backend
python main.py
```

API base URL: `http://localhost:8000`

## Frontend Setup

1. Install dependencies:

```bash
cd frontend
npm install
```

2. Run frontend in development mode:

```bash
cd frontend
npm start
```

The Angular dev server proxies `/api` to `http://localhost:8000` via `frontend/proxy.conf.json`.

## Test Commands

Backend tests:

```bash
cd backend
pytest
```

Frontend tests:

```bash
cd frontend
npm test
```
