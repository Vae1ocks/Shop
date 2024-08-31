import {
  ChangeDetectionStrategy,
  Component,
  DestroyRef,
  inject,
  signal,
} from '@angular/core';
import { takeUntilDestroyed, toSignal } from '@angular/core/rxjs-interop';
import {
  NonNullableFormBuilder,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { Router } from '@angular/router';
import { ROUTE_TOKENS } from '@app/shared/app-config';
import { fieldsMustMatch, FormGroupModelNonNullable } from '@app/shared/forms';
import { ButtonComponent } from '@app/ui/common/button';
import { SetNewPasswordRequest } from '@swagger/models';
import { SetNewPasswordService } from '@swagger/services/set-new-password.service';
import { distinctUntilChanged, map } from 'rxjs/operators';

@Component({
  changeDetection: ChangeDetectionStrategy.OnPush,
  selector: 'app-reset-password-new-password',
  standalone: true,
  imports: [ReactiveFormsModule, ButtonComponent],
  templateUrl: './reset-password-new-password.component.html',
  styleUrl: './reset-password-new-password.component.scss',
})
export class ResetPasswordNewPasswordComponent {
  private readonly ROUTE_TOKENS = ROUTE_TOKENS;

  private readonly formBuilder = inject(NonNullableFormBuilder);

  private readonly createPasswordService = inject(SetNewPasswordService);

  private readonly destroyRef = inject(DestroyRef);

  private readonly router = inject(Router);

  readonly formGroup: FormGroupModelNonNullable<SetNewPasswordRequest> =
    this.formBuilder.group(
      {
        password: ['', [Validators.required, Validators.minLength(8)]],
        password2: ['', Validators.required],
      },
      { validators: fieldsMustMatch('password', 'password2') },
    );

  readonly loading$$ = signal<boolean>(false);

  readonly showError$$ = signal<boolean>(false);

  readonly isButtonDisabled$$ = toSignal(
    this.formGroup.statusChanges.pipe(
      map((status) => status !== 'VALID'),
      distinctUntilChanged(),
    ),
    {
      initialValue: true,
    },
  );

  submit(): void {
    if (this.formGroup.invalid) return;

    this.loading$$.set(true);

    this.createPasswordService
      .setNewPasswordCreate$Json({
        body: <SetNewPasswordRequest>this.formGroup.value,
      })
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: () =>
          this.router.navigate([
            this.ROUTE_TOKENS.REGISTRATION.REGISTRATION_SUCCESS,
          ]),
        error: (error: unknown) => {
          this.loading$$.set(false);
          this.showError$$.set(true);
          console.error(error);
        },
        complete: () => this.loading$$.set(false),
      });
  }
}
