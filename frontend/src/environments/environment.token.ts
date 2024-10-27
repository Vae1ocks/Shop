import { InjectionToken } from '@angular/core';

import { environment } from './environment.development';
import { Environment } from './environment.interface';

export const ENV_TOKEN = new InjectionToken<Environment>('environment.token', {
  providedIn: 'root',
  factory: () => environment,
});
