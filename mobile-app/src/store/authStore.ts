/**
 * Authentication state management with Zustand
 */

import { create } from 'zustand';
import authService, { User, UserWithProfile, LoginData, RegisterData } from '../services/api/auth';

interface AuthState {
  user: UserWithProfile | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;

  // Actions
  initializeAuth: () => Promise<void>;
  login: (data: LoginData) => Promise<void>;
  register: (data: RegisterData) => Promise<void>;
  logout: () => Promise<void>;
  loadUser: () => Promise<void>;
  clearError: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,
  isLoading: false,
  error: null,

  initializeAuth: async () => {
    try {
      const isAuth = await authService.isAuthenticated();

      if (!isAuth) {
        set({ isAuthenticated: false, user: null });
        return;
      }

      // Try to get cached user first for faster startup
      const cachedUser = await authService.getCachedUser();
      if (cachedUser) {
        set({
          user: cachedUser,
          isAuthenticated: true,
        });
      }

      // Then refresh from API in the background
      try {
        const user = await authService.getCurrentUser();
        set({ user, isAuthenticated: true });
      } catch (error) {
        // If API fails but we have cached user, keep using cached
        if (!cachedUser) {
          set({ user: null, isAuthenticated: false });
        }
      }
    } catch (error) {
      console.error('Initialize auth error:', error);
      set({ user: null, isAuthenticated: false });
    }
  },

  login: async (data: LoginData) => {
    set({ isLoading: true, error: null });

    try {
      // Login and get tokens
      await authService.login(data);

      // Get user info
      const user = await authService.getCurrentUser();

      set({
        user,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      });
    } catch (error: any) {
      const errorMessage =
        error.response?.data?.detail || error.message || 'Login failed';

      set({
        error: errorMessage,
        isLoading: false,
        isAuthenticated: false,
        user: null,
      });

      throw error;
    }
  },

  register: async (data: RegisterData) => {
    set({ isLoading: true, error: null });

    try {
      // Register user
      const user = await authService.register(data);

      // Auto-login after registration
      await authService.login({
        email: data.email,
        password: data.password,
      });

      set({
        user,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      });
    } catch (error: any) {
      const errorMessage =
        error.response?.data?.detail || error.message || 'Registration failed';

      set({
        error: errorMessage,
        isLoading: false,
        isAuthenticated: false,
        user: null,
      });

      throw error;
    }
  },

  logout: async () => {
    set({ isLoading: true });

    try {
      await authService.logout();

      set({
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: null,
      });
    } catch (error) {
      console.error('Logout error:', error);

      // Still clear state even if API call fails
      set({
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: null,
      });
    }
  },

  loadUser: async () => {
    set({ isLoading: true });

    try {
      const isAuth = await authService.isAuthenticated();

      if (!isAuth) {
        set({ isLoading: false, isAuthenticated: false, user: null });
        return;
      }

      // Try to get user from API
      const user = await authService.getCurrentUser();

      set({
        user,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      });
    } catch (error) {
      console.error('Load user error:', error);

      // If failed, try cached user
      const cachedUser = await authService.getCachedUser();

      if (cachedUser) {
        set({
          user: cachedUser,
          isAuthenticated: true,
          isLoading: false,
        });
      } else {
        set({
          user: null,
          isAuthenticated: false,
          isLoading: false,
        });
      }
    }
  },

  clearError: () => set({ error: null }),
}));
