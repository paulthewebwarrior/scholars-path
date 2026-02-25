## Why

The platform currently lacks user authentication and profiles, making it impossible to personalize the productivity dashboard or track individual progress. By adding user registration, login, and profiles, we enable personalized experiences tailored to each student's course, year level, and career goals.

## What Changes

- Users can register new accounts with email and password
- Users can log in securely with email/password credentials
- Users have profiles containing name, course, year level, and career goal
- Authentication is required to access the dashboard
- User preferences drive personalized productivity recommendations

## Capabilities

### New Capabilities
- `user-registration`: User account creation with email validation and password security
- `user-login`: Authentication system with session management and secure login handling
- `user-profile`: Profile management with core fields (name, course, year level, career goal)

### Modified Capabilities
<!-- No existing specs are being modified for core behavior -->

## Impact

- **Backend**: New authentication endpoints, user database models, session management
- **Frontend**: Login/register pages, profile editor, protected routes, auth guards
- **Database**: Users table with encrypted credentials and profile fields
- **APIs**: New endpoints for auth flow, profile management
- **Dependencies**: May need bcrypt for password hashing, JWT for session tokens
