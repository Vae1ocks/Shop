import { ChangeDetectionStrategy, Component } from '@angular/core';
import { ButtonComponent } from '@app/ui/common/button';

import { HeaderButtonComponent } from './ui/header-button';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [ButtonComponent, HeaderButtonComponent],
  templateUrl: './header.component.html',
  styleUrl: './header.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class HeaderComponent {}
