import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../_services/auth.service';

@Component({
  selector: 'app-change-password',
  templateUrl: './change-password.component.html',
  styleUrls: ['./change-password.component.css']
})
export class ChangePasswordComponent {
  changePasswordForm: FormGroup;
  submitted = false;
  errorMessage = '';
  successMessage = '';

  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {
    this.changePasswordForm = this.formBuilder.group({
      currentPassword: ['', [Validators.required]],
      newPassword: ['', [Validators.required, Validators.minLength(8)]],
      confirmPassword: ['', [Validators.required, Validators.minLength(8)]]
    }, {
      validator: this.checkPasswords 
    });
  }

  get f() {
    return this.changePasswordForm.controls;
  }

  checkPasswords(control: FormGroup) {
    if (control.get('newPassword')?.value !== control.get('confirmPassword')?.value) {
      return {
        mismatch: true
      };
    } 
    return null; 
  }

  onSubmit() {
    this.submitted = true;
    this.errorMessage = '';
    this.successMessage = '';

    if (this.changePasswordForm.invalid) {
      return;
    }

    const passwordData = {
      password: this.changePasswordForm.get('newPassword')?.value 
    };

    this.authService.changePassword(passwordData).subscribe({
      next: () => {
        this.successMessage = 'Password changed successfully';
        this.changePasswordForm.reset(); 
      },
      error: (error) => {
        this.errorMessage = error.error.detail || 'An error occurred while changing password';
      }
    });
  }
}