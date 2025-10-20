import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { UserCreateRequest, LoginRequest } from '../../models/user.model';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  private authService = inject(AuthService);
  private router = inject(Router);

  isRegistering = false;
  loading = false;
  error = '';

  formData = {
    email: '',
    password: '',
    major: '',
    gradYear: new Date().getFullYear() + 1
  };

  majors = [
    'Applied Sciences',
    'Art',
    'Biology',
    'Business Administration',
    'Chemistry',
    'Computer Science',
    'Data Science',
    'Economics',
    'Neuroscience',
    'Physics'
  ];

  get gradYears(): number[] {
    const currentYear = new Date().getFullYear();
    return Array.from({ length: 10 }, (_, i) => currentYear + i);
  }

  validateEmail(email: string): boolean {
    const uncPattern = /^[a-zA-Z0-9._%+-]+@(unc\.edu|live\.unc\.edu|ad\.unc\.edu)$/;
    return uncPattern.test(email.toLowerCase());
  }

  onSubmit(): void {
    this.loading = true;
    this.error = '';

    if (!this.validateEmail(this.formData.email)) {
      this.error = 'Please use a valid UNC email address (@unc.edu, @live.unc.edu, or @ad.unc.edu)';
      this.loading = false;
      return;
    }

    if (this.isRegistering) {
      const request: UserCreateRequest = {
        email: this.formData.email,
        password: this.formData.password,
        major: this.formData.major,
        gradYear: this.formData.gradYear
      };

      this.authService.register(request).subscribe({
        next: () => this.router.navigate(['/majors']),
        error: (err) => {
          this.error = err.error?.detail || 'Registration failed';
          this.loading = false;
        }
      });
    } else {
      const request: LoginRequest = {
        email: this.formData.email,
        password: this.formData.password
      };

      this.authService.login(request).subscribe({
        next: () => this.router.navigate(['/majors']),
        error: (err) => {
          this.error = err.error?.detail || 'Login failed';
          this.loading = false;
        }
      });
    }
  }

  toggleMode(): void {
    this.isRegistering = !this.isRegistering;
    this.error = '';
  }
}
