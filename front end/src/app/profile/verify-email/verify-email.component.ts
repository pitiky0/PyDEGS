import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AuthService } from '../../_services/auth.service';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-verify-email',
  templateUrl: './verify-email.component.html',
  styleUrls: ['./verify-email.component.css']
})
export class VerifyEmailComponent {
  verifyEmailForm: FormGroup;
  submitted = false;
  successMessage = '';
  errorMessage = '';

  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthService,
    private route: ActivatedRoute,
    private router: Router
  ) {
    this.verifyEmailForm = this.formBuilder.group({
      email: ['', [Validators.required, Validators.email]],
      token: ['', Validators.required]
    });
  }

  get f() {
    return this.verifyEmailForm.controls;
  }

  onSubmit() {
    this.submitted = true;
    this.successMessage = '';
    this.errorMessage = '';

    if (this.verifyEmailForm.invalid) {
      return;
    }

    const { email, token } = this.verifyEmailForm.value;
    this.authService.verifyEmail(token, email).subscribe({
      next: () => {
        this.successMessage = 'Email verified successfully';
        this.router.navigate(['/profile']);
      },
      error: (error) => {
        this.errorMessage = error.error.detail || 'Error verifying email';
      }
    });
  }
}
