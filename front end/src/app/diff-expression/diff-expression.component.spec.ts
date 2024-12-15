import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DiffExpressionComponent } from './diff-expression.component';

describe('DiffExpressionComponent', () => {
  let component: DiffExpressionComponent;
  let fixture: ComponentFixture<DiffExpressionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [DiffExpressionComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(DiffExpressionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
