import { InjectionToken } from '@angular/core';

import { ROUTES_TOKEN_CONFIG } from './routes-token-config';

export const ROUTES_TOKEN = new InjectionToken('route-token.config', {
  providedIn: 'root',
  factory: () => ROUTES_TOKEN_CONFIG,
});
