import { AsyncPipe } from '@angular/common';
import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import { NavigationEnd, Router, RouterOutlet } from '@angular/router';
import { HeaderComponent } from '@app/layout/header';
import { HeaderInfoComponent } from '@app/layout/header-info';
import { ROUTES_TOKEN } from '@app/shared/app-config';
import { SvgIconComponent } from 'angular-svg-icon';
import { distinctUntilChanged, filter, map } from 'rxjs/operators';

@Component({
  standalone: true,
  imports: [
    AsyncPipe,
    RouterOutlet,
    SvgIconComponent,
    HeaderInfoComponent,
    HeaderComponent,
  ],
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class AppComponent {
  private readonly ROUTES_TOKEN = inject(ROUTES_TOKEN);

  private readonly router = inject(Router);

  private readonly routesWithBaseHeader: string[] = [
    this.ROUTES_TOKEN.LOGIN,
    this.ROUTES_TOKEN.REGISTRATION.REGISTRATION,
    this.ROUTES_TOKEN.RESET_PASSWORD.RESET_PASSWORD,
  ] as const;

  readonly isBaseHeader$$ = toSignal(
    this.router.events.pipe(
      filter((event): event is NavigationEnd => event instanceof NavigationEnd),
      map((event) => event.url.split('/').at(-1)),
      filter((url): url is string => !!url),
      map((url) =>
        this.routesWithBaseHeader.some((route) => url.includes(route)),
      ),
      distinctUntilChanged(),
    ),
  );
}
