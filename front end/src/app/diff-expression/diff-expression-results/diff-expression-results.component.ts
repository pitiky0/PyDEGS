import { Component, OnInit } from '@angular/core';
import { FileManagementService } from '../../_services/file-management.service';
import { saveAs } from 'file-saver';

interface File {
  file_name: string;
  isImage: boolean;
  report_url?: string;
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

interface GroupedFiles {
  groupName: string;
  files: File[];
  showFiles: boolean;
}

@Component({
  selector: 'app-diff-expression-results',
  templateUrl: './diff-expression-results.component.html',
  styleUrls: ['./diff-expression-results.component.css']
})
export class DiffExpressionResultsComponent implements OnInit {
  files: File[] = [];
  filteredFiles: GroupedFiles[] = [];
  searchQuery: string = '';

  constructor(private fileManagementService: FileManagementService) {}

  ngOnInit(): void {
    this.fileManagementService.listFiles('def-expression-files').subscribe(
      (response) => {
        this.files = response.files.map((file: any) => ({
          ...file,
          showInfo: false
        }));
        this.groupFiles();
      },
      (error) => {
        console.error('Failed to list files', error);
      }
    );
  }

  groupFiles(): void {
    const groupedFilesMap = new Map<string, File[]>();

    this.files.forEach(file => {
      if (file.file_name.endsWith('.png')) {
        file.isImage = true;
      }
      const groupName = file.file_name.split('/')[0];
      if (!groupedFilesMap.has(groupName)) {
        groupedFilesMap.set(groupName, []);
      }
      groupedFilesMap.get(groupName)?.push(file);
    });

    this.filteredFiles = Array.from(groupedFilesMap.entries()).map(([groupName, files]) => ({
      groupName,
      files,
      showFiles: false
    }));
  }

  toggleGroup(group: GroupedFiles): void {
    group.showFiles = !group.showFiles;
    group.files.forEach(file => this.onOpen(file));
  }

  onDownload(fileName: string): void {
    this.fileManagementService.downloadFile('def-expression-files', fileName).subscribe(
      (response) => {
        saveAs(response, fileName);
      },
      (error) => {
        console.error('Failed to download file', error);
      }
    );
  }

  onDownloadGroup(group: GroupedFiles): void {
    group.files.forEach(file => this.onDownload(file.file_name));
  }

  onOpen(file: File): void {
    if (file.file_name.endsWith('.png')) {
      this.fileManagementService.downloadFile('def-expression-files', file.file_name).subscribe(
        (response) => {
          const blob = new Blob([response], { type: 'image/png' });

          const imageUrl = URL.createObjectURL(blob);

          const fileActionsDiv = document.querySelector(`#${file.file_name.split('/')[1].replace('.', '')}`);
          if (fileActionsDiv) {
            const existingImage = fileActionsDiv.querySelector('.preview-image');
            if (!existingImage) {
              const imageElement = document.createElement('img');
              imageElement.classList.add('preview-image');
              imageElement.style.width = '100%';
              imageElement.style.height = 'auto';
              imageElement.src = imageUrl;

              fileActionsDiv.insertBefore(imageElement, fileActionsDiv.querySelector('.download-btn'));

              imageElement.onload = () => {
                URL.revokeObjectURL(imageUrl);
              };
            }
          } else {
            console.error('fileActionsDiv not found');
          }
        },
        (error) => {
          console.error('Error downloading file:', error);
        }
      );
    }
  }

  onGetInfo(file: File): void {
    if (file.showInfo) {
      file.showInfo = false;
    } else {
      this.fileManagementService.getFileInfo('def-expression-files', file.file_name).subscribe(
        (response) => {
          file.info = response;
          this.fileManagementService.getTags('def-expression-files', file.file_name).subscribe(
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
      this.fileManagementService.deleteFile('def-expression-files', file.file_name).subscribe(
        (response) => {
          file.deleteMessage = 'File deleted successfully';
          file.messageClass = 'success';
          console.log('File deleted successfully', response);
          this.files = this.files.filter(f => f.file_name !== file.file_name);
          this.groupFiles();
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
    this.filteredFiles = this.filteredFiles.filter(group =>
      group.groupName.toLowerCase().includes(this.searchQuery.toLowerCase())
    );
  }

  protected readonly Object = Object;
}
