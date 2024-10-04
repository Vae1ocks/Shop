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
    path: ROUTE_TOKENS.PROFILE,
    loadChildren: () =>
      import('@app/pages/profile').then((c) => c.profileRoutes),
  },
  {
    path: '',
    loadChildren: () =>
      import('@app/pages/registration-shell').then((c) => c.registrationRoutes),
  },
  {
    path: '**',
    redirectTo: '/',
  },
];
