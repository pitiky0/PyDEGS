import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AuthService } from '../_services/auth.service';

@Component({
  selector: 'app-forgot-password',
  templateUrl: './forgot-password.component.html',
  styleUrls: ['./forgot-password.component.css']
})
export class ForgotPasswordComponent {
  forgotPasswordForm: FormGroup;
  submitted = false;
  errorMessage = '';
  successMessage = '';

  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthService
  ) {
    this.forgotPasswordForm = this.formBuilder.group({
      email: ['', [Validators.required, Validators.email]]
    });
  }

  get f() {
    return this.forgotPasswordForm.controls;
  }

  onSubmit() {
    this.submitted = true;
    this.errorMessage = '';
    this.successMessage = '';

    if (this.forgotPasswordForm.invalid) {
      return;
    }

    this.authService.forgotPassword(this.forgotPasswordForm.value.email).subscribe({
      next: (data) => {
        this.successMessage = 'Password reset link sent to your email.';
      },
      error: (error) => {
        this.errorMessage = error.error.detail || 'Failed to send password reset link';
      }
    });
  }
}
