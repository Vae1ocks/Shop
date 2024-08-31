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
    path: '',
    loadChildren: () =>
      import('@app/pages/reset-password-shell').then(
        (c) => c.resetPasswordRoutes,
      ),
  },
  {
    path: '**',
    redirectTo: '/',
  },
];
