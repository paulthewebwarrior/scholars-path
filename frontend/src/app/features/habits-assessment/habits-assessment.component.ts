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

  private readonly stepFields: Record<number, string[]> = {
    1: ['study_hours', 'breaks_per_day', 'assignments_completed_per_week', 'focus_score'],
    2: ['sleep_hours', 'exercise_minutes', 'coffee_intake', 'stress_level'],
    3: ['phone_usage_hours', 'social_media_hours', 'gaming_hours'],
    4: ['attendance_percentage', 'final_grade', 'grade_opt_in'],
  };

  protected readonly STEP_LABELS: Record<number, string> = {
    1: 'Study Patterns',
    2: 'Lifestyle',
    3: 'Digital Usage',
    4: 'Performance',
  };

  protected readonly progressSegments = Array.from({ length: METRIC_FIELDS.length }, (_, i) => i);

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

  protected nextStep(): void {
    const fields = this.stepFields[this.currentStep()];
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
