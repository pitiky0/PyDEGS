import { Component } from '@angular/core';
import { AuthService } from '../_services/auth.service';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {
  isLoggedIn$: Observable<boolean>;
  username$: Observable<string>;
  currentYear = new Date().getFullYear(); // Get current year

  constructor(private authService: AuthService) {
    this.isLoggedIn$ = this.authService.isLoggedIn();
    this.username$ = this.authService.getUsername();
  }
}