import { Route } from '@angular/router';
import { ROUTES_TOKEN_CONFIG } from '@app/shared/app-config';

import { ResetPasswordShellComponent } from './reset-password-shell';

export const resetPasswordRoutes: Route[] = [
  {
    path: '',
    component: ResetPasswordShellComponent,
    children: [
      {
        redirectTo: ROUTES_TOKEN_CONFIG.RESET_PASSWORD.RESET_PASSWORD,
        path: '',
        pathMatch: 'full',
      },
      {
        path: ROUTES_TOKEN_CONFIG.RESET_PASSWORD.RESET_PASSWORD,
        loadComponent: () =>
          import('@app/pages/reset-password').then(
            (c) => c.ResetPasswordComponent,
          ),
      },
      {
        path: ROUTES_TOKEN_CONFIG.RESET_PASSWORD.CONFIRMATION_CODE,
        loadComponent: () =>
          import('@app/pages/reset-password-code').then(
            (c) => c.ResetPasswordCodeComponent,
          ),
      },
      {
        path: ROUTES_TOKEN_CONFIG.RESET_PASSWORD.CREATE_PASSWORD,
        loadComponent: () =>
          import('@app/pages/reset-password-new-password').then(
            (c) => c.ResetPasswordNewPasswordComponent,
          ),
      },
    ],
  },
  {
    path: ROUTES_TOKEN_CONFIG.RESET_PASSWORD.RESET_PASSWORD_SUCCESS,
    loadComponent: () =>
      import('@app/pages/reset-password-success').then(
        (c) => c.ResetPasswordSuccessComponent,
      ),
  },
];
