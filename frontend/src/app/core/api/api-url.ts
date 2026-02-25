const API_PREFIX = '/api';
const LOCAL_DEV_FRONTEND_PORT = '4200';
const LOCAL_DEV_API_ORIGIN = 'http://localhost:8000';

function getBrowserOrigin(): string {
  if (typeof window === 'undefined' || !window.location?.origin) {
    return LOCAL_DEV_API_ORIGIN;
  }
  return window.location.origin;
}

function getPathname(url: string): string {
  try {
    const resolved = new URL(url, getBrowserOrigin());
    return resolved.pathname;
  } catch {
    return url;
  }
}

export function getApiBaseUrl(): string {
  if (typeof window === 'undefined') {
    return API_PREFIX;
  }

  const { hostname, port } = window.location;
  if (hostname === 'localhost' && port === LOCAL_DEV_FRONTEND_PORT) {
    return `${LOCAL_DEV_API_ORIGIN}${API_PREFIX}`;
  }

  return API_PREFIX;
}

export function isApiUrl(url: string): boolean {
  return getPathname(url).startsWith(API_PREFIX);
}

export function isAuthApiUrl(url: string): boolean {
  const pathname = getPathname(url);
  return (
    pathname.startsWith('/api/auth/login')
    || pathname.startsWith('/api/auth/register')
    || pathname.startsWith('/api/auth/refresh')
  );
}
