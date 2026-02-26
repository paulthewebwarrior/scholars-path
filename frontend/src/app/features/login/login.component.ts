import { CommonModule } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { finalize, switchMap } from 'rxjs/operators';

import { AuthService } from '../../core/auth/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './login.component.html',
  styleUrls: ['../auth.shared.css', './login.component.css'],
})
export class LoginComponent {
  private readonly fb = inject(FormBuilder);
  private readonly auth = inject(AuthService);
  private readonly router = inject(Router);
  private readonly route = inject(ActivatedRoute);

  protected readonly loading = signal(false);
  protected readonly errorMessage = signal('');
  protected readonly successMessage = signal('');

  protected readonly loginForm = this.fb.nonNullable.group({
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required]],
  });

  constructor() {
    if (this.route.snapshot.queryParamMap.get('registered') === '1') {
      this.successMessage.set('Registration successful. Please log in.');
    }
  }

  protected submit(): void {
    if (this.loginForm.invalid || this.loading()) {
      this.loginForm.markAllAsTouched();
      return;
    }

    this.loading.set(true);
    this.errorMessage.set('');

    const { email, password } = this.loginForm.getRawValue();
    this.auth
      .login({ email, password })
      .pipe(
        switchMap(() => this.auth.fetchProfile()),
        finalize(() => this.loading.set(false)),
      )
      .subscribe({
        next: (profile) => {
          void this.router.navigate([profile.career_id ? '/dashboard' : '/onboarding/career']);
        },
        error: () => {
          this.errorMessage.set('Invalid email or password');
        },
      });
  }
}
