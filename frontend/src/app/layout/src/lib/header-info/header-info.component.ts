import { ChangeDetectionStrategy, Component } from '@angular/core';
import { SvgIconComponent } from 'angular-svg-icon';

@Component({
  selector: 'app-header-info',
  standalone: true,
  imports: [SvgIconComponent],
  templateUrl: './header-info.component.html',
  styleUrl: './header-info.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class HeaderInfoComponent {}
