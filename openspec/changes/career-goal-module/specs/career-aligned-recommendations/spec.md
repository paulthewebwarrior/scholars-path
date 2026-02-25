## ADDED Requirements

### Requirement: Recommendation engine generates career-aligned subject recommendations
When generating recommendations, the system SHALL prioritize weak subjects that align with the user's selected career's skill requirements.

#### Scenario: Weak subject aligned with career is prioritized
- **WHEN** user has a low score in "Data Structures" and career is "Software Developer"
- **THEN** "Data Structures" appears as a high-priority recommendation

#### Scenario: Weak subject not aligned with career has lower priority
- **WHEN** user has a low score in "Art History" and career is "Software Developer"
- **THEN** "Art History" may be recommended but with lower priority than career-aligned weak subjects

#### Scenario: Recommendation includes career relevance context
- **WHEN** system generates a subject recommendation
- **THEN** the recommendation includes a message explaining why it matters for the user's career (e.g., "Critical for Software Developer careers")

### Requirement: Dashboard displays career-aligned recommendations prominently
The dashboard SHALL highlight subject improvement recommendations that are aligned with the user's career goal.

#### Scenario: Career-aligned section on dashboard
- **WHEN** user views their dashboard
- **THEN** a section titled "Improve Skills for [Career]" displays the top 3 weak subjects relevant to the user's career

#### Scenario: Career recommendations are actionable
- **WHEN** career-aligned recommendations are displayed
- **THEN** each recommendation includes suggested resources (curated static links) for that subject

### Requirement: Simulation mode respects career alignment
When user adjusts study inputs in simulation mode, recommendations SHALL remain aligned with the user's selected career.

#### Scenario: Simulated habit changes recalculate career recommendations
- **WHEN** user adjusts phone usage or study hours in the simulation panel
- **THEN** the system recalculates productivity score and updates career-aligned recommendations accordingly

#### Scenario: Simulation shows skill gap closure progress
- **WHEN** user simulates improvement in a weak subject
- **THEN** the system shows how that improvement impacts alignment with the user's career skill requirements (e.g., "Closes 15% of Data Structures gap")

### Requirement: API endpoint provides career-aligned recommendations
The system SHALL provide an endpoint that returns personalized recommendations filtered and prioritized by career relevance.

#### Scenario: Get career-aligned recommendations
- **WHEN** client calls GET `/api/users/{userId}/recommendations/career-aligned`
- **THEN** the system returns a prioritized list of weak subjects and improvement suggestions relevant to the user's selected career

#### Scenario: Recommendations include resource links
- **WHEN** system returns career-aligned recommendations
- **THEN** each recommendation includes at least one curated static resource link (Khan Academy, Kaggle, etc.) for learning support

### Requirement: Career context integrates with rule-based recommendation engine
Career-aligned subject recommendations SHALL work in conjunction with existing rule-based recommendations (stress management, habit improvements, etc.).

#### Scenario: Multiple recommendation types coexist
- **WHEN** user views recommendations
- **THEN** both career-aligned subject recommendations and general habit-improvement recommendations (e.g., "Reduce phone usage") are displayed together in a prioritized list

#### Scenario: Dashboard shows recommendation hierarchy
- **WHEN** user views the main dashboard
- **THEN** recommendations are organized by impact and type: career-critical weak subjects, then general habit improvements, then other resources
