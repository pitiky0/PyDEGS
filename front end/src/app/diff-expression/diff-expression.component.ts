import { Component, OnInit } from '@angular/core';
import { DiffExpressionService } from '../_services/diff-expression.service';
import { FileManagementService } from '../_services/file-management.service';
import { AuthService } from '../_services/auth.service';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';

interface CountsFile {
  file_name: string;
}

interface MetadataFile {
  file_name: string;
}

interface Condition {
  column: string;
}

@Component({
  selector: 'app-diff-expression',
  templateUrl: './diff-expression.component.html',
  styleUrls: ['./diff-expression.component.css']
})
export class DiffExpressionComponent implements OnInit {
  countsFiles: CountsFile[] = [];
  metadataFiles: MetadataFile[] = [];
  conditions: Condition[] = [];
  selectedCountsFile: string = '';
  selectedMetadataFile: string = '';
  selectedCondition: string = '';
  userId: string | null = null;
  isLoading: boolean = false;
  errorMessage: string = '';
  message: string = '';
  showMetadataModal: boolean = false;

  constructor(
    private diffExpressionService: DiffExpressionService,
    private fileManagementService: FileManagementService,
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.userId = this.authService.getUserId() || '0';
    this.fetchCountsFiles();
  }

  fetchConditions() {
    this.fileManagementService.getConditions(this.selectedMetadataFile).subscribe(
      (response) => {
        this.conditions = response.columns;
      },
      (error) => {
        console.error('Failed to fetch conditions', error);
      }
    );
  }

  onMetadataFileChange(): void {
    if (this.selectedMetadataFile) {
      this.fetchConditions();
    }
  }

  fetchCountsFiles() {
    this.fileManagementService.listFiles('quantification-files').subscribe(
      (response) => {
        this.countsFiles = response.files.map((file: any) => ({ file_name: file.file_name }));
      },
      (error) => {
        console.error('Failed to list counts files', error);
      }
    );
  }

  fetchMetadataFiles() {
    this.fileManagementService.listFiles('study-metadata-files').subscribe(
      (response) => {
        this.metadataFiles = response.files.map((file: any) => ({ file_name: file.file_name }));
      },
      (error) => {
        console.error('Failed to list metadata files', error);
      }
    );
  }

  openMetadataModal(fileName: string) {
    this.selectedCountsFile = fileName;
    this.fetchMetadataFiles();
    this.showMetadataModal = true;
  }

  closeMetadataModal() {
    this.showMetadataModal = false;
    this.selectedMetadataFile = '';
    this.selectedCondition = '';
  }

  performDiffExpression() {
    if (this.userId && this.selectedCountsFile && this.selectedMetadataFile && this.selectedCondition) {
      this.startLoading();
      this.diffExpressionService.performDiffExpression(
        this.selectedCountsFile,
        this.selectedMetadataFile,
        this.selectedCondition,
        this.userId
      )
        .subscribe(
          (response) => {
            this.showSuccessMessage(response.message || 'Differential Expression analysis started successfully!');
            this.stopLoading();
            this.closeMetadataModal();
          },
          (error) => {
            this.handleError('An error occurred during differential expression analysis. Please try again.', error);
          }
        );
    } else {
      this.errorMessage = 'Please select a counts file, metadata file, condition and log in to start differential expression analysis.';
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
