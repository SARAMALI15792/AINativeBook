# Developer Quickstart: Frontend Redesign & Experience Enhancement

**Feature**: 001-frontend-redesign | **Date**: 2026-02-18 | **Version**: 1.0.0

## Purpose

This guide helps developers quickly set up, understand, and contribute to the Frontend Redesign feature. It covers environment setup, project structure, development workflow, and common tasks.

---

## Prerequisites

### Required Software

| Tool | Version | Purpose |
|------|---------|---------|
| Node.js | 18.0+ | JavaScript runtime |
| npm or pnpm | 8.0+ / 8.0+ | Package manager |
| Git | 2.30+ | Version control |
| VS Code | Latest | Recommended IDE |

### Recommended VS Code Extensions

- ESLint
- Prettier
- Tailwind CSS IntelliSense
- TypeScript and JavaScript Language Features
- GitLens

---

## Quick Setup (5 minutes)

### 1. Clone and Install

```bash
# Navigate to project root
cd C:\Users\saram\OneDrive\Desktop\physicalhumoniodbook

# Install Next.js frontend dependencies
cd intellistack/frontend
npm install

# Install Docusaurus dependencies
cd ../content
npm install

# Install Auth Server dependencies (if needed)
cd ../auth-server
npm install
```

### 2. Environment Configuration

**Create `.env.local` in `intellistack/frontend/`**:

```env
# Auth Server
NEXT_PUBLIC_AUTH_URL=http://localhost:3001

# Backend API
NEXT_PUBLIC_API_URL=http://localhost:8000

# Docusaurus URL
NEXT_PUBLIC_DOCUSAURUS_URL=http://localhost:3002

# Environment
NODE_ENV=development
```

**Create `.env` in `intellistack/content/`**:

```env
# Auth Server
AUTH_URL=http://localhost:3001

# Environment
NODE_ENV=development
```

### 3. Start Development Servers

**Terminal 1 - Next.js Frontend**:
```bash
cd intellistack/frontend
npm run dev
# Runs on http://localhost:3000
```

**Terminal 2 - Docusaurus**:
```bash
cd intellistack/content
npm run start
# Runs on http://localhost:3002
```

**Terminal 3 - Auth Server** (if not already running):
```bash
cd intellistack/auth-server
npm run dev
# Runs on http://localhost:3001
```

**Terminal 4 - Backend API** (if not already running):
```bash
cd intellistack/backend
# Activate virtual environment and run
uvicorn src.main:app --reload --port 8000
# Runs on http://localhost:8000
```

### 4. Verify Setup

Open browser and check:
- ✅ Next.js: http://localhost:3000
- ✅ Docusaurus: http://localhost:3002
- ✅ Auth Server: http://localhost:3001/api/auth/session
- ✅ Backend API: http://localhost:8000/docs

---

## Project Structure Overview

```
intellistack/
├── frontend/                    # Next.js Application
│   ├── src/
│   │   ├── app/                # App Router pages
│   │   │   ├── page.tsx        # Landing page (/)
│   │   │   ├── auth/
│   │   │   │   ├── login/page.tsx
│   │   │   │   └── register/page.tsx
│   │   │   └── personalization/page.tsx
│   │   ├── components/         # Reusable components
│   │   │   ├── ui/            # Base UI (Button, Input, Card)
│   │   │   ├── landing/       # Landing page components
│   │   │   ├── auth/          # Auth components
│   │   │   ├── personalization/ # Personalization components
│   │   │   ├── layout/        # Header, Footer
│   │   │   └── effects/       # Neural network, glass effects
│   │   ├── contexts/          # React contexts
│   │   │   ├── AuthContext.tsx
│   │   │   └── ThemeContext.tsx
│   │   ├── lib/               # Utilities
│   │   │   ├── api-client.ts  # API client
│   │   │   └── auth.ts        # Better Auth client
│   │   ├── styles/            # Global styles
│   │   │   ├── tokens.css     # Design tokens
│   │   │   ├── globals.css    # Global CSS
│   │   │   └── animations.css # Animations
│   │   └── types/             # TypeScript types
│   ├── public/                # Static assets
│   ├── tests/                 # Tests
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   └── tsconfig.json
│
├── content/                     # Docusaurus
│   ├── src/
│   │   ├── theme/              # Theme customization
│   │   │   ├── Root.tsx        # Theme provider
│   │   │   └── Layout/         # Layout overrides
│   │   └── css/
│   │       └── custom.css      # Custom styles + tokens
│   ├── docs/                   # Content (unchanged)
│   ├── docusaurus.config.ts
│   └── package.json
│
├── auth-server/                 # Better Auth (existing)
└── backend/                     # FastAPI (existing)
```

---

## Development Workflow

### Creating a New Component

**1. Create Component File**

```bash
# Example: Create a new Button component
cd intellistack/frontend/src/components/ui
touch Button.tsx
```

**2. Implement Component**

```tsx
// components/ui/Button.tsx
import React from 'react';

interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
  onClick?: () => void;
  disabled?: boolean;
  className?: string;
}

export function Button({
  variant = 'primary',
  size = 'md',
  children,
  onClick,
  disabled = false,
  className = '',
}: ButtonProps) {
  const baseStyles = 'rounded-md font-semibold transition-all duration-normal';

  const variantStyles = {
    primary: 'bg-accent-cyan text-bg-primary hover:shadow-glow-cyan',
    secondary: 'bg-accent-violet text-white hover:shadow-glow-violet',
    outline: 'border-2 border-accent-cyan text-accent-cyan hover:bg-accent-cyan hover:text-bg-primary',
  };

  const sizeStyles = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  };

  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`${baseStyles} ${variantStyles[variant]} ${sizeStyles[size]} ${className}`}
    >
      {children}
    </button>
  );
}
```

**3. Export from Index**

```tsx
// components/ui/index.ts
export { Button } from './Button';
export { Input } from './Input';
export { Card } from './Card';
// ... other exports
```

**4. Write Tests**

```tsx
// tests/unit/Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from '@/components/ui/Button';

describe('Button', () => {
  it('renders with text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);
    fireEvent.click(screen.getByText('Click me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('applies variant styles', () => {
    render(<Button variant="secondary">Click me</Button>);
    const button = screen.getByText('Click me');
    expect(button).toHaveClass('bg-accent-violet');
  });
});
```

**5. Use in Pages**

```tsx
// app/page.tsx
import { Button } from '@/components/ui';

export default function LandingPage() {
  return (
    <div>
      <Button variant="primary" size="lg">
        Get Started
      </Button>
    </div>
  );
}
```

---

### Creating a New Page

**1. Create Page File**

```bash
cd intellistack/frontend/src/app
mkdir my-page
touch my-page/page.tsx
```

**2. Implement Page**

```tsx
// app/my-page/page.tsx
import { Header, Footer } from '@/components/layout';
import { NeuralNetworkBackground } from '@/components/effects';

export default function MyPage() {
  return (
    <>
      <NeuralNetworkBackground variant="canvas" animated opacity={0.1} />
      <Header transparent showAuth />
      <main className="min-h-screen flex items-center justify-center">
        <div className="container mx-auto px-4">
          <h1 className="text-5xl font-bold text-accent-cyan">My Page</h1>
          <p className="text-text-secondary mt-4">Page content goes here</p>
        </div>
      </main>
      <Footer />
    </>
  );
}
```

**3. Add Metadata**

```tsx
// app/my-page/page.tsx
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'My Page | IntelliStack',
  description: 'Description of my page',
};

export default function MyPage() {
  // ... component code
}
```

**4. Add to Navigation**

```tsx
// components/layout/Header.tsx
const navLinks = [
  { label: 'Home', href: '/' },
  { label: 'My Page', href: '/my-page' },
  { label: 'Learn', href: '/learn' },
];
```

---

### Customizing Docusaurus Theme

**1. Swizzle Component**

```bash
cd intellistack/content
npm run swizzle @docusaurus/theme-classic ComponentName -- --wrap
```

**2. Customize Component**

```tsx
// src/theme/ComponentName/index.tsx
import React from 'react';
import ComponentName from '@theme-original/ComponentName';
import type ComponentNameType from '@theme/ComponentName';
import type {WrapperProps} from '@docusaurus/types';

type Props = WrapperProps<typeof ComponentNameType>;

export default function ComponentNameWrapper(props: Props): JSX.Element {
  return (
    <>
      {/* Add custom elements */}
      <ComponentName {...props} />
    </>
  );
}
```

**3. Update Custom CSS**

```css
/* src/css/custom.css */
.custom-class {
  background: var(--color-bg-primary);
  color: var(--color-text-primary);
}
```

---

## Common Tasks

### Task 1: Add a New Design Token

**1. Update `styles/tokens.css`**

```css
:root {
  /* Add new token */
  --color-accent-orange: #ff6b35;
}
```

**2. Update `tailwind.config.js`**

```javascript
module.exports = {
  theme: {
    extend: {
      colors: {
        'accent-orange': 'var(--color-accent-orange)',
      },
    },
  },
};
```

**3. Update `contracts/design-tokens.json`**

```json
{
  "colors": {
    "accent": {
      "orange": {
        "value": "#ff6b35",
        "description": "Orange - Quaternary accent color",
        "cssVar": "--color-accent-orange"
      }
    }
  }
}
```

**4. Use in Components**

```tsx
<div className="text-accent-orange">Orange text</div>
```

---

### Task 2: Add API Endpoint Integration

**1. Define TypeScript Types**

```typescript
// types/api.ts
export interface MyDataRequest {
  field1: string;
  field2: number;
}

export interface MyDataResponse {
  success: boolean;
  data: {
    id: string;
    field1: string;
    field2: number;
  };
}
```

**2. Add API Client Method**

```typescript
// lib/api-client.ts
class ApiClient {
  async getMyData(): Promise<MyDataResponse> {
    return this.request(`${this.baseUrl}/api/v1/my-data`);
  }

  async createMyData(data: MyDataRequest): Promise<MyDataResponse> {
    return this.request(`${this.baseUrl}/api/v1/my-data`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
}
```

**3. Use in Component**

```tsx
import { apiClient } from '@/lib/api-client';
import { useState, useEffect } from 'react';

export function MyComponent() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiClient.getMyData()
      .then(response => setData(response.data))
      .catch(error => console.error(error))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div>Loading...</div>;

  return <div>{JSON.stringify(data)}</div>;
}
```

---

### Task 3: Add Animation

**1. Define Animation in CSS**

```css
/* styles/animations.css */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in-up {
  animation: fadeInUp var(--duration-normal) var(--ease-out);
}
```

**2. Use in Component**

```tsx
<div className="animate-fade-in-up">
  Content with fade-in animation
</div>
```

**3. Use Framer Motion (Alternative)**

```tsx
import { motion } from 'framer-motion';

export function AnimatedComponent() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      Content with fade-in animation
    </motion.div>
  );
}
```

---

### Task 4: Add Form with Validation

**1. Install React Hook Form + Zod**

```bash
npm install react-hook-form zod @hookform/resolvers
```

**2. Define Validation Schema**

```typescript
// lib/validation.ts
import { z } from 'zod';

export const myFormSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  name: z.string().min(2, 'Name must be at least 2 characters'),
});

export type MyFormData = z.infer<typeof myFormSchema>;
```

**3. Create Form Component**

```tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { myFormSchema, MyFormData } from '@/lib/validation';
import { Input, Button } from '@/components/ui';

export function MyForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<MyFormData>({
    resolver: zodResolver(myFormSchema),
  });

  const onSubmit = async (data: MyFormData) => {
    console.log('Form data:', data);
    // Submit to API
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <Input
        {...register('email')}
        type="email"
        label="Email"
        error={errors.email?.message}
      />
      <Input
        {...register('password')}
        type="password"
        label="Password"
        error={errors.password?.message}
      />
      <Input
        {...register('name')}
        type="text"
        label="Name"
        error={errors.name?.message}
      />
      <Button type="submit" variant="primary" fullWidth>
        Submit
      </Button>
    </form>
  );
}
```

---

## Testing

### Run Unit Tests

```bash
cd intellistack/frontend
npm run test
```

### Run E2E Tests

```bash
cd intellistack/frontend
npm run test:e2e
```

### Run Accessibility Tests

```bash
cd intellistack/frontend
npm run test:a11y
```

### Run Lighthouse Audit

```bash
cd intellistack/frontend
npm run lighthouse
```

---

## Building for Production

### Build Next.js

```bash
cd intellistack/frontend
npm run build
npm run start  # Test production build locally
```

### Build Docusaurus

```bash
cd intellistack/content
npm run build
npm run serve  # Test production build locally
```

---

## Troubleshooting

### Issue: Port Already in Use

**Solution**:
```bash
# Find process using port 3000
netstat -ano | findstr :3000

# Kill process (Windows)
taskkill /PID <PID> /F

# Or use different port
PORT=3001 npm run dev
```

### Issue: Module Not Found

**Solution**:
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Issue: TypeScript Errors

**Solution**:
```bash
# Restart TypeScript server in VS Code
# Ctrl+Shift+P -> "TypeScript: Restart TS Server"

# Or rebuild types
npm run build
```

### Issue: Styles Not Updating

**Solution**:
```bash
# Clear Next.js cache
rm -rf .next

# Restart dev server
npm run dev
```

### Issue: Auth Session Not Persisting

**Solution**:
- Check cookie domain in `.env.local`
- Ensure `credentials: 'include'` in fetch requests
- Verify auth server is running
- Check browser console for CORS errors

---

## Code Style Guidelines

### TypeScript

- Use TypeScript for all new code
- Define interfaces for all props and data structures
- Avoid `any` type - use `unknown` if type is truly unknown
- Use type inference where possible

### React

- Use functional components with hooks
- Prefer named exports over default exports for components
- Use React.memo() for expensive components
- Keep components small and focused (< 200 lines)

### CSS

- Use Tailwind utility classes first
- Use CSS modules for component-specific styles
- Use CSS custom properties for theming
- Follow BEM naming for custom classes

### File Naming

- Components: PascalCase (e.g., `Button.tsx`)
- Utilities: camelCase (e.g., `apiClient.ts`)
- Pages: lowercase with hyphens (e.g., `my-page/page.tsx`)
- Tests: `*.test.tsx` or `*.spec.tsx`

---

## Useful Commands

```bash
# Development
npm run dev              # Start dev server
npm run build            # Build for production
npm run start            # Start production server
npm run lint             # Run ESLint
npm run format           # Run Prettier

# Testing
npm run test             # Run unit tests
npm run test:watch       # Run tests in watch mode
npm run test:e2e         # Run E2E tests
npm run test:a11y        # Run accessibility tests

# Code Quality
npm run type-check       # Run TypeScript compiler
npm run lighthouse       # Run Lighthouse audit

# Utilities
npm run clean            # Clean build artifacts
npm run analyze          # Analyze bundle size
```

---

## Getting Help

### Documentation

- **Specification**: `specs/001-frontend-redesign/spec.md`
- **Architecture Plan**: `specs/001-frontend-redesign/plan.md`
- **Data Model**: `specs/001-frontend-redesign/data-model.md`
- **API Contracts**: `specs/001-frontend-redesign/contracts/api-contracts.md`
- **Component API**: `specs/001-frontend-redesign/contracts/component-api.md`
- **Theme API**: `specs/001-frontend-redesign/contracts/theme-api.md`
- **Design Tokens**: `specs/001-frontend-redesign/contracts/design-tokens.json`

### External Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Docusaurus Documentation](https://docusaurus.io/docs)
- [Better Auth Documentation](https://better-auth.com/docs)
- [Framer Motion Documentation](https://www.framer.com/motion/)
- [React Three Fiber Documentation](https://docs.pmnd.rs/react-three-fiber)

### Team Communication

- Ask questions in team chat
- Create GitHub issues for bugs
- Submit pull requests for features
- Review code with team members

---

## Next Steps

1. ✅ Complete environment setup
2. ✅ Explore project structure
3. ✅ Read specification and architecture documents
4. ✅ Run development servers
5. ✅ Create your first component
6. ✅ Write tests for your component
7. ✅ Submit pull request

**Welcome to the team! Happy coding! 🚀**

---

**Quickstart Status**: ✅ Complete
**Last Updated**: 2026-02-18
