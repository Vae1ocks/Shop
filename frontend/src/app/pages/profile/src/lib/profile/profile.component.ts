import { CommonModule } from '@angular/common';
import { ChangeDetectionStrategy, Component, ElementRef, inject, TemplateRef, ViewChild } from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import {
  NavigationEnd,
  Router,
  RouterLink,
  RouterLinkActive,
  RouterOutlet,
} from '@angular/router';
import { ROUTE_TOKENS } from '@app/shared/app-config';
import { filter, map } from 'rxjs/operators';
import { MatDialog, MatDialogRef } from '@angular/material/dialog';

@Component({
  changeDetection: ChangeDetectionStrategy.OnPush,
  selector: 'lib-profile',
  standalone: true,
  imports: [RouterOutlet, CommonModule, RouterLink, RouterLinkActive],
  templateUrl: './profile.component.html',
  styleUrl: './profile.component.scss',
})
export class ProfileComponent {
  private readonly ROUTE_TOKENS = ROUTE_TOKENS;

  private readonly activeRouteName: Record<string, string> = {
    [this.ROUTE_TOKENS.PROFILE.USER]: 'Профиль',
    [this.ROUTE_TOKENS.PROFILE.PROMO]: 'Промокоды',
    [this.ROUTE_TOKENS.PROFILE.REVIEWS]: 'Мои отзывы',
    [this.ROUTE_TOKENS.PROFILE.SETTING]: 'Настройки',
  };

  private readonly router = inject(Router);
  private readonly dialog = inject( MatDialog);
  @ViewChild('popup') popup!: TemplateRef<ElementRef>
  dialogRef: MatDialogRef<any> | null = null

  readonly activeUrl$$ = toSignal(
    this.router.events.pipe(
      filter((event): event is NavigationEnd => event instanceof NavigationEnd),
      map((event) => {
        const urlSegment = event.url.split('/').at(-1);
        return urlSegment ? this.activeRouteName[urlSegment] : '';
      }),
    ),
  );

  openPopup() {
  this.dialogRef = this.dialog.open(this.popup)
  }

  closePopup() {
    this.dialogRef?.close()
  }
}
