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
  changeDetection: ChangeDetectionStrategy.OnPush,
  selector: 'app-reset-password-shell',
  standalone: true,
  imports: [RouterOutlet, PanelWrapperComponent, DotsStepperComponent],
  templateUrl: './reset-password-shell.component.html',
  styleUrl: './reset-password-shell.component.scss',
})
export class ResetPasswordShellComponent {
  private readonly ROUTE_TOKENS = ROUTE_TOKENS;

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
      [this.ROUTE_TOKENS.RESET_PASSWORD.RESET_PASSWORD]: 0,
      [this.ROUTE_TOKENS.RESET_PASSWORD.CONFIRMATION_CODE]: 1,
      [this.ROUTE_TOKENS.RESET_PASSWORD.CREATE_PASSWORD]: 2,
    };

    return route[<keyof typeof route>this.routerUrl$$()];
  });
}
