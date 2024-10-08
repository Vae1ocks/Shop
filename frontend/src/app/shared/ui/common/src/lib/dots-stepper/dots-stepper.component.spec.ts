import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DotsStepperComponent } from './dots-stepper.component';

describe('DotsStepperComponent', () => {
  let component: DotsStepperComponent;
  let fixture: ComponentFixture<DotsStepperComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DotsStepperComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(DotsStepperComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
