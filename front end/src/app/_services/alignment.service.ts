import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import {catchError} from "rxjs/operators";

@Injectable({
  providedIn: 'root'
})
export class AlignmentService {
  private apiUrl = 'http://localhost:8000/alignment_fastq_files/'; // Replace with your actual API URL

  performAlignment(fastqFile: string, referenceFile: string, userId: string): Observable<any> {
    const params = new HttpParams()
      .set('reference_file', referenceFile)
      .set('is_paired',false)
      .set('user_id', userId.toString());

    const body = Array.isArray(fastqFile) ? fastqFile : fastqFile;  // Adapt body based on input type

    return this.http.post<any>(`${this.apiUrl}`, body, { params }).pipe(
      catchError(error => {
        console.error('Error aligning FASTQ file:', error);
        throw error; // Rethrow to handle the error in the component
      })
    );
  }

  constructor(private http: HttpClient) {}
}
