import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RegistrationCodeComponent } from './registration-code.component';

describe('RegistrationCodeComponent', () => {
  let component: RegistrationCodeComponent;
  let fixture: ComponentFixture<RegistrationCodeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RegistrationCodeComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(RegistrationCodeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
