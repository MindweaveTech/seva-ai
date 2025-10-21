/**
 * Authentication API service
 */

import AsyncStorage from '@react-native-async-storage/async-storage';
import apiClient, { STORAGE_KEYS } from './client';

export interface RegisterData {
  email: string;
  password: string;
  full_name: string;
}

export interface LoginData {
  email: string;
  password: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface User {
  id: string;
  email: string;
  full_name: string;
  role: string;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
  last_login_at: string | null;
}

export interface UserWithProfile extends User {
  profile: {
    id: string;
    user_id: string;
    date_of_birth: string | null;
    phone_number: string | null;
    emergency_contact_name: string | null;
    emergency_contact_phone: string | null;
    preferences: Record<string, any>;
  } | null;
}

class AuthService {
  /**
   * Register a new user
   */
  async register(data: RegisterData): Promise<UserWithProfile> {
    const response = await apiClient.post<UserWithProfile>('/auth/register', data);
    return response.data;
  }

  /**
   * Login user and store tokens
   */
  async login(data: LoginData): Promise<AuthTokens> {
    const response = await apiClient.post<AuthTokens>('/auth/login', data);
    const tokens = response.data;

    // Store tokens
    await AsyncStorage.setItem(STORAGE_KEYS.ACCESS_TOKEN, tokens.access_token);
    await AsyncStorage.setItem(STORAGE_KEYS.REFRESH_TOKEN, tokens.refresh_token);

    return tokens;
  }

  /**
   * Logout user and clear tokens
   */
  async logout(): Promise<void> {
    try {
      // Call logout endpoint
      await apiClient.post('/auth/logout');
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      // Clear tokens regardless of API call result
      await AsyncStorage.multiRemove([
        STORAGE_KEYS.ACCESS_TOKEN,
        STORAGE_KEYS.REFRESH_TOKEN,
        STORAGE_KEYS.USER,
      ]);
    }
  }

  /**
   * Get current user info
   */
  async getCurrentUser(): Promise<UserWithProfile> {
    const response = await apiClient.get<UserWithProfile>('/auth/me');

    // Cache user data
    await AsyncStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(response.data));

    return response.data;
  }

  /**
   * Check if user is authenticated
   */
  async isAuthenticated(): Promise<boolean> {
    const token = await AsyncStorage.getItem(STORAGE_KEYS.ACCESS_TOKEN);
    return !!token;
  }

  /**
   * Get cached user data
   */
  async getCachedUser(): Promise<UserWithProfile | null> {
    const userStr = await AsyncStorage.getItem(STORAGE_KEYS.USER);
    return userStr ? JSON.parse(userStr) : null;
  }

  /**
   * Refresh access token
   */
  async refreshToken(): Promise<AuthTokens> {
    const refreshToken = await AsyncStorage.getItem(STORAGE_KEYS.REFRESH_TOKEN);

    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    const response = await apiClient.post<AuthTokens>('/auth/refresh', {
      refresh_token: refreshToken,
    });

    const tokens = response.data;

    // Store new tokens
    await AsyncStorage.setItem(STORAGE_KEYS.ACCESS_TOKEN, tokens.access_token);
    await AsyncStorage.setItem(STORAGE_KEYS.REFRESH_TOKEN, tokens.refresh_token);

    return tokens;
  }
}

export default new AuthService();
