import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../_services/auth.service';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-edit-profile',
  templateUrl: './edit-profile.component.html',
  styleUrls: ['./edit-profile.component.css']
})
export class EditProfileComponent implements OnInit {
  editProfileForm: FormGroup;
  isLoading = true;
  errorMessage = '';
  successMessage = '';

  constructor(
    private authService: AuthService,
    public router: Router,  // Change made here: made router public
    private fb: FormBuilder
  ) {
    this.editProfileForm = this.fb.group({
      username: ['', [Validators.required]],
      email: ['', [Validators.required, Validators.email]],
      first_name: [''],
      last_name: [''],
      gender: [''],
      birthdate: [''],
      about_me: [''],
      image_url: ['']
    });
  }

  ngOnInit() {
    this.authService.getProfile().subscribe({
      next: (data: any) => {
        this.editProfileForm.patchValue(data);
        this.isLoading = false;
      },
      error: (error) => {
        console.error(error);
        this.errorMessage = error.error.detail || 'Failed to load profile';
        this.isLoading = false;
      }
    });
  }

  onSubmit() {
    if (this.editProfileForm.invalid) {
      return;
    }

    this.authService.updateProfile(this.editProfileForm.value).subscribe({
      next: (response) => {
        this.successMessage = 'Profile updated successfully!';
        this.errorMessage = '';
        setTimeout(() => {
          this.router.navigate(['/profile']);
        }, 2000);
      },
      error: (error) => {
        console.error(error);
        this.errorMessage = error.error.detail || 'Failed to update profile';
        this.successMessage = '';
      }
    });
  }
}
