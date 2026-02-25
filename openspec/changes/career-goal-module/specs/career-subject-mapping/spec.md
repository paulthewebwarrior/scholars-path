## ADDED Requirements

### Requirement: System maps skill areas to academic subjects
The system SHALL define which academic subjects are relevant to each skill area. The mapping SHALL be curated and static for MVP.

#### Scenario: Skill area has associated subjects
- **WHEN** the system loads skill area metadata for a career
- **THEN** each skill area (e.g., "Programming", "Statistics") has an associated list of relevant academic subjects

#### Scenario: Example subjects for Programming skill
- **WHEN** system retrieves subjects for the Programming skill area
- **THEN** the list includes subjects such as: Computer Science, Software Development, Introduction to Programming, Object-Oriented Programming

#### Scenario: Example subjects for Statistics skill
- **WHEN** system retrieves subjects for the Statistics skill area
- **THEN** the list includes subjects such as: Statistics, Mathematics, Data Analysis, Probability Theory

### Requirement: API retrieves subjects for skill areas
The system SHALL provide an endpoint to fetch academic subjects for a given skill area within a career context.

#### Scenario: Fetch subjects for skill area
- **WHEN** client calls GET `/api/careers/{careerName}/skills/{skillId}/subjects`
- **THEN** the system returns a JSON list of relevant academic subjects

#### Scenario: Subject includes metadata
- **WHEN** system returns a subject
- **THEN** the subject includes: name, field of study, description, and relevance indicator

### Requirement: Subject recommendations respect user's field of study
When mapping skills to subjects, the system SHALL filter subjects by the user's declared field of study (e.g., Computer Science, Medicine, Business).

#### Scenario: User field filters subject recommendations
- **WHEN** user's field is "Computer Science" and career is "Data Analyst"
- **THEN** system returns only subjects available within Computer Science (e.g., Statistics, Programming, not Organic Chemistry)

#### Scenario: Cross-disciplinary subjects are included
- **WHEN** a skill area (e.g., "Statistics") is needed for multiple fields
- **THEN** system includes that subject in recommendations regardless of field

### Requirement: System provides subject difficulty context
Each subject recommendation SHALL include an indicator of how weak the user is in that subject, based on assessment data.

#### Scenario: Subject shows performance indicator
- **WHEN** system generates subject recommendations for a user
- **THEN** each subject includes the user's latest quiz score or confidence rating in that area
