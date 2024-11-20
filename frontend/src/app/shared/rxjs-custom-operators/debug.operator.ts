/* eslint-disable @typescript-eslint/no-unused-expressions */
/* eslint-disable no-console */
import { isDevMode } from '@angular/core';
import { MonoTypeOperatorFunction } from 'rxjs';
import { tap } from 'rxjs/operators';

export function debug<T>(tag: string): MonoTypeOperatorFunction<T> {
  return tap({
    complete() {
      isDevMode() &&
        console.log(
          `%c[${tag}]: Complete`,
          'background: #069e27; color: #fff; padding: 3px; font-size: 11px;',
        );
    },
    error(error: unknown) {
      isDevMode() &&
        console.log(
          `%[${tag}: Error]`,
          'background: #f22c2c; color: #fff; padding: 3px; font-size: 11px;',
          error,
        );
    },
    next(value) {
      isDevMode() &&
        console.log(
          `%c[${tag}: Next]`,
          'background: #208ff7; color: #fff; padding: 3px; font-size: 11px;',
          value,
        );
    },
  });
}
