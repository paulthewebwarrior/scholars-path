## 1. Database Schema & Backend Setup

- [x] 1.1 Design and create habits_assessment table (assessment_id, user_id, 13 metrics columns, timestamps)
- [x] 1.2 Design and create habits_correlations table for storing correlation results
- [x] 1.3 Design and create habits_recommendations table for storing generated recommendations
- [x] 1.4 Add database migrations and version control for new tables
- [x] 1.5 Implement database encryption for sensitive habit metrics (AES-256)
- [x] 1.6 Create database indexes on user_id and created_at for query performance

## 2. Backend Models & API Setup

- [x] 2.1 Create HabitsAssessment model/DTO with validation for all 13 metrics
- [x] 2.2 Implement input validation (numeric ranges, required fields, type checking)
- [x] 2.3 Create HabitsCorrelation model for correlation results
- [x] 2.4 Create HabitsRecommendation model with recommendation text and metadata

## 3. API Endpoints - Assessment Management

- [x] 3.1 Implement POST /api/habits/{userId}/assessment to submit questionnaire
- [x] 3.2 Implement GET /api/habits/{userId}/latest to retrieve most recent assessment
- [x] 3.3 Implement GET /api/habits/{userId}/history to retrieve assessment history with pagination
- [x] 3.4 Add authentication/authorization checks (users can only access their own assessments)
- [x] 3.5 Implement error handling and validation error responses
- [x] 3.6 Add request logging for audit trail

## 4. API Endpoints - Analysis & Recommendations

- [x] 4.1 Implement GET /api/habits/{userId}/correlations to retrieve correlation insights
- [x] 4.2 Implement GET /api/habits/{userId}/recommendations to retrieve personalized recommendations
- [x] 4.3 Add filtering for correlations (only show |r| ≥ 0.3, confidence >= 95%)

## 5. Correlation Analysis Engine

- [x] 5.1 Create PearsonCorrelationCalculator utility to compute correlations between habit metrics and performance
- [x] 5.2 Implement Pearson correlation coefficient formula with proper statistical handling
- [x] 5.3 Calculate confidence intervals and p-values for each correlation
- [x] 5.4 Create correlation batch job that runs periodically (weekly/monthly) on all assessments
- [x] 5.5 Store correlation results with calculation metadata (sample size, timestamp)
- [x] 5.6 Implement correlation caching to avoid redundant calculations
- [x] 5.7 Export normalized habit metrics (0-1 scale) for future ML model integration

## 6. Recommendations Engine

- [x] 6.1 Create RecommendationGenerator utility class
- [x] 6.2 Implement rule engine: IF metric_value AND correlation_strength THEN recommendation
- [x] 6.3 Generate 3-5 personalized recommendations based on user's specific habits
- [x] 6.4 Implement sleep recommendation logic (if < 7h AND r > 0.4, recommend increase)
- [x] 6.5 Implement phone usage recommendation logic (if > 4h AND negative correlation, recommend reduce)
- [x] 6.6 Implement exercise recommendation logic (if < 30min AND positive correlation, recommend increase)
- [x] 6.7 Implement social media recommendation logic (if > 2h AND negative correlation, recommend limit)
- [x] 6.8 Implement study hours optimization logic (if < 2h AND positive correlation, recommend increase)
- [x] 6.9 Generate recommendations with priority ranking and supporting metrics
- [x] 6.10 Store recommendations linked to assessment with correlation strength metadata

## 7. Frontend - Questionnaire Form Component

- [x] 7.1 Create Angular ReactiveFormGroup component with all 13 form fields
- [x] 7.2 Organize form fields into logical sections (Study Patterns, Lifestyle, Performance Metrics)
- [x] 7.3 Implement form validation with real-time feedback
- [x] 7.4 Add input type validation (numeric fields, range constraints)
- [x] 7.5 Implement progress indicator showing completion percentage
- [x] 7.6 Create field-level error messages for invalid inputs
- [x] 7.7 Add accessibility attributes (labels, descriptions, ARIA roles)
- [x] 7.8 Implement form styling with responsive design for mobile and desktop

## 8. Frontend - Draft Saving & Form Management

- [x] 8.1 Implement localStorage support to save draft responses locally
- [x] 8.2 Add "Save Draft" button that persists current form state
- [x] 8.3 Implement logic to restore draft on form page reload
- [x] 8.4 Show draft status indicator (unsaved changes, last saved time)
- [x] 8.5 Implement confirmation dialog before leaving page with unsaved changes
- [x] 8.6 Clear draft after successful submission

## 9. Frontend - Form Submission & Results

- [x] 9.1 Implement form submission handler with loading state
- [x] 9.2 Call POST /api/habits/{userId}/assessment with form data
- [x] 9.3 Handle submission errors with user-friendly error messages
- [x] 9.4 Implement retry logic for failed submissions
- [x] 9.5 Display success message after successful submission
- [x] 9.6 Redirect to results/recommendations page after submission
- [x] 9.7 Disable submit button during API call to prevent double submissions

## 10. Frontend - Results & Recommendations Dashboard

- [x] 10.1 Create results page component to display assessment results
- [x] 10.2 Display user's submitted habit metrics for reference
- [x] 10.3 Show top 5 habits correlated with performance (positive and negative)
- [x] 10.4 Display correlation coefficients and confidence intervals
- [x] 10.5 Add tooltip: "Correlation does not imply causation" on hover
- [x] 10.6 Display 3-5 personalized recommendations in priority order
- [x] 10.7 Add "Why this recommendation?" expandable sections showing cohort context
- [x] 10.8 Implement recommendation feedback buttons (attempted, completed, not applicable)
- [x] 10.9 Show previous assessment comparison when available

## 11. Testing - Backend

- [ ] 11.1 Unit tests for HabitsAssessment model validation
- [ ] 11.2 Unit tests for PearsonCorrelationCalculator
- [ ] 11.3 Unit tests for RecommendationGenerator rules
- [ ] 11.4 Integration tests for POST /api/habits assessment submission
- [ ] 11.5 Integration tests for GET /api/habits endpoints
- [ ] 11.6 Authorization tests (verify users can't access others' data)
- [ ] 11.7 Database tests for data persistence and retrieval
- [ ] 11.8 Test edge cases (null values, invalid ranges, empty assessments)

## 12. Testing - Frontend

- [ ] 12.1 Unit tests for form validation logic
- [ ] 12.2 Unit tests for draft save/restore functionality
- [ ] 12.3 Component tests for questionnaire form rendering
- [ ] 12.4 Component tests for form submission flow
- [ ] 12.5 E2E tests for end-to-end questionnaire completion
- [ ] 12.6 E2E tests for results/recommendations display
- [ ] 12.7 Cross-browser testing (Chrome, Firefox, Safari)
- [ ] 12.8 Mobile responsiveness testing

## 13. Security & Privacy

- [ ] 13.1 Implement input sanitization to prevent XSS attacks
- [ ] 13.2 Add CSRF protection to form submission
- [ ] 13.3 Verify HTTPS enforcement for all assessment endpoints
- [ ] 13.4 Implement rate limiting on assessment submission endpoint
- [ ] 13.5 Test encryption of sensitive metrics at rest
- [ ] 13.6 Add privacy policy documentation for habit data collection
- [ ] 13.7 Implement data deletion/anonymization request handling

## 14. Integration & Deployment

- [x] 14.1 Integrate assessment results into user dashboard
- [x] 14.2 Add link to questionnaire from main navigation
- [x] 14.3 Prepare data export pipeline for future ML model integration
- [ ] 14.4 Create documentation for API endpoints (Swagger/OpenAPI)
- [x] 14.5 Set up monitoring/logging for correlation calculation job
- [ ] 14.6 Create database backup strategy for assessment data
- [ ] 14.7 Deploy to staging environment for QA testing
- [ ] 14.8 Perform performance testing under load
- [ ] 14.9 Production deployment with rollback plan
- [ ] 14.10 Monitor error rates and user feedback post-launch

## 15. Documentation & Analytics

- [ ] 15.1 Create user documentation for questionnaire completion
- [ ] 15.2 Write developer guide for correlation/recommendation algorithms
- [ ] 15.3 Document API endpoints with example requests/responses
- [ ] 15.4 Create database schema documentation
- [ ] 15.5 Set up analytics to track questionnaire completion rates
- [ ] 15.6 Create dashboard for admin to view aggregate habit statistics
- [ ] 15.7 Document methodology for correlation analysis on dashboard UI
