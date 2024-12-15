
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class FileManagementService {
  private apiUrl = 'http://localhost:8003/files'; // Replace with your actual backend URL

  constructor(private http: HttpClient) {}

  uploadFile(bucketName: string, userId: string, file: File, folderName: string = ''): Observable<any> {
    const formData: FormData = new FormData();
    formData.append('file', file, file.name);
    const url = `${this.apiUrl}/${bucketName}/upload_file/?user_id=${userId}&folder_name=${folderName}`;
    return this.http.post(url, formData, {
      reportProgress: true,
      observe: 'events'
    });
  }

  listFiles(bucketName: string): Observable<any> {
    const url = `${this.apiUrl}/${bucketName}/list_files/`;
    return this.http.get(url);
  }

  getConditions(fileName: string): Observable<any> {
    const url = `${this.apiUrl}/metadata_columns/?file_name=${fileName}`;
    return this.http.get(url);
  }

  downloadFile(bucketName: string, fileName: string): Observable<Blob> {
    const url = `${this.apiUrl}/${bucketName}/download_file/?file_name=${fileName}`;
    return this.http.get(url, { responseType: 'blob' });
  }

  downloadFolder(bucketName: string, folderName: string): Observable<Blob> {
    const url = `${this.apiUrl}/${bucketName}/download_folder/?folder_name=${folderName}`;
    return this.http.get(url, { responseType: 'blob' });
  }

  getFileTags(bucketName: string, fileName: string): Observable<any> {
    const url = `${this.apiUrl}/${bucketName}/get_tags/?file_name=${fileName}`;
    return this.http.get(url);
  }

  addTagsToFile(bucketName: string, fileName: string, tags: { [key: string]: string }): Observable<any> {
    const url = `${this.apiUrl}/${bucketName}/add_tags/?file_name=${fileName}`;
    const body = { tags };
    return this.http.post(url, body);
  }

  getFileInfo(bucketName: string, fileName: string): Observable<any> {
    const url = `${this.apiUrl}/${bucketName}/get_file_info/?file_name=${fileName}`;
    return this.http.get(url);
  }

  deleteFile(bucketName: string, fileName: string): Observable<any> {
    const url = `${this.apiUrl}/${bucketName}/delete_file/?file_name=${fileName}`;
    return this.http.delete(url);
  }

  getTags(bucketName: string, fileName: string): Observable<any> {
    const url = `${this.apiUrl}/${bucketName}/get_tags/?file_name=${fileName}`;
    return this.http.get(url);
  }

  getTopReads(fileName: string): Observable<any> {
    const url = `${this.apiUrl}/get_top_reads/?file_name=${fileName}`;
    return this.http.get(url);
  }

  groupFiles(bucketName: string, groupName: string, files: string[]): Observable<any> {
    const url = `${this.apiUrl}/${bucketName}/${groupName}/group_files`;
    return this.http.post(url, files, {
      headers: { 'Content-Type': 'application/json' } // Ensure JSON content type
    });
  }


}
