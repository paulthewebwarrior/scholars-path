import { CommonModule } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { finalize } from 'rxjs/operators';

import { AuthService } from '../../core/auth/auth.service';
import { ProfileUpdatePayload } from '../../core/auth/auth.types';

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

  protected readonly yearLevels = YEAR_LEVELS;
  protected readonly loading = signal(false);
  protected readonly saving = signal(false);
  protected readonly editing = signal(false);
  protected readonly successMessage = signal('');
  protected readonly errorMessage = signal('');

  protected readonly profileForm = this.fb.nonNullable.group({
    name: ['', [Validators.required, Validators.maxLength(100)]],
    course: ['', [Validators.required]],
    year_level: ['Freshman' as (typeof YEAR_LEVELS)[number], [Validators.required]],
    career_goal: [''],
  });

  constructor() {
    this.loadProfile();
  }

  protected loadProfile(): void {
    if (this.auth.user()) {
      this.profileForm.patchValue({
        name: this.auth.user()!.name,
        course: this.auth.user()!.course,
        year_level: this.auth.user()!.year_level,
        career_goal: this.auth.user()!.career_goal,
      });
      return;
    }

    this.loading.set(true);
    this.auth
      .fetchProfile()
      .pipe(finalize(() => this.loading.set(false)))
      .subscribe({
        next: (profile) => {
          this.profileForm.patchValue({
            name: profile.name,
            course: profile.course,
            year_level: profile.year_level,
            career_goal: profile.career_goal,
          });
        },
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
    this.loadProfile();
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

  protected logout(): void {
    this.auth.logout().subscribe();
  }
}
