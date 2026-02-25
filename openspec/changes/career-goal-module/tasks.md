## 1. Database Schema and Seed Data

- [ ] 1.1 Create `careers` table with fields: id, name, description
- [ ] 1.2 Create `skill_areas` table with fields: id, name, description, importance_level
- [ ] 1.3 Create `career_skills` junction table linking careers to skill areas
- [ ] 1.4 Create `subjects` table with fields: id, name, field_of_study, description
- [ ] 1.5 Create `skill_subjects` junction table linking skill areas to subjects
- [ ] 1.6 Add `career_id` foreign key to `users` table (nullable for existing users)
- [ ] 1.7 Create and run seed data migrations for: 5 careers, core skill areas, skill-area mappings, academic subjects, skill-subject mappings
- [ ] 1.8 Set up database indexes on foreign keys and frequently queried columns

## 2. Backend Career API Endpoints

- [ ] 2.1 Implement GET `/api/careers` endpoint to list all available careers
- [ ] 2.2 Implement GET `/api/careers/{careerName}` endpoint to fetch single career with metadata
- [ ] 2.3 Implement GET `/api/careers/{careerName}/skills` endpoint to return skill areas for a career
- [ ] 2.4 Implement GET `/api/careers/{careerName}/skills/{skillId}/subjects` endpoint to return subjects for a skill
- [ ] 2.5 Add input validation and error handling for all career endpoints
- [ ] 2.6 Add unit tests for all career API endpoints

## 3. Backend Profile and Career Management

- [ ] 3.1 Create or update database migration to add `career_id` to users table
- [ ] 3.2 Implement POST `/api/profile/career` endpoint to set user's selected career
- [ ] 3.3 Implement PUT `/api/profile/career` endpoint to update user's career
- [ ] 3.4 Update GET `/api/profile` endpoint to include user's selected career
- [ ] 3.5 Add validation to ensure career_id exists before saving
- [ ] 3.6 Add unit tests for career update endpoints

## 4. Recommendation Engine Integration

- [ ] 4.1 Audit existing rule-based recommendation engine for integration points
- [ ] 4.2 Create new function: `get_career_skill_areas(career_id)` to retrieve required skills for user's career
- [ ] 4.3 Create new function: `get_weak_subjects_for_skills(user_id, skill_areas)` to identify weak subjects matching career skills
- [ ] 4.4 Modify recommendation generation to prioritize career-aligned subjects: integrate into main recommendation generation pipeline
- [ ] 4.5 Create new endpoint: GET `/api/users/{userId}/recommendations/career-aligned` to return prioritized recommendations
- [ ] 4.6 Ensure career recommendations coexist with existing habit-based recommendations (no conflicts)
- [ ] 4.7 Add unit tests for recommendation engine updates

## 5. Career Resource Library (Static Data)

- [ ] 5.1 Create seed data or JSON config file with curated learning resources by subject (Khan Academy links, Kaggle datasets, etc.)
- [ ] 5.2 Create or update endpoint: GET `/api/resources/subject/{subjectId}` to return curated resources
- [ ] 5.3 Link resources to career-aligned subject recommendations in recommendation payload
- [ ] 5.4 Add at least 2 resources per subject for MVP

## 6. Frontend UI - Career Selection (Onboarding)

- [ ] 6.1 Create CareerSelectionComponent for onboarding flow
- [ ] 6.2 Fetch and display list of 5 careers with descriptions from GET `/api/careers`
- [ ] 6.3 Implement career dropdown/selection UI with clear visual feedback
- [ ] 6.4 Add validation: require user to select a career before proceeding
- [ ] 6.5 Call POST `/api/profile/career` to save selected career
- [ ] 6.6 Add error handling and user feedback on save
- [ ] 6.7 Test career selection flow end-to-end in onboarding

## 7. Frontend UI - Profile Display and Editing

- [ ] 7.1 Update profile page to display user's currently selected career
- [ ] 7.2 Create "Edit Career" button/link on profile
- [ ] 7.3 Implement modal or page to allow user to change career selection
- [ ] 7.4 Call PUT `/api/profile/career` and refresh UI on successful update
- [ ] 7.5 Add success/error notifications
- [ ] 7.6 Test career update flow with data persistence

## 8. Frontend Dashboard - Career-Aligned Recommendations

- [ ] 8.1 Create DashboardCareerSection component: "Improve Skills for [Career]"
- [ ] 8.2 Fetch recommendations from GET `/api/users/{userId}/recommendations/career-aligned`
- [ ] 8.3 Display top 3 weak career-aligned subjects on dashboard
- [ ] 8.4 Display career relevance context for each recommendation (e.g., "Critical for Data Analyst")
- [ ] 8.5 Integrate curated resource links from GET `/api/resources/subject/{subjectId}`
- [ ] 8.6 Style recommendations prominently to draw user attention
- [ ] 8.7 Test dashboard displays correct career-aligned recommendations after career selection

## 9. Simulation Mode Integration

- [ ] 9.1 Update simulation panel to trigger recommendation refresh when inputs change
- [ ] 9.2 Ensure career-aligned recommendations update in real time during simulation
- [ ] 9.3 Add messaging to explain how simulated changes impact career skill alignment
- [ ] 9.4 Calculate and display skill gap closure metrics (e.g., "Closes 15% of Data Structures gap")
- [ ] 9.5 Test simulation flow: change inputs → recommendations update → career context maintained

## 10. Testing and Integration

- [ ] 10.1 Create end-to-end test: register user → select career → view career-aligned recommendations
- [ ] 10.2 Test career change triggers recommendation refresh
- [ ] 10.3 Test that non-aligned weak subjects still appear but with lower priority
- [ ] 10.4 Manual testing: verify dashboard displays career-aligned section correctly
- [ ] 10.5 Test API error handling (invalid career, missing career, database errors)
- [ ] 10.6 Performance test: verify recommendations load in <2 seconds

## 11. Documentation and Demo Preparation

- [ ] 11.1 Document new API endpoints in API reference or Swagger/OpenAPI spec
- [ ] 11.2 Document career-to-skill-subject mapping structure for future maintainers
- [ ] 11.3 Add comments to recommendation engine changes
- [ ] 11.4 Create demo script showing: onboarding → career selection → dashboard with recommendations
- [ ] 11.5 Test demo flow with different careers (Software Developer, Data Analyst) to validate variety

## 12. Code Review and Deployment

- [ ] 12.1 Code review: backend career endpoints and recommendation engine changes
- [ ] 12.2 Code review: frontend career selection and dashboard components
- [ ] 12.3 Address feedback and merge to main branch
- [ ] 12.4 Deploy to staging environment
- [ ] 12.5 Smoke test in staging: full career selection and recommendations flow
- [ ] 12.6 Merge to production and deploy
