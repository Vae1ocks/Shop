import {
  booleanAttribute,
  ChangeDetectionStrategy,
  Component,
  inject,
  input,
} from '@angular/core';
import { RouterLink } from '@angular/router';
import { ROUTES_TOKEN } from '@app/shared/app-config';
import { ButtonComponent } from '@app/ui/common/button';

import { HeaderButtonComponent } from './ui/header-button';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [RouterLink, ButtonComponent, HeaderButtonComponent],
  templateUrl: './header.component.html',
  styleUrl: './header.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class HeaderComponent {
  readonly ROUTES_TOKEN = inject(ROUTES_TOKEN);

  readonly baseHeader = input(false, {
    transform: booleanAttribute,
  });
}
