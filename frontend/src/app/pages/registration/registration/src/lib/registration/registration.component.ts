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
import { Router, RouterLink, RouterOutlet } from '@angular/router';
import { ROUTE_TOKENS } from '@app/shared/app-config';
import { FormGroupModel } from '@app/shared/forms';
import { ButtonComponent } from '@app/ui/common/button';
import { DotsStepperComponent } from '@app/ui/common/dots-stepper';
import { PanelWrapperComponent } from '@app/ui/common/panel-wrapper';
import { RegistrationRequest } from '@swagger/models';
import { RegistrationService } from '@swagger/services/registration.service';
import { debounceTime } from 'rxjs/operators';

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
export class RegistrationComponent implements OnInit {
  readonly ROUTE_TOKENS = ROUTE_TOKENS;

  readonly formBuilder = inject(FormBuilder);

  private readonly registrationService = inject(RegistrationService);

  private readonly destroyRef = inject(DestroyRef);

  private readonly router = inject(Router);

  readonly loading$$ = signal<boolean>(false);

  readonly showError$$ = signal<boolean>(false);

  readonly formGroup: FormGroupModel<Required<RegistrationRequest>> =
    this.formBuilder.group({
      email: ['', [Validators.required, Validators.email]],
      first_name: ['', Validators.minLength(2)],
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

    this.registrationService
      .registrationCreate$Json({
        body: <RegistrationRequest>this.formGroup.value,
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
