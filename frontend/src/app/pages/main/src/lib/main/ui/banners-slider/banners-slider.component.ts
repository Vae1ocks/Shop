import {
  ChangeDetectionStrategy,
  Component,
  CUSTOM_ELEMENTS_SCHEMA,
} from '@angular/core';
import { SwiperDirective } from '@app/shared/libs/directives/swiper.directive';
import { SvgIconComponent } from 'angular-svg-icon';
import { Navigation } from 'swiper/modules';
import { SwiperOptions } from 'swiper/types';

@Component({
  selector: 'app-banners-slider',
  standalone: true,
  imports: [SwiperDirective, SvgIconComponent],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
  templateUrl: './banners-slider.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
  host: {
    class: 'block w-full relative',
  },
})
export class BannersSliderComponent {
  readonly config: SwiperOptions = {
    slidesPerView: 1,
    rewind: true,
    modules: [Navigation],
    navigation: {
      prevEl: '.nav-prev',
      nextEl: '.nav-next',
    },
  };
}
