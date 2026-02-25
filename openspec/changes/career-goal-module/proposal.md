## Why

Students need clear alignment between their study habits, weak subjects, and career aspirations. Currently, the system provides general productivity insights but lacks career-specific guidance. This module connects personalized assessments to actual career requirements, enabling students to prioritize subject improvements based on their target career's skill demands.

## What Changes

- New UI component for career selection (Software Developer, Data Analyst, Cybersecurity Specialist, Doctor, Engineer)
- Backend mapping system linking careers to required skill areas
- Backend mapping system linking skills to relevant academic subjects
- Integration of career recommendations into the main dashboard and recommendations engine
- Real-time career-aligned suggestions when users update their career goal

## Capabilities

### New Capabilities
- `career-selection`: Allow users to select and manage a target career from a predefined list
- `career-skills-mapping`: Map careers to required skill areas and competencies
- `career-subject-mapping`: Map skill areas to relevant academic subjects for the user's field of study
- `career-aligned-recommendations`: Generate personalized recommendations based on weak subjects and career-skill alignment

### Modified Capabilities
<!-- No existing capabilities have changing requirements -->

## Impact

- **Frontend**: Add career selection component to profile/onboarding flow and dashboard
- **Backend**: New endpoints for career metadata, skill-subject mappings, and career-aligned recommendation generation
- **Database**: New tables for careers, skill areas, skill-subject relationships, and user career selections
- **Dashboard**: Integrate career context into recommendation display and simulation mode
- **Recommendation Engine**: Augment rule-based engine to factor in career-aligned skill gaps
