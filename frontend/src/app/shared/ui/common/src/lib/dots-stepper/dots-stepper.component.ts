import {
  ChangeDetectionStrategy,
  Component,
  computed,
  input,
  numberAttribute,
} from '@angular/core';

@Component({
  selector: 'app-dots-stepper',
  standalone: true,
  imports: [],
  templateUrl: './dots-stepper.component.html',
  styleUrl: './dots-stepper.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class DotsStepperComponent {
  stepsAmount = input.required({ transform: numberAttribute });

  activeStep = input<number>(0);

  readonly steps = computed(() => Array.from({ length: this.stepsAmount() }));
}
