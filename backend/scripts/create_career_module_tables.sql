CREATE TABLE IF NOT EXISTS schema_migrations (
    version VARCHAR(100) PRIMARY KEY,
    applied_at DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS careers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS skill_areas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT NOT NULL,
    importance_level VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS career_skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    career_id INTEGER NOT NULL,
    skill_area_id INTEGER NOT NULL,
    FOREIGN KEY (career_id) REFERENCES careers(id) ON DELETE CASCADE,
    FOREIGN KEY (skill_area_id) REFERENCES skill_areas(id) ON DELETE CASCADE,
    UNIQUE(career_id, skill_area_id)
);

CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(120) NOT NULL,
    field_of_study VARCHAR(120) NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS skill_subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    skill_area_id INTEGER NOT NULL,
    subject_id INTEGER NOT NULL,
    relevance_indicator VARCHAR(20) NOT NULL,
    FOREIGN KEY (skill_area_id) REFERENCES skill_areas(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE,
    UNIQUE(skill_area_id, subject_id)
);

CREATE TABLE IF NOT EXISTS subject_resources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    url VARCHAR(512) NOT NULL,
    provider VARCHAR(100) NOT NULL,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS ix_careers_name ON careers(name);
CREATE INDEX IF NOT EXISTS ix_skill_areas_name ON skill_areas(name);
CREATE INDEX IF NOT EXISTS ix_career_skills_career_id ON career_skills(career_id);
CREATE INDEX IF NOT EXISTS ix_career_skills_skill_area_id ON career_skills(skill_area_id);
CREATE INDEX IF NOT EXISTS ix_subjects_name ON subjects(name);
CREATE INDEX IF NOT EXISTS ix_subjects_field_of_study ON subjects(field_of_study);
CREATE INDEX IF NOT EXISTS ix_skill_subjects_skill_area_id ON skill_subjects(skill_area_id);
CREATE INDEX IF NOT EXISTS ix_skill_subjects_subject_id ON skill_subjects(subject_id);
CREATE INDEX IF NOT EXISTS ix_subject_resources_subject_id ON subject_resources(subject_id);

INSERT OR IGNORE INTO schema_migrations (version, applied_at)
VALUES ('20260225_career_goal_module', CURRENT_TIMESTAMP);
