## ADDED Requirements

### Requirement: Generate personalized habit recommendations
The system SHALL analyze user's assessed habits against correlation data to provide customized actionable recommendations for improving academic performance.

#### Scenario: Recommendations generated on submission
- **WHEN** user completes and submits habit questionnaire
- **THEN** system generates 3-5 personalized recommendations based on user's specific habit patterns and calculated correlations

#### Scenario: Low sleep impact recommendation
- **WHEN** user's sleep_hours metric is below 7 hours AND sleep_hours shows strong positive correlation (r > 0.4) with performance
- **THEN** system recommends: "Increase sleep to 7-8 hours per night for better focus and grades"

#### Scenario: High phone usage impact recommendation
- **WHEN** user's phone_usage_hours exceeds 4 hours AND phone_usage shows strong negative correlation with performance
- **THEN** system recommends: "Reduce phone usage during study sessions - consider using app blockers"

#### Scenario: Exercise recommendation
- **WHEN** user's exercise_minutes is below 30 minutes AND exercise_minutes shows positive correlation with performance
- **THEN** system recommends: "Add 30+ minutes of daily exercise to improve focus and energy levels"

#### Scenario: Social media management
- **WHEN** user's social_media_hours exceeds 2 hours AND social_media shows negative correlation with performance
- **THEN** system recommends: "Limit social media to 30-60 minutes daily during study breaks only"

#### Scenario: Study schedule optimization
- **WHEN** user's study_hours is below 2 hours per day AND shows positive correlation with grades
- **THEN** system recommends: "Increase focused study time to 2-3 hours daily in consistent blocks"

### Requirement: Store and retrieve recommendations
The system SHALL persist recommendations linked to each assessment and provide retrieval for user access and tracking.

#### Scenario: Recommendations persisted with assessment
- **WHEN** recommendations are generated
- **THEN** system stores recommendations in habits_recommendations table linked to assessment_id with: recommendation_text, priority_rank, supporting_metric, correlation_strength, created_at

#### Scenario: User retrieves their recommendations
- **WHEN** user views their assessment results
- **THEN** system displays recommendations in priority order (strongest to weakest correlation basis)

#### Scenario: Recommendation history tracked
- **WHEN** user submits new assessment at later date
- **THEN** system retains previous recommendations for comparison and allows user to see how habits/recommendations have changed

### Requirement: Support iterative habit improvement
The system SHALL allow users to track progress toward recommendations and receive updated guidance as habits change.

#### Scenario: Recommendation feedback mechanism
- **WHEN** user views recommendations
- **THEN** system displays options to mark recommendation as "attempted", "completed", "not applicable", with timestamp for tracking behavior change

#### Scenario: Progress comparison
- **WHEN** user submits new assessment after previous one
- **THEN** system shows: "Previous study hours: 1.5h → Current: 2.5h ✓ - You're making progress on that recommendation!"

#### Scenario: Updated recommendations
- **WHEN** new assessment shows improved habits
- **THEN** system generates new recommendations acknowledging improvements and suggesting next focus areas based on remaining opportunities

### Requirement: Recommendation confidence and transparency
The system SHALL provide context for recommendations so users understand the reasoning behind suggestions.

#### Scenario: Recommendation rationale displayed
- **WHEN** user clicks "Why this recommendation?"
- **THEN** system shows: "Based on cohort data analysis, students who increased their sleep from X to Y hours improved their grades by Z% on average. Correlation strength: medium."

#### Scenario: Individual vs. cohort insights
- **WHEN** displaying recommendation
- **THEN** system notes: "Your study hours are 1.5h/day (vs. cohort average 2.5h/day)" to contextualize the user's relative position
