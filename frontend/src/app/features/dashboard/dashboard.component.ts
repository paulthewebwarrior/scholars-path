import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { RouterLink } from '@angular/router';

import { AuthService } from '../../core/auth/auth.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css',
})
export class DashboardComponent {
  protected readonly auth = inject(AuthService);

  constructor() {
    if (!this.auth.user()) {
      this.auth.fetchProfile().subscribe({
        error: () => {
          // Guarded route should already ensure auth state.
        },
      });
    }
  }
}
