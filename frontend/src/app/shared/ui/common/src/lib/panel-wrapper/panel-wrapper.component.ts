import { ChangeDetectionStrategy, Component } from '@angular/core';

@Component({
  selector: 'app-panel-wrapper',
  standalone: true,
  imports: [],
  templateUrl: './panel-wrapper.component.html',
  styleUrl: './panel-wrapper.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
  host: {
    class: 'flex flex-col justify-between',
  },
})
export class PanelWrapperComponent {}
