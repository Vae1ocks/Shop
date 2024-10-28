import { ChangeDetectionStrategy, Component } from '@angular/core';
import { ProductCardComponent } from '@app/entities/product-card';

import { BannersSliderComponent } from './ui/banners-slider';

@Component({
  selector: 'app-main',
  standalone: true,
  imports: [BannersSliderComponent, ProductCardComponent],
  templateUrl: './main.component.html',
   changeDetection: ChangeDetectionStrategy.OnPush,
})
export class MainComponent {}
