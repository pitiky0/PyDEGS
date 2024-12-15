// list-filtering-files.component.ts

import { Component, OnInit } from '@angular/core';
import { FileManagementService } from '../../_services/file-management.service';
import { saveAs } from 'file-saver';

interface File {
  file_name: string;
  info?: {
    file_name: string;
    size: number;
    last_modified: string;
    etag: string;
    content_type: string;
    tags?: any; // Add tags property to info
  };
  showInfo: boolean;
  showTopReads: boolean; // Add showTopReads property
  topReads?: any; // Add topReads property
  deleteMessage?: string;
  messageClass?: string;
}
@Component({
  selector: 'app-list-filtering-files',
  templateUrl: './list-filtering-files.component.html',
  styleUrl: './list-filtering-files.component.css'
})
export class ListFilteringFilesComponent implements OnInit{

  files: File[] = [];
  filteredFiles: File[] = [];
  searchQuery: string = '';

  constructor(private fileManagementService: FileManagementService) {}


  ngOnInit(): void {
    this.fileManagementService.listFiles('filtered-fastq-files').subscribe(
      (response) => {
        this.files = response.files
          .filter((file: any) => file.file_name.includes('.fastq')) // Filter to include only .fastq files
          .map((file: any) => ({
            ...file,
            showInfo: false,
            showTopReads: false // Initialize showTopReads to false
          }));

        this.filteredFiles = this.files;
      },
      (error) => {
        console.error('Failed to list files', error);
      }
    );
  }


  onDownload(fileName: string): void {
    this.fileManagementService.downloadFile('filtered-fastq-files', fileName).subscribe(
      (response) => {
        saveAs(response, fileName);
      },
      (error) => {
        console.error('Failed to download file', error);
      }
    );
  }

  onGetInfo(file: File): void {
    if (file.showInfo) {
      file.showInfo = false;
      file.showTopReads = false; // Hide Top Reads if Info is hidden
    } else {
      this.fileManagementService.getFileInfo('filtered-fastq-files', file.file_name).subscribe(
        (response) => {
          file.info = response;
          this.fileManagementService.getTags('filtered-fastq-files', file.file_name).subscribe(
            (tagsResponse) => {
              file.info!.tags = tagsResponse.tags; // Add tags to info object
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

  onGetTopReads(file: File): void {
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

  onDelete(file: File): void {
    const confirmed = window.confirm(`Are you sure you want to delete the file: ${file.file_name}?`);
    if (confirmed) {
      this.fileManagementService.deleteFile('filtered-fastq-files', file.file_name).subscribe(
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

    protected readonly Object = Object;
}
