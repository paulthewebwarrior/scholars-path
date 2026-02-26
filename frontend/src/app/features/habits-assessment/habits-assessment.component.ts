import { CommonModule } from '@angular/common';
import { Component, HostListener, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { finalize } from 'rxjs/operators';

import { AuthService } from '../../core/auth/auth.service';
import { HabitsService } from '../../core/habits/habits.service';
import { HabitsAssessmentPayload } from '../../core/habits/habits.types';

const DRAFT_KEY = 'habits_assessment_draft_v1';
const DRAFT_TIME_KEY = 'habits_assessment_draft_time_v1';

const METRIC_FIELDS = [
  'study_hours', 'sleep_hours', 'phone_usage_hours', 'social_media_hours',
  'gaming_hours', 'breaks_per_day', 'coffee_intake', 'exercise_minutes',
  'stress_level', 'focus_score', 'attendance_percentage',
  'assignments_completed_per_week', 'final_grade',
] as const;

export interface ScaleQuestion {
  field: string;
  text: string;
  type: 'scale';
  /** Actual metric values corresponding to ratings 1–5 */
  values: [number, number, number, number, number];
  reverseScale?: boolean; /** true when lower rating = more of the metric (e.g. stress/coffee) */
}
export interface NumberQuestion  { field: string; text: string; type: 'number'; min: number; max: number; step: number; unit: string; optional?: boolean; }
export interface CheckboxQuestion { field: string; text: string; type: 'checkbox'; }
export type Question = ScaleQuestion | NumberQuestion | CheckboxQuestion;

const STEP_QUESTIONS: Record<number, Question[]> = {
  1: [
    { field: 'study_hours',                    type: 'scale',   text: 'I dedicate enough time to studying each day.',          values: [0, 1.5, 3.5, 5.5, 8]   },
    { field: 'breaks_per_day',                 type: 'scale',   text: 'I take regular breaks to stay refreshed while studying.', values: [0, 1, 3, 5, 8]         },
    { field: 'assignments_completed_per_week', type: 'scale',   text: 'I consistently complete my assignments each week.',      values: [0, 2, 5, 8, 12]         },
    { field: 'focus_score',                    type: 'scale',   text: 'I maintain strong focus throughout my study sessions.',  values: [10, 30, 55, 75, 95]     },
  ],
  2: [
    { field: 'sleep_hours',      type: 'scale', text: 'I get enough sleep to feel rested each morning.',           values: [4, 5, 6.5, 7.5, 9]      },
    { field: 'exercise_minutes', type: 'scale', text: 'I maintain a consistent exercise routine.',                 values: [0, 10, 30, 60, 120]     },
    { field: 'coffee_intake',    type: 'scale', text: 'I rely on coffee or caffeine to get through the day.',      values: [0, 1, 2, 3, 5],  reverseScale: true },
    { field: 'stress_level',     type: 'scale', text: 'I feel overwhelmed by my academic workload.',               values: [1, 3, 5, 7, 10], reverseScale: true },
  ],
  3: [
    { field: 'phone_usage_hours',  type: 'scale', text: 'I use my phone frequently throughout the day.',          values: [0, 1, 2.5, 4, 6],   reverseScale: true },
    { field: 'social_media_hours', type: 'scale', text: 'Social media takes up a large portion of my daily time.',values: [0, 0.5, 1, 2, 4],   reverseScale: true },
    { field: 'gaming_hours',       type: 'scale', text: 'I spend significant time gaming each day.',              values: [0, 0.5, 1, 2, 4],   reverseScale: true },
  ],
  4: [
    { field: 'attendance_percentage', type: 'scale',    text: 'I attend most of my classes and lectures.',         values: [50, 65, 75, 85, 95] },
    { field: 'final_grade',           type: 'number',   text: 'Final grade (optional)',  min: 0, max: 100, step: 0.1, unit: 'pts', optional: true },
    { field: 'grade_opt_in',          type: 'checkbox', text: 'I consent to use my grade data for analytics and recommendations.' },
  ],
};

@Component({
  selector: 'app-habits-assessment',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './habits-assessment.component.html',
  styleUrl: './habits-assessment.component.css',
})
export class HabitsAssessmentComponent {
  private readonly fb = inject(FormBuilder);
  private readonly auth = inject(AuthService);
  private readonly habitsService = inject(HabitsService);
  private readonly router = inject(Router);

  protected readonly submitting = signal(false);
  protected readonly successMessage = signal('');
  protected readonly errorMessage = signal('');
  protected readonly draftStatus = signal('No draft saved yet.');
  protected readonly hasUnsavedChanges = signal(false);
  protected readonly leaving = signal(false);

  // ── Multi-step ──
  protected readonly TOTAL_STEPS = 4;
  protected readonly currentStep = signal(1);
  protected readonly stepDots = Array.from({ length: 4 }, (_, i) => i);
  protected readonly SCALE_NUMS = [1, 2, 3, 4, 5] as const;
  protected readonly STEP_QUESTIONS = STEP_QUESTIONS;

  protected readonly STEP_LABELS: Record<number, string> = {
    1: 'Study Habits',
    2: 'Lifestyle',
    3: 'Digital Life',
    4: 'Grades & Attendance',
  };

  protected readonly STEP_SUBTITLES: Record<number, string> = {
    1: 'Rate your current study routines to unlock insights.',
    2: 'Tell us about your daily health and wellness habits.',
    3: 'How much does technology compete with your focus?',
    4: 'Share your academic performance to personalize results.',
  };

  protected readonly progressSegments = Array.from({ length: METRIC_FIELDS.length }, (_, i) => i);

  /** 1–5 display rating per field; actual metric value is stored on habitsForm */
  protected ratings: Record<string, number | null> = {};

  private lastSubmissionPayload: HabitsAssessmentPayload | null = null;

  protected readonly habitsForm = this.fb.nonNullable.group({
    study_hours: [2, [Validators.required, Validators.min(0), Validators.max(24)]],
    sleep_hours: [7, [Validators.required, Validators.min(0), Validators.max(24)]],
    phone_usage_hours: [2, [Validators.required, Validators.min(0), Validators.max(24)]],
    social_media_hours: [1, [Validators.required, Validators.min(0), Validators.max(24)]],
    gaming_hours: [0, [Validators.required, Validators.min(0), Validators.max(24)]],
    breaks_per_day: [3, [Validators.required, Validators.min(0), Validators.max(50)]],
    coffee_intake: [1, [Validators.required, Validators.min(0), Validators.max(20)]],
    exercise_minutes: [30, [Validators.required, Validators.min(0), Validators.max(300)]],
    stress_level: [5, [Validators.required, Validators.min(1), Validators.max(10)]],
    focus_score: [70, [Validators.required, Validators.min(0), Validators.max(100)]],
    attendance_percentage: [90, [Validators.required, Validators.min(0), Validators.max(100)]],
    assignments_completed_per_week: [5, [Validators.required, Validators.min(0), Validators.max(50)]],
    final_grade: [null as number | null, [Validators.min(0), Validators.max(100)]],
    grade_opt_in: [false, [Validators.required]],
  });

  constructor() {
    this.restoreDraft();
    this.habitsForm.valueChanges.subscribe(() => {
      this.hasUnsavedChanges.set(true);
      this.draftStatus.set('Unsaved changes');
    });
  }

  @HostListener('window:beforeunload', ['$event'])
  protected onBeforeUnload(event: BeforeUnloadEvent): void {
    if (!this.hasUnsavedChanges()) {
      return;
    }
    event.preventDefault();
    event.returnValue = '';
  }

  protected get completionPercentage(): number {
    return Math.round((this.progressCount / METRIC_FIELDS.length) * 100);
  }

  protected get progressCount(): number {
    let complete = 0;
    for (const key of METRIC_FIELDS) {
      const val = this.habitsForm.controls[key as keyof typeof this.habitsForm.controls]?.value;
      if (val !== null && `${val}` !== '') complete += 1;
    }
    return complete;
  }

  protected rangeValue(controlName: string): number {
    return (this.habitsForm.controls[controlName as keyof typeof this.habitsForm.controls]?.value as number) ?? 0;
  }

  protected getStressClass(): string {
    const v = this.rangeValue('stress_level');
    if (v >= 8) return 'high';
    if (v >= 5) return 'mid';
    return 'low';
  }

  protected getRating(field: string): number | null {
    return this.ratings[field] ?? null;
  }

  protected selectRating(field: string, rating: number): void {
    this.ratings[field] = rating;
    const q = Object.values(STEP_QUESTIONS).flat().find(x => x.field === field);
    if (q?.type === 'scale') {
      const value = q.values[rating - 1];
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const ctrl = (this.habitsForm.controls as any)[field];
      ctrl?.setValue(value);
    }
  }

  private ratingFromValue(q: ScaleQuestion, value: number): number {
    let best = 0;
    let bestDist = Infinity;
    q.values.forEach((v, i) => {
      const d = Math.abs(v - value);
      if (d < bestDist) { bestDist = d; best = i + 1; }
    });
    return best;
  }

  protected nextStep(): void {
    const fields = STEP_QUESTIONS[this.currentStep()].map(q => q.field);
    fields.forEach(f => {
      const ctrl = this.habitsForm.controls[f as keyof typeof this.habitsForm.controls];
      ctrl?.markAsTouched();
    });
    const allValid = fields.every(f => {
      const ctrl = this.habitsForm.controls[f as keyof typeof this.habitsForm.controls];
      return !ctrl || ctrl.valid;
    });
    if (!allValid) return;
    if (this.currentStep() < this.TOTAL_STEPS) {
      this.currentStep.update(s => s + 1);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  }

  protected prevStep(): void {
    if (this.currentStep() > 1) {
      this.currentStep.update(s => s - 1);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  }

  protected saveDraft(): void {
    localStorage.setItem(DRAFT_KEY, JSON.stringify(this.habitsForm.getRawValue()));
    const now = new Date().toISOString();
    localStorage.setItem(DRAFT_TIME_KEY, now);
    this.draftStatus.set(`Draft saved at ${new Date(now).toLocaleString()}`);
    this.hasUnsavedChanges.set(false);
  }

  protected submit(): void {
    if (this.habitsForm.invalid || this.submitting()) {
      this.habitsForm.markAllAsTouched();
      return;
    }
    const user = this.auth.user();
    if (!user) {
      this.errorMessage.set('Please sign in again to submit your assessment.');
      return;
    }
    const payload = this.habitsForm.getRawValue() as HabitsAssessmentPayload;
    this.lastSubmissionPayload = payload;

    this.submitting.set(true);
    this.errorMessage.set('');
    this.successMessage.set('');
    this.habitsService
      .submitAssessment(user.id, payload)
      .pipe(finalize(() => this.submitting.set(false)))
      .subscribe({
        next: async (assessment) => {
          this.successMessage.set('Assessment submitted successfully.');
          this.clearDraft();
          this.leaving.set(true);
          await new Promise(r => setTimeout(r, 360));
          void this.router.navigate(['/habits/results'], {
            queryParams: { assessmentId: assessment.assessment_id },
          });
        },
        error: () => {
          this.errorMessage.set('Submission failed. Please retry or save your draft.');
        },
      });
  }

  protected retryLastSubmission(): void {
    if (!this.lastSubmissionPayload || this.submitting()) {
      return;
    }
    const user = this.auth.user();
    if (!user) {
      this.errorMessage.set('Please sign in again to retry.');
      return;
    }
    this.submitting.set(true);
    this.errorMessage.set('');
    this.habitsService
      .submitAssessment(user.id, this.lastSubmissionPayload)
      .pipe(finalize(() => this.submitting.set(false)))
      .subscribe({
        next: async () => {
          this.successMessage.set('Assessment submitted successfully.');
          this.clearDraft();
          this.leaving.set(true);
          await new Promise(r => setTimeout(r, 360));
          void this.router.navigate(['/habits/results']);
        },
        error: () => {
          this.errorMessage.set('Retry failed. Please check values and try again.');
        },
      });
  }

  protected fieldError(controlName: string): string {
    const control = this.habitsForm.controls[controlName as keyof typeof this.habitsForm.controls];
    if (!control || !control.touched || !control.errors) {
      return '';
    }
    if (control.errors['required']) {
      return 'This field is required.';
    }
    if (control.errors['min'] || control.errors['max']) {
      return 'Value is out of allowed range.';
    }
    return 'Invalid value.';
  }

  private restoreDraft(): void {
    const draftRaw = localStorage.getItem(DRAFT_KEY);
    if (!draftRaw) {
      return;
    }
    try {
      const parsed = JSON.parse(draftRaw) as Partial<HabitsAssessmentPayload>;
      this.habitsForm.patchValue(parsed);
      // Restore display ratings from saved numeric values
      Object.values(STEP_QUESTIONS).flat().forEach(q => {
        if (q.type === 'scale') {
          const ctrl = this.habitsForm.controls[q.field as keyof typeof this.habitsForm.controls];
          const val = ctrl?.value as number | null;
          if (val !== null && val !== undefined) {
            this.ratings[q.field] = this.ratingFromValue(q, val);
          }
        }
      });
      const draftTime = localStorage.getItem(DRAFT_TIME_KEY);
      this.draftStatus.set(
        draftTime
          ? `Draft restored from ${new Date(draftTime).toLocaleString()}`
          : 'Draft restored.',
      );
      this.hasUnsavedChanges.set(false);
    } catch {
      this.draftStatus.set('Draft found but could not be restored.');
    }
  }

  private clearDraft(): void {
    localStorage.removeItem(DRAFT_KEY);
    localStorage.removeItem(DRAFT_TIME_KEY);
    this.hasUnsavedChanges.set(false);
    this.draftStatus.set('Draft cleared after successful submission.');
  }
}
