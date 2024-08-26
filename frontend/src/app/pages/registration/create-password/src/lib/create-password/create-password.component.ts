import { Component, DestroyRef, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { ButtonComponent } from '@app/ui/common/button';
import { fieldsMustMatch } from '@app/shared/forms';
import { takeUntilDestroyed, toSignal } from '@angular/core/rxjs-interop';
import { distinctUntilChanged, map } from 'rxjs/operators';
import { SetNewPasswordService } from '@swagger/services/set-new-password.service';
import { Router } from '@angular/router';
import { ROUTE_TOKENS } from '@app/shared/app-config';

@Component({
  selector: 'app-create-password',
  standalone: true,
  imports: [ReactiveFormsModule, ButtonComponent],
  templateUrl: './create-password.component.html',
  styleUrl: './create-password.component.scss',
})
export class CreatePasswordComponent {
  private readonly ROUTE_TOKENS = ROUTE_TOKENS;

  private readonly formBuilder = inject(FormBuilder);

  private readonly createPasswordService = inject(SetNewPasswordService);

  private readonly destroyRef = inject(DestroyRef);

  private readonly router = inject(Router);

  readonly formGroup = this.formBuilder.group(
    {
      password: ['', [Validators.required, Validators.minLength(8)]],
      confirmPassword: ['', Validators.required],
    },
    { validators: fieldsMustMatch('password', 'confirmPassword') },
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
    const password = this.formGroup.get('password')?.value;
    const confirmPassword = this.formGroup.get('confirmPassword')?.value;

    if (!password || !confirmPassword) return;

    this.loading$$.set(true);

    this.createPasswordService
      .setNewPasswordCreate$Json({
        body: {
          password,
          password2: confirmPassword,
        },
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
