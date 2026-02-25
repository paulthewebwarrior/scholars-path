# Career Goal Module API

## Careers

- `GET /api/careers`
  - Returns all available careers in alphabetical order.
- `GET /api/careers/{careerName}`
  - Returns a single career by name or slug (for example `software-developer`).
- `GET /api/careers/{careerName}/skills`
  - Returns the skill areas mapped to the given career.
- `GET /api/careers/{careerName}/skills/{skillId}/subjects`
  - Returns subject mappings for a career skill.
  - Subject list is filtered by the authenticated user's `course` plus cross-disciplinary subjects.

## Profile Career Management

- `POST /api/profile/career`
  - Sets the user's selected career.
  - Body: `{ "career_id": number }`
- `PUT /api/profile/career`
  - Updates the user's selected career.
  - Body: `{ "career_id": number }`
- `GET /api/profile/me`
  - Includes `career_id` and nested `career` metadata.

## Career-Aligned Recommendations

- `GET /api/users/{userId}/recommendations/career-aligned`
  - Returns top subject recommendations aligned to the user's selected career.
  - Supports optional simulation query params (for example `study_hours`, `focus_score`, `phone_usage_hours`) and `limit`.

## Subject Resources

- `GET /api/resources/subject/{subjectId}`
  - Returns curated resources linked to a subject.
