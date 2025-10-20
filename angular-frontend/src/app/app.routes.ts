import { Routes } from '@angular/router';
import { LoginComponent } from './components/login/login.component';
import { authGuard } from './guards/auth.guard';

export const routes: Routes = [
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  // Add more routes here as you convert components
  // { path: 'majors', component: MajorSelectionComponent, canActivate: [authGuard] },
  // { path: 'major/:major', component: MajorPageComponent, canActivate: [authGuard] },
  { path: '**', redirectTo: '/login' }
];
