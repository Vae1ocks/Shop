import {
  ChangeDetectionStrategy,
  Component,
  computed,
  inject,
} from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import { NavigationEnd, Router, RouterOutlet } from '@angular/router';
import { ROUTE_TOKENS } from '@app/shared/app-config';
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
  private readonly ROUTE_TOKENS = ROUTE_TOKENS;

  private readonly router = inject(Router);

  private readonly routerUrl$$ = toSignal(
    this.router.events.pipe(
      filter((event): event is NavigationEnd => event instanceof NavigationEnd),
      map((event) => event.url.replace('/', '')),
    ),
  );

  readonly activeStep$$ = computed(() => {
    switch (this.routerUrl$$()) {
      case this.ROUTE_TOKENS.REGISTRATION.REGISTRATION:
        return 0;
      case this.ROUTE_TOKENS.REGISTRATION.CONFIRMATION_CODE:
        return 1;
      case this.ROUTE_TOKENS.REGISTRATION.CREATE_PASSWORD:
        return 2;
      default:
        return 0;
    }
  });
}
