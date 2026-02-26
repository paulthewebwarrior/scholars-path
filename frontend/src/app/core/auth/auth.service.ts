import { Injectable, computed, inject, signal } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { Observable, map, of, tap } from 'rxjs';
import { catchError } from 'rxjs/operators';

import { getApiBaseUrl } from '../api/api-url';
import {
  CareerSelectionPayload,
  LoginPayload,
  LogoutResponse,
  ProfileUpdatePayload,
  RegisterPayload,
  RegisterResponse,
  TokenResponse,
  UserProfile,
} from './auth.types';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly http = inject(HttpClient);
  private readonly router = inject(Router);

  private readonly apiBaseUrl = getApiBaseUrl();
  private readonly accessToken = signal<string | null>(null);
  private readonly userProfile = signal<UserProfile | null>(null);

  readonly user = computed(() => this.userProfile());

  isAuthenticated(): boolean {
    return this.accessToken() !== null;
  }

  getToken(): string | null {
    return this.accessToken();
  }

  setAccessToken(token: string): void {
    this.accessToken.set(token);
  }

  clearSession(): void {
    this.accessToken.set(null);
    this.userProfile.set(null);
  }

  forceLogoutRedirect(): void {
    this.clearSession();
    void this.router.navigate(['/login']);
  }

  register(payload: RegisterPayload): Observable<RegisterResponse> {
    return this.http.post<RegisterResponse>(`${this.apiBaseUrl}/auth/register`, payload);
  }

  login(payload: LoginPayload): Observable<TokenResponse> {
    return this.http
      .post<TokenResponse>(`${this.apiBaseUrl}/auth/login`, payload, { withCredentials: true })
      .pipe(tap((response) => this.setAccessToken(response.access_token)));
  }

  refreshAccessToken(): Observable<TokenResponse> {
    return this.http
      .post<TokenResponse>(`${this.apiBaseUrl}/auth/refresh`, {}, { withCredentials: true })
      .pipe(tap((response) => this.setAccessToken(response.access_token)));
  }

  fetchProfile(): Observable<UserProfile> {
    return this.http
      .get<UserProfile>(`${this.apiBaseUrl}/profile/me`)
      .pipe(tap((profile) => this.userProfile.set(profile)));
  }

  updateProfile(payload: ProfileUpdatePayload): Observable<UserProfile> {
    return this.http
      .put<UserProfile>(`${this.apiBaseUrl}/profile/me`, payload)
      .pipe(tap((profile) => this.userProfile.set(profile)));
  }

  setCareer(payload: CareerSelectionPayload): Observable<UserProfile> {
    return this.http
      .post<UserProfile>(`${this.apiBaseUrl}/profile/career`, payload)
      .pipe(tap((profile) => this.userProfile.set(profile)));
  }

  updateCareer(payload: CareerSelectionPayload): Observable<UserProfile> {
    return this.http
      .put<UserProfile>(`${this.apiBaseUrl}/profile/career`, payload)
      .pipe(tap((profile) => this.userProfile.set(profile)));
  }

  logout(): Observable<void> {
    return this.http
      .post<LogoutResponse>(`${this.apiBaseUrl}/auth/logout`, {}, { withCredentials: true })
      .pipe(
        catchError(() => of({ message: 'Logged out' } satisfies LogoutResponse)),
        tap(() => this.forceLogoutRedirect()),
        map(() => undefined),
      );
  }
}
