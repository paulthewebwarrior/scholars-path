import { CommonModule } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormBuilder, ReactiveFormsModule } from '@angular/forms';
import { forkJoin, of } from 'rxjs';
import { catchError, debounceTime, finalize, map, switchMap } from 'rxjs/operators';

import { AuthService } from '../../core/auth/auth.service';
import { CareersService } from '../../core/careers/careers.service';
import { CareerAlignedRecommendation } from '../../core/careers/careers.types';
import { HabitsService } from '../../core/habits/habits.service';
import {
  HabitsAssessment,
  HabitsCorrelation,
  HabitsRecommendation,
  RecommendationStatus,
} from '../../core/habits/habits.types';

interface MetricConfig {
  key: keyof HabitsAssessment;
  label: string;
  icon: string;
  unit: string;
  classify: (v: number) => 'good' | 'warn' | 'bad';
}

const METRIC_CONFIG: MetricConfig[] = [
  { key: 'study_hours',                    label: 'Study',        icon: 'fa-book',                   unit: 'hrs/day',  classify: v => v >= 4 ? 'good' : v >= 2 ? 'warn' : 'bad' },
  { key: 'sleep_hours',                    label: 'Sleep',        icon: 'fa-moon',                   unit: 'hrs/day',  classify: v => v >= 7 ? 'good' : v >= 5 ? 'warn' : 'bad' },
  { key: 'phone_usage_hours',              label: 'Phone',        icon: 'fa-mobile-screen-button',   unit: 'hrs/day',  classify: v => v <= 3 ? 'good' : v <= 6 ? 'warn' : 'bad' },
  { key: 'social_media_hours',             label: 'Social',       icon: 'fa-hashtag',                unit: 'hrs/day',  classify: v => v <= 2 ? 'good' : v <= 4 ? 'warn' : 'bad' },
  { key: 'gaming_hours',                   label: 'Gaming',       icon: 'fa-gamepad',                unit: 'hrs/day',  classify: v => v <= 2 ? 'good' : v <= 4 ? 'warn' : 'bad' },
  { key: 'breaks_per_day',                 label: 'Breaks',       icon: 'fa-mug-saucer',             unit: '/day',     classify: v => v >= 3 ? 'good' : v >= 1 ? 'warn' : 'bad' },
  { key: 'coffee_intake',                  label: 'Coffee',       icon: 'fa-mug-hot',                unit: 'cups/day', classify: v => v <= 2 ? 'good' : v <= 4 ? 'warn' : 'bad' },
  { key: 'exercise_minutes',               label: 'Exercise',     icon: 'fa-person-running',         unit: 'min/day',  classify: v => v >= 30 ? 'good' : v >= 10 ? 'warn' : 'bad' },
  { key: 'stress_level',                   label: 'Stress',       icon: 'fa-heart-crack',            unit: '/ 10',     classify: v => v <= 4 ? 'good' : v <= 6 ? 'warn' : 'bad' },
  { key: 'focus_score',                    label: 'Focus',        icon: 'fa-bullseye',               unit: '/ 100',    classify: v => v >= 70 ? 'good' : v >= 40 ? 'warn' : 'bad' },
  { key: 'attendance_percentage',          label: 'Attendance',   icon: 'fa-calendar-check',         unit: '%',        classify: v => v >= 80 ? 'good' : v >= 60 ? 'warn' : 'bad' },
  { key: 'assignments_completed_per_week', label: 'Assignments',  icon: 'fa-clipboard-check',        unit: '/week',    classify: v => v >= 4 ? 'good' : v >= 2 ? 'warn' : 'bad' },
  { key: 'final_grade',                    label: 'Grade',        icon: 'fa-graduation-cap',         unit: 'pts',      classify: v => v >= 75 ? 'good' : v >= 60 ? 'warn' : 'bad' },
];

@Component({
  selector: 'app-habits-results',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './habits-results.component.html',
  styleUrl: './habits-results.component.css',
})
export class HabitsResultsComponent {
  private readonly auth = inject(AuthService);
  private readonly habitsService = inject(HabitsService);
  private readonly careersService = inject(CareersService);
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly fb = inject(FormBuilder);

  protected readonly loading = signal(true);
  protected readonly errorMessage = signal('');
  protected readonly latestAssessment = signal<HabitsAssessment | null>(null);
  protected readonly previousAssessment = signal<HabitsAssessment | null>(null);
  protected readonly topCorrelations = signal<HabitsCorrelation[]>([]);
  protected readonly recommendations = signal<HabitsRecommendation[]>([]);
  protected readonly expandedRecommendationIds = signal<Set<number>>(new Set<number>());
  protected readonly leaving = signal(false);

  protected readonly careerRecommendationsLoading = signal(false);
  protected readonly careerRecommendationsError = signal('');
  protected readonly careerRecommendations = signal<CareerAlignedRecommendation[]>([]);
  protected readonly selectedCareerName = signal('');
  protected readonly simulationImpactMessage = signal('');

  protected readonly simulationForm = this.fb.nonNullable.group({
    study_hours: [2],
    focus_score: [60],
    phone_usage_hours: [2],
    social_media_hours: [1],
    sleep_hours: [7],
    assignments_completed_per_week: [5],
  });

  protected readonly metricConfig = METRIC_CONFIG;

  constructor() {
    this.loadResults();

    this.simulationForm.valueChanges.pipe(debounceTime(280)).subscribe(() => {
      if (!this.latestAssessment() || this.loading()) {
        return;
      }
      this.refreshCareerRecommendations(true);
    });
  }

  protected metricClass(key: keyof HabitsAssessment, value: number | null | undefined): 'good' | 'warn' | 'bad' {
    if (value === null || value === undefined) return 'warn';
    const cfg = METRIC_CONFIG.find(m => m.key === key);
    return cfg ? cfg.classify(value) : 'warn';
  }

  protected correlationBarWidth(coefficient: number): string {
    return `${Math.min(100, Math.abs(coefficient) * 100)}%`;
  }

  protected correlationSign(coefficient: number): 'pos' | 'neg' {
    return coefficient >= 0 ? 'pos' : 'neg';
  }

  protected metricDelta(key: keyof HabitsAssessment): string | null {
    const prev = this.previousAssessment();
    const curr = this.latestAssessment();
    if (!prev || !curr) return null;
    const prevVal = prev[key] as number | null;
    const currVal = curr[key] as number | null;
    if (prevVal === null || currVal === null) return null;
    const diff = Number((currVal - prevVal).toFixed(2));
    if (diff === 0) return '—';
    return diff > 0 ? `+${diff}` : `${diff}`;
  }

  protected metricDeltaClass(key: keyof HabitsAssessment): 'up' | 'down' | 'neutral' {
    const delta = this.metricDelta(key);
    if (!delta || delta === '—') return 'neutral';
    return delta.startsWith('+') ? 'up' : 'down';
  }

  protected formatMetricName(metric: string): string {
    return metric.replaceAll('_', ' ');
  }

  protected weaknessPercent(score: number): number {
    return Math.round(score * 100);
  }

  protected resetSimulation(): void {
    const latest = this.latestAssessment();
    if (!latest) {
      return;
    }

    this.simulationForm.patchValue(
      {
        study_hours: latest.study_hours,
        focus_score: latest.focus_score,
        phone_usage_hours: latest.phone_usage_hours,
        social_media_hours: latest.social_media_hours,
        sleep_hours: latest.sleep_hours,
        assignments_completed_per_week: latest.assignments_completed_per_week,
      },
      { emitEvent: false },
    );
    this.refreshCareerRecommendations(false);
  }

  protected toggleWhy(recommendationId: number): void {
    const copy = new Set(this.expandedRecommendationIds());
    if (copy.has(recommendationId)) {
      copy.delete(recommendationId);
    } else {
      copy.add(recommendationId);
    }
    this.expandedRecommendationIds.set(copy);
  }

  protected isWhyExpanded(recommendationId: number): boolean {
    return this.expandedRecommendationIds().has(recommendationId);
  }

  protected async retakeAssessment(): Promise<void> {
    this.leaving.set(true);
    await new Promise(r => setTimeout(r, 360));
    void this.router.navigate(['/habits/assessment']);
  }

  protected sendFeedback(recommendationId: number, statusValue: RecommendationStatus): void {
    const user = this.auth.user();
    if (!user) return;
    this.habitsService.updateRecommendationFeedback(user.id, recommendationId, statusValue).subscribe({
      next: (updated) => {
        this.recommendations.set(
          this.recommendations().map((item) => (item.id === updated.id ? updated : item)),
        );
      },
    });
  }

  private loadResults(): void {
    const user = this.auth.user();
    const user$ = user ? of(user) : this.auth.fetchProfile();

    user$
      .pipe(
        switchMap((profile) => {
          const queryAssessmentId = Number(this.route.snapshot.queryParamMap.get('assessmentId') || '');
          return forkJoin({
            latest: this.habitsService.getLatestAssessment(profile.id),
            history: this.habitsService.getAssessmentHistory(profile.id, 1, 2),
            correlations: this.habitsService.getCorrelations(profile.id).pipe(catchError(() => of([]))),
            recommendations: this.habitsService
              .getRecommendations(profile.id, Number.isNaN(queryAssessmentId) ? undefined : queryAssessmentId)
              .pipe(map((res) => res.items), catchError(() => of([]))),
          });
        }),
        finalize(() => this.loading.set(false)),
      )
      .subscribe({
        next: ({ latest, history, correlations, recommendations }) => {
          this.latestAssessment.set(latest);
          this.previousAssessment.set(history.items.length > 1 ? history.items[1] : null);
          this.topCorrelations.set(
            correlations.sort((a, b) => Math.abs(b.correlation_coefficient) - Math.abs(a.correlation_coefficient)).slice(0, 5),
          );
          this.recommendations.set(recommendations.slice(0, 5));

          this.simulationForm.patchValue(
            {
              study_hours: latest.study_hours,
              focus_score: latest.focus_score,
              phone_usage_hours: latest.phone_usage_hours,
              social_media_hours: latest.social_media_hours,
              sleep_hours: latest.sleep_hours,
              assignments_completed_per_week: latest.assignments_completed_per_week,
            },
            { emitEvent: false },
          );

          this.refreshCareerRecommendations(false);
        },
        error: () => {
          this.errorMessage.set('Unable to load results right now. Please try again.');
        },
      });
  }

  private refreshCareerRecommendations(useSimulation: boolean): void {
    const user = this.auth.user();
    if (!user || !user.career_id) {
      this.careerRecommendations.set([]);
      this.selectedCareerName.set('');
      this.simulationImpactMessage.set('');
      return;
    }

    const query = useSimulation
      ? {
          ...this.simulationForm.getRawValue(),
          limit: 3,
        }
      : { limit: 3 };

    this.careerRecommendationsLoading.set(true);
    this.careerRecommendationsError.set('');

    this.careersService
      .getCareerAlignedRecommendations(user.id, query)
      .pipe(finalize(() => this.careerRecommendationsLoading.set(false)))
      .subscribe({
        next: (response) => {
          this.selectedCareerName.set(response.career?.name ?? user.career?.name ?? '');
          this.careerRecommendations.set(response.items.slice(0, 3));

          if (!useSimulation || response.items.length === 0) {
            this.simulationImpactMessage.set('');
            return;
          }

          const strongest = response.items
            .slice()
            .sort((a, b) => b.gap_closure_percent - a.gap_closure_percent)[0];

          if (strongest && strongest.gap_closure_percent > 0) {
            this.simulationImpactMessage.set(
              `Simulation closes ${strongest.gap_closure_percent.toFixed(1)}% of ${strongest.subject_name} gap.`,
            );
          } else {
            this.simulationImpactMessage.set(
              'Simulation changed inputs, but no immediate career-gap closure was detected.',
            );
          }
        },
        error: () => {
          this.careerRecommendationsError.set('Unable to load career-aligned recommendations.');
        },
      });
  }
}
