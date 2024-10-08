import { ChangeDetectionStrategy, Component } from '@angular/core';

import { BannersSliderComponent } from './ui/banners-slider';

@Component({
  selector: 'app-main',
  standalone: true,
  imports: [BannersSliderComponent],
  templateUrl: './main.component.html',
  styleUrl: './main.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class MainComponent {}
