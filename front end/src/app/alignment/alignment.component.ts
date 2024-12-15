import { Component, OnInit } from '@angular/core';
import { AlignmentService } from '../_services/alignment.service';
import { AuthService } from '../_services/auth.service';
import { FileManagementService } from '../_services/file-management.service';
import { Observable } from 'rxjs';
import { forkJoin } from 'rxjs';

interface FastqFile {
  file_name: string;
}

@Component({
  selector: 'app-alignment',
  templateUrl: './alignment.component.html',
  styleUrls: ['./alignment.component.css']
})
export class AlignmentComponent implements OnInit {
  fastqFiles: FastqFile[] = [];
  referenceFiles: FastqFile[] = [];
  selectedFastqFile: string = '';
  selectedReferenceFile: string = '';
  selectedFileToUpload: File | null = null;
  userId: string | null = null;
  isLoading: boolean = false;
  errorMessage: string = '';
  message: string = '';
  showReferenceModal: boolean = false;

  constructor(
    private alignmentService: AlignmentService,
    private authService: AuthService,
    private fileManagementService: FileManagementService
  ) {}

  ngOnInit(): void {
    this.userId = this.authService.getUserId() || '0';
    this.fetchFastqFiles();
  }


fetchFastqFiles() {
  const fastqFiles$ = this.fileManagementService.listFiles('fastq-files');
  const filteredFastqFiles$ = this.fileManagementService.listFiles('filtered-fastq-files');

  forkJoin([fastqFiles$, filteredFastqFiles$]).subscribe(
    ([fastqResponse, filteredFastqResponse]) => {
      this.fastqFiles = [
        ...fastqResponse.files
          .filter((file: any) => file.file_name.includes('.fastq'))
          .map((file: any) => ({ file_name: file.file_name })),
        ...filteredFastqResponse.files
          .filter((file: any) => file.file_name.includes('.fastq'))
          .map((file: any) => ({ file_name: file.file_name }))
      ];
    },
    (error) => {
      this.handleError('Failed to list FASTQ files', error);
    }
  );
}


fetchReferenceFiles() {
    this.fileManagementService.listFiles('reference-genomes-files').subscribe(
      (response) => {
        this.referenceFiles = response.files.map((file: any) => ({ file_name: file.file_name }));
      },
      (error) => {
        this.handleError('Failed to list reference genome files', error);
      }
    );
  }

  openReferenceModal(fileName: string) {
    this.selectedFastqFile = fileName;
    this.fetchReferenceFiles();
    this.showReferenceModal = true;
  }

  closeReferenceModal() {
    this.showReferenceModal = false;
    this.selectedReferenceFile = '';
    this.selectedFileToUpload = null;
  }

  onFileSelected(event: any) {
    this.selectedFileToUpload = event.target.files[0];
  }

  uploadSelectedFile() {
    if (this.selectedFileToUpload && this.userId) {
      this.uploadFile(this.selectedFileToUpload).subscribe(
        (response) => {
          this.selectedReferenceFile = response.file_name;
          this.showSuccessMessage('File uploaded successfully');
          this.fetchReferenceFiles();
        },
        (error) => {
          this.handleError('File upload failed. Please try again.', error);
        }
      );
    }
  }

  uploadFile(file: File): Observable<any> {
    return this.fileManagementService.uploadFile('reference-genomes-files', this.userId!.toString(), file);
  }

  performAlignment() {
    if (this.userId && this.selectedFastqFile && this.selectedReferenceFile) {
      this.startLoading();
      this.alignmentService.performAlignment(this.selectedFastqFile, this.selectedReferenceFile, this.userId)
        .subscribe(
          (response) => {
            this.showSuccessMessage(response.message || 'Alignment started successfully!');
            this.stopLoading();
            this.closeReferenceModal();
          },
          (error) => {
            this.handleError('An error occurred during alignment. Please try again.', error);
          }
        );
    } else {
      this.errorMessage = 'Please select both a FASTQ file and a reference genome file.';
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
