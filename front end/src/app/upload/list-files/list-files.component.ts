
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { FileManagementService } from '../../_services/file-management.service';
import { QualityControlService } from '../../_services/quality-control.service';
import { FilteringService } from '../../_services/filtering.service';
import { AlignmentService } from '../../_services/alignment.service';
import { AuthService } from '../../_services/auth.service';
import { saveAs } from 'file-saver';
import { Observable } from 'rxjs';
import { HttpEventType, HttpResponse } from '@angular/common/http';

interface CustomFile {
  file_name: string;
  info?: {
    file_name: string;
    size: number;
    last_modified: string;
    etag: string;
    content_type: string;
    tags?: any;
  };
  topReads?: any;
  showInfo: boolean;
  showTags: boolean;
  showTopReads: boolean;
  deleteMessage?: string;
  messageClass?: string;
  selected: boolean;
}

@Component({
  selector: 'app-list-files',
  templateUrl: './list-files.component.html',
  styleUrls: ['./list-files.component.css']
})
export class ListFilesComponent implements OnInit {
  files: CustomFile[] = [];
  filteredFiles: CustomFile[] = [];
  searchQuery: string = '';
  userId: string | null = null;
  isLoading: boolean = false;
  errorMessage: string = '';
  message: string = '';
  selectAll: boolean = false;
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
  showGroupNameModal: boolean = false; // Flag for group name modal
  groupName: string = '';

  constructor(
    private fileManagementService: FileManagementService,
    private qualityControlService: QualityControlService,
    private filteringService: FilteringService,
    private alignmentService: AlignmentService,
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.userId = this.authService.getUserId() || '0';
    this.fileManagementService.listFiles('fastq-files').subscribe(
      (response) => {
        this.files = response.files.map((file: any) => ({
          ...file,
          showInfo: false,
          showTags: false,
          showTopReads: false,
          selected: false
        }));
        this.filteredFiles = this.files;
      },
      (error) => {
        console.error('Failed to list files', error);
      }
    );
  }

  onDownload(fileName: string): void {
    this.fileManagementService.downloadFile('fastq-files', fileName).subscribe(
      (response) => {
        saveAs(response, fileName);
      },
      (error) => {
        console.error('Failed to download file', error);
      }
    );
  }

  onGetInfo(file: CustomFile): void {
    if (file.showInfo) {
      file.showInfo = false;
      file.showTopReads = false; // Hide Top Reads if Info is hidden
    } else {
      this.fileManagementService.getFileInfo('fastq-files', file.file_name).subscribe(
        (response) => {
          file.info = response;
          this.fileManagementService.getTags('fastq-files', file.file_name).subscribe(
            (tagsResponse) => {
              file.info!.tags = tagsResponse.tags;
              file.showInfo = true;
            },
            (error) => {
              console.error('Failed to get tags', error);
              file.showInfo = true;
            }
          );
        },
        (error) => {
          console.error('Failed to get file info', error);
        }
      );
    }
  }

  onGetTopReads(file: CustomFile): void {
    if (file.showTopReads) {
      file.showTopReads = false;
    } else {
      this.fileManagementService.getTopReads(file.file_name).subscribe(
        (response) => {
          file.topReads = response;
          file.showTopReads = true;
        },
        (error) => {
          console.error('Failed to get top reads', error);
        }
      );
    }
  }

  onDelete(file: CustomFile): void {
    const confirmed = window.confirm(`Are you sure you want to delete the file: ${file.file_name}?`);
    if (confirmed) {
      this.fileManagementService.deleteFile('fastq-files', file.file_name).subscribe(
        (response) => {
          file.deleteMessage = 'File deleted successfully';
          file.messageClass = 'success';
          console.log('File deleted successfully', response);
          this.files = this.files.filter(f => f.file_name !== file.file_name);
          this.filteredFiles = this.filteredFiles.filter(f => f.file_name !== file.file_name);
        },
        (error) => {
          file.deleteMessage = 'File deletion failed';
          file.messageClass = 'error';
          console.error('File deletion failed', error);
        }
      );
    }
  }

  onSearch(): void {
    this.filteredFiles = this.files.filter(file =>
      file.file_name.toLowerCase().includes(this.searchQuery.toLowerCase())
    );
  }

  onSingleClick(file: CustomFile): void {
    this.router.navigate(['/file-details', file.file_name]);
  }

  onSelectAllChange(): void {
    this.filteredFiles.forEach(file => file.selected = this.selectAll);
  }

  onDeselectAll(): void {
    this.filteredFiles.forEach(file => file.selected = false);
    this.selectAll = false;
  }

  getSelectedCount(): number {
    return this.filteredFiles.filter(file => file.selected).length;
  }

  isAnyFileSelected(): boolean {
    return this.getSelectedCount() > 0;
  }

  onBulkDownload(): void {
    const selectedFiles = this.filteredFiles.filter(file => file.selected);
    selectedFiles.forEach(file => this.onDownload(file.file_name));
  }

  onBulkDelete(): void {
    const selectedFiles = this.filteredFiles.filter(file => file.selected);
    selectedFiles.forEach(file => this.onDelete(file));
  }

  onBulkAnalyze(): void {
    const selectedFiles = this.filteredFiles.filter(file => file.selected);
    selectedFiles.forEach(file => this.performQualityControl(file.file_name));
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

  onBulkFilter(): void {
    this.filteredFiles.filter(file => file.selected).forEach(file => this.toggleForm(file.file_name));
  }

  onBulkAlign(): void {
    this.filteredFiles.filter(file => file.selected).forEach(file => this.openReferenceModal(file.file_name));
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
    const userId=this.authService.getUserId() || '0';
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
          this.showForm = false; // Hide form after filtering
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
      (error) => {
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

  onGroupFiles(): void {
    this.showGroupNameModal = true; // Show the modal when "Group" is clicked
  }

  closeGroupNameModal(): void {
    this.showGroupNameModal = false;
    this.groupName = ''; // Clear the group name input
  }

  confirmGroupName(): void {
    if (this.groupName.trim() !== '') {
      const selectedFiles = this.filteredFiles.filter(file => file.selected);
      const fileNames = selectedFiles.map(file => file.file_name);

      if (fileNames.length > 0) {
        this.fileManagementService.groupFiles('fastq-files', this.groupName, fileNames).subscribe(
          (response) => {
            this.message = `Files grouped successfully into ${this.groupName}`;
            // Refresh file list after grouping
            this.fileManagementService.listFiles('fastq-files').subscribe(
              (response) => {
                this.files = response.files.map((file: any) => ({
                  ...file,
                  showInfo: false,
                  selected: false
                }));
                this.filteredFiles = this.files;
              },
              (error) => {
                console.error('Failed to list files', error);
              }
            );
            this.closeGroupNameModal(); // Close the modal
          },
          (error) => {
            this.errorMessage = 'Failed to group files';
            console.error('Failed to group files', error);
          }
        );
      }
    } else {
      this.errorMessage = 'Please enter a group name.';
    }
  }

    protected readonly Object = Object;
}
