## ADDED Requirements

### Requirement: Performance Gap Calculation
The system SHALL calculate the gap between a student's confidence level and their actual test performance.

#### Scenario: Positive gap (underconfident)
- **WHEN** student has low confidence (1-2) but high score (70%+)
- **THEN** system calculates a positive gap and identifies student as underconfident
- **AND** gap value = confidence_level - (score/20) rounded to nearest 0.5

#### Scenario: Negative gap (overconfident)
- **WHEN** student has high confidence (4-5) but low score (<70%)
- **THEN** system calculates a negative gap and identifies student as overconfident
- **AND** gap value = confidence_level - (score/20) rounded to nearest 0.5

#### Scenario: Aligned performance and confidence
- **WHEN** student's confidence rating aligns with test performance
- **THEN** system calculates gap close to zero (within ±0.5 range)

### Requirement: Gap Analysis Report Generation
The system SHALL generate a comprehensive performance gap analysis report.

#### Scenario: Gap summary display
- **WHEN** analysis completes for assessed subjects
- **THEN** system displays a summary showing:
  - Total number of subjects analyzed
  - Number of underconfident subjects
  - Number of overconfident subjects
  - Number of well-aligned subjects

#### Scenario: Individual subject gap visualization
- **WHEN** student views individual subject details
- **THEN** system displays confidence level, actual score, and visual gap indicator
- **AND** visual indicator clearly shows if student is underconfident or overconfident

#### Scenario: Gap trend analysis
- **WHEN** student has multiple assessment records for same subject over time
- **THEN** system shows how confidence-performance gap has changed

### Requirement: Confidence-Performance Insights
The system SHALL provide actionable insights based on identified gaps.

#### Scenario: Overconfidentence insights
- **WHEN** a subject shows overconfidence (high confidence, low score)
- **THEN** system suggests: realistic self-assessment strategies, focused study on weak topics, and practice tests

#### Scenario: Underconfidence insights
- **WHEN** a subject shows underconfidence (low confidence, high score)
- **THEN** system suggests: confidence building strategies, recognition of actual competence, and advanced learning opportunities

#### Scenario: Aligned performance insights
- **WHEN** confidence and performance are well-aligned
- **THEN** system suggests: consolidating knowledge or exploring related advanced topics

### Requirement: Gap Analysis Data Export
The system SHALL allow students to view their performance gap analysis in exportable format.

#### Scenario: View performance gap report
- **WHEN** student completes multiple assessments
- **THEN** system generates a comprehensive report with all gaps calculated and visualized

#### Scenario: Performance comparison
- **WHEN** student has assessments across multiple fields
- **THEN** system allows filtering and comparing gaps by field or subject
