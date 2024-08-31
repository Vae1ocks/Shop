import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ResetPasswordCodeComponent } from './reset-password-code.component';

describe('ResetPasswordCodeComponent', () => {
  let component: ResetPasswordCodeComponent;
  let fixture: ComponentFixture<ResetPasswordCodeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ResetPasswordCodeComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(ResetPasswordCodeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
