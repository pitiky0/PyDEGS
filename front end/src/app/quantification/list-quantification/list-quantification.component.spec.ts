import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ListQuantificationComponent } from './list-quantification.component';

describe('ListQuantificationComponent', () => {
  let component: ListQuantificationComponent;
  let fixture: ComponentFixture<ListQuantificationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ListQuantificationComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ListQuantificationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
