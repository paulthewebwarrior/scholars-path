## ADDED Requirements

### Requirement: Weak Subject Identification Logic
The system SHALL analyze submitted subject assessments and identify weak subjects based on test performance.

#### Scenario: Subject classified as weak
- **WHEN** a student submits an assessment with a test score below 70%
- **THEN** system classifies that subject as weak

#### Scenario: Subject classified as strong
- **WHEN** a student submits an assessment with a test score of 70% or above
- **THEN** system classifies that subject as strong or competent

#### Scenario: Multiple weak subjects ranking
- **WHEN** student has submitted assessments for multiple subjects
- **THEN** system ranks weak subjects by performance score (lowest first)

### Requirement: Weak Subject Display
The system SHALL display identified weak subjects in a clear, prioritized list.

#### Scenario: Weak subjects list generation
- **WHEN** assessment analysis completes
- **THEN** system generates a list of weak subjects sorted by performance (lowest to highest)
- **AND** list includes subject name, field, and score for each weak subject

#### Scenario: No weak subjects identified
- **WHEN** all assessed subjects have scores of 70% or above
- **THEN** system displays a positive message confirming student strength across all subjects

#### Scenario: Initial state with no assessments
- **WHEN** student has submitted no assessments yet
- **THEN** system displays a message prompting student to enter subject assessments

### Requirement: Weak Subject Metadata
The system SHALL track and display additional context for weak subjects.

#### Scenario: Subject details display
- **WHEN** student views weak subject in the list
- **THEN** system displays: subject name, field, latest score, date of assessment, and confidence level

#### Scenario: History of weak subjects
- **WHEN** student has reassessed a previously weak subject
- **THEN** system shows both current and previous scores allowing student to track improvement

### Requirement: Weak Subject Recommendations
The system SHALL suggest study recommendations for identified weak subjects.

#### Scenario: Study resource suggestions
- **WHEN** a weak subject is identified
- **THEN** system may suggest: topic breakdown, recommended study methods, or prerequisite topics to review

#### Scenario: Confidence-based recommendations
- **WHEN** weak subject shows low confidence
- **THEN** system suggests confidence-building strategies in addition to performance improvement strategies
