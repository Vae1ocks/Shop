import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ResetPasswordShellComponent } from './reset-password-shell.component';

describe('ResetPasswordShellComponent', () => {
  let component: ResetPasswordShellComponent;
  let fixture: ComponentFixture<ResetPasswordShellComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ResetPasswordShellComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(ResetPasswordShellComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
