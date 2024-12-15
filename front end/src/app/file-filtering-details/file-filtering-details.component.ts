import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { FileManagementService } from '../_services/file-management.service';
import { QualityControlService } from '../_services/quality-control.service';
import { FilteringService } from '../_services/filtering.service';
import { AlignmentService } from '../_services/alignment.service';
import { AuthService } from '../_services/auth.service';
import { HttpEventType, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-file-filtering-details',
  templateUrl: './file-filtering-details.component.html',
  styleUrls: ['./file-filtering-details.component.css']
})
export class FileFilteringDetailsComponent implements OnInit {
  fileName: string = '';
  fileInfo: any;
  isLoading: boolean = false;
  errorMessage: string = '';
  message: string = '';
  progress: number = 0;
  selectedFile: string = '';
  truncateStartBases: number = 0;
  truncateEndBases: number = 0;
  leftAdapter: string = '';
  rightAdapter: string = '';
  minLength: number = 0;
  nBases: number = 0;
  complexity: number = 0;
  showForm: boolean = false;
  referenceFiles: any[] = [];
  selectedReferenceFile: string = '';
  selectedFileToUpload: File | null = null;
  showReferenceModal: boolean = false;

  activeTab: string = 'Analyze';

  constructor(
    private route: ActivatedRoute,
    private fileManagementService: FileManagementService,
    private qualityControlService: QualityControlService,
    private filteringService: FilteringService,
    private alignmentService: AlignmentService,
    private authService: AuthService
  ) {}

  ngOnInit(): void {
    this.fileName = this.route.snapshot.paramMap.get('fileName') || '';
    this.getFileInfo();
  }

  setActiveTab(tabName: string): void {
    this.activeTab = tabName;
  }

  getFileInfo(): void {
    this.isLoading = true;
    this.fileManagementService.getFileInfo('filtered-fastq-files', this.fileName).subscribe(
      (response) => {
        this.fileInfo = response;
        this.isLoading = false;
      },
      (error) => {
        this.errorMessage = 'Failed to get file info';
        this.isLoading = false;
        console.error('Failed to get file info', error);
      }
    );
  }

  performQualityControl(fileName: string): void {
    const userId = this.authService.getUserId() || '0';
    if (userId) {
      this.isLoading = true;
      this.errorMessage = '';
      this.progress = 0;

      this.qualityControlService.performQualityControl(fileName, userId).subscribe(
        (event) => {
          if (event.type === HttpEventType.UploadProgress) {
            this.progress = Math.round((100 * event.loaded) / event.total);
          } else if (event instanceof HttpResponse) {
            this.message = event.body.message || 'Quality Control Successful!';
            this.isLoading = false;
            this.progress = 100;
          }
        },
        (error) => {
          this.isLoading = false;
          this.errorMessage = 'An error occurred during quality control. Please try again.';
          this.progress = 0;
          console.error('Error performing quality control:', error);
        }
      );
    } else {
      this.errorMessage = 'Please log in to perform quality control.';
    }
  }

  toggleForm(fileName: string) {
    if (this.selectedFile === fileName && this.showForm) {
      this.closeForm();
    } else {
      this.selectedFile = fileName;
      this.showForm = true;
    }
    this.errorMessage = '';
    this.message = '';
  }

  closeForm() {
    this.showForm = false;
    this.selectedFile = '';
  }

  isFormValid(): boolean {
    return (
      this.truncateStartBases >= 0 &&
      this.truncateEndBases >= 0 &&
      this.minLength > 0 &&
      this.nBases >= 0 &&
      this.complexity >= 0 && this.complexity <= 100
    );
  }

  onFilter(): void {
    const userId =this.authService.getUserId() || '0';
    if (userId && this.selectedFile) {
      this.isLoading = true;
      this.errorMessage = '';
      this.message = '';

      this.filteringService.filterFastqFile(
        this.selectedFile,
        userId,
        false,
        this.truncateStartBases,
        this.truncateEndBases,
        this.leftAdapter,
        this.rightAdapter,
        this.minLength,
        this.nBases,
        this.complexity
      ).subscribe(
        (response: any) => {
          this.message = response.message || 'Filtering started successfully!';
          this.isLoading = false;
          this.showForm = false;
        },
        (error: any) => {
          this.isLoading = false;
          this.errorMessage = 'An error occurred during filtering. Please try again.';
          console.error('Error filtering FASTQ file:', error);
        }
      );
    } else {
      this.errorMessage = 'Please select a file and log in to start filtering.';
    }
  }

  openReferenceModal(fileName: string) {
    this.selectedFile = fileName;
    this.fetchReferenceFiles();
    this.showReferenceModal = true;
  }

  closeReferenceModal() {
    this.showReferenceModal = false;
    this.selectedReferenceFile = '';
    this.selectedFileToUpload = null;
  }

  fetchReferenceFiles() {
    this.fileManagementService.listFiles('reference-genomes-files').subscribe(
      (response: any) => {
        this.referenceFiles = response.files.map((file: any) => ({ file_name: file.file_name }));
      },
      (error: any) => {
        this.handleError('Failed to list reference genome files', error);
      }
    );
  }

  onFileSelected(event: any) {
    this.selectedFileToUpload = event.target.files[0];
  }

  uploadSelectedFile() {
    const userId = this.authService.getUserId() || '0';
    if (this.selectedFileToUpload && userId) {
      this.uploadFile(this.selectedFileToUpload).subscribe(
        (response: any) => {
          this.selectedReferenceFile = response.file_name;
          this.showSuccessMessage('File uploaded successfully');
          this.fetchReferenceFiles();
        },
        (error: any) => {
          this.handleError('File upload failed. Please try again.', error);
        }
      );
    }
  }

  uploadFile(file: File): Observable<any> {
    const userId = this.authService.getUserId() || '0';
    return this.fileManagementService.uploadFile('reference-genomes-files', userId.toString(), file);
  }

  performAlignment() {
    const userId = this.authService.getUserId() || '0';
    if (userId && this.selectedFile && this.selectedReferenceFile) {
      this.startLoading();
      this.alignmentService.performAlignment(this.selectedFile, this.selectedReferenceFile, userId)
        .subscribe(
          (response: any) => {
            this.showSuccessMessage(response.message || 'Alignment started successfully!');
            this.stopLoading();
          },
          (error: any) => {
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
