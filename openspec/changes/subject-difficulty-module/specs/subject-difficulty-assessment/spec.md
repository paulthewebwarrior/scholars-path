## ADDED Requirements

### Requirement: Field and Subject Selection
The system SHALL provide a user interface for students to select an academic field (e.g., Computer Science, Mathematics, Biology) and enter a specific subject name within that field.

#### Scenario: Student selects field and enters subject
- **WHEN** student accesses the Subject Difficulty Module
- **THEN** system displays a dropdown or selection interface for academic fields
- **AND** upon field selection, system displays an input field to enter subject name

#### Scenario: Subject is recorded and persisted
- **WHEN** student enters a subject name and confirms
- **THEN** system stores the field and subject combination for the assessment session

### Requirement: Test Score Input
The system SHALL allow students to enter their latest quiz or test score for the selected subject.

#### Scenario: Student enters numeric score
- **WHEN** student is in the assessment form
- **THEN** system displays an input field labeling "Latest Quiz/Test Score"
- **AND** system accepts numeric values (0-100 or percentage format)

#### Scenario: Score validation
- **WHEN** student enters an invalid score (non-numeric, out of range)
- **THEN** system displays an error message and prevents form submission

### Requirement: Confidence Level Rating
The system SHALL allow students to rate their confidence level for the subject on a 1-5 scale.

#### Scenario: Student rates confidence
- **WHEN** student completes score entry
- **THEN** system displays a confidence rating interface (1-5 scale with clear labels)
- **AND** system stores the selected confidence level

#### Scenario: Confidence labels are intuitive
- **WHEN** student views the confidence scale
- **THEN** labels range from "Very Low Confidence" (1) to "Very High Confidence" (5)

### Requirement: Subject Assessment Data Collection
The system SHALL collect and validate all assessment data before allowing submission.

#### Scenario: Complete assessment submission
- **WHEN** student has filled field, subject, score, and confidence rating
- **THEN** system enables the submit button
- **AND** upon submission, system saves the complete assessment record

#### Scenario: Partial form submission prevention
- **WHEN** any required field is empty
- **THEN** system disables the submit button and displays which fields are required
