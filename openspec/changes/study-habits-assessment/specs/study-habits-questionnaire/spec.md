## ADDED Requirements

### Requirement: Display habit questionnaire form
The system SHALL present a comprehensive questionnaire form that captures 13 study habit and performance metrics organized into logical sections.

#### Scenario: Form loads successfully
- **WHEN** user navigates to the habits assessment page
- **THEN** system displays the complete questionnaire with all 13 fields grouped by category (study patterns, lifestyle, performance)

#### Scenario: Form displays all required fields
- **WHEN** the questionnaire form renders
- **THEN** the form includes fields for: study hours/day, sleep hours/day, phone usage hours, social media hours, gaming hours, breaks per day, coffee intake, exercise minutes, stress level (1-10), focus score (0-100), attendance %, assignments completed/week, and final grade

### Requirement: Validate questionnaire input
The system SHALL validate user input on the questionnaire form before submission to ensure data quality and provide immediate feedback.

#### Scenario: Valid input accepted
- **WHEN** user enters valid values (numeric within expected ranges, required fields populated)
- **THEN** system enables the submit button and shows no validation errors

#### Scenario: Invalid input rejected with feedback
- **WHEN** user enters invalid data (negative numbers, values outside ranges, missing required fields)
- **THEN** system displays inline error messages and disables submit until corrected

#### Scenario: Numeric ranges validated
- **WHEN** user enters values
- **THEN** system validates stress level (1-10), focus score (0-100), attendance (0-100%), and other metrics are within acceptable ranges

### Requirement: Submit questionnaire response
The system SHALL allow users to submit completed questionnaires and provide confirmation of submission.

#### Scenario: Successful submission
- **WHEN** user completes all required fields and clicks submit
- **THEN** system sends data to backend API, displays success message, and redirects to dashboard or next step

#### Scenario: Submission failure handling
- **WHEN** API call fails during submission
- **THEN** system displays error message and allows user to retry or save as draft

### Requirement: Save questionnaire draft
The system SHALL allow users to save their in-progress questionnaire responses to resume later.

#### Scenario: Draft saving
- **WHEN** user clicks "Save Draft" button
- **THEN** system stores current responses locally and displays confirmation message

#### Scenario: Resume from draft
- **WHEN** user returns to the questionnaire page with a saved draft
- **THEN** system restores previous responses and allows editing before final submission
