import { Component, OnInit } from '@angular/core';
import { FilteringService } from '../_services/filtering.service';
import { AuthService } from '../_services/auth.service';

interface FastqFile {
  file_name: string;
}

@Component({
  selector: 'app-filtering',
  templateUrl: './filtering.component.html',
  styleUrls: ['./filtering.component.css']
})
export class FilteringComponent implements OnInit {
  fastqFiles: FastqFile[] = [];
  selectedFile: string = '';
  truncateStartBases: number = 0;
  truncateEndBases: number = 0;
  leftAdapter: string = '';
  rightAdapter: string = '';
  minLength: number = 0;
  nBases: number = 0;
  complexity: number = 0;
  userId: string | null = null;
  isLoading: boolean = false;
  errorMessage: string = '';
  message: string = '';
  showForm: boolean = false; // To toggle the display of the form

  constructor(private filteringService: FilteringService, private authService: AuthService) {}

  ngOnInit(): void {
    this.userId = this.authService.getUserId() || '0';
    this.fetchFastqFiles();
  }

  fetchFastqFiles() {
    this.filteringService.listFiles('fastq-files').subscribe(
      (response) => {
        this.fastqFiles = response.files.map((file: any) => ({ file_name: file.file_name }));
      },
      (error) => {
        console.error('Failed to list FASTQ files', error);
      }
    );
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
    if (this.userId && this.selectedFile) {
      this.isLoading = true;
      this.errorMessage = '';
      this.message = '';

      this.filteringService.filterFastqFile(
        this.selectedFile,
        this.userId,
        false,
        this.truncateStartBases,
        this.truncateEndBases,
        this.leftAdapter,
        this.rightAdapter,
        this.minLength,
        this.nBases,
        this.complexity
      ).subscribe(
        (response) => {
          this.message = response.message || 'Filtering started successfully!';
          this.isLoading = false;
          this.showForm = false; // Hide form after filtering
        },
        (error) => {
          this.isLoading = false;
          this.errorMessage = 'An error occurred during filtering. Please try again.';
          console.error('Error filtering FASTQ file:', error);
        }
      );
    } else {
      this.errorMessage = 'Please select a file and log in to start filtering.';
    }
  }
}
