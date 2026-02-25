## Context

The system currently provides productivity scoring and general habit-based recommendations. Students have profile data (name, course, year level) but lack career-specific guidance. The proposed Career Goal Module integrates with the existing recommendation engine to provide targeted advice based on the user's selected career. This is a cross-cutting change affecting frontend UI, backend APIs, and database schema.

## Goals / Non-Goals

**Goals:**
- Enable students to select and specify a target career during onboarding
- Map careers to required skill areas and competencies
- Map skill areas to academic subjects relevant to the student's field
- Integrate career context into personalized recommendations
- Show career-aligned subject improvement suggestions on the dashboard

**Non-Goals:**
- Dynamically create new careers via admin UI (static, curated list only)
- Provide unlimited career paths or micro-specializations
- Modify the core ML productivity scoring algorithm
- Create a full career exploration tool or career assessment quiz

## Decisions

**Decision 1: Static Career Data**
- **Choice**: Use hardcoded, curated career list (Software Developer, Data Analyst, Cybersecurity Specialist, Doctor, Engineer)
- **Rationale**: Reduces database complexity, ensures consistency, and enables easy manual curation. Simpler for MVP. Career data can be moved to a JSON config or seed data if scalability becomes critical.
- **Alternative considered**: Database-driven careers with admin UI for management (deferred to future phase)

**Decision 2: Skill-Subject Mapping Strategy**
- **Choice**: Define a static mapping of (career → skill areas → academic subjects) as seed data or configuration file
- **Rationale**: Ensures predictable, curated recommendations. Domain experts can define which subjects matter for each career and skill.
- **Alternative considered**: Use NLP to auto-infer connections (higher complexity, lower control over recommendations)

**Decision 3: Career Selection in Profile**
- **Choice**: Add `career_id` field to user profile, populated during onboarding and editable thereafter
- **Rationale**: Simple, aligns with existing profile structure. Users can update career goal at any time.
- **Alternative considered**: Separate career history table to track previous goals (deferred; not needed for MVP)

**Decision 4: Recommendation Integration**
- **Choice**: Augment rule-based recommendation engine to access career-skill-subject mapping and filter/prioritize subject recommendations
- **Rationale**: Reuses existing recommendation structure. Subject improvement suggestions can be weighted by career relevance.
- **Alternative considered**: Separate LLM-only career recommendation pipeline (adds complexity; not needed if rule-based works)

**Decision 5: API Design**
- **Choice**: New endpoints: `GET /careers` (list), `GET /careers/{id}/skills`, `GET /careers/{id}/skills/{skill_id}/subjects`, `POST /profile/career` (set user's career)
- **Rationale**: RESTful, follows existing API conventions. Separates career metadata from user profile for flexibility.
- **Alternative considered**: Embed career data in profile endpoint (less modular)

## Risks / Trade-offs

| Risk | Mitigation |
|------|-----------|
| Career data becomes stale or incomplete | Maintain a living document of career definitions and update in code/seed data as needed. Gather feedback from users on missing subjects. |
| Static mapping doesn't cover edge cases (e.g., interdisciplinary fields) | Allow multiple career selections per user in future iteration. For now, guide user to closest match in onboarding. |
| Performance if career metadata queries become frequent | Cache career-skills mapping in frontend after first load or use Redis on backend. Not critical for MVP. |
| Subject recommendations conflict with career priorities | Implement a priority/weight system in recommendation engine so career-aligned subjects appear first in the UI. |

## Migration Plan

1. **Database**: Add `career_id` foreign key to users table. Create careers, skills, and skill_subject_mapping tables with seed data.
2. **Backend**: Implement new career endpoints above. Update recommendation engine to filter/order suggestions by career.
3. **Frontend**: Add career dropdown to onboarding and profile edit flow. Update dashboard to show career-aligned recommendations prominently.
4. **Testing**: Verify end-to-end flow: select career → see subject recommendations → update habit → recommendations stay career-aligned.
5. **Rollback**: If critical issue, career selection feature can be hidden without database rollback (career_id becomes optional).

## Open Questions

- Should users be able to select multiple careers for hedging? (Defer to post-MVP)
- Should career-aligned recommendations override general recommendations in priority? (Yes, for MVP—clarify with design team)
- Do we need to track career-focused study metrics separately? (No for MVP; explore in future)
