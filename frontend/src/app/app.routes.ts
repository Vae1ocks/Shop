import { Route } from '@angular/router';
import { ROUTE_TOKENS } from '@app/shared/app-config';

import { LayoutComponent } from './layout.component';

export const appRoutes: Route[] = [
  {
    component: LayoutComponent,
    path: '',
    children: [
      {
        path: ROUTE_TOKENS.MAIN,
        loadComponent: () =>
          import('@app/pages/main').then((c) => c.MainComponent),
      },
    ],
  },
  {
    path: ROUTE_TOKENS.LOGIN,
    loadComponent: () =>
      import('@app/pages/login').then((c) => c.LoginComponent),
  },
  {
    path: '',
    loadChildren: () =>
      import('@app/pages/registration-shell').then((c) => c.registrationRoutes),
  },
  {
    path: ROUTE_TOKENS.REGISTRATION.REGISTRATION_SUCCESS,
    loadComponent: () =>
      import('@app/pages/registration-success').then(
        (c) => c.RegistrationSuccessComponent,
      ),
  },
  {
    path: ROUTE_TOKENS.RESET_PASSWORD,
    loadComponent: () =>
      import('@app/pages/reset-password').then((c) => c.ResetPasswordComponent),
  },
  {
    path: '**',
    redirectTo: '/',
  },
];
