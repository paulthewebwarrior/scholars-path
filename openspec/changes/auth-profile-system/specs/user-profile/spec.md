## ADDED Requirements

### Requirement: User profile viewing
The system SHALL allow authenticated users to view their own profile containing name, course, year level, and career goal information.

#### Scenario: Authenticated user can view their profile
- **WHEN** authenticated user navigates to profile page
- **THEN** system displays user's name, course, year level, and career goal

#### Scenario: Profile displays registration timestamp
- **WHEN** user views their profile
- **THEN** system shows account creation date

#### Scenario: Unauthenticated access to profile redirected to login
- **WHEN** unauthenticated user attempts to access profile page
- **THEN** system redirects to login page

### Requirement: User profile updating
The system SHALL allow authenticated users to update their name, course, year level, and career goal at any time.

#### Scenario: User successfully updates profile fields
- **WHEN** authenticated user modifies name, course, year level, or career goal and clicks save
- **THEN** system validates inputs, updates database, and displays confirmation message

#### Scenario: Profile update fails with empty required fields
- **WHEN** user attempts to save profile with blank name, course, year level, or career goal
- **THEN** system displays "All fields are required" and does not save changes

#### Scenario: Profile changes persist across sessions
- **WHEN** user updates profile and logs out, then logs back in
- **THEN** system displays previously saved profile information

#### Scenario: Only authenticated user can update their own profile
- **WHEN** user attempts to modify another user's profile via API
- **THEN** system returns 403 Forbidden and does not modify profile

### Requirement: Profile field validation
The system SHALL validate profile data to ensure data quality and consistency.

#### Scenario: Name field accepts letters, spaces, and common punctuation
- **WHEN** user enters name like "Marie-Anne O'Connor"
- **THEN** system accepts name without validation error

#### Scenario: Name field rejects extremely long inputs
- **WHEN** user attempts to save name longer than 100 characters
- **THEN** system displays "Name too long (max 100 characters)" error

#### Scenario: Course field has consistent format
- **WHEN** user selects course from predefined list or enters custom course
- **THEN** system stores course value consistently for filtering/analytics

#### Scenario: Year level restricted to valid academic levels
- **WHEN** user selects year level
- **THEN** system offers options like "Freshman", "Sophomore", "Junior", "Senior" or equivalent

### Requirement: Career goal tracking
The system SHALL store and display career goals to support personalized recommendations in future features.

#### Scenario: Career goal field accepts free text
- **WHEN** user enters career goal like "Software Engineer at Google" or "Data Scientist"
- **THEN** system stores text without modification (trimmed, cleaned)

#### Scenario: Career goal updates influence personalization
- **WHEN** user updates career goal from "Software Engineer" to "Product Manager"
- **THEN** system adjusts personalized productivity recommendations based on new goal

#### Scenario: Career goal can be cleared
- **WHEN** user deletes career goal text and saves
- **THEN** system allows empty career goal and stores update

### Requirement: Profile data consistency and audit trail
The system SHALL maintain accurate profile update records for debugging and support purposes.

#### Scenario: System records profile update timestamp
- **WHEN** user modifies profile information
- **THEN** system updates "last_modified" timestamp in database

#### Scenario: Profile data not partially updated on error
- **WHEN** user submits profile update with one invalid field among multiple changes
- **THEN** system rejects entire update (atomic operation), no partial saves
