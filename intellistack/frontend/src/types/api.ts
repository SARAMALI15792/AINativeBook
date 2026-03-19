// API Types

export interface PersonalizationPreferences {
  userId: string;
  learningGoal: LearningGoal;
  experienceLevel: ExperienceLevel;
  weeklyCommitment: number;
  interests: string[];
  preferredLanguage: string;
  createdAt: string;
  updatedAt: string;
}

export enum LearningGoal {
  CAREER_TRANSITION = 'career_transition',
  ACADEMIC_RESEARCH = 'academic_research',
  HOBBY_PROJECT = 'hobby_project',
  SKILL_ENHANCEMENT = 'skill_enhancement',
}

export enum ExperienceLevel {
  BEGINNER = 'beginner',
  INTERMEDIATE = 'intermediate',
  ADVANCED = 'advanced',
}

export interface UserSession {
  user: User | null;
  isAuthenticated: boolean;
  preferences: PersonalizationPreferences | null;
  hasCompletedPersonalization: boolean;
  theme: ThemeConfig;
}

export interface User {
  id: string;
  email: string;
  name: string;
  image?: string;
  createdAt: string;
}

export interface ThemeConfig {
  mode: ThemeMode;
  reducedMotion: boolean;
  highContrast: boolean;
  customColors?: Partial<ColorPalette>;
}

export enum ThemeMode {
  DARK = 'dark',
  LIGHT = 'light',
}

export interface ColorPalette {
  bgPrimary: string;
  bgSecondary: string;
  accentCyan: string;
  accentViolet: string;
  accentTeal: string;
  textPrimary: string;
  textSecondary: string;
}

// API Request/Response Types

export interface SavePreferencesRequest {
  learningGoal: LearningGoal;
  experienceLevel: ExperienceLevel;
  weeklyCommitment: number;
  interests: string[];
  preferredLanguage: string;
}

export interface SavePreferencesResponse {
  success: true;
  data: PersonalizationPreferences;
}

export interface ApiError {
  success: false;
  error: {
    code: string;
    message: string;
    fields?: Record<string, string>;
  };
}

export interface SignupRequest {
  email: string;
  password: string;
  name: string;
}

export interface SigninRequest {
  email: string;
  password: string;
  rememberMe?: boolean;
}

export interface AuthResponse {
  user: User;
  session: {
    token: string;
    expiresAt: string;
  };
}

// Form State Types

export interface PersonalizationFormState {
  currentStep: number;
  learningGoal: LearningGoal | null;
  experienceLevel: ExperienceLevel | null;
  weeklyCommitment: number | null;
  interests: string[];
  preferredLanguage: string;
  errors: Record<string, string>;
  isSubmitting: boolean;
  submitError: string | null;
}
