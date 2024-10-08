import {
  ChangeDetectionStrategy,
  Component,
  CUSTOM_ELEMENTS_SCHEMA,
} from '@angular/core';
import { SwiperOptions } from 'swiper/types';
import { SwiperDirective } from '@app/shared/libs/src/lib/directives/swiper.directive';

@Component({
  selector: 'app-banners-slider',
  standalone: true,
  imports: [SwiperDirective],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
  templateUrl: './banners-slider.component.html',
  styleUrl: './banners-slider.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
  host: {
    class: 'block w-full',
  },
})
export class BannersSliderComponent {
  readonly config: SwiperOptions = {
    slidesPerView: 1,
    rewind: true,
  };
}
