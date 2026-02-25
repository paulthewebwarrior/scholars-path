## Why

Students often struggle to understand how their daily habits—sleep, exercise, phone usage, and study patterns—impact their academic productivity and performance. Without structured assessment and feedback, they cannot identify which behaviors are hindering or helping their success. This feature provides a data-driven questionnaire to help students assess their habits, gain insights into their productivity patterns, and receive actionable recommendations for improvement.

## What Changes

- Add a comprehensive study habits questionnaire that captures 13 key behavioral and performance metrics
- Implement data collection frontend component for user input
- Calculate productivity correlations based on habit patterns and academic performance
- Store assessment responses for historical tracking and trend analysis
- Integrate assessment data with the ML model to enhance productivity predictions

## Capabilities

### New Capabilities
- `study-habits-questionnaire`: Frontend form component that collects study habits data (study hours, sleep, phone usage, social media, gaming, breaks, coffee, exercise, stress, focus, attendance, assignments, grades)
- `habits-data-storage`: Backend API endpoint to persist questionnaire responses and link them to user profiles
- `productivity-correlation-analysis`: Backend analytics module to identify correlations between habits and academic performance
- `habit-recommendations`: Logic to generate personalized recommendations based on assessed habits and identified patterns

### Modified Capabilities
<!-- No existing capabilities require specification changes -->

## Impact

- **Frontend**: New questionnaire form component and UI integration
- **Backend**: New database schema to store habits assessments, new API endpoints for data submission and retrieval
- **ML Model**: Enhanced training data integration to correlate habits with productivity predictions
- **Database**: New tables for habits assessments and historical tracking
