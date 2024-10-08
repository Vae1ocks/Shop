import {
  ChangeDetectionStrategy,
  Component,
  DestroyRef,
  inject,
  OnInit,
  signal,
} from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { ROUTE_TOKENS } from '@app/shared/app-config';
import { FormGroupModel } from '@app/shared/forms';
import { ButtonComponent } from '@app/ui/common/button';
import { ResetPasswordRequest } from '@swagger/models';
import { ResetPasswordService } from '@swagger/services/reset-password.service';
import { debounceTime } from 'rxjs/operators';

@Component({
  changeDetection: ChangeDetectionStrategy.OnPush,
  selector: 'app-reset-password',
  standalone: true,
  imports: [ReactiveFormsModule, ButtonComponent],
  templateUrl: './reset-password.component.html',
  styleUrl: './reset-password.component.scss',
})
export class ResetPasswordComponent implements OnInit {
  readonly ROUTE_TOKENS = ROUTE_TOKENS;

  readonly formBuilder = inject(FormBuilder);

  private readonly destroyRef = inject(DestroyRef);

  private readonly router = inject(Router);

  readonly loading$$ = signal<boolean>(false);

  readonly showError$$ = signal<boolean>(false);

  private readonly resetPasswordService = inject(ResetPasswordService);

  readonly formGroup: FormGroupModel<ResetPasswordRequest> =
    this.formBuilder.group({
      email: ['', [Validators.required, Validators.email]],
    });

  ngOnInit(): void {
    this.formGroup.valueChanges
      .pipe(debounceTime(300), takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: () => this.showError$$.set(false),
      });
  }

  submit(): void {
    this.formGroup.markAllAsTouched();
    if (this.formGroup.invalid) return;

    this.loading$$.set(true);

    this.resetPasswordService
      .resetPasswordSendMailCreate$Json({
        body: <ResetPasswordRequest>this.formGroup.value,
      })
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: () =>
          this.router.navigate([
            this.ROUTE_TOKENS.RESET_PASSWORD.CONFIRMATION_CODE,
          ]),
        error: (error: unknown) => {
          this.showError$$.set(true);
          this.loading$$.set(false);
          console.error(error);
        },
        complete: () => this.loading$$.set(false),
      });
  }
}
