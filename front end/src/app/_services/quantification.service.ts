import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class QuantificationService {
  private apiUrl = 'http://localhost:8000/quantification_features'; // Corrected to match backend route

  constructor(private http: HttpClient) {}

  performQuantification(bamFile: string, annotationFile: string, userId: string): Observable<any> {
    const params = new HttpParams()
      .set('bam_file', bamFile)
      .set('annotation_file', annotationFile)
      .set('user_id', userId);

    return this.http.get<any>(this.apiUrl, { params }).pipe(
      catchError(error => {
        console.error('Error performing quantification:', error);
        throw error; // Rethrow to handle the error in the component
      })
    );
  }
}
