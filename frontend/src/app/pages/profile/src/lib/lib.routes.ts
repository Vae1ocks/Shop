import { Route } from '@angular/router';
import { ProfileComponent } from './profile/profile.component';
import { ROUTE_TOKENS } from '@app/shared/app-config';
import { UserComponent } from './components/user/user.component';
import { OrdersComponent } from './components/orders/orders.component';

export const profileRoutes: Route[] = [
  {
    path: '',
    component: ProfileComponent,
    children: [
      {
        path: ROUTE_TOKENS.PROFILE.USER,
        component: UserComponent,
      },
      {
        path: ROUTE_TOKENS.PROFILE.ORDER,
        component: OrdersComponent,
      },
      {
        path: ROUTE_TOKENS.PROFILE.HISTORY,
        loadChildren: () => import('./components/history/history.component').then(m => m.HistoryComponent),
      },
      {
        path: ROUTE_TOKENS.PROFILE.PROMO,
        loadChildren: () => import('./components/promo/promo.component').then(m => m.PromoComponent),
      },
      {
        path: ROUTE_TOKENS.PROFILE.REVIEWS,
        loadChildren: () => import('./components/reviews/reviews.component').then(m => m.ReviewsComponent),
      },
      {
        path: ROUTE_TOKENS.PROFILE.SETTING,
        loadChildren: () => import('./components/setting/setting.component').then(m => m.SettingComponent),
      },
    ],
  },
];
