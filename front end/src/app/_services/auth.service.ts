import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { environment } from '../../environments/environment';
import { Router } from '@angular/router';
import { tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = `${environment.apiUrl}/auth`;
  private isLoggedInSubject = new BehaviorSubject<boolean>(false);
  isLoggedIn$ = this.isLoggedInSubject.asObservable();
  private usernameSubject = new BehaviorSubject<string>('');
  username$ = this.usernameSubject.asObservable();

  constructor(private http: HttpClient, private router: Router) {}

  register(user: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/register`, user);
  }

  login(credentials: { email: string; password: string }): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/x-www-form-urlencoded'
    });

    const body = `username=${encodeURIComponent(credentials.email)}&password=${encodeURIComponent(credentials.password)}`;

    return this.http.post(`${this.apiUrl}/login`, body, { headers }).pipe(
      tap((data: any) => {
        console.log(data)
        this.fetchAndStoreUserProfile(data.access_token);

      })
    );
  }

  logout(): Observable<any> {
    return this.http.post(`${this.apiUrl}/logout`, {});
  }

  getProfile(): Observable<any> {
    const token = localStorage.getItem('jwtToken');
    if (!token) {
      this.router.navigate(['/login']);
      return new Observable<any>();
    }

    const headers = new HttpHeaders({
      Authorization: `Bearer ${token}`
    });
    return this.http.get(`${this.apiUrl}/profile`, { headers });
  }

  /*updateProfile(userData: any): Observable<any> {
    const token = localStorage.getItem('jwtToken');
    if (!token) {
      this.router.navigate(['/login']);
      return new Observable<any>();
    }

    console.log('Using token:', token); // Log the token
    console.log('User data being sent:', userData); // Log user data

    const headers = new HttpHeaders({
      Authorization: `Bearer ${token}`
    });
    return this.http.put(`${this.apiUrl}/profile`, userData, { headers });
  }*/


  changePassword(passwordData: any): Observable<any> {
    const token = localStorage.getItem('jwtToken');
    if (!token) {
      this.router.navigate(['/login']);
      return new Observable<any>();
    }
    const headers = new HttpHeaders({
      Authorization: `Bearer ${token}`
    });
    return this.http.put(`${this.apiUrl}/profile/change-password`, passwordData, { headers });
  }

  forgotPassword(email: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/forgot-password`, { email });
  }

  resetPassword(resetData: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/reset-password`, resetData);
  }

  verifyEmail(token: string, email: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/profile/verify-email`, {
      params: { token, email }
    });
  }

  deleteProfile(): Observable<any> {
    const token = localStorage.getItem('jwtToken');
    if (!token) {
      this.router.navigate(['/login']);
      return new Observable<any>();
    }
    const headers = new HttpHeaders({
      Authorization: `Bearer ${token}`
    });
    return this.http.delete(`${this.apiUrl}/profile/delete`, { headers });
  }

  isLoggedIn(): Observable<boolean> {
    return this.isLoggedInSubject.asObservable();
  }

  getUsername(): Observable<string> {
    return this.usernameSubject.asObservable();
  }

  private setLoginStatus(isLoggedIn: boolean, username?: string) {
    this.isLoggedInSubject.next(isLoggedIn);
    if (username) {
      this.usernameSubject.next(username);
    }
  }

  /*handleLoginSuccess(data: any) {
    console.log(`Login success. User ID: ${data.user_id}`);
    console.log(`${data.access_token} ${data.user_id} ${data.username}`);
    localStorage.setItem('jwtToken', data.access_token);
    localStorage.setItem('user_id', data.user_id);
    this.setLoginStatus(true, data.username);
    this.router.navigate(['/profile']);
  }*/


  /*private handleLoginSuccess(data: any) {


    this.fetchAndStoreUserProfile(data.access_token);
  }*/


  public fetchAndStoreUserProfile(token: string) {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    });

    this.http.get(`${this.apiUrl}/profile`, { headers }).subscribe(
      (profileData: any) => {
        localStorage.setItem('jwtToken', token);
        localStorage.setItem('user_id', profileData.user_id);
        localStorage.setItem('username', profileData.username);
        localStorage.setItem('email', profileData.email);
        console.log(`${profileData.email} ${profileData.user_id} ${profileData.username}`);
        this.setLoginStatus(true, profileData.username);
        this.router.navigate(['/home']);
      },
      (error) => {
        console.error('Error fetching profile data:', error);
      }
    );
  }



  handleLogoutSuccess() {
    localStorage.removeItem('jwtToken');
    localStorage.removeItem('user_id');
    this.setLoginStatus(false);
    this.router.navigate(['/login']);
  }

  getUserId(): string | null {
    return localStorage.getItem('username');
  }



  updateProfile(user: any): Observable<any> {
    const token = localStorage.getItem('jwtToken');
    if (!token) {
      this.router.navigate(['/login']);
      return new Observable<any>();
    }
    const headers = new HttpHeaders({
      Authorization: `Bearer ${token}`
    });
    return this.http.put(`${this.apiUrl}/profile`, user, { headers });
  }
}

