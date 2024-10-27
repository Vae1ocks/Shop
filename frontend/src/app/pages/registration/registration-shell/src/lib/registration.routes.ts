import { Route } from '@angular/router';
import { ROUTES_TOKEN_CONFIG } from '@app/shared/app-config';

import { RegistrationShellComponent } from './registration-shell';

export const registrationRoutes: Route[] = [
  {
    path: '',
    component: RegistrationShellComponent,
    children: [
      {
        redirectTo: ROUTES_TOKEN_CONFIG.REGISTRATION.REGISTRATION,
        path: '',
        pathMatch: 'full',
      },
      {
        path: ROUTES_TOKEN_CONFIG.REGISTRATION.REGISTRATION,
        loadComponent: () =>
          import('@app/pages/registration').then(
            (c) => c.RegistrationComponent,
          ),
      },
      {
        path: ROUTES_TOKEN_CONFIG.REGISTRATION.CONFIRMATION_CODE,
        loadComponent: () =>
          import('@app/pages/registration-code').then(
            (c) => c.RegistrationCodeComponent,
          ),
      },
      {
        path: ROUTES_TOKEN_CONFIG.REGISTRATION.CREATE_PASSWORD,
        loadComponent: () =>
          import('@app/pages/registration-new-password').then(
            (c) => c.RegistrationNewPasswordComponent,
          ),
      },
    ],
  },
  {
    path: ROUTES_TOKEN_CONFIG.REGISTRATION.REGISTRATION_SUCCESS,
    loadComponent: () =>
      import('@app/pages/registration-success').then(
        (c) => c.RegistrationSuccessComponent,
      ),
  },
];
