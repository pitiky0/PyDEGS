import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../_services/auth.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent {
  registerForm: FormGroup;
  submitted = false;
  errorMessage = '';
  infoVisible: { [key: string]: boolean } = {
    username: false,
    email: false,
    password: false
  };

  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {
    this.registerForm = this.formBuilder.group({
      username: ['', [Validators.required]],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(8)]],
      first_name: [''],
      last_name: [''],
      gender: [''],
      birthdate: ['']
    });
  }

  get f() {
    return this.registerForm.controls;
  }

  onSubmit() {
    this.submitted = true;
    this.errorMessage = '';

    if (this.registerForm.invalid) {
      return;
    }

    this.authService.register(this.registerForm.value).subscribe({
      next: (data) => {
        this.router.navigate(['/login']);
      },
      error: (error) => {
        this.errorMessage = error.error.detail || 'An error occurred during registration';
      }
    });
  }

  showInfo(field: string) {
    this.infoVisible[field] = true;
  }

  hideInfo(field: string) {
    this.infoVisible[field] = false;
  }
}
