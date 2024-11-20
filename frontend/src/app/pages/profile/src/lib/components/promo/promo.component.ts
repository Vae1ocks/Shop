import { ChangeDetectionStrategy, Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'promo-layout',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './promo.component.html',
  styleUrl: './promo.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class PromoComponent {}
