import { Component, OnInit } from '@angular/core';
import { QuantificationService } from '../_services/quantification.service';
import { FileManagementService } from '../_services/file-management.service';
import { AuthService } from '../_services/auth.service';
import { HttpClient, HttpResponse, HttpEventType } from '@angular/common/http';
import { Router } from '@angular/router';
import { saveAs } from 'file-saver';
import { Observable } from 'rxjs';

interface BamFile {
  file_name: string;
}

interface AnnotationFile {
  file_name: string;
}

interface QuantificationResult {
  file_name: string;
  report_url: string; // Assuming you have a URL to download the quantification report
}

@Component({
  selector: 'app-quantification',
  templateUrl: './quantification.component.html',
  styleUrls: ['./quantification.component.css']
})
export class QuantificationComponent implements OnInit {
  bamFiles: BamFile[] = [];
  annotationFiles: AnnotationFile[] = [];
  selectedBamFile: string = '';
  selectedAnnotationFile: string = '';
  userId: string | null = null;
  isLoading: boolean = false;
  errorMessage: string = '';
  message: string = '';
  progress: number = 0;
  showAnnotationModal: boolean = false;
  selectedFileToUpload: File | null = null;

  constructor(
    private quantificationService: QuantificationService,
    private fileManagementService: FileManagementService,
    private authService: AuthService,
    private http: HttpClient,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.userId = this.authService.getUserId() || '0';
    this.fetchBamFiles();
    this.fetchAnnotationFiles(); // Fetch initially
  }

  fetchBamFiles() {
    this.fileManagementService.listFiles('alignment-files').subscribe(
      (response) => {
        this.bamFiles = response.files.map((file: any) => ({ file_name: file.file_name }));
      },
      (error) => {
        console.error('Failed to list BAM files', error);
      }
    );
  }

  fetchAnnotationFiles() {
    this.fileManagementService.listFiles('gtf-gff-files').subscribe(
      (response) => {
        this.annotationFiles = response.files.map((file: any) => ({ file_name: file.file_name }));
      },
      (error) => {
        if (error.status === 404) {
          this.errorMessage = 'No annotation files found.';
          console.error('Failed to list annotation files:', error);
        } else {
          console.error('Failed to list annotation files:', error);
        }
      }
    );
  }

  openAnnotationModal(fileName: string) {
    this.selectedBamFile = fileName;
    // Fetch annotation files when the modal opens
    this.fetchAnnotationFiles();
    this.showAnnotationModal = true;
  }

  closeAnnotationModal() {
    this.showAnnotationModal = false;
    this.selectedAnnotationFile = '';
    this.selectedFileToUpload = null;
  }

  onFileSelected(event: any) {
    this.selectedFileToUpload = event.target.files[0];
  }

  uploadSelectedFile() {
    if (this.selectedFileToUpload && this.userId) {
      this.uploadFile(this.selectedFileToUpload).subscribe(
        (response) => {
          this.selectedAnnotationFile = response.file_name;
          this.showSuccessMessage('File uploaded successfully');
          this.fetchAnnotationFiles();
        },
        (error) => {
          this.handleError('File upload failed. Please try again.', error);
        }
      );
    }
  }

  uploadFile(file: File): Observable<any> {
    return this.fileManagementService.uploadFile('gtf-gff-files', this.userId!.toString(), file);
  }

  performQuantification() {
    if (this.userId && (this.selectedAnnotationFile || this.selectedFileToUpload)) {
      this.startLoading();
      const annotationFile = this.selectedAnnotationFile || this.selectedFileToUpload?.name;

      if (annotationFile) {
        this.quantificationService.performQuantification(this.selectedBamFile, annotationFile, this.userId)
          .subscribe(
            (response) => {
              this.showSuccessMessage(response.message || 'Quantification started successfully!');
              this.stopLoading();
              this.closeAnnotationModal();
            },
            (error) => {
              this.handleError('An error occurred during quantification. Please try again.', error);
            }
          );
      } else {
        this.errorMessage = 'Please select or upload an annotation file.';
      }
    } else {
      this.errorMessage = 'Please select a BAM file and an annotation file.';
    }
  }

  private startLoading() {
    this.isLoading = true;
    this.clearMessages();
  }

  private stopLoading() {
    this.isLoading = false;
  }

  private clearMessages() {
    this.errorMessage = '';
    this.message = '';
  }

  private handleError(message: string, error: any) {
    this.errorMessage = message;
    console.error(message, error);
    this.stopLoading();
  }

  private showSuccessMessage(message: string) {
    this.message = message;
  }
}
