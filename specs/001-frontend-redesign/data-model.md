# Data Model: Frontend Redesign & Experience Enhancement

**Feature**: 001-frontend-redesign | **Date**: 2026-02-18 | **Phase**: 1 (Design)

## Purpose

This document defines the data structures, state management, and data flow for the Frontend Redesign feature. It focuses on personalization preferences, user session state, and theme configuration.

---

## Data Entities

### 1. User Personalization Preferences

**Storage**: Backend API (PostgreSQL)
**Access**: Authenticated users only
**Lifecycle**: Persists across sessions

```typescript
interface PersonalizationPreferences {
  userId: string;                    // Foreign key to user table
  learningGoal: LearningGoal;        // Primary learning objective
  experienceLevel: ExperienceLevel;  // Current skill level
  weeklyCommitment: number;          // Hours per week (1-20)
  interests: string[];               // Selected interest tags
  preferredLanguage: string;         // ISO 639-1 code (e.g., 'en', 'ur')
  createdAt: Date;                   // Timestamp of creation
  updatedAt: Date;                   // Timestamp of last update
}

enum LearningGoal {
  CAREER_TRANSITION = 'career_transition',
  ACADEMIC_RESEARCH = 'academic_research',
  HOBBY_PROJECT = 'hobby_project',
  SKILL_ENHANCEMENT = 'skill_enhancement',
}

enum ExperienceLevel {
  BEGINNER = 'beginner',           // No prior robotics experience
  INTERMEDIATE = 'intermediate',   // Some programming/robotics basics
  ADVANCED = 'advanced',           // Experienced in robotics/AI
}
```

**Validation Rules**:
- `userId`: Required, must exist in users table
- `learningGoal`: Required, must be one of enum values
- `experienceLevel`: Required, must be one of enum values
- `weeklyCommitment`: Required, integer between 1 and 20
- `interests`: Optional, array of strings (max 10 items, each max 50 chars)
- `preferredLanguage`: Required, must be valid ISO 639-1 code
- `createdAt`: Auto-generated on insert
- `updatedAt`: Auto-updated on modification

**Default Values**:
```typescript
const DEFAULT_PREFERENCES: Partial<PersonalizationPreferences> = {
  weeklyCommitment: 5,
  interests: [],
  preferredLanguage: 'en',
};
```

---

### 2. User Session State

**Storage**: Client-side (React Context + Better Auth)
**Access**: Current session only
**Lifecycle**: Cleared on logout

```typescript
interface UserSession {
  user: User | null;                 // User profile from Better Auth
  isAuthenticated: boolean;          // Authentication status
  preferences: PersonalizationPreferences | null; // Loaded preferences
  hasCompletedPersonalization: boolean; // Onboarding status
  theme: ThemeConfig;                // Current theme settings
}

interface User {
  id: string;                        // User ID from Better Auth
  email: string;                     // User email
  name: string;                      // Display name
  image?: string;                    // Profile picture URL
  createdAt: Date;                   // Account creation date
}
```

**State Management**:
- Managed by React Context (`AuthContext`)
- Initialized on app mount
- Updated on login/logout/preference changes
- Persisted via Better Auth session cookie

---

### 3. Theme Configuration

**Storage**: CSS Custom Properties + Client-side state
**Access**: All users (public)
**Lifecycle**: Persists across sessions (localStorage)

```typescript
interface ThemeConfig {
  mode: ThemeMode;                   // Light or dark mode
  reducedMotion: boolean;            // Accessibility preference
  highContrast: boolean;             // Accessibility preference
  customColors?: Partial<ColorPalette>; // User color overrides
}

enum ThemeMode {
  DARK = 'dark',                     // Default AI Neural Network theme
  LIGHT = 'light',                   // Future: light mode variant
}

interface ColorPalette {
  bgPrimary: string;                 // --color-bg-primary
  bgSecondary: string;               // --color-bg-secondary
  accentCyan: string;                // --color-accent-cyan
  accentViolet: string;              // --color-accent-violet
  accentTeal: string;                // --color-accent-teal
  textPrimary: string;               // --color-text-primary
  textSecondary: string;             // --color-text-secondary
}
```

**Default Theme**:
```typescript
const DEFAULT_THEME: ThemeConfig = {
  mode: ThemeMode.DARK,
  reducedMotion: false,              // Detect from media query
  highContrast: false,
  customColors: undefined,
};

const AI_NEURAL_NETWORK_PALETTE: ColorPalette = {
  bgPrimary: '#1a1a2e',              // Charcoal
  bgSecondary: '#16213e',            // Midnight Blue
  accentCyan: '#00efff',             // Cyan
  accentViolet: '#a855f7',           // Violet
  accentTeal: '#14b8a6',             // Teal
  textPrimary: '#ffffff',            // White
  textSecondary: '#e0e0e0',          // Light Gray
};
```

**Persistence**:
```typescript
// Save to localStorage
localStorage.setItem('theme-config', JSON.stringify(themeConfig));

// Load from localStorage
const savedTheme = localStorage.getItem('theme-config');
const themeConfig = savedTheme ? JSON.parse(savedTheme) : DEFAULT_THEME;
```

---

### 4. Personalization Form State

**Storage**: Client-side (React state)
**Access**: During personalization flow only
**Lifecycle**: Temporary (cleared after submission)

```typescript
interface PersonalizationFormState {
  currentStep: number;               // Current step (1-4)
  learningGoal: LearningGoal | null;
  experienceLevel: ExperienceLevel | null;
  weeklyCommitment: number | null;
  interests: string[];
  preferredLanguage: string;
  errors: Record<string, string>;    // Field-level validation errors
  isSubmitting: boolean;             // Submission in progress
  submitError: string | null;        // Submission error message
}
```

**Step Progression**:
1. **Step 1**: Learning goal selection
2. **Step 2**: Experience level selection
3. **Step 3**: Weekly commitment slider
4. **Step 4**: Interests and language selection

**Validation**:
```typescript
interface ValidationResult {
  isValid: boolean;
  errors: Record<string, string>;
}

function validateStep(step: number, state: PersonalizationFormState): ValidationResult {
  const errors: Record<string, string> = {};

  switch (step) {
    case 1:
      if (!state.learningGoal) {
        errors.learningGoal = 'Please select a learning goal';
      }
      break;
    case 2:
      if (!state.experienceLevel) {
        errors.experienceLevel = 'Please select your experience level';
      }
      break;
    case 3:
      if (!state.weeklyCommitment || state.weeklyCommitment < 1 || state.weeklyCommitment > 20) {
        errors.weeklyCommitment = 'Please select a commitment between 1-20 hours';
      }
      break;
    case 4:
      if (state.interests.length > 10) {
        errors.interests = 'Maximum 10 interests allowed';
      }
      if (!state.preferredLanguage) {
        errors.preferredLanguage = 'Please select a language';
      }
      break;
  }

  return {
    isValid: Object.keys(errors).length === 0,
    errors,
  };
}
```

---

## API Contracts

### 1. Save Personalization Preferences

**Endpoint**: `POST /api/personalization/preferences`
**Authentication**: Required (Bearer token)

**Request**:
```typescript
interface SavePreferencesRequest {
  learningGoal: LearningGoal;
  experienceLevel: ExperienceLevel;
  weeklyCommitment: number;
  interests: string[];
  preferredLanguage: string;
}
```

**Response (Success)**:
```typescript
interface SavePreferencesResponse {
  success: true;
  data: PersonalizationPreferences;
}
```

**Response (Error)**:
```typescript
interface SavePreferencesError {
  success: false;
  error: {
    code: string;                    // Error code (e.g., 'VALIDATION_ERROR')
    message: string;                 // Human-readable error message
    fields?: Record<string, string>; // Field-level errors
  };
}
```

**Status Codes**:
- `200 OK`: Preferences saved successfully
- `400 Bad Request`: Validation error
- `401 Unauthorized`: Not authenticated
- `500 Internal Server Error`: Server error

---

### 2. Get Personalization Preferences

**Endpoint**: `GET /api/personalization/preferences`
**Authentication**: Required (Bearer token)

**Response (Success)**:
```typescript
interface GetPreferencesResponse {
  success: true;
  data: PersonalizationPreferences | null; // null if not set
}
```

**Response (Error)**:
```typescript
interface GetPreferencesError {
  success: false;
  error: {
    code: string;
    message: string;
  };
}
```

**Status Codes**:
- `200 OK`: Preferences retrieved (or null if not set)
- `401 Unauthorized`: Not authenticated
- `500 Internal Server Error`: Server error

---

### 3. Update Personalization Preferences

**Endpoint**: `PATCH /api/personalization/preferences`
**Authentication**: Required (Bearer token)

**Request**:
```typescript
interface UpdatePreferencesRequest {
  learningGoal?: LearningGoal;
  experienceLevel?: ExperienceLevel;
  weeklyCommitment?: number;
  interests?: string[];
  preferredLanguage?: string;
}
```

**Response**: Same as Save Preferences

**Status Codes**: Same as Save Preferences

---

## State Management Architecture

### React Context Structure

```typescript
// contexts/AuthContext.tsx
interface AuthContextValue {
  session: UserSession;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  register: (email: string, password: string, name: string) => Promise<void>;
  updatePreferences: (preferences: Partial<PersonalizationPreferences>) => Promise<void>;
  refreshSession: () => Promise<void>;
}

// contexts/ThemeContext.tsx
interface ThemeContextValue {
  theme: ThemeConfig;
  setTheme: (theme: Partial<ThemeConfig>) => void;
  toggleMode: () => void;
  applyTheme: () => void; // Apply CSS custom properties
}
```

### Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                        User Actions                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    React Components                          │
│  (Landing, Auth, Personalization, Docusaurus)               │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    React Context                             │
│  (AuthContext, ThemeContext)                                │
└─────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┴─────────────┐
                ▼                           ▼
┌───────────────────────────┐   ┌───────────────────────────┐
│    Better Auth Client     │   │    API Client             │
│  (Session Management)     │   │  (Preferences CRUD)       │
└───────────────────────────┘   └───────────────────────────┘
                │                           │
                ▼                           ▼
┌───────────────────────────┐   ┌───────────────────────────┐
│    Auth Server            │   │    Backend API            │
│  (Better Auth)            │   │  (FastAPI)                │
└───────────────────────────┘   └───────────────────────────┘
                │                           │
                ▼                           ▼
┌───────────────────────────┐   ┌───────────────────────────┐
│    Session Store          │   │    PostgreSQL             │
│  (Cookie/Redis)           │   │  (Preferences)            │
└───────────────────────────┘   └───────────────────────────┘
```

---

## Client-Side State Initialization

### App Mount Sequence

```typescript
// app/layout.tsx (Next.js)
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <ThemeProvider>      {/* 1. Initialize theme from localStorage */}
          <AuthProvider>     {/* 2. Initialize auth from Better Auth */}
            {children}
          </AuthProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}

// ThemeProvider initialization
function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<ThemeConfig>(() => {
    // 1. Load from localStorage
    const saved = localStorage.getItem('theme-config');
    if (saved) return JSON.parse(saved);

    // 2. Detect system preferences
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    return {
      ...DEFAULT_THEME,
      mode: prefersDark ? ThemeMode.DARK : ThemeMode.LIGHT,
      reducedMotion: prefersReducedMotion,
    };
  });

  useEffect(() => {
    // Apply theme to CSS custom properties
    applyTheme(theme);
    // Save to localStorage
    localStorage.setItem('theme-config', JSON.stringify(theme));
  }, [theme]);

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

// AuthProvider initialization
function AuthProvider({ children }: { children: React.ReactNode }) {
  const [session, setSession] = useState<UserSession>({
    user: null,
    isAuthenticated: false,
    preferences: null,
    hasCompletedPersonalization: false,
    theme: DEFAULT_THEME,
  });

  useEffect(() => {
    // 1. Check Better Auth session
    authClient.getSession().then(async (user) => {
      if (user) {
        // 2. Load preferences from API
        const preferences = await fetchPreferences();
        setSession({
          user,
          isAuthenticated: true,
          preferences,
          hasCompletedPersonalization: !!preferences,
          theme: DEFAULT_THEME,
        });
      }
    });
  }, []);

  return (
    <AuthContext.Provider value={{ session, /* ...methods */ }}>
      {children}
    </AuthContext.Provider>
  );
}
```

---

## Data Persistence Strategy

### Client-Side (Browser)

| Data | Storage | Lifetime | Size Limit |
|------|---------|----------|------------|
| Theme Config | localStorage | Permanent | ~1KB |
| Auth Session | Cookie (httpOnly) | Session/Remember | ~4KB |
| Form Draft | sessionStorage | Tab session | ~10KB |

### Server-Side (Backend)

| Data | Storage | Lifetime | Indexing |
|------|---------|----------|----------|
| User Profile | PostgreSQL | Permanent | Primary key: id |
| Preferences | PostgreSQL | Permanent | Foreign key: userId |
| Session | Redis/Cookie | Configurable | Key: sessionId |

---

## Data Migration Strategy

**Current State**: No existing personalization data (new feature)

**Migration Plan**: N/A (new tables)

**Rollback Plan**: Drop personalization tables if needed

**Future Migrations**:
- Add new preference fields: Use nullable columns with defaults
- Change enum values: Create migration script with data transformation
- Split preferences table: Create new table + migrate data + update foreign keys

---

## Privacy & Security Considerations

### Data Classification

| Data | Classification | Encryption | Retention |
|------|---------------|------------|-----------|
| User ID | PII | At rest + transit | Account lifetime |
| Email | PII | At rest + transit | Account lifetime |
| Preferences | Non-PII | Transit only | Account lifetime |
| Session Token | Sensitive | Transit only | Session duration |

### GDPR Compliance

- **Right to Access**: Provide API endpoint to export all user data
- **Right to Erasure**: Cascade delete preferences on account deletion
- **Right to Portability**: Export preferences as JSON
- **Data Minimization**: Only collect necessary preference data

### Security Measures

- **Authentication**: All preference endpoints require valid session
- **Authorization**: Users can only access their own preferences
- **Input Validation**: Validate all inputs on client and server
- **Rate Limiting**: Limit preference updates to 10/minute per user
- **Audit Logging**: Log all preference changes with timestamp and user ID

---

## Testing Strategy

### Unit Tests

```typescript
// Test preference validation
describe('validatePreferences', () => {
  it('should accept valid preferences', () => {
    const prefs = {
      learningGoal: LearningGoal.CAREER_TRANSITION,
      experienceLevel: ExperienceLevel.BEGINNER,
      weeklyCommitment: 10,
      interests: ['robotics', 'ai'],
      preferredLanguage: 'en',
    };
    expect(validatePreferences(prefs)).toEqual({ isValid: true, errors: {} });
  });

  it('should reject invalid weekly commitment', () => {
    const prefs = { /* ... */ weeklyCommitment: 25 };
    const result = validatePreferences(prefs);
    expect(result.isValid).toBe(false);
    expect(result.errors.weeklyCommitment).toBeDefined();
  });
});
```

### Integration Tests

```typescript
// Test API integration
describe('Preferences API', () => {
  it('should save and retrieve preferences', async () => {
    const prefs = { /* valid preferences */ };
    await savePreferences(prefs);
    const retrieved = await getPreferences();
    expect(retrieved).toEqual(expect.objectContaining(prefs));
  });

  it('should return 401 for unauthenticated requests', async () => {
    authClient.logout();
    await expect(savePreferences({})).rejects.toThrow('Unauthorized');
  });
});
```

### E2E Tests

```typescript
// Test personalization flow
test('complete personalization flow', async ({ page }) => {
  await page.goto('/personalization');

  // Step 1: Select learning goal
  await page.click('[data-testid="goal-career"]');
  await page.click('[data-testid="next-button"]');

  // Step 2: Select experience level
  await page.click('[data-testid="level-beginner"]');
  await page.click('[data-testid="next-button"]');

  // Step 3: Set weekly commitment
  await page.fill('[data-testid="commitment-slider"]', '10');
  await page.click('[data-testid="next-button"]');

  // Step 4: Select interests and language
  await page.click('[data-testid="interest-robotics"]');
  await page.selectOption('[data-testid="language-select"]', 'en');
  await page.click('[data-testid="submit-button"]');

  // Verify redirect to Docusaurus
  await expect(page).toHaveURL(/\/learn/);
});
```

---

## Performance Considerations

### Client-Side

- **State Updates**: Use React.memo() for expensive components
- **API Calls**: Debounce preference updates (500ms)
- **localStorage**: Limit writes to prevent blocking main thread
- **Context Re-renders**: Split contexts to minimize re-renders

### Server-Side

- **Database Queries**: Index userId column for fast lookups
- **Caching**: Cache preferences in Redis (5-minute TTL)
- **Batch Updates**: Support bulk preference updates
- **Connection Pooling**: Reuse database connections

---

**Data Model Status**: ✅ Complete
**Next Step**: Create contracts/ directory with API and design token specifications
