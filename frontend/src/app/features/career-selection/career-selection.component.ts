import { CommonModule } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { finalize } from 'rxjs/operators';

import { AuthService } from '../../core/auth/auth.service';
import { Career } from '../../core/careers/careers.types';
import { CareersService } from '../../core/careers/careers.service';

@Component({
  selector: 'app-career-selection',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './career-selection.component.html',
  styleUrls: ['../pixel-ui.css', './career-selection.component.css'],
})
export class CareerSelectionComponent {
  private readonly fb = inject(FormBuilder);
  private readonly auth = inject(AuthService);
  private readonly careersService = inject(CareersService);
  private readonly router = inject(Router);

  protected readonly loading = signal(true);
  protected readonly saving = signal(false);
  protected readonly errorMessage = signal('');
  protected readonly successMessage = signal('');
  protected readonly careers = signal<Career[]>([]);

  protected readonly selectionForm = this.fb.nonNullable.group({
    career_id: [0, [Validators.required, Validators.min(1)]],
  });

  constructor() {
    this.loadCareers();
  }

  protected chooseCareer(careerId: number): void {
    this.selectionForm.patchValue({ career_id: careerId });
    this.errorMessage.set('');
  }

  protected saveSelection(): void {
    if (this.selectionForm.invalid || this.saving()) {
      this.selectionForm.markAllAsTouched();
      this.errorMessage.set('Select a career to continue.');
      return;
    }

    this.saving.set(true);
    this.errorMessage.set('');
    this.successMessage.set('');

    const payload = this.selectionForm.getRawValue();
    const isUpdate = !!this.auth.user()?.career_id;
    const request$ = isUpdate ? this.auth.updateCareer(payload) : this.auth.setCareer(payload);

    request$.pipe(finalize(() => this.saving.set(false))).subscribe({
      next: async () => {
        this.successMessage.set('Career saved successfully.');
        await new Promise((resolve) => setTimeout(resolve, 260));
        void this.router.navigate(['/dashboard']);
      },
      error: () => {
        this.errorMessage.set('Unable to save your career selection right now.');
      },
    });
  }

  private loadCareers(): void {
    const user = this.auth.user();

    this.loading.set(true);
    this.careersService
      .getCareers()
      .pipe(finalize(() => this.loading.set(false)))
      .subscribe({
        next: (careers) => {
          this.careers.set(careers);
          const preselectedCareer = user?.career_id ?? 0;
          if (preselectedCareer > 0) {
            this.selectionForm.patchValue({ career_id: preselectedCareer });
          }
        },
        error: () => {
          this.errorMessage.set('Unable to load careers. Please retry.');
        },
      });
  }
}
