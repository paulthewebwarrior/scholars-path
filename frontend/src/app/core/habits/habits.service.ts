import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import {
  HabitsAssessment,
  HabitsAssessmentHistory,
  HabitsAssessmentPayload,
  HabitsCorrelation,
  HabitsRecommendation,
  HabitsRecommendationsResponse,
  RecommendationStatus,
} from './habits.types';

@Injectable({ providedIn: 'root' })
export class HabitsService {
  private readonly http = inject(HttpClient);
  private readonly apiBaseUrl = '/api/habits';

  submitAssessment(userId: number, payload: HabitsAssessmentPayload): Observable<HabitsAssessment> {
    return this.http.post<HabitsAssessment>(`${this.apiBaseUrl}/${userId}/assessment`, payload);
  }

  getLatestAssessment(userId: number): Observable<HabitsAssessment> {
    return this.http.get<HabitsAssessment>(`${this.apiBaseUrl}/${userId}/latest`);
  }

  getAssessmentHistory(userId: number, page = 1, pageSize = 10): Observable<HabitsAssessmentHistory> {
    return this.http.get<HabitsAssessmentHistory>(
      `${this.apiBaseUrl}/${userId}/history?page=${page}&page_size=${pageSize}`,
    );
  }

  getCorrelations(userId: number, minAbsR = 0.3, minConfidence = 95): Observable<HabitsCorrelation[]> {
    return this.http.get<HabitsCorrelation[]>(
      `${this.apiBaseUrl}/${userId}/correlations?min_abs_r=${minAbsR}&min_confidence=${minConfidence}`,
    );
  }

  getRecommendations(userId: number, assessmentId?: number): Observable<HabitsRecommendationsResponse> {
    const query = assessmentId ? `?assessment_id=${assessmentId}` : '';
    return this.http.get<HabitsRecommendationsResponse>(
      `${this.apiBaseUrl}/${userId}/recommendations${query}`,
    );
  }

  updateRecommendationFeedback(
    userId: number,
    recommendationId: number,
    statusValue: RecommendationStatus,
  ): Observable<HabitsRecommendation> {
    return this.http.post<HabitsRecommendation>(
      `${this.apiBaseUrl}/${userId}/recommendations/${recommendationId}/feedback?status_value=${statusValue}`,
      {},
    );
  }
}
