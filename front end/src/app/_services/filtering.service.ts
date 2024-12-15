import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import {catchError} from "rxjs/operators";

@Injectable({
  providedIn: 'root'
})
export class FilteringService {
  private apiUrl = 'http://localhost:8000/filtering_fastq_files/'; // Replace with your actual backend URL

  constructor(private http: HttpClient) {}

  filterFastqFile(
    fileName: string | string[],
    userId: string,
    is_paired_end: boolean,
    truncateStartBases: number,
    truncateEndBases: number,
    leftAdapter: string,
    rightAdapter: string,
    minLength: number,
    nBases: number,
    complexity: number,
    isPairedEnd: boolean = false
  ): Observable<any> {
    const params = new HttpParams()
      .set('user_id', userId.toString())
      .set('is_paired_end', isPairedEnd.toString())
      .set('truncate_start_bases', truncateStartBases.toString())
      .set('truncate_end_bases', truncateEndBases.toString())
      .set('left_adapter', leftAdapter)
      .set('right_adapter', rightAdapter)
      .set('min_length', minLength.toString())
      .set('n_bases', nBases.toString())
      .set('complexity', complexity.toString());

    const body = Array.isArray(fileName) ? fileName : fileName;  // Adapt body based on input type

    return this.http.post<any>(`${this.apiUrl}`, body, { params }).pipe(
      catchError(error => {
        console.error('Error filtering FASTQ file:', error);
        throw error; // Rethrow to handle the error in the component
      })
    );
  }


  listFiles(bucketName: string): Observable<any> {
    const url = `http://localhost:8003/files/${bucketName}/list_files/`;
    return this.http.get<any>(url);
  }
}

