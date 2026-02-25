import { CommonModule } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { finalize } from 'rxjs/operators';

import { AuthService } from '../../core/auth/auth.service';
import { ProfileUpdatePayload } from '../../core/auth/auth.types';
import { CareersService } from '../../core/careers/careers.service';
import { Career } from '../../core/careers/careers.types';

const YEAR_LEVELS = ['Freshman', 'Sophomore', 'Junior', 'Senior'] as const;

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './profile.component.html',
  styleUrls: ['../pixel-ui.css', './profile.component.css'],
})
export class ProfileComponent {
  private readonly fb = inject(FormBuilder);
  protected readonly auth = inject(AuthService);
  private readonly careersService = inject(CareersService);

  protected readonly yearLevels = YEAR_LEVELS;
  protected readonly loading = signal(false);
  protected readonly saving = signal(false);
  protected readonly editing = signal(false);
  protected readonly successMessage = signal('');
  protected readonly errorMessage = signal('');

  protected readonly careerEditing = signal(false);
  protected readonly careerSaving = signal(false);
  protected readonly careerErrorMessage = signal('');
  protected readonly careerOptions = signal<Career[]>([]);

  protected readonly profileForm = this.fb.nonNullable.group({
    name: ['', [Validators.required, Validators.maxLength(100)]],
    course: ['', [Validators.required]],
    year_level: ['Freshman' as (typeof YEAR_LEVELS)[number], [Validators.required]],
  });

  protected readonly careerForm = this.fb.nonNullable.group({
    career_id: [0, [Validators.required, Validators.min(1)]],
  });

  constructor() {
    this.loadProfile();
    this.loadCareerOptions();
  }

  protected loadProfile(): void {
    if (this.auth.user()) {
      this.patchFormsFromProfile();
      return;
    }

    this.loading.set(true);
    this.auth
      .fetchProfile()
      .pipe(finalize(() => this.loading.set(false)))
      .subscribe({
        next: () => this.patchFormsFromProfile(),
        error: () => {
          this.errorMessage.set('Unable to load profile.');
        },
      });
  }

  protected startEdit(): void {
    this.editing.set(true);
    this.successMessage.set('');
    this.errorMessage.set('');
  }

  protected cancelEdit(): void {
    this.editing.set(false);
    this.successMessage.set('');
    this.errorMessage.set('');
    this.patchFormsFromProfile();
  }

  protected save(): void {
    if (this.profileForm.invalid || this.saving()) {
      this.profileForm.markAllAsTouched();
      return;
    }

    this.saving.set(true);
    this.successMessage.set('');
    this.errorMessage.set('');

    const payload = this.profileForm.getRawValue() as ProfileUpdatePayload;
    this.auth
      .updateProfile(payload)
      .pipe(finalize(() => this.saving.set(false)))
      .subscribe({
        next: () => {
          this.editing.set(false);
          this.successMessage.set('Profile updated successfully.');
        },
        error: () => {
          this.errorMessage.set('Unable to update profile.');
        },
      });
  }

  protected startCareerEdit(): void {
    this.careerEditing.set(true);
    this.careerErrorMessage.set('');
    const currentCareerId = this.auth.user()?.career_id ?? 0;
    this.careerForm.patchValue({ career_id: currentCareerId });
  }

  protected cancelCareerEdit(): void {
    this.careerEditing.set(false);
    this.careerErrorMessage.set('');
    this.patchFormsFromProfile();
  }

  protected saveCareer(): void {
    if (this.careerForm.invalid || this.careerSaving()) {
      this.careerForm.markAllAsTouched();
      this.careerErrorMessage.set('Please select a career before saving.');
      return;
    }

    this.careerSaving.set(true);
    this.careerErrorMessage.set('');
    this.successMessage.set('');

    this.auth
      .updateCareer(this.careerForm.getRawValue())
      .pipe(finalize(() => this.careerSaving.set(false)))
      .subscribe({
        next: () => {
          this.careerEditing.set(false);
          this.successMessage.set('Career updated successfully.');
        },
        error: () => {
          this.careerErrorMessage.set('Unable to update selected career.');
        },
      });
  }

  protected logout(): void {
    this.auth.logout().subscribe();
  }

  private loadCareerOptions(): void {
    this.careersService.getCareers().subscribe({
      next: (careers) => this.careerOptions.set(careers),
      error: () => {
        this.careerErrorMessage.set('Unable to load careers.');
      },
    });
  }

  private patchFormsFromProfile(): void {
    const profile = this.auth.user();
    if (!profile) {
      return;
    }

    this.profileForm.patchValue({
      name: profile.name,
      course: profile.course,
      year_level: profile.year_level,
    });
    this.careerForm.patchValue({ career_id: profile.career_id ?? 0 });
  }
}
