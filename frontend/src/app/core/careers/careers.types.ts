export type ImportanceLevel = 'critical' | 'high' | 'moderate';

export interface Career {
  id: number;
  name: string;
  description: string;
}

export interface CareerSkillArea {
  id: number;
  name: string;
  description: string;
  importance_level: ImportanceLevel;
}

export interface CareerSubject {
  id: number;
  name: string;
  field_of_study: string;
  description: string;
  relevance_indicator: ImportanceLevel;
}

export interface SubjectResource {
  id: number;
  title: string;
  url: string;
  provider: string;
}

export interface CareerAlignedRecommendation {
  subject_id: number;
  subject_name: string;
  field_of_study: string;
  description: string;
  relevance_indicator: ImportanceLevel;
  weakness_score: number;
  baseline_weakness_score: number;
  gap_closure_percent: number;
  career_relevance_context: string;
  supporting_skills: string[];
  resources: SubjectResource[];
}

export interface CareerAlignedRecommendationsResponse {
  career: Career | null;
  items: CareerAlignedRecommendation[];
}

export interface CareerSimulationQuery {
  study_hours?: number;
  sleep_hours?: number;
  phone_usage_hours?: number;
  social_media_hours?: number;
  gaming_hours?: number;
  breaks_per_day?: number;
  coffee_intake?: number;
  exercise_minutes?: number;
  stress_level?: number;
  focus_score?: number;
  attendance_percentage?: number;
  assignments_completed_per_week?: number;
  final_grade?: number;
  limit?: number;
}
