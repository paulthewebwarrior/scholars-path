## ADDED Requirements

### Requirement: Store habit assessment data
The system SHALL securely persist questionnaire responses in the database, linked to user profiles with timestamps for audit and historical tracking.

#### Scenario: Assessment persisted successfully
- **WHEN** user submits a valid questionnaire
- **THEN** system stores all 13 habit metrics in database with user ID, submission timestamp, and assessment ID

#### Scenario: Assessment linked to user profile
- **WHEN** assessment is stored
- **THEN** system creates foreign key relationship between habits_assessment table and user_profile table ensuring data integrity

#### Scenario: Multiple assessments tracked
- **WHEN** user submits a new assessment after a previous one
- **THEN** system stores both assessments with distinct timestamps allowing historical tracking of habit changes

### Requirement: Retrieve assessment history
The system SHALL provide API endpoints to retrieve a user's current and historical habit assessments.

#### Scenario: User retrieves latest assessment
- **WHEN** user requests their current assessment via GET /api/habits/{userId}/latest
- **THEN** system returns the most recent assessment with all 13 metrics and submission timestamp

#### Scenario: User retrieves assessment history
- **WHEN** user requests assessment history via GET /api/habits/{userId}/history
- **THEN** system returns paginated list of all past assessments ordered by most recent first

#### Scenario: Assessment access control
- **WHEN** user attempts to retrieve another user's assessment
- **THEN** system denies access and returns 403 Forbidden error

### Requirement: Database schema for habits data
The system SHALL maintain a normalized database schema to store habit assessments with efficient querying and historical tracking capabilities.

#### Scenario: Habits assessment table structure
- **WHEN** database schema is initialized
- **THEN** habits_assessment table exists with columns: assessment_id (PK), user_id (FK), study_hours, sleep_hours, phone_usage_hours, social_media_hours, gaming_hours, breaks_per_day, coffee_intake, exercise_minutes, stress_level, focus_score, attendance_percentage, assignments_completed_per_week, final_grade, created_at, updated_at

#### Scenario: Audit trail captured
- **WHEN** assessment is created or updated
- **THEN** system automatically records created_at timestamp and updates updated_at timestamp

### Requirement: Data encryption and privacy
The system SHALL encrypt sensitive habit data and restrict access according to user privacy policies.

#### Scenario: Habit data encrypted at rest
- **WHEN** assessment data is stored in database
- **THEN** system encrypts personal habit metrics using AES-256 encryption

#### Scenario: Grade data handling
- **WHEN** assessment includes optional final grade
- **THEN** system stores grade separately with flag indicating whether user opted-in to grade collection for analytics
