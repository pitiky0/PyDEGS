import { TestBed } from '@angular/core/testing';

import { DiffExpressionService } from './diff-expression.service';

describe('DiffExpressionService', () => {
  let service: DiffExpressionService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(DiffExpressionService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
