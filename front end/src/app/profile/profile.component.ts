import { Component, OnInit } from '@angular/core';
import { AuthService } from '../_services/auth.service';
import { Router } from '@angular/router';

interface User {
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  gender: string;
  birthdate: string;
  about_me: string;
  image_url?: string; // Add any other optional fields as needed
}

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {
  user: Partial<User> = {}; // Use Partial<User> to allow for partial initialization
  isLoading = true;
  errorMessage = '';
  userFields = [
    { label: 'Username', key: 'username' },
    { label: 'Email', key: 'email' },
    { label: 'First Name', key: 'first_name' },
    { label: 'Last Name', key: 'last_name' },
    { label: 'Gender', key: 'gender' },
    { label: 'Birthdate', key: 'birthdate' },
    { label: 'About Me', key: 'about_me' }
  ];

  constructor(private authService: AuthService, private router: Router) {}

  ngOnInit() {
    this.authService.getProfile().subscribe({
      next: (data: User) => {
        this.user = data;
        this.isLoading = false;
      },
      error: (error) => {
        console.error(error);
        this.errorMessage = error.error.detail || 'Failed to get profile';
        this.isLoading = false;
      }
    });
  }

  confirmDelete() {
    if (confirm('Are you sure you want to delete your account?')) {
      this.router.navigate(['/profile/delete']);
    }
  }

  logout() {
    this.authService.logout().subscribe({
      next: () => {
        this.router.navigate(['/login']);
      },
      error: (error) => {
        console.error('Logout failed', error);
      }
    });
  }

  getIconClass(key: string): string {
    const icons: { [key: string]: string } = {
      username: 'fas fa-user',
      email: 'fas fa-envelope',
      first_name: 'fas fa-id-card',
      last_name: 'fas fa-id-card',
      gender: 'fas fa-venus-mars',
      birthdate: 'fas fa-calendar-alt',
      about_me: 'fas fa-info-circle'
    };
    return icons[key] || 'fas fa-info-circle';
  }

  getUserField(key: string): string {
    return (this.user as any)[key] || '';
  }
}
