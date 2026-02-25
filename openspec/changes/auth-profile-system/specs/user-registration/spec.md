## ADDED Requirements

### Requirement: User account creation via registration form
The system SHALL allow users to create new accounts by providing email, password, and initial profile information (name, course, year level, career goal). The system MUST validate all inputs and enforce security constraints.

#### Scenario: Successful registration with valid inputs
- **WHEN** user submits registration form with valid email (not already registered), strong password, and complete profile information
- **THEN** system creates user account, hashes password with bcrypt, and redirects to login page with success message

#### Scenario: Registration fails with existing email
- **WHEN** user attempts to register with an email already associated with an account
- **THEN** system displays error "Email already registered" without creating account

#### Scenario: Registration fails with weak password
- **WHEN** user submits registration with password shorter than 8 characters or without mix of uppercase, lowercase, and numbers
- **THEN** system displays error "Password must be at least 8 characters with uppercase, lowercase, and numbers" and does not create account

#### Scenario: Registration fails with missing required fields
- **WHEN** user submits registration form with blank name, course, year level, or career goal fields
- **THEN** system displays "All fields are required" error and does not create account

#### Scenario: Registration validates email format
- **WHEN** user enters malformed email (missing @, invalid domain)
- **THEN** system displays "Invalid email format" and does not create account

### Requirement: Password security during registration
The system SHALL never store passwords in plaintext. All passwords MUST be hashed using bcrypt before storage in the database.

#### Scenario: Passwords are hashed before storage
- **WHEN** user successfully registers with a password
- **THEN** database stores hashed password, not original plaintext

#### Scenario: Password hashing uses cryptographic salt
- **WHEN** two users register with the same password
- **THEN** their stored hashes are different due to unique salts

### Requirement: Registration form client-side validation
The system SHALL provide immediate feedback on registration form inputs before submission to reduce server load and improve user experience.

#### Scenario: Real-time email validation feedback
- **WHEN** user types in email field
- **THEN** system shows "Invalid format" if email is malformed, clears when corrected

#### Scenario: Real-time password strength indicator
- **WHEN** user types password
- **THEN** system shows password strength (weak/medium/strong) with feedback on missing requirements

#### Scenario: Submit button disabled until form is valid
- **WHEN** form has missing or invalid fields
- **THEN** submit button is disabled and grayed out
