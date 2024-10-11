import { ChangeDetectionStrategy, Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { HeaderComponent } from '@app/layout/header';
import { HeaderInfoComponent } from '@app/layout/header-info';
import { SvgIconComponent } from 'angular-svg-icon';

@Component({
  standalone: true,
  imports: [
    RouterOutlet,
    SvgIconComponent,
    HeaderInfoComponent,
    HeaderComponent,
  ],
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class AppComponent {}
