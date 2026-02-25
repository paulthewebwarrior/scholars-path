## ADDED Requirements

### Requirement: User login with email and password
The system SHALL authenticate users by email and password, issuing tokens upon successful verification. Failed attempts MUST be rate-limited to prevent brute force attacks.

#### Scenario: Successful login generates access token
- **WHEN** user provides correct email and password
- **THEN** system verifies credentials, generates JWT access token and refresh token, and redirects to dashboard

#### Scenario: Login fails with incorrect password
- **WHEN** user provides valid email but wrong password
- **THEN** system displays error "Invalid email or password" without revealing which field was wrong

#### Scenario: Login fails with non-existent email
- **WHEN** user attempts to login with email not in system
- **THEN** system displays error "Invalid email or password" without confirming email existence

#### Scenario: Rate limiting prevents brute force attacks
- **WHEN** user submits 5 failed login attempts within 15 minutes from same IP
- **THEN** system blocks further attempts from that IP for 15 minutes with message "Too many login attempts. Try again later."

### Requirement: JWT token generation and validation
The system SHALL generate and validate JSON Web Tokens (JWT) containing user identity. Access tokens MUST expire in 15 minutes; refresh tokens in 7 days.

#### Scenario: Access token contains user ID and email
- **WHEN** user logs in successfully
- **THEN** issued JWT access token contains user ID and email in payload

#### Scenario: Access token expires after 15 minutes
- **WHEN** user has valid access token and 15 minutes have passed
- **THEN** system rejects token as expired

#### Scenario: Refresh token renews access token
- **WHEN** user has valid refresh token but expired access token
- **THEN** system validates refresh token and issues new access token (extends session)

#### Scenario: Refresh token expires after 7 days
- **WHEN** 7 days have passed since refresh token issuance
- **THEN** system rejects refresh token, user must log in again

### Requirement: Session persistence and logout
The system SHALL maintain user sessions and provide logout capability to invalidate tokens.

#### Scenario: User remains logged in across page refreshes
- **WHEN** user logs in and refreshes the page
- **THEN** system uses stored refresh token to maintain session without requiring re-login

#### Scenario: Logout invalidates tokens
- **WHEN** user clicks logout button
- **THEN** system clears stored tokens and redirect to login page; session ends

#### Scenario: Token stored securely in HTTP-only cookie
- **WHEN** user logs in successfully
- **THEN** refresh token stored in HTTP-only cookie (inaccessible to JavaScript), preventing XSS token theft

### Requirement: Authentication required for protected resources
The system SHALL protect dashboard and profile endpoints, returning 401 Unauthorized without valid token.

#### Scenario: Dashboard accessible only with valid token
- **WHEN** unauthenticated user attempts to access dashboard
- **THEN** system redirects to login page

#### Scenario: API endpoint returns 401 for missing token
- **WHEN** API client requests protected endpoint without Authorization header
- **THEN** system returns 401 status with message "Unauthorized"

#### Scenario: API endpoint returns 401 for invalid token
- **WHEN** API client requests protected endpoint with malformed or expired token
- **THEN** system returns 401 status, never accepting invalid tokens
