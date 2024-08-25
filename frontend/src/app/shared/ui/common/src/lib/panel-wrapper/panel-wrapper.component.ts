import { ChangeDetectionStrategy, Component } from '@angular/core';

@Component({
  selector: 'app-panel-wrapper',
  standalone: true,
  imports: [],
  templateUrl: './panel-wrapper.component.html',
  styleUrl: './panel-wrapper.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class PanelWrapperComponent {}
