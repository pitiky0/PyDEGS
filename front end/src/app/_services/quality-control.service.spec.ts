import { TestBed } from '@angular/core/testing';

import { QualityControlService } from './quality-control.service';

describe('QualityControlService', () => {
  let service: QualityControlService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(QualityControlService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
