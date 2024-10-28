import { Route } from '@angular/router';
import { ROUTES_TOKEN_CONFIG } from '@app/shared/app-config';

import { LayoutComponent } from './layout.component';

export const appRoutes: Route[] = [
  {
    path: '',
    data: { baseHeader: true },
    children: [
      {
        path: ROUTES_TOKEN_CONFIG.LOGIN,
        loadComponent: () =>
          import('@app/pages/login').then((c) => c.LoginComponent),
      },
      {
        path: '',
        loadChildren: () =>
          import('@app/pages/registration-shell').then(
            (c) => c.registrationRoutes,
          ),
      },
      {
        path: '',
        loadChildren: () =>
          import('@app/pages/reset-password-shell').then(
            (c) => c.resetPasswordRoutes,
          ),
      },
    ],
  },
  {
    component: LayoutComponent,
    path: '',
    children: [
      {
        path: ROUTES_TOKEN_CONFIG.MAIN,
        loadComponent: () =>
          import('@app/pages/main').then((c) => c.MainComponent),
      },
      {
        path: ROUTES_TOKEN_CONFIG.CATEGORIES,
        loadComponent: () =>
          import('@app/pages/categories').then((c) => c.CategoriesComponent),
      },
      {
        path: ROUTES_TOKEN_CONFIG.SEARCH,
        loadComponent: () =>
          import('@app/pages/search').then((c) => c.SearchComponent),
      },
      {
        path: ROUTES_TOKEN_CONFIG.FAVOURITES,
        loadComponent: () =>
          import('@app/pages/favourites').then((c) => c.FavouritesComponent),
      },
    ],
  },
  {
    path: '**',
    redirectTo: '/',
  },
];
