import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ListFilteringFilesComponent } from './list-filtering-files.component';

describe('ListFilteringFilesComponent', () => {
  let component: ListFilteringFilesComponent;
  let fixture: ComponentFixture<ListFilteringFilesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ListFilteringFilesComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ListFilteringFilesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
