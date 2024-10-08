import { DatePipe } from '@angular/common';
import {
  ChangeDetectionStrategy,
  Component,
  effect,
  input,
  output,
} from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import { BehaviorSubject, timer } from 'rxjs';
import { filter, map, switchMap, takeWhile, tap } from 'rxjs/operators';

@Component({
  changeDetection: ChangeDetectionStrategy.OnPush,
  selector: 'app-countdown',
  standalone: true,
  imports: [DatePipe],
  templateUrl: './countdown.component.html',
  styleUrl: './countdown.component.scss',
  host: {
    class: 'block w-full text-center',
  },
})
export class CountdownComponent {
  seconds = input.required<number>();

  start = input.required<boolean>();

  readonly isFinished = output<void>();

  private readonly startTimer = effect(() =>
    this.startSubject$.next(this.start()),
  );

  private readonly startSubject$ = new BehaviorSubject<boolean>(false);

  readonly timeRemaining$$ = toSignal(
    this.startSubject$.pipe(
      filter((v) => !!v),
      switchMap(() =>
        timer(0, 1000).pipe(
          map((n) => (this.seconds() - n) * 1000),
          tap((n) => {
            if (!n) this.isFinished.emit();
          }),
          takeWhile((n) => n >= 0),
          // finalize(() => this.isFinished.emit()),
        ),
      ),
    ),
  );
}
