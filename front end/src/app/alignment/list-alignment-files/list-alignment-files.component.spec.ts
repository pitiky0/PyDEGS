import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ListAlignmentFilesComponent } from './list-alignment-files.component';

describe('ListAlignmentFilesComponent', () => {
  let component: ListAlignmentFilesComponent;
  let fixture: ComponentFixture<ListAlignmentFilesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ListAlignmentFilesComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ListAlignmentFilesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
