export interface HabitsAssessmentPayload {
  study_hours: number;
  sleep_hours: number;
  phone_usage_hours: number;
  social_media_hours: number;
  gaming_hours: number;
  breaks_per_day: number;
  coffee_intake: number;
  exercise_minutes: number;
  stress_level: number;
  focus_score: number;
  attendance_percentage: number;
  assignments_completed_per_week: number;
  final_grade: number | null;
  grade_opt_in: boolean;
}

export interface HabitsAssessment extends HabitsAssessmentPayload {
  assessment_id: number;
  user_id: number;
  productivity_score: number | null;
  created_at: string;
  updated_at: string;
}

export interface HabitsAssessmentHistory {
  items: HabitsAssessment[];
  page: number;
  page_size: number;
  total: number;
}

export interface HabitsCorrelation {
  id: number;
  metric_name: string;
  performance_metric: string;
  correlation_coefficient: number;
  sample_size: number;
  confidence_interval_low: number;
  confidence_interval_high: number;
  confidence_level: number;
  p_value: number;
  calculation_timestamp: string;
}

export type RecommendationStatus = 'pending' | 'attempted' | 'completed' | 'not_applicable';

export interface HabitsRecommendation {
  id: number;
  assessment_id: number;
  user_id: number;
  recommendation_text: string;
  priority_rank: number;
  supporting_metric: string;
  correlation_strength: number;
  status: RecommendationStatus;
  status_updated_at: string | null;
  created_at: string;
}

export interface HabitsRecommendationsResponse {
  items: HabitsRecommendation[];
}
