import { Inject, Injectable } from '@angular/core';
import { WA_LOCAL_STORAGE } from '@ng-web-apis/common';

@Injectable({ providedIn: 'root' })
export class LocalStorageService implements Storage {
  constructor(
    @Inject(WA_LOCAL_STORAGE) private readonly localStorage: Storage,
  ) {}

  clear(): void {
    this.localStorage.clear();
  }

  getItem(key: string): null | string {
    return this.localStorage.getItem(key);
  }

  key(index: number): null | string {
    return this.localStorage.key(index);
  }

  removeItem(key: string): void {
    this.localStorage.removeItem(key);
  }

  setItem(key: string, value: string): void {
    this.localStorage.setItem(key, value);
  }

  get length(): number {
    return this.localStorage.length;
  }
}
