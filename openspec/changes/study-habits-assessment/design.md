## Context

The current productivity prediction system uses a trained ML model but lacks comprehensive user habit data. Students need to self-report their daily behaviors and academic metrics through a structured questionnaire. This data will be stored and used to improve prediction accuracy and provide personalized insights.

**Current State:**
- ML model exists (trained on partial dataset) for productivity prediction
- No structured habit assessment mechanism
- User profiles exist in authentication system
- Database schema supports user-profile relationship

**Stakeholders:** Students (users), backend team (API development), frontend team (form UI), ML/data team (model training and analysis).

## Goals / Non-Goals

**Goals:**
- Provide a user-friendly questionnaire form for collecting 13 habit metrics
- Persist habit assessments securely linked to user profiles
- Enable basic correlation analysis between habits and academic outcomes
- Prepare data infrastructure for future ML model enhancements

**Non-Goals:**
- Real-time habit tracking (out of scope; questionnaire is point-in-time assessment)
- Mobile app support (scope limited to web)
- Advanced predictive modeling (initial phase focuses on data collection)
- Third-party integrations for habit tracking (e.g., phone usage APIs)

## Decisions

**1. Frontend Form Architecture**
- **Decision**: Use reactive form component (Angular) with field-level validation
- **Rationale**: Ensures data quality before submission, enables progressive validation feedback, integrates with existing Angular architecture
- **Alternative Considered**: Server-side validation only → Rejected due to worse UX and higher server load

**2. Data Storage Model**
- **Decision**: Create `habits_assessment` table with denormalized metrics and a `habit_trends` table for historical tracking
- **Rationale**: Denormalization optimizes for analytical queries; separates assessments from user profile data for cleaner schema
- **Alternative**: Single table with all data → Would complicate historical analysis and trend calculations

**3. API Design**
- **Decision**: POST endpoint `/api/habits/<userId>/assessment` to submit questionnaire; GET endpoint to retrieve user's assessment history
- **Rationale**: RESTful convention, user-scoped endpoints ensure privacy, history retrieval enables trend visualization
- **Alternative**: Single generic endpoint → Less explicit, harder to manage permissions

**4. Correlation Analysis**
- **Decision**: Compute Pearson correlation coefficients between each habit metric and final grade (offline, batch processing)
- **Rationale**: Statistical soundness, computationally simple, results cached for fast dashboard querying
- **Alternative**: Real-time correlation → Overkill for initial phase, adds unnecessary computation

**5. Data Integration with ML Model**
- **Decision**: Make habit features optional/supplementary in model predictions (don't retrain initial model; prepare data pipeline)
- **Rationale**: Avoids immediate model retraining risk; establishes data pipeline for future updates
- **Alternative**: Immediate model retraining → Higher risk; insufficient data volume for initial phase

## Risks / Trade-offs

| Risk | Mitigation |
|------|-----------|
| Data entry burden (13 fields may cause abandonment) → Implement optional fields, provide progress indicator, allow draft saving |
| Correlation misinterpretation (correlation ≠ causation) → Display confidence intervals, document methodology in UI |
| Privacy concerns (tracking phone/gaming habits) → Encrypt stored data, comply with privacy policy, make collection voluntary |
| Schema scalability (adding more habit metrics later) → Design habits table with JSONB column for flexible metric storage |
| Grade leakage in model testing → Prepare "no-grade" dataset variant for evaluation; distinguish train/test phases |

## Migration Plan

1. **Phase 1**: Deploy backend API and database schema (no frontend yet); provide manual testing endpoints
2. **Phase 2**: Release frontend questionnaire form in beta; collect initial responses
3. **Phase 3**: Compute initial correlations; publish analytics dashboard
4. **Phase 4**: (Future) Integrate habits data into retrained ML model

## Open Questions

- Should questionnaire be mandatory for all new users or optional?
- What frequency for re-assessment? (One-time, weekly, monthly?)
- How to handle incomplete assessments (auto-save drafts)?
