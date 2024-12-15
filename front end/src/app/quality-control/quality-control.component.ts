import { Component, OnInit } from '@angular/core';
import { QualityControlService } from '../_services/quality-control.service';
import { FileManagementService } from '../_services/file-management.service';
import { AuthService } from '../_services/auth.service';
import { HttpClient, HttpResponse, HttpEventType } from '@angular/common/http';
import { Router } from '@angular/router';
import { saveAs } from 'file-saver';

interface FastqFile {
  file_name: string;
}

interface QualityControlReport {
  file_name: string;
  report_url: string;
  report_type: 'zip' | 'html';
}

@Component({
  selector: 'app-quality-control',
  templateUrl: './quality-control.component.html',
  styleUrls: ['./quality-control.component.css']
})
export class QualityControlComponent implements OnInit {
  fastqFiles: FastqFile[] = [];
  qualityControlReports: QualityControlReport[] = [];
  userId: string | null = null;
  isLoading: boolean = false;
  errorMessage: string = '';
  message: string = '';
  progress: number = 0;

  constructor(
    private qualityControlService: QualityControlService,
    private fileManagementService: FileManagementService,
    private authService: AuthService,
    private http: HttpClient,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.userId = this.authService.getUserId() || '0';
    this.fetchFastqFiles();

  }

  fetchFastqFiles() {
    this.fileManagementService.listFiles('fastq-files').subscribe(
      (response) => {
        this.fastqFiles = response.files.map((file: any) => ({ file_name: file.file_name }));
      },
      (error) => {
        console.error('Failed to list FASTQ files', error);
      }
    );
  }


  performQualityControl(fileName: string) {
    if (this.userId) {
      this.isLoading = true;
      this.errorMessage = '';
      this.message = '';
      this.progress = 0;

      this.qualityControlService.performQualityControl(fileName, this.userId)
        .subscribe(
          (event) => {
            if (event.type === HttpEventType.UploadProgress) {
              this.progress = Math.round((100 * event.loaded) / event.total);
            } else if (event instanceof HttpResponse) {
              this.message = event.body.message || 'Quality Control Successful!';
              this.isLoading = false;
              this.progress = 100;

              setTimeout(() => {
                this.router.navigate(['/list-qc-files']);
              }, 10000);
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
}
