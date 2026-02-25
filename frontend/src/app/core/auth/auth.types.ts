import { Career } from '../careers/careers.types';

export interface RegisterPayload {
  email: string;
  password: string;
  name: string;
  course: string;
  year_level: 'Freshman' | 'Sophomore' | 'Junior' | 'Senior';
}

export interface LoginPayload {
  email: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface RegisterResponse {
  message: string;
}

export interface LogoutResponse {
  message: string;
}

export interface UserProfile {
  id: number;
  email: string;
  name: string;
  course: string;
  year_level: 'Freshman' | 'Sophomore' | 'Junior' | 'Senior';
  career_id: number | null;
  career: Career | null;
  created_at: string;
  updated_at: string;
}

export interface ProfileUpdatePayload {
  name: string;
  course: string;
  year_level: 'Freshman' | 'Sophomore' | 'Junior' | 'Senior';
}

export interface CareerSelectionPayload {
  career_id: number;
}
