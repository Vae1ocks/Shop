import { FormControl, FormGroup } from '@angular/forms';

export type FormGroupModelNonNullable<T> = FormGroup<{
  [K in keyof T]: FormControl<T[K]>;
}>;

export type FormGroupModel<T> = FormGroup<{
  [K in keyof T]: FormControl<T[K] | null>;
}>;
