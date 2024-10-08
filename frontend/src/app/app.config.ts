import { provideHttpClient, withInterceptors } from '@angular/common/http';
import {
  ApplicationConfig,
  importProvidersFrom,
  provideZoneChangeDetection,
} from '@angular/core';
import { provideRouter } from '@angular/router';
import { authInterceptor } from '@app/core';
import { provideAngularSvgIcon } from 'angular-svg-icon';
import { register as registerSwiper } from 'swiper/element';

import { appRoutes } from './app.routes';
import { ApiModule } from './swagger/api.module';

registerSwiper();

export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(appRoutes),
    provideHttpClient(withInterceptors([authInterceptor])),
    importProvidersFrom(ApiModule.forRoot({ rootUrl: '' })),
    provideAngularSvgIcon(),
  ],
};
