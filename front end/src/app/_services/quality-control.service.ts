import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class QualityControlService {
  private apiUrl = 'http://localhost:8000/quality-control/'; // FastAPI server URL

  constructor(private http: HttpClient) { }

  performQualityControl(filenames: string | string[], userId: string): Observable<any> {
    const params = new HttpParams().set('user_id', userId);
    const body = Array.isArray(filenames) ? filenames : filenames;  // Adapt body based on input type

    return this.http.post<any>(this.apiUrl, body, { params, observe: 'events', reportProgress: true }).pipe(
      catchError(error => {
        console.error('Error performing quality control:', error);
        throw error; // Rethrow to handle the error in the component
      })
    );
  }
}
