import { Route } from '@angular/router';
import { ROUTE_TOKENS } from '@app/shared/app-config';

import { RegistrationShellComponent } from './registration-shell';

export const registrationRoutes: Route[] = [
  {
    path: '',
    component: RegistrationShellComponent,
    children: [
      {
        redirectTo: ROUTE_TOKENS.REGISTRATION.REGISTRATION,
        path: '',
        pathMatch: 'full',
      },
      {
        path: ROUTE_TOKENS.REGISTRATION.REGISTRATION,
        loadComponent: () =>
          import('@app/pages/registration').then(
            (c) => c.RegistrationComponent,
          ),
      },
      {
        path: ROUTE_TOKENS.REGISTRATION.CONFIRMATION_CODE,
        loadComponent: () =>
          import('@app/pages/registration-code').then(
            (c) => c.RegistrationCodeComponent,
          ),
      },
      {
        path: ROUTE_TOKENS.REGISTRATION.CREATE_PASSWORD,
        loadComponent: () =>
          import('@app/pages/registration-new-password').then(
            (c) => c.RegistrationNewPasswordComponent,
          ),
      },
    ],
  },
  {
    path: ROUTE_TOKENS.REGISTRATION.REGISTRATION_SUCCESS,
    loadComponent: () =>
      import('@app/pages/registration-success').then(
        (c) => c.RegistrationSuccessComponent,
      ),
  },
];
