import {
  ChangeDetectionStrategy,
  Component,
  DestroyRef,
  inject,
  signal,
} from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Router } from '@angular/router';
import { SessionStorageService } from '@app/shared/api';
import { APP_CONFIG, ROUTES_TOKEN } from '@app/shared/app-config';
import { ButtonComponent } from '@app/ui/common/button';
import { CountdownComponent } from '@app/ui/common/countdown';
import { ConfirmRegistrationService } from '@swagger/services/confirm-registration.service';
import { ResetPasswordService } from '@swagger/services/reset-password.service';
import { CodeInputModule } from 'angular-code-input';

@Component({
  changeDetection: ChangeDetectionStrategy.OnPush,
  selector: 'app-reset-password-code',
  standalone: true,
  imports: [CodeInputModule, ButtonComponent, CountdownComponent],
  templateUrl: './reset-password-code.component.html',
  styleUrl: './reset-password-code.component.scss',
})
export class ResetPasswordCodeComponent {
  private readonly APP_CONFIG = inject(APP_CONFIG);

  private readonly ROUTES_TOKEN = inject(ROUTES_TOKEN);

  private readonly sessionStorage = inject(SessionStorageService);

  private readonly confirmRegistrationService = inject(
    ConfirmRegistrationService,
  );

  private readonly resetPasswordService = inject(ResetPasswordService);

  private readonly destroyRef = inject(DestroyRef);

  private readonly router = inject(Router);

  readonly CODE_LENGTH = 6;

  readonly TIMER_INTERVAL = 300;

  private shortCode!: string;

  readonly loading$$ = signal<boolean>(false);

  readonly showError$$ = signal<boolean>(false);

  readonly isSubmitButtonDisabled$$ = signal<boolean>(true);

  readonly startTimer$$ = signal<boolean>(true);

  readonly isTimerFinished$$ = signal<boolean>(false);

  onCodeChanged(value: string): void {
    this.showError$$.set(false);
    const isDisabled = value.length !== this.CODE_LENGTH;
    this.isSubmitButtonDisabled$$.set(isDisabled);
    this.shortCode = value;
  }

  previousStep(): void {
    this.router.navigate([this.ROUTES_TOKEN.RESET_PASSWORD.RESET_PASSWORD]);
  }

  timerFinished(): void {
    this.isTimerFinished$$.set(true);
  }

  submit(): void {
    this.loading$$.set(true);

    this.confirmRegistrationService
      .confirmRegistrationCreate$Json({
        body: { short_code: this.shortCode },
      })
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: () => {
          this.router.navigate([
            this.ROUTES_TOKEN.REGISTRATION.CREATE_PASSWORD,
          ]);
        },
        error: (error: unknown) => {
          this.showError$$.set(true);
          this.loading$$.set(false);
          console.error(error);
        },
        complete: () => this.loading$$.set(false),
      });
  }

  resendCode(): void {
    const savedFormValue = this.sessionStorage.getItem(
      this.APP_CONFIG.RESET_PASSWORD_FORM_STORAGE_KEY,
    );

    if (!savedFormValue) return;

    this.resetPasswordService
      .resetPasswordSendMailCreate$Json({
        body: JSON.parse(savedFormValue),
      })
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: () => {
          this.isTimerFinished$$.set(false);
          this.startTimer$$.set(true);
        },
      });
  }
}
