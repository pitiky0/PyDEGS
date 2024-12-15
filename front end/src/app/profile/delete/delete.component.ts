import { Component } from '@angular/core';
import { AuthService } from '../../_services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-delete',
  templateUrl: './delete.component.html',
  styleUrls: ['./delete.component.css']
})
export class DeleteComponent {
  errorMessage = '';
  successMessage = '';

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  onDelete() {
    this.authService.deleteProfile().subscribe({
      next: () => {
        this.successMessage = 'Account deleted successfully';
        localStorage.removeItem('access_token');
        this.router.navigate(['/register']);
      },
      error: (error) => {
        this.errorMessage = error.error.detail || 'Error deleting account';
      }
    });
  }
}
