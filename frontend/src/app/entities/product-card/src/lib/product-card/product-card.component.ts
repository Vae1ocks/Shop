import { ChangeDetectionStrategy, Component } from '@angular/core';
import { ButtonComponent } from '@app/ui/common/button';
import { StarRatingComponent } from '@app/ui/common/star-rating';

@Component({
  changeDetection: ChangeDetectionStrategy.OnPush,
  selector: 'app-product-card',
  standalone: true,
  imports: [StarRatingComponent, ButtonComponent],
  templateUrl: './product-card.component.html',
  styleUrl: './product-card.component.css',
})
export class ProductCardComponent {}
