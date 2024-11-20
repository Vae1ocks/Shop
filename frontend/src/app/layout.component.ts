import { ChangeDetectionStrategy, Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { FooterComponent } from '@app/layout/footer';

@Component({
  selector: 'app-layout',
  standalone: true,
  imports: [RouterOutlet, FooterComponent],
  templateUrl: './layout.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
  host: { class: 'w-full h-full' },
})
export class LayoutComponent {}
