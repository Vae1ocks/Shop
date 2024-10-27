import {
  ChangeDetectionStrategy,
  Component,
  DestroyRef,
  inject,
  OnInit,
  signal,
} from '@angular/core';
import { takeUntilDestroyed, toSignal } from '@angular/core/rxjs-interop';
import {
  NonNullableFormBuilder,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { ROUTES_TOKEN } from '@app/shared/app-config';
import { FormGroupModelNonNullable } from '@app/shared/forms';
import { debug } from '@app/shared/rxjs-custom-operators';
import { ButtonComponent } from '@app/ui/common/button';
import { PanelWrapperComponent } from '@app/ui/common/panel-wrapper';
import { LoginRequest } from '@swagger/models';
import { LoginService } from '@swagger/services/login.service';
import { SvgIconComponent } from 'angular-svg-icon';
import { debounceTime } from 'rxjs/operators';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    ReactiveFormsModule,
    RouterLink,
    PanelWrapperComponent,
    ButtonComponent,
    SvgIconComponent,
  ],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class LoginComponent implements OnInit {
  readonly ROUTES_TOKEN = inject(ROUTES_TOKEN);

  readonly formBuilder = inject(NonNullableFormBuilder);

  private readonly destroyRef = inject(DestroyRef);

  private readonly loginService = inject(LoginService);

  private readonly router = inject(Router);

  readonly loading$$ = signal<boolean>(false);

  readonly route = inject(ActivatedRoute);

  readonly data = toSignal(this.route.data.pipe(debug('data')));

  readonly formGroup: FormGroupModelNonNullable<LoginRequest> =
    this.formBuilder.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required],
    });

  readonly showError$$ = signal<boolean>(false);

  showPassword = false;

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
    this.showError$$.set(false);

    this.loginService
      .loginCreate$Json({
        body: {
          email: this.formGroup.get('email')?.value ?? '',
          password: this.formGroup.get('password')?.value ?? '',
        },
      })
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: () => {
          this.router.navigate([this.ROUTES_TOKEN.MAIN]);
        },
        error: (error: unknown) => {
          this.showError$$.set(true);
          this.loading$$.set(false);
          console.error(error);
        },
        complete: () => this.loading$$.set(false),
      });
  }
}
