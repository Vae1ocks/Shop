import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RegistrationShellComponent } from './registration-shell.component';

describe('RegistrationShellComponent', () => {
  let component: RegistrationShellComponent;
  let fixture: ComponentFixture<RegistrationShellComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RegistrationShellComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(RegistrationShellComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
