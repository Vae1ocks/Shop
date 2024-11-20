import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RegistrationNewPasswordComponent } from './registration-new-password.component';

describe('RegistrationNewPasswordComponent', () => {
  let component: RegistrationNewPasswordComponent;
  let fixture: ComponentFixture<RegistrationNewPasswordComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RegistrationNewPasswordComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(RegistrationNewPasswordComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
