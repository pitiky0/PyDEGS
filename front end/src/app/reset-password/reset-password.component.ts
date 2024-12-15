import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthService } from '../_services/auth.service';

@Component({
  selector: 'app-reset-password',
  templateUrl: './reset-password.component.html',
  styleUrls: ['./reset-password.component.css']
})
export class ResetPasswordComponent {
  resetPasswordForm: FormGroup;
  submitted = false;
  errorMessage = '';
  successMessage = '';
  token: string;
  email: string;

  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthService,
    private route: ActivatedRoute,
    private router: Router
  ) {
    this.token = this.route.snapshot.queryParamMap.get('token') || '';
    this.email = this.route.snapshot.queryParamMap.get('email') || '';

    console.log(this.token)
    console.log(this.email)

    
    this.resetPasswordForm = this.formBuilder.group({
      password: ['', [Validators.required, Validators.minLength(8)]],
      confirmPassword: ['', [Validators.required]]
    }, { validator: this.passwordMatchValidator });
  }

  get f() {
    return this.resetPasswordForm.controls;
  }

  passwordMatchValidator(form: FormGroup) {
    return form.get('password')?.value === form.get('confirmPassword')?.value
      ? null : { 'mismatch': true };
  }

  onSubmit() {
    this.submitted = true;
    this.errorMessage = '';
    this.successMessage = '';

    if (this.resetPasswordForm.invalid) {
      return;
    }

    const resetData = {
      email: this.email,
      token: this.token,
      password: this.resetPasswordForm.value.password
    };

    this.authService.resetPassword(resetData).subscribe({
      next: (data) => {
        this.successMessage = 'Password reset successfully';
        this.router.navigate(['/login']);
      },
      error: (error) => {
        this.errorMessage = error.error.detail || 'Failed to reset password';
      }
    });
  }
}
