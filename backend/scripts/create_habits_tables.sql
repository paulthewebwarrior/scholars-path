CREATE TABLE IF NOT EXISTS schema_migrations (
    version VARCHAR(100) PRIMARY KEY,
    applied_at DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS habits_assessment (
    assessment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    study_hours BLOB NOT NULL,
    sleep_hours BLOB NOT NULL,
    phone_usage_hours BLOB NOT NULL,
    social_media_hours BLOB NOT NULL,
    gaming_hours BLOB NOT NULL,
    breaks_per_day BLOB NOT NULL,
    coffee_intake BLOB NOT NULL,
    exercise_minutes BLOB NOT NULL,
    stress_level BLOB NOT NULL,
    focus_score BLOB NOT NULL,
    attendance_percentage BLOB NOT NULL,
    assignments_completed_per_week BLOB NOT NULL,
    final_grade BLOB NULL,
    grade_opt_in BOOLEAN NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS habits_correlations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    metric_name VARCHAR(100) NOT NULL,
    performance_metric VARCHAR(100) NOT NULL,
    correlation_coefficient FLOAT NOT NULL,
    sample_size INTEGER NOT NULL,
    confidence_interval_low FLOAT NOT NULL,
    confidence_interval_high FLOAT NOT NULL,
    confidence_level FLOAT NOT NULL DEFAULT 95.0,
    p_value FLOAT NOT NULL,
    calculation_timestamp DATETIME NOT NULL,
    created_at DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS habits_recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    assessment_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    recommendation_text TEXT NOT NULL,
    priority_rank INTEGER NOT NULL,
    supporting_metric VARCHAR(100) NOT NULL,
    correlation_strength FLOAT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    status_updated_at DATETIME NULL,
    created_at DATETIME NOT NULL,
    FOREIGN KEY (assessment_id) REFERENCES habits_assessment(assessment_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS habits_normalized_exports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    assessment_id INTEGER NOT NULL UNIQUE,
    user_id INTEGER NOT NULL,
    study_hours FLOAT NOT NULL,
    sleep_hours FLOAT NOT NULL,
    phone_usage_hours FLOAT NOT NULL,
    social_media_hours FLOAT NOT NULL,
    gaming_hours FLOAT NOT NULL,
    breaks_per_day FLOAT NOT NULL,
    coffee_intake FLOAT NOT NULL,
    exercise_minutes FLOAT NOT NULL,
    stress_level FLOAT NOT NULL,
    focus_score FLOAT NOT NULL,
    attendance_percentage FLOAT NOT NULL,
    assignments_completed_per_week FLOAT NOT NULL,
    final_grade FLOAT NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL,
    FOREIGN KEY (assessment_id) REFERENCES habits_assessment(assessment_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS ix_habits_assessment_user_id ON habits_assessment (user_id);
CREATE INDEX IF NOT EXISTS ix_habits_assessment_created_at ON habits_assessment (created_at);
CREATE INDEX IF NOT EXISTS ix_habits_assessment_user_id_created_at
    ON habits_assessment (user_id, created_at);
CREATE INDEX IF NOT EXISTS ix_habits_recommendations_assessment_priority
    ON habits_recommendations (assessment_id, priority_rank);
CREATE INDEX IF NOT EXISTS ix_habits_recommendations_user_id_created_at
    ON habits_recommendations (user_id, created_at);
CREATE INDEX IF NOT EXISTS ix_habits_correlations_metric_performance
    ON habits_correlations (metric_name, performance_metric);

INSERT OR IGNORE INTO schema_migrations (version, applied_at)
VALUES ('20260225_study_habits_assessment', CURRENT_TIMESTAMP);
