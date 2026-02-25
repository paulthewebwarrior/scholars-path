import { CommonModule } from '@angular/common';
import { Component, computed, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { finalize } from 'rxjs/operators';

import { AuthService } from '../../core/auth/auth.service';
import { RegisterPayload } from '../../core/auth/auth.types';

const YEAR_LEVELS = ['Freshman', 'Sophomore', 'Junior', 'Senior'] as const;

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './register.component.html',
  styleUrl: './register.component.css',
})
export class RegisterComponent {
  private readonly fb = inject(FormBuilder);
  private readonly auth = inject(AuthService);
  private readonly router = inject(Router);

  protected readonly yearLevels = YEAR_LEVELS;
  protected readonly loading = signal(false);
  protected readonly serverError = signal('');

  protected readonly registerForm = this.fb.nonNullable.group({
    email: ['', [Validators.required, Validators.email]],
    password: [
      '',
      [
        Validators.required,
        Validators.minLength(8),
        Validators.pattern(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$/),
      ],
    ],
    name: ['', [Validators.required, Validators.maxLength(100)]],
    course: ['', [Validators.required]],
    year_level: ['Freshman' as (typeof YEAR_LEVELS)[number], [Validators.required]],
    career_goal: ['', [Validators.required]],
  });

  protected readonly passwordStrength = computed(() => {
    const value = this.registerForm.controls.password.value;
    const checks = {
      length: value.length >= 8,
      uppercase: /[A-Z]/.test(value),
      lowercase: /[a-z]/.test(value),
      number: /\d/.test(value),
    };
    const score = Object.values(checks).filter(Boolean).length;

    if (score <= 1) {
      return { label: 'Weak', checks };
    }
    if (score <= 3) {
      return { label: 'Medium', checks };
    }
    return { label: 'Strong', checks };
  });

  protected submit(): void {
    if (this.registerForm.invalid || this.loading()) {
      this.registerForm.markAllAsTouched();
      return;
    }

    this.loading.set(true);
    this.serverError.set('');

    const payload = this.registerForm.getRawValue() as RegisterPayload;
    this.auth
      .register(payload)
      .pipe(finalize(() => this.loading.set(false)))
      .subscribe({
        next: () => {
          void this.router.navigate(['/login'], { queryParams: { registered: 1 } });
        },
        error: (error: { status?: number; error?: { detail?: string } }) => {
          if (error.status === 400 && error.error?.detail) {
            this.serverError.set(error.error.detail);
            return;
          }
          if (error.status === 422) {
            this.serverError.set('Please correct validation errors and try again.');
            return;
          }
          this.serverError.set('Unable to register. Please try again.');
        },
      });
  }
}
