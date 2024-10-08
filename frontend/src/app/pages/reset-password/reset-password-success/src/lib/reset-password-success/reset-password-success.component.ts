import { ChangeDetectionStrategy, Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import { ROUTE_TOKENS } from '@app/shared/app-config';
import { ButtonComponent } from '@app/ui/common/button';
import { PanelWrapperComponent } from '@app/ui/common/panel-wrapper';
import { SvgIconComponent } from 'angular-svg-icon';

@Component({
  changeDetection: ChangeDetectionStrategy.OnPush,
  selector: 'app-reset-password-success',
  standalone: true,
  imports: [
    RouterLink,
    ButtonComponent,
    SvgIconComponent,
    PanelWrapperComponent,
  ],
  templateUrl: './reset-password-success.component.html',
  styleUrl: './reset-password-success.component.scss',
})
export class ResetPasswordSuccessComponent {
  readonly ROUTE_TOKENS = ROUTE_TOKENS;
}
