## ADDED Requirements

### Requirement: Calculate habit-performance correlations
The system SHALL compute statistical correlations between each habit metric and academic performance indicators to identify patterns and insights.

#### Scenario: Correlation calculation triggered
- **WHEN** new assessment is submitted or batch analysis runs
- **THEN** system computes Pearson correlation coefficients between each of the 12 habit metrics and final_grade (or average assignment score if grade unavailable)

#### Scenario: Study hours correlation identified
- **WHEN** correlation analysis runs
- **THEN** system calculates correlation coefficient between study_hours and academic_performance metric showing positive/negative relationship

#### Scenario: Sleep and focus correlation tracked
- **WHEN** analysis executes
- **THEN** system computes correlation between sleep_hours and focus_score, and separately between sleep_hours and final_grade

#### Scenario: Lifestyle factor analysis
- **WHEN** correlation analysis runs
- **THEN** system calculates correlations for phone_usage_hours, social_media_hours, gaming_hours, coffee_intake, exercise_minutes, and breaks_per_day against performance metrics

### Requirement: Store correlation results
The system SHALL persist calculated correlations with confidence metrics for display and trend tracking.

#### Scenario: Correlation results persisted
- **WHEN** correlation calculation completes
- **WHEN** system stores correlation coefficients in habits_correlations table with: metric_name, performance_metric, correlation_coefficient, sample_size, confidence_interval, calculation_timestamp

#### Scenario: Correlation updates with new data
- **WHEN** new assessments are submitted over time
- **THEN** system recalculates correlations periodically (weekly/monthly) to reflect growing dataset

### Requirement: Provide correlation insights
The system SHALL present correlation findings to users through dashboards and notifications with statistical confidence levels.

#### Scenario: User views correlation dashboard
- **WHEN** user accesses habits analytics dashboard
- **THEN** system displays top 5 habits most strongly correlated with performance (positive and negative), with correlation coefficients and confidence intervals

#### Scenario: Insight threshold filtering
- **WHEN** dashboard loads
- **THEN** system only displays correlations with |r| ≥ 0.3 (moderate strength) and confidence >= 95% to avoid spurious correlations

#### Scenario: Correlation methodology displayed
- **WHEN** user hovers over correlation metrics
- **THEN** system displays tooltip: "Correlation does not imply causation. These results show statistical relationships in this cohort's data."

### Requirement: Prepare data for model integration
The system SHALL format habit correlations and metrics for future integration with ML model retraining.

#### Scenario: Normalized feature export
- **WHEN** correlation analysis completes
- **THEN** system exports habit metrics in normalized format (0-1 scale) suitable for model training, stored in separate analytics export table

#### Scenario: Data quality metrics
- **WHEN** export runs
- **THEN** system calculates and records: number of complete assessments, missing data percentage per metric, temporal distribution of submissions for model training purposes
