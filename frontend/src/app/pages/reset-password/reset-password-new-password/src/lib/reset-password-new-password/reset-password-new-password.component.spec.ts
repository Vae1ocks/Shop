import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ResetPasswordNewPasswordComponent } from './reset-password-new-password.component';

describe('ResetPasswordNewPasswordComponent', () => {
  let component: ResetPasswordNewPasswordComponent;
  let fixture: ComponentFixture<ResetPasswordNewPasswordComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ResetPasswordNewPasswordComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(ResetPasswordNewPasswordComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
