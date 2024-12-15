import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FileFilteringDetailsComponent } from './file-filtering-details.component';

describe('FileFilteringDetailsComponent', () => {
  let component: FileFilteringDetailsComponent;
  let fixture: ComponentFixture<FileFilteringDetailsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [FileFilteringDetailsComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(FileFilteringDetailsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
