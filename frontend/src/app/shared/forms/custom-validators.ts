import { AbstractControl } from '@angular/forms';

export function fieldsMustMatch(
  controlName: string,
  matchingControlName: string,
) {
  return (group: AbstractControl) => {
    const control = group.get(controlName);
    const matchingControl = group.get(matchingControlName);

    if (!control || !matchingControl) return null;

    // eslint-disable-next-line @typescript-eslint/dot-notation
    if (matchingControl.errors && !matchingControl.errors['fieldsMustMatch'])
      return null;

    if (control.value !== matchingControl.value)
      matchingControl.setErrors({ fieldsMustMatch: true });
    else matchingControl.setErrors(null);

    return null;
  };
}
