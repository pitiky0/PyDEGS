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
    tags?: any;
  };
  showInfo: boolean;
  deleteMessage?: string;
  messageClass?: string;
}

@Component({
  selector: 'app-list-qc-files',
  templateUrl: './list-qc-files.component.html',
  styleUrls: ['./list-qc-files.component.css']
})
export class ListQCFilesComponent implements OnInit {

  files: File[] = [];
  filteredFiles: File[] = [];
  searchQuery: string = '';

  constructor(private fileManagementService: FileManagementService) {}

  ngOnInit(): void {
    this.fileManagementService.listFiles('quality-control-files').subscribe(
      (response) => {
        this.files = response.files.map((file: any) => ({
          ...file,
          showInfo: false
        }));
        this.filteredFiles = this.files;
      },
      (error) => {
        console.error('Failed to list files', error);
      }
    );
  }

  onDownload(fileName: string): void {
    this.fileManagementService.downloadFile('quality-control-files', fileName).subscribe(
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
    } else {
      this.fileManagementService.getFileInfo('quality-control-files', file.file_name).subscribe(
        (response) => {
          file.info = response;
          this.fileManagementService.getTags('quality-control-files', file.file_name).subscribe(
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

  onDelete(file: File): void {
    const confirmed = window.confirm(`Are you sure you want to delete the file: ${file.file_name}?`);
    if (confirmed) {
      this.fileManagementService.deleteFile('quality-control-files', file.file_name).subscribe(
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

  onOpen(file: File): void {
    if (file.file_name.endsWith('.html')) {
      this.fileManagementService.downloadFile('quality-control-files', file.file_name).subscribe(
        (response) => {
          const blob = new Blob([response], { type: 'text/html' });
          const url = window.URL.createObjectURL(blob);
          window.open(url, '_blank');
        },
        (error) => {
          console.error('Failed to open file', error);
        }
      );
    } else {
      alert('Only .html files can be opened in a new tab.');
    }
  }

  protected readonly Object = Object;
}
