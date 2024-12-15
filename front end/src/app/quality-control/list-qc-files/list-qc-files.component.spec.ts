import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ListQCFilesComponent } from './list-qc-files.component';

describe('ListQCFilesComponent', () => {
  let component: ListQCFilesComponent;
  let fixture: ComponentFixture<ListQCFilesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ListQCFilesComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ListQCFilesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
