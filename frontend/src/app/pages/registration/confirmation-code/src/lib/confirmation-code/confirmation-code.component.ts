import { Location } from '@angular/common';
import {
  ChangeDetectionStrategy,
  Component,
  DestroyRef,
  inject,
  signal,
} from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Router } from '@angular/router';
import { ROUTE_TOKENS } from '@app/shared/app-config';
import { ButtonComponent } from '@app/ui/common/button';
import { ConfirmRegistrationService } from '@swagger/services/confirm-registration.service';
import { CodeInputModule } from 'angular-code-input';
import { timer } from 'rxjs';

@Component({
  selector: 'app-confirmation-code',
  standalone: true,
  imports: [CodeInputModule, ButtonComponent],
  templateUrl: './confirmation-code.component.html',
  styleUrl: './confirmation-code.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ConfirmationCodeComponent {
  private readonly ROUTE_TOKENS = ROUTE_TOKENS;

  private readonly location = inject(Location);

  private readonly confirmRegistrationService = inject(
    ConfirmRegistrationService,
  );

  private readonly destroyRef = inject(DestroyRef);

  private readonly router = inject(Router);

  readonly CODE_LENGTH = 6;

  private shortCode!: string;

  readonly loading$$ = signal<boolean>(false);

  onCodeChanged(value: string): void {
    const isDisabled = value.length !== this.CODE_LENGTH;
    this.isSubmitButtonDisabled$$.set(isDisabled);
    this.shortCode = value;
  }

  readonly isSubmitButtonDisabled$$ = signal<boolean>(true);

  readonly timer$ = timer(0, 1000);

  previousStep(): void {
    this.location.back();
  }

  submit(): void {
    this.loading$$.set(true);

    this.confirmRegistrationService
      .confirmRegistrationCreate$Json({
        body: { short_code: this.shortCode },
      })
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: () =>
          this.router.navigate([
            this.ROUTE_TOKENS.REGISTRATION.CREATE_PASSWORD,
          ]),
        complete: () => this.loading$$.set(false),
      });
  }
}
