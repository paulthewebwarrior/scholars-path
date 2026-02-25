# Auth Deployment Checklist

## Pre-Deploy

- [ ] Set production `AUTH_JWT_SECRET_KEY` to a strong secret
- [ ] Set `AUTH_COOKIE_SECURE=true` for HTTPS-only cookies
- [ ] Set `AUTH_COOKIE_SAMESITE` policy for deployment environment
- [ ] Configure production `AUTH_DATABASE_URL`
- [ ] Configure `AUTH_ALLOWED_ORIGINS` for frontend domain(s)

## Database Migration

- [ ] Run `python scripts/create_users_table.py` from `backend/`
- [ ] Confirm `users` table exists
- [ ] Confirm email uniqueness and email index are present

## API Verification

- [ ] `POST /api/auth/register` creates account with hashed password
- [ ] `POST /api/auth/login` returns access token and sets refresh cookie
- [ ] `POST /api/auth/refresh` issues new access token from refresh cookie
- [ ] `GET /api/profile/me` returns 401 without bearer token
- [ ] `PUT /api/profile/me` updates profile atomically

## Frontend Verification

- [ ] Login/register pages load and submit correctly
- [ ] Unauthenticated access to `/dashboard` and `/profile` redirects to `/login`
- [ ] Authenticated navigation shows user menu, profile link, and logout
- [ ] Refresh workflow retries expired-token requests after `/api/auth/refresh`

## Post-Deploy

- [ ] Monitor failed login rate-limit behavior
- [ ] Monitor authentication errors (401/429 trends)
- [ ] Run smoke test of full registration -> login -> profile edit flow
