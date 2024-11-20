import { ChangeDetectionStrategy, Component, input } from '@angular/core';
import { SvgIconComponent } from 'angular-svg-icon';

@Component({
  selector: 'app-header-button',
  standalone: true,
  imports: [SvgIconComponent],
  templateUrl: './header-button.component.html',
  styleUrl: './header-button.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
  host: { class: 'flex flex-col items-center justify-center' },
})
export class HeaderButtonComponent {
  text = input.required<string>();

  icon = input.required<string>();
}
