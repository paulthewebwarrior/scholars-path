import { CommonModule } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { finalize } from 'rxjs/operators';

import { AuthService } from '../../core/auth/auth.service';
import { UserProfile } from '../../core/auth/auth.types';
import { CareersService } from '../../core/careers/careers.service';
import { CareerAlignedRecommendation } from '../../core/careers/careers.types';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './dashboard.component.html',
  styleUrls: ['../pixel-ui.css', './dashboard.component.css'],
})
export class DashboardComponent {
  protected readonly auth = inject(AuthService);
  private readonly careersService = inject(CareersService);

  protected readonly recommendationsLoading = signal(false);
  protected readonly recommendationsError = signal('');
  protected readonly careerRecommendations = signal<CareerAlignedRecommendation[]>([]);
  protected readonly selectedCareerName = signal('');

  constructor() {
    this.loadDashboardData();
  }

  protected weaknessPercent(score: number): number {
    return Math.round(score * 100);
  }

  private loadDashboardData(): void {
    const existing = this.auth.user();
    if (existing) {
      this.handleProfileReady(existing);
      return;
    }

    this.auth.fetchProfile().subscribe({
      next: (profile) => this.handleProfileReady(profile),
      error: () => {
        this.recommendationsError.set('Unable to load dashboard profile data.');
      },
    });
  }

  private handleProfileReady(profile: UserProfile): void {
    if (!profile.career_id) {
      this.selectedCareerName.set('');
      this.careerRecommendations.set([]);
      return;
    }

    this.selectedCareerName.set(profile.career?.name ?? profile.career_goal);
    this.recommendationsLoading.set(true);
    this.recommendationsError.set('');

    this.careersService
      .getCareerAlignedRecommendations(profile.id, { limit: 3 })
      .pipe(finalize(() => this.recommendationsLoading.set(false)))
      .subscribe({
        next: (response) => {
          this.selectedCareerName.set(response.career?.name ?? profile.career_goal);
          this.careerRecommendations.set(response.items.slice(0, 3));
        },
        error: () => {
          this.recommendationsError.set('Unable to load career-aligned recommendations.');
        },
      });
  }
}
