# Career Goal Module Demo Script

## Flow

1. Register a new user.
2. Login.
3. Open `Career` page and select a career (for example `Software Developer`).
4. Navigate to `Habits Assessment` and submit with realistic values.
5. Open `Dashboard`:
   - Confirm section title `Improve Skills for Software Developer`.
   - Confirm top 3 weak subjects and resource links are visible.
6. Open `Results`:
   - Confirm career-aligned recommendations show relevance context.
   - Use Simulation sliders and confirm recommendations refresh.
   - Highlight `gap closure` message.
7. Open `Profile`:
   - Click `Edit Career`.
   - Switch to `Data Analyst` and save.
8. Return to `Dashboard` and confirm career-aligned recommendations changed.

## Validation Checklist

- Career options list has 5 predefined careers.
- Career selection is required before save.
- Invalid career IDs return `404` from API.
- Career-aligned recommendations and habit recommendations both appear in the app flow.
