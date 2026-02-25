## Context

The Scholars' Path application currently tracks student productivity and study habits. The backend is built with Python and uses TensorFlow models for analysis. The frontend is an Angular application. Existing systems include habit tracking, productivity correlation analysis, and a study habits questionnaire. The Subject Difficulty Module will extend this ecosystem to help students understand their performance gaps and identify weak subjects.

Current application stack:
- **Backend**: Python-based API server
- **Frontend**: Angular Single Page Application
- **Data**: CSV-based datasets and TensorFlow models
- **Existing features**: Study habits questionnaire, productivity correlation, habits data storage

## Goals / Non-Goals

**Goals:**
- Enable students to assess subject difficulty and performance across multiple academic fields
- Identify weak subjects based on test scores
- Calculate and visualize the gap between student confidence and actual performance
- Provide personalized recommendations based on confidence-performance analysis
- Integrate seamlessly with existing study habits and productivity systems
- Store subject difficulty assessments for historical analysis and improvement tracking

**Non-Goals:**
- This module does NOT create or manage study plans or schedules
- Does NOT directly modify the productivity correlation algorithm (though may provide input data)
- Does NOT handle tutoring recommendations or external resource linking (future phase)
- Does NOT perform real-time quiz/test score synchronization (manual entry only)
- Does NOT implement gamification or achievement badges in this phase

## Decisions

### 1. Data Model: Subject Assessments
**Decision**: Create a new `SubjectAssessment` entity with fields: field, subject_name, test_score, confidence_level, assessment_date, user_id

**Rationale**: 
- Normalizing this data allows for efficient querying of weak subjects and gap analysis
- Maintains separation from study habits data (different concern)
- Enables historical tracking and trend analysis over time

**Alternatives Considered**:
- Storing assessments as flat JSON in habits data: Would reduce schema clarity and make gap analysis queries complex
- Using only test scores without confidence: Would not support gap analysis

### 2. Architecture: Analysis Engine Separation
**Decision**: Implement weak subject identification and performance gap analysis as separate backend services/modules, not UI logic

**Rationale**:
- Ensures consistency across platforms (web, mobile future)
- Enables these analyses to be used by other features (recommendations, study planning)
- Allows for algorithm improvements without UI changes
- Better testability and reusability

**Alternatives Considered**:
- Client-side JavaScript calculations: Risk of inconsistency, performance issues with large datasets, security of calculations

### 3. Weak Subject Threshold
**Decision**: Define "weak subject" as test_score < 70%

**Rationale**:
- Clear, understandable threshold for students
- Aligns with common academic standards (C-level performance)
- Can be adjusted later if data shows different optimal threshold

**Alternatives Considered**:
- Dynamic threshold based on user's average: Too complex initially, can add as enhancement
- Lower threshold (60%): More lenient, might miss opportunities for growth

### 4. Performance Gap Calculation
**Decision**: Gap = confidence_level - (test_score / 20), rounded to nearest 0.5
- Positive gap: Underconfident (confidence higher than warrant)
- Negative gap: Overconfident (confidence lower than warranted)
- Gap near 0: Well-aligned

**Rationale**:
- Simple, interpretable metric
- Scale of 1-5 for confidence normalizes with 0-100 score range
- Rounding prevents false precision

**Alternatives Considered**:
- Percentage-based gap: More complex, less intuitive
- Categorical classifications only: Loses nuance of how far off confidence is

### 5. Frontend Integration
**Decision**: Add Subject Difficulty Module as a new section in the main student dashboard, with separate assessment form and results view

**Rationale**:
- Clear separation of concerns
- Non-disruptive to existing workflow
- Students can navigate to it when ready to assess

**Alternatives Considered**:
- Integrate into existing study habits questionnaire: Would make that form too long and complex
- Popup/modal only: Would feel secondary to core experience

### 6. Data Persistence
**Decision**: Store assessments in backend database (alongside other user data), not in session/local storage

**Rationale**:
- Enables historical analysis and trend tracking
- Survives page refreshes/sessions
- Allows backend analysis to aggregate across time

## Risks / Trade-offs

| Risk | Mitigation |
|------|-----------|
| Manual score entry leads to data quality issues (typos, guessing) | Implement input validation (0-100 range), confirmation step before saving, option to edit/delete assessments |
| Confidence self-rating may not correlate with actual ability | Document that confidence is subjective; emphasis on trends over single entries; consider calibration exercises |
| Gap threshold of 70% may not suit all students/fields | Store raw score for future re-analysis; make threshold configurable in admin panel; gather user feedback |
| Performance at scale if many subjects assessed | Implement pagination/lazy loading in UI; index assessments by user_id and date; consider caching for gap calculations |
| Integration complexity with existing productivity system | Use event pattern: emit "subject_assessed" event that productivity service can optionally subscribe to |
| Student overwhelm from too many weak subjects | Prioritize display (sort by lowest score); suggest focusing on top 3 weakest; progressive disclosure of details |

## Migration Plan

**Phase 1: Backend Implementation**
1. Design and create `SubjectAssessment` database schema
2. Implement API endpoints:
   - `POST /api/assessments` - Submit new assessment
   - `GET /api/assessments` - List user's assessments
   - `GET /api/weak-subjects` - Get weak subjects with analysis
   - `GET /api/performance-gaps` - Get gap analysis
3. Implement analysis engine (weak subject ID, gap calculation)
4. Add unit tests for analysis logic

**Phase 2: Frontend Implementation**
1. Create assessment form component (field selection, subject input, score entry, confidence rating)
2. Create results view component (weak subjects list, gap analysis visualization)
3. Add routing for new module pages
4. Integrate with existing dashboard navigation
5. Add e2e tests

**Phase 3: Integration & Deployment**
1. Test API integration with frontend
2. User acceptance testing
3. Deploy to staging environment
4. Production rollout with feature flag (initially disabled)
5. Monitor for errors, data quality issues

**Rollback Strategy**:
- Feature flag to disable module for all users
- Assessment data retained but not displayed/analyzed if issues arise
- Can revert database schema if critical data structure issues found (within first 24-48 hours)

## Open Questions

1. **Score Format**: Should system accept 0-100 percentage only, or also 0-letter grades (A-F), 0-points format? Recommend: 0-100 percentage for MVP, extensible later.

2. **Multiple Assessments Same Subject**: Should system show all historical assessments or just the latest? Recommend: Latest by default, with history view as option.

3. **Data Visualization**: What visualization types for gap analysis? Recommend: Bar chart (confidence vs performance), heatmap (many subjects).

4. **Field Categories**: Should fields be predefined (hardcoded list) or user-created/free-form? Recommend: Predefined set initially (CS, Math, Biology, etc.), can extend later.

5. **Integration with Recommendations**: Should weak subject data feed automatically into study recommendations system? Recommend: Yes, architecture should support this, but detailed integration left for follow-up feature.
