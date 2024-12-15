import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class DiffExpressionService {
  private apiUrl = 'http://localhost:8000/diff_expression_analyse/'; // Replace with your actual API URL

  constructor(private http: HttpClient) { }

  performDiffExpression(countsFile: string, metadata: string, condition: string, userId: string): Observable<any> {
    const params = new HttpParams()
      .set('counts_file', countsFile)
      .set('metadata', metadata)
      .set('condition', condition)
      .set('user_id', userId);

    return this.http.get<any>(this.apiUrl, { params }).pipe(
      catchError(error => {
        console.error('Error performing differential expression analysis:', error);
        throw error; // Rethrow to handle the error in the component
      })
    );
  }
}
