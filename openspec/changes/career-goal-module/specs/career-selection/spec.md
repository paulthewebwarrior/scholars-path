## ADDED Requirements

### Requirement: User can select career during onboarding
The system SHALL allow users to select a target career during initial profile setup. The selected career SHALL be saved to the user's profile.

#### Scenario: Career selection appears in onboarding
- **WHEN** a new user completes authentication and enters the profile setup flow
- **THEN** the system displays a career selection step with the available career options

#### Scenario: User selects a career
- **WHEN** user selects a career from the list (e.g., "Software Developer")
- **THEN** the system saves the selection to the user's profile and proceeds to the next step

#### Scenario: No career selected
- **WHEN** user attempts to proceed without selecting a career
- **THEN** the system displays a validation error and prevents progression until a career is selected

### Requirement: User can view their selected career
The system SHALL display the user's currently selected career on their profile page.

#### Scenario: View career on profile
- **WHEN** user visits their profile page
- **THEN** the system displays their currently selected career

### Requirement: User can change their career selection
The system SHALL allow users to update their selected career at any time from their profile settings.

#### Scenario: Update career
- **WHEN** user clicks "Edit" on their career selection and chooses a different career
- **THEN** the system updates the career, saves it to the profile, and persists the change

#### Scenario: Career update triggers recommendation refresh
- **WHEN** user changes their career selection
- **THEN** the system updates and refreshes all career-aligned recommendations on the dashboard within 2 seconds

### Requirement: Career dropdown displays available careers
The system SHALL provide a dropdown or selection list with the five predefined careers: Software Developer, Data Analyst, Cybersecurity Specialist, Doctor, Engineer.

#### Scenario: Dropdown shows all careers
- **WHEN** user clicks the career selection dropdown
- **THEN** the system displays all five career options in alphabetical order

#### Scenario: Career labels are clear
- **WHEN** user hovers over a career option (on web) or taps it (on mobile)
- **THEN** the system may display a brief description (e.g., "Software Developer: Build and maintain software systems")
