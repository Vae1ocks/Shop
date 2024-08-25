import { ChangeDetectionStrategy, Component, input } from '@angular/core';

import { ButtonType } from './model';

@Component({
  selector: 'app-button',
  standalone: true,
  imports: [],
  templateUrl: './button.component.html',
  styleUrl: './button.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ButtonComponent {
  type = input<ButtonType>('button');

  loading = input<boolean>(false);

  disabled = input<boolean>(false);
}
