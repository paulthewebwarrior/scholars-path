## 1. Backend Database Setup

- [x] 1.1 Create users table migration with email (unique), hashed_password, name, course, year_level, career_goal, created_at, updated_at columns
- [x] 1.2 Add SQLAlchemy database connection and session management to FastAPI app
- [x] 1.3 Create SQLAlchemy User model with all profile fields
- [x] 1.4 Add database indexes on email for fast login lookups

## 2. Backend Authentication Service

- [x] 2.1 Install and configure FastAPI, python-jose/PyJWT, and bcrypt for password hashing
- [x] 2.2 Create password hashing utility functions (hash and verify)
- [x] 2.3 Create JWT token generation functions (access and refresh tokens with expiration)
- [x] 2.4 Create FastAPI dependency for JWT validation and token decoding
- [x] 2.5 Setup HTTP-only cookie configuration for refresh tokens in FastAPI response
- [x] 2.6 Implement rate limiting for login attempts (track by IP/email) using slowapi or similar

## 3. Backend Registration Endpoint (FastAPI)

- [x] 3.1 Create FastAPI POST /api/auth/register endpoint with Pydantic model for input validation
- [x] 3.2 Validate email format and check email uniqueness in database
- [x] 3.3 Validate password strength (min 8 chars, uppercase, lowercase, numbers)
- [x] 3.4 Validate all profile fields are non-empty
- [x] 3.5 Hash password with bcrypt and create user in database
- [x] 3.6 Return success response with redirect to login or initial tokens
- [x] 3.7 Add error handling for duplicate email, validation failures

## 4. Backend Login Endpoint (FastAPI)

- [x] 4.1 Create FastAPI POST /api/auth/login endpoint with Pydantic model for credentials
- [x] 4.2 Validate email exists in database
- [x] 4.3 Compare submitted password hash against stored hash using bcrypt
- [x] 4.4 Generate JWT access token (15 min expiration)
- [x] 4.5 Generate JWT refresh token (7 day expiration)
- [x] 4.6 Set refresh token in HTTP-only cookie with secure/SameSite flags
- [x] 4.7 Return access token in response body
- [x] 4.8 Implement rate limiting check before processing login

## 5. Backend Profile Endpoints (FastAPI)

- [x] 5.1 Create FastAPI GET /api/profile/me endpoint with JWT dependency for current user retrieval
- [x] 5.2 Create PUT /api/profile/me endpoint to update profile fields (protected by JWT)
- [x] 5.3 Validate profile update inputs (non-empty fields, name length limits)
- [x] 5.4 Update user record with new profile data atomically (all or nothing)
- [x] 5.5 Add authentication check to reject unauthorized profile access/modification
- [x] 5.6 Return updated profile or error responses

## 6. Backend Token Refresh

- [x] 6.1 Create POST /api/auth/refresh endpoint to issue new access tokens
- [x] 6.2 Validate refresh token from cookie
- [x] 6.3 Generate new access token if refresh token valid
- [x] 6.4 Return new access token in response
- [x] 6.5 Handle expired/invalid refresh tokens with 401 response

## 7. Frontend Registration Page

- [x] 7.1 Create register component with form for email, password, name, course, year_level, career_goal
- [x] 7.2 Implement real-time email format validation feedback
- [x] 7.3 Implement password strength meter showing requirements (8 chars, uppercase, lowercase, numbers)
- [x] 7.4 Disable submit button until all fields are valid
- [x] 7.5 Implement course selection dropdown or input field
- [x] 7.6 Implement year_level selection (Freshman/Sophomore/Junior/Senior)
- [x] 7.7 Add link to login page for existing users
- [x] 7.8 Create form error display area for server responses

## 8. Frontend Login Page

- [x] 8.1 Create login component with email and password input fields
- [x] 8.2 Implement form submission to POST /api/auth/login
- [x] 8.3 Store access token in memory/state
- [x] 8.4 Store refresh token via HTTP cookie (automatic with API calls)
- [x] 8.5 Handle login success by redirecting to dashboard
- [x] 8.6 Display error messages for failed login (generic "Invalid email or password")
- [x] 8.7 Add link to registration page for new users
- [x] 8.8 Show loading indicator during login request

## 9. Frontend HTTP Interceptor & Auth Service

- [x] 9.1 Create HTTP interceptor that injects Authorization header with access token on all requests
- [x] 9.2 Implement interceptor to handle 401 responses by attempting token refresh
- [x] 9.3 If refresh succeeds, retry original request with new token
- [x] 9.4 If refresh fails, redirect to login page
- [x] 9.5 Create auth service with methods: isAuthenticated(), getToken(), logout()
- [x] 9.6 Implement logout() to clear token from memory and redirect to login

## 10. Frontend Route Guards

- [x] 10.1 Create auth guard that checks if user is authenticated before allowing access
- [x] 10.2 Apply auth guard to dashboard route(s)
- [x] 10.3 Apply auth guard to profile route(s)
- [x] 10.4 Redirect unauthenticated access attempts to login page
- [x] 10.5 Add public routes exemption for login and register pages

## 11. Frontend Profile Page

- [x] 11.1 Create profile component to display user's name, course, year_level, career_goal
- [x] 11.2 Create edit mode toggle to switch between view and edit
- [x] 11.3 In edit mode, display form with editable fields matching spec validation
- [x] 11.4 Implement form validation for profile update (non-empty fields, max length)
- [x] 11.5 Implement PUT /api/profile/me call to save profile changes
- [x] 11.6 Show success message after profile save
- [x] 11.7 Handle and display errors from profile update endpoint
- [x] 11.8 Add logout button that clears tokens and redirects to login

## 12. Frontend User Menu & Navigation

- [x] 12.1 Add user menu/dropdown showing current user's name in app header
- [x] 12.2 Add "Profile" link to access profile page
- [x] 12.3 Add "Logout" button to clear session and redirect to login
- [x] 12.4 Show "Login" link in header when not authenticated
- [x] 12.5 Update navigation based on authentication state

## 13. Database Migrations & Initial Setup

- [x] 13.1 Write database migration script to create users table on fresh install
- [x] 13.2 Document database setup instructions for deployment
- [x] 13.3 Create seed/test data script for development (test user accounts)

## 14. Testing

- [x] 14.1 Unit test password hashing (hash/verify functions)
- [x] 14.2 Unit test JWT token generation and validation
- [x] 14.3 Integration test registration endpoint with valid and invalid inputs
- [x] 14.4 Integration test login endpoint with correct/incorrect credentials
- [x] 14.5 Integration test profile GET/PUT endpoints with authentication
- [x] 14.6 E2E test full registration → login → profile view/edit flow
- [x] 14.7 E2E test token refresh on expired access token
- [x] 14.8 E2E test protected route redirect when unauthenticated

## 15. Deployment & Documentation

- [x] 15.1 Update README with authentication setup instructions
- [x] 15.2 Document environment variables needed (JWT secret, token expiration times)
- [x] 15.3 Update frontend build configuration if needed
- [x] 15.4 Create deployment checklist for users table migration
- [ ] 15.5 Test full flow in staging environment
- [ ] 15.6 Deploy to production with database migrations
