## 1. Backend Database Setup

- [ ] 1.1 Create users table migration with email (unique), hashed_password, name, course, year_level, career_goal, created_at, updated_at columns
- [ ] 1.2 Add SQLAlchemy database connection and session management to FastAPI app
- [ ] 1.3 Create SQLAlchemy User model with all profile fields
- [ ] 1.4 Add database indexes on email for fast login lookups

## 2. Backend Authentication Service

- [ ] 2.1 Install and configure FastAPI, python-jose/PyJWT, and bcrypt for password hashing
- [ ] 2.2 Create password hashing utility functions (hash and verify)
- [ ] 2.3 Create JWT token generation functions (access and refresh tokens with expiration)
- [ ] 2.4 Create FastAPI dependency for JWT validation and token decoding
- [ ] 2.5 Setup HTTP-only cookie configuration for refresh tokens in FastAPI response
- [ ] 2.6 Implement rate limiting for login attempts (track by IP/email) using slowapi or similar

## 3. Backend Registration Endpoint (FastAPI)

- [ ] 3.1 Create FastAPI POST /api/auth/register endpoint with Pydantic model for input validation
- [ ] 3.2 Validate email format and check email uniqueness in database
- [ ] 3.3 Validate password strength (min 8 chars, uppercase, lowercase, numbers)
- [ ] 3.4 Validate all profile fields are non-empty
- [ ] 3.5 Hash password with bcrypt and create user in database
- [ ] 3.6 Return success response with redirect to login or initial tokens
- [ ] 3.7 Add error handling for duplicate email, validation failures

## 4. Backend Login Endpoint (FastAPI)

- [ ] 4.1 Create FastAPI POST /api/auth/login endpoint with Pydantic model for credentials
- [ ] 4.2 Validate email exists in database
- [ ] 4.3 Compare submitted password hash against stored hash using bcrypt
- [ ] 4.4 Generate JWT access token (15 min expiration)
- [ ] 4.5 Generate JWT refresh token (7 day expiration)
- [ ] 4.6 Set refresh token in HTTP-only cookie with secure/SameSite flags
- [ ] 4.7 Return access token in response body
- [ ] 4.8 Implement rate limiting check before processing login

## 5. Backend Profile Endpoints (FastAPI)

- [ ] 5.1 Create FastAPI GET /api/profile/me endpoint with JWT dependency for current user retrieval
- [ ] 5.2 Create PUT /api/profile/me endpoint to update profile fields (protected by JWT)
- [ ] 5.3 Validate profile update inputs (non-empty fields, name length limits)
- [ ] 5.4 Update user record with new profile data atomically (all or nothing)
- [ ] 5.5 Add authentication check to reject unauthorized profile access/modification
- [ ] 5.6 Return updated profile or error responses

## 6. Backend Token Refresh

- [ ] 6.1 Create POST /api/auth/refresh endpoint to issue new access tokens
- [ ] 6.2 Validate refresh token from cookie
- [ ] 6.3 Generate new access token if refresh token valid
- [ ] 6.4 Return new access token in response
- [ ] 6.5 Handle expired/invalid refresh tokens with 401 response

## 7. Frontend Registration Page

- [ ] 7.1 Create register component with form for email, password, name, course, year_level, career_goal
- [ ] 7.2 Implement real-time email format validation feedback
- [ ] 7.3 Implement password strength meter showing requirements (8 chars, uppercase, lowercase, numbers)
- [ ] 7.4 Disable submit button until all fields are valid
- [ ] 7.5 Implement course selection dropdown or input field
- [ ] 7.6 Implement year_level selection (Freshman/Sophomore/Junior/Senior)
- [ ] 7.7 Add link to login page for existing users
- [ ] 7.8 Create form error display area for server responses

## 8. Frontend Login Page

- [ ] 8.1 Create login component with email and password input fields
- [ ] 8.2 Implement form submission to POST /api/auth/login
- [ ] 8.3 Store access token in memory/state
- [ ] 8.4 Store refresh token via HTTP cookie (automatic with API calls)
- [ ] 8.5 Handle login success by redirecting to dashboard
- [ ] 8.6 Display error messages for failed login (generic "Invalid email or password")
- [ ] 8.7 Add link to registration page for new users
- [ ] 8.8 Show loading indicator during login request

## 9. Frontend HTTP Interceptor & Auth Service

- [ ] 9.1 Create HTTP interceptor that injects Authorization header with access token on all requests
- [ ] 9.2 Implement interceptor to handle 401 responses by attempting token refresh
- [ ] 9.3 If refresh succeeds, retry original request with new token
- [ ] 9.4 If refresh fails, redirect to login page
- [ ] 9.5 Create auth service with methods: isAuthenticated(), getToken(), logout()
- [ ] 9.6 Implement logout() to clear token from memory and redirect to login

## 10. Frontend Route Guards

- [ ] 10.1 Create auth guard that checks if user is authenticated before allowing access
- [ ] 10.2 Apply auth guard to dashboard route(s)
- [ ] 10.3 Apply auth guard to profile route(s)
- [ ] 10.4 Redirect unauthenticated access attempts to login page
- [ ] 10.5 Add public routes exemption for login and register pages

## 11. Frontend Profile Page

- [ ] 11.1 Create profile component to display user's name, course, year_level, career_goal
- [ ] 11.2 Create edit mode toggle to switch between view and edit
- [ ] 11.3 In edit mode, display form with editable fields matching spec validation
- [ ] 11.4 Implement form validation for profile update (non-empty fields, max length)
- [ ] 11.5 Implement PUT /api/profile/me call to save profile changes
- [ ] 11.6 Show success message after profile save
- [ ] 11.7 Handle and display errors from profile update endpoint
- [ ] 11.8 Add logout button that clears tokens and redirects to login

## 12. Frontend User Menu & Navigation

- [ ] 12.1 Add user menu/dropdown showing current user's name in app header
- [ ] 12.2 Add "Profile" link to access profile page
- [ ] 12.3 Add "Logout" button to clear session and redirect to login
- [ ] 12.4 Show "Login" link in header when not authenticated
- [ ] 12.5 Update navigation based on authentication state

## 13. Database Migrations & Initial Setup

- [ ] 13.1 Write database migration script to create users table on fresh install
- [ ] 13.2 Document database setup instructions for deployment
- [ ] 13.3 Create seed/test data script for development (test user accounts)

## 14. Testing

- [ ] 14.1 Unit test password hashing (hash/verify functions)
- [ ] 14.2 Unit test JWT token generation and validation
- [ ] 14.3 Integration test registration endpoint with valid and invalid inputs
- [ ] 14.4 Integration test login endpoint with correct/incorrect credentials
- [ ] 14.5 Integration test profile GET/PUT endpoints with authentication
- [ ] 14.6 E2E test full registration → login → profile view/edit flow
- [ ] 14.7 E2E test token refresh on expired access token
- [ ] 14.8 E2E test protected route redirect when unauthenticated

## 15. Deployment & Documentation

- [ ] 15.1 Update README with authentication setup instructions
- [ ] 15.2 Document environment variables needed (JWT secret, token expiration times)
- [ ] 15.3 Update frontend build configuration if needed
- [ ] 15.4 Create deployment checklist for users table migration
- [ ] 15.5 Test full flow in staging environment
- [ ] 15.6 Deploy to production with database migrations
