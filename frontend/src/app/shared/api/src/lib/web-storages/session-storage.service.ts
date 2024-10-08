import { Inject, Injectable } from '@angular/core';
import { WA_SESSION_STORAGE } from '@ng-web-apis/common';

@Injectable({ providedIn: 'root' })
export class SessionStorageService implements Storage {
  constructor(
    @Inject(WA_SESSION_STORAGE) private readonly sessionStorage: Storage,
  ) {}

  clear(): void {
    this.sessionStorage.clear();
  }

  getItem(key: string): null | string {
    return this.sessionStorage.getItem(key);
  }

  key(index: number): null | string {
    return this.sessionStorage.key(index);
  }

  removeItem(key: string): void {
    this.sessionStorage.removeItem(key);
  }

  setItem(key: string, value: string): void {
    this.sessionStorage.setItem(key, value);
  }

  get length(): number {
    return this.sessionStorage.length;
  }
}
