import { Route } from '@angular/router';
import { ROUTE_TOKENS } from '@app/shared/app-config';

import { ResetPasswordShellComponent } from './reset-password-shell';

export const resetPasswordRoutes: Route[] = [
  {
    path: '',
    component: ResetPasswordShellComponent,
    children: [
      {
        redirectTo: ROUTE_TOKENS.RESET_PASSWORD.RESET_PASSWORD,
        path: '',
        pathMatch: 'full',
      },
      {
        path: ROUTE_TOKENS.RESET_PASSWORD.RESET_PASSWORD,
        loadComponent: () =>
          import('@app/pages/reset-password').then(
            (c) => c.ResetPasswordComponent,
          ),
      },
      {
        path: ROUTE_TOKENS.RESET_PASSWORD.CONFIRMATION_CODE,
        loadComponent: () =>
          import('@app/pages/reset-password-code').then(
            (c) => c.ResetPasswordCodeComponent,
          ),
      },
      {
        path: ROUTE_TOKENS.RESET_PASSWORD.CREATE_PASSWORD,
        loadComponent: () =>
          import('@app/pages/reset-password-new-password').then(
            (c) => c.ResetPasswordNewPasswordComponent,
          ),
      },
    ],
  },
  {
    path: ROUTE_TOKENS.RESET_PASSWORD.RESET_PASSWORD_SUCCESS,
    loadComponent: () =>
      import('@app/pages/reset-password-success').then(
        (c) => c.ResetPasswordSuccessComponent,
      ),
  },
];
