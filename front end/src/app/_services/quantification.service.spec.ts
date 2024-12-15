import { TestBed } from '@angular/core/testing';

import { QuantificationService } from './quantification.service';

describe('QuantificationService', () => {
  let service: QuantificationService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(QuantificationService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
