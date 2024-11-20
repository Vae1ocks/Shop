import { Route } from '@angular/router';
import { ROUTE_TOKENS } from '@app/shared/app-config';

import { ProfileComponent } from './profile/profile.component';

export const profileRoutes: Route[] = [
  {
    path: '',
    component: ProfileComponent,
    children: [
      {
        path: '',
        pathMatch: 'full',
        redirectTo: ROUTE_TOKENS.PROFILE.USER,
      },
      {
        path: ROUTE_TOKENS.PROFILE.USER,
        loadComponent: () =>
          import('./components/user/user.component').then(
            (c) => c.UserComponent,
          ),
      },
      {
        path: ROUTE_TOKENS.PROFILE.PROMO,
        loadComponent: () =>
          import('./components/promo/promo.component').then(
            (m) => m.PromoComponent,
          ),
      },
      {
        path: ROUTE_TOKENS.PROFILE.REVIEWS,
        loadComponent: () =>
          import('./components/reviews/reviews.component').then(
            (m) => m.ReviewsComponent,
          ),
      },
      {
        path: ROUTE_TOKENS.PROFILE.SETTING,
        loadComponent: () =>
          import('./components/setting/setting.component').then(
            (m) => m.SettingComponent,
          ),
      },
    ],
  },
];
