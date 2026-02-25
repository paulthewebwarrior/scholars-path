# Career to Skill to Subject Mapping

The module uses curated static data seeded into database tables:

- `careers`
- `skill_areas`
- `career_skills`
- `subjects`
- `skill_subjects`
- `subject_resources`

## Career Set (MVP)

- Cybersecurity Specialist
- Data Analyst
- Doctor
- Engineer
- Software Developer

## Mapping Structure

1. A career maps to multiple skill areas via `career_skills`.
2. A skill area maps to multiple subjects via `skill_subjects` with `relevance_indicator`.
3. Each subject has curated resources via `subject_resources`.
4. Recommendation scoring combines:
   - skill importance (`critical`, `high`, `moderate`)
   - subject relevance indicator (`critical`, `high`, `moderate`)
   - user weakness estimation from latest habits assessment metrics

## Field-of-Study Filtering

- Subject filtering uses the authenticated user's `course`.
- Cross-disciplinary subjects (`field_of_study = General`) are always included.
- Alias matching supports common overlaps (for example Computer Science and Information Technology).
