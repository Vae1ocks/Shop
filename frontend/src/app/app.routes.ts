import { Route } from '@angular/router';

import { ROUTE_TOKENS } from './shared/app-config/route-tokens';

export const appRoutes: Route[] = [
  {
    path: ROUTE_TOKENS.LOGIN,
    loadComponent: () =>
      import('@app/pages/login').then((c) => c.LoginComponent),
  },
  {
    path: ROUTE_TOKENS.REGISTRATION.REGISTRATION,
    loadComponent: () =>
      import('@app/pages/registration').then((c) => c.RegistrationComponent),
  },
  {
    path: ROUTE_TOKENS.REGISTRATION.CONFIRMATION_CODE,
    loadComponent: () =>
      import('@app/pages/confirmation-code').then(
        (c) => c.ConfirmationCodeComponent,
      ),
  },
  {
    path: ROUTE_TOKENS.REGISTRATION.CREATE_PASSWORD,
    loadComponent: () =>
      import('@app/pages/create-password').then(
        (c) => c.CreatePasswordComponent,
      ),
  },
  {
    path: ROUTE_TOKENS.REGISTRATION.REGISTRATION_SUCCESS,
    loadComponent: () =>
      import('@app/pages/registration-success').then(
        (c) => c.RegistrationSuccessComponent,
      ),
  },
  {
    path: '**',
    redirectTo: '/',
  },
];
