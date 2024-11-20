import { ChangeDetectionStrategy, Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import { ROUTE_TOKENS } from '@app/shared/app-config';
import { ButtonComponent } from '@app/ui/common/button';
import { PanelWrapperComponent } from '@app/ui/common/panel-wrapper';
import { SvgIconComponent } from 'angular-svg-icon';

@Component({
  selector: 'app-registration-success',
  standalone: true,
  imports: [
    RouterLink,
    ButtonComponent,
    SvgIconComponent,
    PanelWrapperComponent,
  ],
  templateUrl: './registration-success.component.html',
  styleUrl: './registration-success.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class RegistrationSuccessComponent {
  readonly ROUTE_TOKENS = ROUTE_TOKENS;
}
