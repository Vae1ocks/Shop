import {
  ChangeDetectionStrategy,
  Component,
  DestroyRef,
  inject,
  signal,
} from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import {
  NonNullableFormBuilder,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { Router, RouterLink, RouterOutlet } from '@angular/router';
import { ROUTE_TOKENS } from '@app/shared/app-config';
import { ButtonComponent } from '@app/ui/common/button';
import { DotsStepperComponent } from '@app/ui/common/dots-stepper';
import { PanelWrapperComponent } from '@app/ui/common/panel-wrapper';
import { RegistrationService } from '@swagger/services/registration.service';

@Component({
  selector: 'app-registration',
  standalone: true,
  imports: [
    RouterOutlet,
    RouterLink,
    ReactiveFormsModule,
    PanelWrapperComponent,
    ButtonComponent,
    DotsStepperComponent,
  ],
  templateUrl: './registration.component.html',
  styleUrl: './registration.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class RegistrationComponent {
  readonly ROUTE_TOKENS = ROUTE_TOKENS;

  readonly formBuilder = inject(NonNullableFormBuilder);

  private readonly registrationService = inject(RegistrationService);

  private readonly destroyRef = inject(DestroyRef);

  private readonly router = inject(Router);

  readonly loading$$ = signal<boolean>(false);

  readonly showError$$ = signal<boolean>(false);

  readonly formGroup = this.formBuilder.group({
    email: ['', [Validators.required, Validators.email]],
    name: [''],
  });

  submit(): void {
    this.formGroup.markAllAsTouched();
    if (this.formGroup.invalid) return;

    this.loading$$.set(true);

    this.registrationService
      .registrationCreate$Json({
        body: {
          email: this.formGroup.get('email')?.value ?? '',
          first_name: this.formGroup.get('name')?.value ?? '',
        },
      })
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: () =>
          this.router.navigate([
            this.ROUTE_TOKENS.REGISTRATION.CONFIRMATION_CODE,
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
