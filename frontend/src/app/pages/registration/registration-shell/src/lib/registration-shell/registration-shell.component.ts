import {
  ChangeDetectionStrategy,
  Component,
  computed,
  inject,
} from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import { NavigationEnd, Router, RouterOutlet } from '@angular/router';
import { ROUTES_TOKEN } from '@app/shared/app-config';
import { DotsStepperComponent } from '@app/ui/common/dots-stepper';
import { PanelWrapperComponent } from '@app/ui/common/panel-wrapper';
import { filter, map } from 'rxjs/operators';

@Component({
  selector: 'app-registration-shell',
  standalone: true,
  imports: [RouterOutlet, PanelWrapperComponent, DotsStepperComponent],
  templateUrl: './registration-shell.component.html',
  styleUrl: './registration-shell.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class RegistrationShellComponent {
  private readonly ROUTES_TOKEN = inject(ROUTES_TOKEN);

  private readonly router = inject(Router);

  private readonly routerUrl$$ = toSignal(
    this.router.events.pipe(
      filter((event): event is NavigationEnd => event instanceof NavigationEnd),
      map((event) => event.url.replace('/', '')),
    ),
    { initialValue: '' },
  );

  readonly activeStep$$ = computed(() => {
    const route = {
      [this.ROUTES_TOKEN.REGISTRATION.REGISTRATION]: 0,
      [this.ROUTES_TOKEN.REGISTRATION.CONFIRMATION_CODE]: 1,
      [this.ROUTES_TOKEN.REGISTRATION.CREATE_PASSWORD]: 2,
    };

    return route[<keyof typeof route>this.routerUrl$$()];
  });
}
