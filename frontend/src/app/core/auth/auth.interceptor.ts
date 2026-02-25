import {
  HttpContextToken,
  HttpErrorResponse,
  HttpHandlerFn,
  HttpInterceptorFn,
  HttpRequest,
} from '@angular/common/http';
import { inject } from '@angular/core';
import { throwError } from 'rxjs';
import { catchError, switchMap } from 'rxjs/operators';

import { AuthService } from './auth.service';

const SHOULD_RETRY_ONCE = new HttpContextToken<boolean>(() => true);

function isApiRequest(url: string): boolean {
  return url.startsWith('/api');
}

function isAuthEndpoint(url: string): boolean {
  return (
    url.startsWith('/api/auth/login')
    || url.startsWith('/api/auth/register')
    || url.startsWith('/api/auth/refresh')
  );
}

function addBearerToken(request: HttpRequest<unknown>, token: string): HttpRequest<unknown> {
  return request.clone({
    setHeaders: {
      Authorization: `Bearer ${token}`,
    },
  });
}

function handleUnauthorizedError(request: HttpRequest<unknown>, next: HttpHandlerFn) {
  const auth = inject(AuthService);

  if (!request.context.get(SHOULD_RETRY_ONCE)) {
    return throwError(() => new HttpErrorResponse({ status: 401, statusText: 'Unauthorized' }));
  }

  return auth.refreshAccessToken().pipe(
    switchMap((tokenResponse) => {
      const retriedRequest = addBearerToken(request, tokenResponse.access_token).clone({
        context: request.context.set(SHOULD_RETRY_ONCE, false),
      });
      return next(retriedRequest);
    }),
    catchError((refreshError) => {
      auth.forceLogoutRedirect();
      return throwError(() => refreshError);
    }),
  );
}

export const authInterceptor: HttpInterceptorFn = (request, next) => {
  const auth = inject(AuthService);

  const token = auth.getToken();
  let authRequest = request;
  if (token && isApiRequest(request.url) && !isAuthEndpoint(request.url)) {
    authRequest = addBearerToken(request, token);
  }

  return next(authRequest).pipe(
    catchError((error: unknown) => {
      if (!(error instanceof HttpErrorResponse) || error.status !== 401) {
        return throwError(() => error);
      }

      if (!isApiRequest(request.url) || isAuthEndpoint(request.url)) {
        return throwError(() => error);
      }

      return handleUnauthorizedError(request, next);
    }),
  );
};
