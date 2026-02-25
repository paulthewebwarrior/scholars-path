import { Component } from '@angular/core';
import { TestBed } from '@angular/core/testing';
import { ActivatedRouteSnapshot, Router, RouterStateSnapshot, UrlTree, provideRouter } from '@angular/router';
import { Observable, firstValueFrom, of, throwError } from 'rxjs';

import { authGuard } from './auth.guard';
import { AuthService } from './auth.service';

@Component({
  template: '',
})
class DummyComponent {}

describe('authGuard', () => {
  const authServiceStub: Pick<AuthService, 'isAuthenticated' | 'refreshAccessToken'> = {
    isAuthenticated: () => true,
    refreshAccessToken: () => of({ access_token: 'token', token_type: 'bearer' }),
  };

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        provideRouter([{ path: 'login', component: DummyComponent }]),
        { provide: AuthService, useValue: authServiceStub },
      ],
    });
  });

  it('allows navigation when already authenticated', () => {
    authServiceStub.isAuthenticated = () => true;

    const result = TestBed.runInInjectionContext(() =>
      authGuard({} as ActivatedRouteSnapshot, {} as RouterStateSnapshot),
    );

    expect(result).toBe(true);
  });

  it('redirects to login when refresh fails', async () => {
    authServiceStub.isAuthenticated = () => false;
    authServiceStub.refreshAccessToken = () => throwError(() => new Error('refresh failed'));

    const result = TestBed.runInInjectionContext(() =>
      authGuard({} as ActivatedRouteSnapshot, {} as RouterStateSnapshot),
    );

    const value = await firstValueFrom(result as Observable<boolean | UrlTree>);
    const router = TestBed.inject(Router);
    expect(value.toString()).toBe(router.createUrlTree(['/login']).toString());
  });
});
