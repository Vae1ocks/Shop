import { ChangeDetectionStrategy, Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'setting-layout',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './setting.component.html',
  styleUrl: './setting.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SettingComponent {}
