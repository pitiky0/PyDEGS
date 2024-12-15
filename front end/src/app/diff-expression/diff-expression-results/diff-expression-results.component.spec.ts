import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DiffExpressionResultsComponent } from './diff-expression-results.component';

describe('DiffExpressionResultsComponent', () => {
  let component: DiffExpressionResultsComponent;
  let fixture: ComponentFixture<DiffExpressionResultsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [DiffExpressionResultsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DiffExpressionResultsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
