# Student Productivity & Digital Distraction Intelligence System

**Tagline:** *Measure. Improve. Achieve.*

## 1) Core Problem

Students commonly struggle with:

- Digital distractions
- Poor study habits
- Stress and burnout
- Unclear career direction
- Weak subjects without structured guidance

Current gaps:

- No simple system to quantify productivity
- No clear root-cause analysis of low performance
- No personalized improvement suggestions
- No career-aligned guidance connected to habits and subject performance

## 2) Core Solution

A behavior-based AI system that:

- Collects study and lifestyle data
- Predicts a productivity score
- Identifies risk level
- Recommends habit improvements
- Suggests resources for weak subjects
- Aligns plans with career goals

---

## 3) MVP Features

### 3.1 Authentication & Profile

- Register/Login
- Basic profile fields:
  - Name
  - Course
  - Year level
  - Career goal

### 3.2 Study Habits Assessment (Questionnaire)

Inputs:

- Study hours per day
- Sleep hours per day
- Phone usage hours
- Social media hours
- Gaming hours
- Breaks per day
- Coffee intake
- Exercise minutes
- Stress level (1–10)
- Focus score (0–100)
- Attendance %
- Assignments completed per week
- Final grade (optional; can be removed for no-leakage version)

### 3.3 Subject Difficulty Module

Flow:

1. Select field (e.g., Computer Science)
2. Enter subject (e.g., Data Structures)
3. Enter latest quiz/test score
4. Rate confidence (1–5)

Output:

- Weak subjects identified
- Performance gap analysis

### 3.4 Career Goal Module

User selects a target career, such as:

- Software Developer
- Data Analyst
- Cybersecurity Specialist
- Doctor
- Engineer

System maps:

- Career → Required skill areas → Relevant subjects

### 3.5 Productivity Score Engine

- Model: Linear Regression (already implemented)
- Output: Predicted Productivity Score (0–100)

Classification:

- **0–40:** At Risk
- **41–70:** Moderate
- **71–85:** High
- **86–100:** Excellent

### 3.6 Recommendation Engine (Rule-Based + Model Insights)

System should:

- Analyze key feature contributions from model coefficients
- Identify strongest negative contributors
- Generate personalized actions

Example recommendations:

- High phone usage → Pomodoro + app blocker
- High stress → Structured revision schedule
- Low sleep → 7–8 hour sleep strategy
- Low assignments completed → Weekly task planning template

### 3.7 Career-Aligned Resource Suggestions

Use curated static links (no scraping required).

Example:

- Career: Data Analyst
- Weak Subject: Statistics
- Suggestions:
  - Khan Academy statistics playlist
  - Kaggle beginner datasets
  - Python pandas roadmap
  - Practice problem sets

### 3.8 Simulation Mode

Allow user to change inputs (e.g., reduce phone usage to 2 hours), then:

- Recalculate productivity score in real time
- Compare before vs after
- Explain what changed and why

---

## 4) Recommendation Logic Structure

### 4.1 Rule-Based Mapping

- If `stress_level > 7`:
  - Recommend stress management plan
- If `phone_usage > 6`:
  - Recommend digital detox strategies
- If `sleep < 6`:
  - Recommend sleep hygiene checklist
- If `attendance < 75`:
  - Flag academic risk
- If `assignments_completed < 4`:
  - Suggest weekly productivity planner

### 4.2 Subject-Based Logic

- If `quiz_score < 60`:
  - Recommend subject-specific resources

### 4.3 Career-Based Logic

- Map `career → core skill areas → learning roadmap`

---

## 5) Dashboard Design

### Main Screen

- Productivity Score (example: **71.46**)
- Risk Level (example: **Moderate**)

### Contribution Breakdown (example)

- Focus Contribution: `+12`
- Attendance: `+9`
- Phone Usage: `-6`
- Stress: `-4`

### Dashboard Sections

- Your Strengths
- Areas for Improvement
- Weak Subjects
- Career Path Guidance
- Simulation Panel

---

## 6) Project Phases (4-Week MVP Plan)

### Week 1 — Foundation

- Decide stack and architecture
  - Frontend: Angular
  - Backend: FastAPI
  - Database: PostgreSQL
- Build auth and profile module
- Create initial DB schema
- Implement onboarding and assessment form UI

### Week 2 — Intelligence Core

- Integrate existing linear regression model API
- Add productivity classification logic
- Build rule-based recommendation engine
- Add model contribution explanation layer

### Week 3 — Subject + Career Intelligence

- Implement subject difficulty workflow
- Implement career-to-skill mapping
- Add curated resource suggestion dataset
- Merge habit + subject + career recommendations

### Week 4 — Chat + Simulation + Demo Readiness

- Integrate Gemini API for recommendation chat
- Ground chat responses with user profile + latest assessment + model outputs
- Build simulation panel for real-time score recalculation
- Add score delta insights and final dashboard polish

---

## 7) Gemini API Integration Plan

### Purpose

Provide conversational, personalized recommendations based on:

- User profile
- Habit assessment inputs
- Productivity score and risk level
- Feature contribution breakdown
- Weak subjects and career goal

### Guardrails

- Keep API key server-side only
- Validate and sanitize all payloads
- Ground responses in actual user data (avoid generic hallucinations)
- Provide fallback to deterministic rule-based recommendations if LLM fails

### Suggested Chat Prompt Context

- Current score + risk level
- Top 3 negative contributors
- Top strengths
- Weak subjects + latest scores
- Career goal + required skill areas
- User request (e.g., “How do I improve in 2 weeks?”)

---

## 8) MVP Acceptance Criteria

- User completes assessment in <5 minutes
- System returns productivity score + risk label
- Dashboard shows contribution breakdown and clear next actions
- At least 3 personalized recommendations are generated
- Weak subjects are identified when scores are low
- Career path guidance and at least 2 curated resources are shown
- Simulation updates score quickly and explains changes
- Gemini chat returns context-aware, actionable suggestions

---

## 9) Suggested Backlog (Implementation Order)

1. Auth + profile + DB models
2. Assessment form + backend persistence
3. Model inference endpoint and risk classification
4. Rule-based recommendations
5. Dashboard with contribution breakdown
6. Subject difficulty module
7. Career mapping + resource library
8. Simulation engine
9. Gemini chat endpoint + grounded prompting
10. QA, demo script, and polish
