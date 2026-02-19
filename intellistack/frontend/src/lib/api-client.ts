import type {
  SavePreferencesRequest,
  SavePreferencesResponse,
  ApiError,
  PersonalizationPreferences,
} from '@/types/api';

interface RetryOptions {
  maxRetries?: number;
  retryDelay?: number;
  retryableStatuses?: number[];
}

class ApiClient {
  private baseUrl: string;
  private isOnline: boolean = true;
  private onlineListeners: Set<(online: boolean) => void> = new Set();

  constructor() {
    this.baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

    // Monitor online/offline status
    if (typeof window !== 'undefined') {
      window.addEventListener('online', () => this.setOnlineStatus(true));
      window.addEventListener('offline', () => this.setOnlineStatus(false));
      this.isOnline = navigator.onLine;
    }
  }

  private setOnlineStatus(online: boolean) {
    this.isOnline = online;
    this.onlineListeners.forEach(listener => listener(online));
  }

  public onOnlineStatusChange(listener: (online: boolean) => void) {
    this.onlineListeners.add(listener);
    return () => this.onlineListeners.delete(listener);
  }

  public getOnlineStatus(): boolean {
    return this.isOnline;
  }

  private async sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  private async getAuthToken(): Promise<string | null> {
    try {
      // Dynamically import auth client to avoid circular dependencies
      const { getAuthClient } = await import('@/lib/auth');
      const client = getAuthClient();
      const token = await client.getJwtToken();
      return token;
    } catch (error) {
      console.warn('Failed to get auth token:', error);
      return null;
    }
  }

  private async request<T>(
    url: string,
    options: RequestInit = {},
    retryOptions: RetryOptions = {}
  ): Promise<T> {
    const {
      maxRetries = 3,
      retryDelay = 1000,
      retryableStatuses = [408, 429, 500, 502, 503, 504],
    } = retryOptions;

    let lastError: Error | null = null;

    for (let attempt = 0; attempt <= maxRetries; attempt++) {
      try {
        // Check if offline
        if (!this.isOnline) {
          throw new NetworkError('No internet connection');
        }

        // Get JWT token for authentication
        const token = await this.getAuthToken();

        const response = await fetch(url, {
          ...options,
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
            ...(token ? { Authorization: `Bearer ${token}` } : {}),
            ...options.headers,
          },
        });

        if (!response.ok) {
          // Check if status is retryable
          if (attempt < maxRetries && retryableStatuses.includes(response.status)) {
            await this.sleep(retryDelay * Math.pow(2, attempt)); // Exponential backoff
            continue;
          }

          // Try to parse error response
          let error: ApiError;
          try {
            error = await response.json();
          } catch {
            // If JSON parsing fails, create a generic error
            error = {
              success: false,
              error: {
                code: `HTTP_${response.status}`,
                message: response.statusText || `Request failed with status ${response.status}`,
              },
            };
          }

          // Ensure error has the expected structure
          if (!error.error || !error.error.message) {
            error = {
              success: false,
              error: {
                code: error.error?.code || `HTTP_${response.status}`,
                message: error.error?.message || response.statusText || `Request failed with status ${response.status}`,
              },
            };
          }

          throw new ApiClientError(error);
        }

        return response.json();
      } catch (error) {
        lastError = error as Error;

        // Network errors (fetch failed)
        if (error instanceof TypeError && error.message.includes('fetch')) {
          if (attempt < maxRetries) {
            await this.sleep(retryDelay * Math.pow(2, attempt));
            continue;
          }
          throw new NetworkError('Network request failed. Please check your connection.');
        }

        // Don't retry ApiClientError (4xx errors)
        if (error instanceof ApiClientError) {
          throw error;
        }

        // Don't retry NetworkError
        if (error instanceof NetworkError) {
          throw error;
        }

        // Retry other errors
        if (attempt < maxRetries) {
          await this.sleep(retryDelay * Math.pow(2, attempt));
          continue;
        }

        throw error;
      }
    }

    throw lastError || new Error('Request failed after retries');
  }

  // Preferences methods
  async savePreferences(
    data: SavePreferencesRequest
  ): Promise<SavePreferencesResponse> {
    return this.request(`${this.baseUrl}/api/v1/users/onboarding`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getPreferences(): Promise<{
    success: true;
    data: PersonalizationPreferences | null;
  }> {
    return this.request(`${this.baseUrl}/api/v1/users/me`);
  }

  async updatePreferences(
    data: Partial<SavePreferencesRequest>
  ): Promise<SavePreferencesResponse> {
    // Transform frontend PersonalizationPreferences to backend OnboardingPreferencesRequest
    const backendData = {
      learning_style: 'visual', // Default - can be enhanced later
      learning_pace: 'moderate', // Default - can be enhanced later
      preferred_language: (data as any).preferredLanguage || 'en',
      focus_areas: (data as any).interests || [],
      adaptive_complexity: true,
      personalized_exercises: true,
      personalized_time_estimates: true,
      goal_timeframe: (data as any).learningGoal || null,
      programming_experience: (data as any).experienceLevel || null,
      robotics_experience: null,
      math_background: null,
      linux_familiarity: null,
      operating_system: null,
      preferred_ide: null,
      shell: null,
      domain_preference: null,
    };

    return this.request(`${this.baseUrl}/api/v1/users/preferences/onboarding`, {
      method: 'POST',
      body: JSON.stringify(backendData),
    });
  }

  async deletePreferences(): Promise<{ success: true; message: string }> {
    return this.request(`${this.baseUrl}/api/v1/users/preferences/reset`, {
      method: 'POST',
    });
  }
}

export class ApiClientError extends Error {
  constructor(public error: ApiError) {
    super(error.error.message);
    this.name = 'ApiClientError';
  }

  get code() {
    return this.error.error.code;
  }

  get fields() {
    return this.error.error.fields;
  }
}

export class NetworkError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'NetworkError';
  }
}

export const apiClient = new ApiClient();
