import { Component, OnInit, ViewChild } from '@angular/core';
import { AuthService } from './_services/auth.service';
import { Router } from '@angular/router';
import { MatSidenav } from '@angular/material/sidenav';
import { ChangeDetectorRef } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  @ViewChild('sidenav') sidenav!: MatSidenav;
  isLoggedIn = false;
  username = '';
  title = 'PyDEGS';
  isFastqDropdownOpen = false;
  isQualityContolDropdownOpen = false;
  isFilteringDropdownOpen = false;
  isAlignmentDropdownOpen = false;
  isQuantificationDropdownOpen = false;
  isDiffExpressionDropdownOpen = false;

  constructor(
    private authService: AuthService,
    private router: Router,
    private cdRef: ChangeDetectorRef

  ) {}

  ngOnInit() {
    // Subscribe to the observables to keep track of login status and username
    this.authService.isLoggedIn$.subscribe(isLoggedIn => {
      this.isLoggedIn = isLoggedIn;
      this.cdRef.detectChanges(); // Mark for change detection
    });

    this.authService.username$.subscribe(username => {
      this.username = username;
      this.cdRef.detectChanges(); // Mark for change detection
    });

    // Check if token exists in localStorage and update the login status
    const token = localStorage.getItem('jwtToken');
    if (token) {
      // Validate the token by getting the user profile
      this.authService.getProfile().subscribe({
        next: (profile) => {
          // Set the login status and username if token is valid
          this.authService.fetchAndStoreUserProfile(token);
        },
        error: () => {
          // If the token is invalid, clear the local storage and log out the user
          this.authService.handleLogoutSuccess();
        }
      });
    }
  }

  toggleDropdown(type: string) {
    if (type === 'fastq') {
      this.isFastqDropdownOpen = !this.isFastqDropdownOpen;
    } else if (type === 'quality-control') {
      this.isQualityContolDropdownOpen = !this.isQualityContolDropdownOpen;
    }else if (type === 'filtering') {
      this.isFilteringDropdownOpen = !this.isFilteringDropdownOpen;
    }else if (type === 'alignment') {
      this.isAlignmentDropdownOpen = !this.isAlignmentDropdownOpen;
    }else if (type === 'quantification') {
      this.isQuantificationDropdownOpen = !this.isQuantificationDropdownOpen;
    }else if (type === 'diff-expression') {
      this.isDiffExpressionDropdownOpen = !this.isDiffExpressionDropdownOpen;
    }
  }

  logout() {
    this.authService.logout().subscribe({
      next: () => {
        this.authService.handleLogoutSuccess();
      },
      error: () => {
        this.authService.handleLogoutSuccess(); // Fallback in case of error
      }
    });
  }
}
