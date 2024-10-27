import { InjectionToken } from '@angular/core';

import { AppConfig } from './app.config.interface';

const APP_DI_CONFIG: AppConfig = {
  REGISTRATION_FORM_STORAGE_KEY: 'registration-form',
  RESET_PASSWORD_FORM_STORAGE_KEY: 'reset-password-form',
};

export const APP_CONFIG = new InjectionToken<AppConfig>('app.config', {
  providedIn: 'root',
  factory: () => APP_DI_CONFIG,
});
