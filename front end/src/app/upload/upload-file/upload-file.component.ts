import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FileManagementService } from '../../_services/file-management.service';
import { AuthService } from '../../_services/auth.service';
import { HttpEventType, HttpResponse } from '@angular/common/http';

@Component({
  selector: 'app-upload-file',
  templateUrl: './upload-file.component.html',
  styleUrls: ['./upload-file.component.css']
})
export class UploadFileComponent {
  selectedFile: File | null = null;
  fileError: string | null = null;
  userId: string | null = null;
  uploadMessage: string | null = null;
  messageClass: string | null = null;
  uploadProgress: number = -1;
  successMessage: string = ""; // Add a property to store success message

  constructor(
    private fileManagementService: FileManagementService, 
    private authService: AuthService,
    private router: Router // Inject the Router service
  ) {
    this.userId = this.authService.getUserId();
  }

  onFileSelected(event: any): void {
    const file = event.target.files[0];
    this.resetState();
    if (file) {
      if (!file.name.endsWith('.fastq.gz')) {
        this.fileError = 'Invalid file format. Only .fastq.gz files are allowed.';
        this.selectedFile = null;
      } else {
        this.selectedFile = file;
      }
    }
  }

  onUpload(): void {
    if (this.selectedFile && this.userId) {
      this.uploadProgress = 0;
      this.fileManagementService.uploadFile('fastq-files', this.userId, this.selectedFile).subscribe(
        (event: any) => {
          if (event.type === HttpEventType.UploadProgress) {
            this.uploadProgress = Math.round((100 * event.loaded) / event.total);
          } else if (event instanceof HttpResponse) {
            this.uploadMessage = 'File uploaded successfully';
            this.messageClass = 'success';
            this.successMessage = `File uploaded successfully!`; // Set success message
            this.resetState();
            console.log('File uploaded successfully', event.body);
            this.router.navigate(['/list-files']); // Navigate to the list-files page
          }
        },
        (error) => {
          this.uploadMessage = 'File upload failed';
          this.messageClass = 'error';
          this.uploadProgress = -1;
          console.error('File upload failed', error);
        }
      );
    }
  }

  resetState(): void {
    this.uploadMessage = null;
    this.uploadProgress = -1;
    this.fileError = null;
  }
}
