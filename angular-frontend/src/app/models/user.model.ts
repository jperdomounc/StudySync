export interface User {
  id: string;
  email: string;
  displayName: string;
  major: string;
  gradYear: number;
}

export interface UserCreateRequest {
  email: string;
  password: string;
  major: string;
  gradYear: number;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface AuthResponse {
  accessToken: string;
  tokenType: string;
  user: User;
}
