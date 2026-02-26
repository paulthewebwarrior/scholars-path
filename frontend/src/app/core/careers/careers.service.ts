import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

import { getApiBaseUrl } from '../api/api-url';
import {
  Career,
  CareerAlignedRecommendationsResponse,
  CareerSimulationQuery,
  CareerSkillArea,
  CareerSubject,
  SubjectResource,
} from './careers.types';

@Injectable({ providedIn: 'root' })
export class CareersService {
  private readonly http = inject(HttpClient);
  private readonly apiBaseUrl = getApiBaseUrl();

  getCareers(): Observable<Career[]> {
    return this.http.get<Career[]>(`${this.apiBaseUrl}/careers`);
  }

  getCareerByName(careerName: string): Observable<Career> {
    return this.http.get<Career>(`${this.apiBaseUrl}/careers/${careerName}`);
  }

  getCareerSkills(careerName: string): Observable<CareerSkillArea[]> {
    return this.http.get<CareerSkillArea[]>(`${this.apiBaseUrl}/careers/${careerName}/skills`);
  }

  getSkillSubjects(careerName: string, skillId: number): Observable<CareerSubject[]> {
    return this.http.get<CareerSubject[]>(`${this.apiBaseUrl}/careers/${careerName}/skills/${skillId}/subjects`);
  }

  getSubjectResources(subjectId: number): Observable<SubjectResource[]> {
    return this.http.get<SubjectResource[]>(`${this.apiBaseUrl}/resources/subject/${subjectId}`);
  }

  getCareerAlignedRecommendations(
    userId: number,
    query: CareerSimulationQuery = {},
  ): Observable<CareerAlignedRecommendationsResponse> {
    let params = new HttpParams();
    for (const [key, value] of Object.entries(query)) {
      if (value === null || value === undefined || value === '') {
        continue;
      }
      params = params.set(key, `${value}`);
    }

    return this.http.get<CareerAlignedRecommendationsResponse>(
      `${this.apiBaseUrl}/users/${userId}/recommendations/career-aligned`,
      { params },
    );
  }
}
