# Component API: Frontend Redesign & Experience Enhancement

**Feature**: 001-frontend-redesign | **Date**: 2026-02-18 | **Version**: 1.0.0

## Purpose

This document defines the public API for all reusable components in the Frontend Redesign feature. It specifies props, events, slots, and usage patterns for consistent component usage across the application.

---

## Component Categories

1. **UI Components**: Base building blocks (Button, Input, Card, etc.)
2. **Landing Components**: Landing page specific components
3. **Auth Components**: Authentication flow components
4. **Personalization Components**: Personalization flow components
5. **Layout Components**: Header, Footer, Navigation
6. **Effect Components**: Neural network, glassmorphism effects

---

## UI Components

### Button

**Location**: `components/ui/Button.tsx`

**Props**:
```typescript
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  loading?: boolean;
  fullWidth?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  onClick?: (event: React.MouseEvent<HTMLButtonElement>) => void;
  type?: 'button' | 'submit' | 'reset';
  children: React.ReactNode;
  className?: string;
  'aria-label'?: string;
}
```

**Usage**:
```tsx
<Button variant="primary" size="lg" onClick={handleClick}>
  Get Started
</Button>

<Button variant="secondary" leftIcon={<ArrowIcon />} loading>
  Loading...
</Button>
```

**Accessibility**:
- Keyboard accessible (Enter/Space)
- Focus visible indicator
- Disabled state announced to screen readers
- Loading state announced with aria-live

---

### Input

**Location**: `components/ui/Input.tsx`

**Props**:
```typescript
interface InputProps {
  type?: 'text' | 'email' | 'password' | 'number';
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  label?: string;
  error?: string;
  disabled?: boolean;
  required?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  className?: string;
  'aria-label'?: string;
  'aria-describedby'?: string;
}
```

**Usage**:
```tsx
<Input
  type="email"
  value={email}
  onChange={setEmail}
  label="Email Address"
  placeholder="you@example.com"
  error={errors.email}
  required
/>
```

**Accessibility**:
- Label associated with input
- Error messages announced
- Required fields indicated
- Placeholder not used as label

---

### Card

**Location**: `components/ui/Card.tsx`

**Props**:
```typescript
interface CardProps {
  variant?: 'default' | 'glass' | 'elevated';
  padding?: 'none' | 'sm' | 'md' | 'lg';
  hover?: boolean;
  onClick?: () => void;
  children: React.ReactNode;
  className?: string;
}
```

**Usage**:
```tsx
<Card variant="glass" padding="lg" hover>
  <h3>Card Title</h3>
  <p>Card content goes here</p>
</Card>
```

**Variants**:
- `default`: Solid background with border
- `glass`: Glassmorphism effect with backdrop-filter
- `elevated`: Shadow elevation without glass effect

---

### Slider

**Location**: `components/ui/Slider.tsx`

**Props**:
```typescript
interface SliderProps {
  value: number;
  onChange: (value: number) => void;
  min: number;
  max: number;
  step?: number;
  label?: string;
  showValue?: boolean;
  marks?: { value: number; label: string }[];
  disabled?: boolean;
  className?: string;
  'aria-label'?: string;
}
```

**Usage**:
```tsx
<Slider
  value={weeklyCommitment}
  onChange={setWeeklyCommitment}
  min={1}
  max={20}
  step={1}
  label="Weekly Commitment (hours)"
  showValue
  marks={[
    { value: 1, label: '1h' },
    { value: 10, label: '10h' },
    { value: 20, label: '20h' },
  ]}
/>
```

**Accessibility**:
- Keyboard accessible (Arrow keys)
- Value announced to screen readers
- Min/max values indicated
- Step increment announced

---

### Modal

**Location**: `components/ui/Modal.tsx`

**Props**:
```typescript
interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  closeOnOverlayClick?: boolean;
  closeOnEscape?: boolean;
  children: React.ReactNode;
  footer?: React.ReactNode;
  className?: string;
}
```

**Usage**:
```tsx
<Modal
  isOpen={isOpen}
  onClose={handleClose}
  title="Confirm Action"
  size="md"
  footer={
    <>
      <Button variant="ghost" onClick={handleClose}>Cancel</Button>
      <Button variant="primary" onClick={handleConfirm}>Confirm</Button>
    </>
  }
>
  <p>Are you sure you want to proceed?</p>
</Modal>
```

**Accessibility**:
- Focus trapped within modal
- Escape key closes modal
- Focus returned to trigger on close
- Overlay click closes modal (configurable)
- aria-modal and role="dialog"

---

## Landing Components

### Hero

**Location**: `components/landing/Hero.tsx`

**Props**:
```typescript
interface HeroProps {
  title: string;
  subtitle: string;
  ctaText: string;
  ctaHref: string;
  showRobot?: boolean;
  className?: string;
}
```

**Usage**:
```tsx
<Hero
  title="Master Physical AI & Humanoid Robotics"
  subtitle="Learn cutting-edge robotics with AI-powered guidance"
  ctaText="Start Learning"
  ctaHref="/auth/register"
  showRobot
/>
```

**Features**:
- Animated gradient background
- Neural network pattern overlay
- 3D robot model (desktop) or 2D illustration (mobile)
- Responsive typography scaling

---

### FeatureCard

**Location**: `components/landing/FeatureCard.tsx`

**Props**:
```typescript
interface FeatureCardProps {
  icon: React.ReactNode;
  title: string;
  description: string;
  href?: string;
  className?: string;
}
```

**Usage**:
```tsx
<FeatureCard
  icon={<RobotIcon />}
  title="Hands-On Projects"
  description="Build real robots with step-by-step guidance"
  href="/learn/projects"
/>
```

**Features**:
- Glass card effect
- Hover animation
- Icon with accent glow
- Optional link navigation

---

### TestimonialCarousel

**Location**: `components/landing/TestimonialCarousel.tsx`

**Props**:
```typescript
interface TestimonialCarouselProps {
  testimonials: Array<{
    id: string;
    name: string;
    role: string;
    image: string;
    quote: string;
  }>;
  autoplay?: boolean;
  interval?: number;
  className?: string;
}
```

**Usage**:
```tsx
<TestimonialCarousel
  testimonials={testimonials}
  autoplay
  interval={5000}
/>
```

**Features**:
- Auto-rotating carousel
- Swipe gestures on mobile
- Keyboard navigation
- Pause on hover

---

## Auth Components

### LoginForm

**Location**: `components/auth/LoginForm.tsx`

**Props**:
```typescript
interface LoginFormProps {
  onSuccess?: (user: User) => void;
  onError?: (error: Error) => void;
  redirectTo?: string;
  className?: string;
}
```

**Usage**:
```tsx
<LoginForm
  onSuccess={(user) => console.log('Logged in:', user)}
  redirectTo="/personalization"
/>
```

**Features**:
- Email and password validation
- Show/hide password toggle
- Remember me checkbox
- Error message display
- Loading state during submission

---

### RegisterForm

**Location**: `components/auth/RegisterForm.tsx`

**Props**:
```typescript
interface RegisterFormProps {
  onSuccess?: (user: User) => void;
  onError?: (error: Error) => void;
  redirectTo?: string;
  className?: string;
}
```

**Usage**:
```tsx
<RegisterForm
  onSuccess={(user) => console.log('Registered:', user)}
  redirectTo="/personalization"
/>
```

**Features**:
- Email, password, and name validation
- Password strength indicator
- Terms of service checkbox
- Error message display
- Loading state during submission

---

### SocialAuthButtons

**Location**: `components/auth/SocialAuthButtons.tsx`

**Props**:
```typescript
interface SocialAuthButtonsProps {
  providers: Array<'google' | 'github' | 'microsoft'>;
  onSuccess?: (user: User) => void;
  onError?: (error: Error) => void;
  className?: string;
}
```

**Usage**:
```tsx
<SocialAuthButtons
  providers={['google', 'github']}
  onSuccess={(user) => console.log('Logged in:', user)}
/>
```

**Features**:
- OAuth provider buttons
- Loading states
- Error handling
- Redirect after success

---

## Personalization Components

### PersonalizationWizard

**Location**: `components/personalization/PersonalizationWizard.tsx`

**Props**:
```typescript
interface PersonalizationWizardProps {
  onComplete?: (preferences: PersonalizationPreferences) => void;
  onSkip?: () => void;
  initialStep?: number;
  className?: string;
}
```

**Usage**:
```tsx
<PersonalizationWizard
  onComplete={(prefs) => console.log('Completed:', prefs)}
  onSkip={() => router.push('/learn')}
/>
```

**Features**:
- Multi-step wizard (4 steps)
- Progress indicator
- Step validation
- Back/Next navigation
- Skip option

---

### LearningGoalSelector

**Location**: `components/personalization/LearningGoalSelector.tsx`

**Props**:
```typescript
interface LearningGoalSelectorProps {
  value: LearningGoal | null;
  onChange: (goal: LearningGoal) => void;
  error?: string;
  className?: string;
}
```

**Usage**:
```tsx
<LearningGoalSelector
  value={learningGoal}
  onChange={setLearningGoal}
  error={errors.learningGoal}
/>
```

**Features**:
- Card-based selection
- Icon for each goal
- Description text
- Single selection
- Keyboard navigation

---

### ExperienceLevelSelector

**Location**: `components/personalization/ExperienceLevelSelector.tsx`

**Props**:
```typescript
interface ExperienceLevelSelectorProps {
  value: ExperienceLevel | null;
  onChange: (level: ExperienceLevel) => void;
  error?: string;
  className?: string;
}
```

**Usage**:
```tsx
<ExperienceLevelSelector
  value={experienceLevel}
  onChange={setExperienceLevel}
  error={errors.experienceLevel}
/>
```

**Features**:
- Card-based selection
- Visual level indicator
- Description text
- Single selection
- Keyboard navigation

---

### InterestTagSelector

**Location**: `components/personalization/InterestTagSelector.tsx`

**Props**:
```typescript
interface InterestTagSelectorProps {
  value: string[];
  onChange: (interests: string[]) => void;
  maxSelections?: number;
  availableTags: string[];
  error?: string;
  className?: string;
}
```

**Usage**:
```tsx
<InterestTagSelector
  value={interests}
  onChange={setInterests}
  maxSelections={10}
  availableTags={['robotics', 'ai', 'computer-vision', 'ros2']}
  error={errors.interests}
/>
```

**Features**:
- Multi-select tags
- Max selection limit
- Visual selection state
- Keyboard navigation
- Search/filter tags

---

## Layout Components

### Header

**Location**: `components/layout/Header.tsx`

**Props**:
```typescript
interface HeaderProps {
  transparent?: boolean;
  showAuth?: boolean;
  className?: string;
}
```

**Usage**:
```tsx
<Header transparent showAuth />
```

**Features**:
- Logo with link to home
- Navigation menu
- Auth buttons (Login/Register or User menu)
- Mobile hamburger menu
- Sticky on scroll

---

### Footer

**Location**: `components/layout/Footer.tsx`

**Props**:
```typescript
interface FooterProps {
  className?: string;
}
```

**Usage**:
```tsx
<Footer />
```

**Features**:
- Links to important pages
- Social media icons
- Copyright notice
- Newsletter signup (optional)

---

### MobileMenu

**Location**: `components/layout/MobileMenu.tsx`

**Props**:
```typescript
interface MobileMenuProps {
  isOpen: boolean;
  onClose: () => void;
  links: Array<{ label: string; href: string }>;
  className?: string;
}
```

**Usage**:
```tsx
<MobileMenu
  isOpen={isMenuOpen}
  onClose={() => setIsMenuOpen(false)}
  links={[
    { label: 'Home', href: '/' },
    { label: 'Learn', href: '/learn' },
    { label: 'About', href: '/about' },
  ]}
/>
```

**Features**:
- Slide-in animation
- Overlay backdrop
- Close on link click
- Close on escape key
- Focus trap

---

## Effect Components

### NeuralNetworkBackground

**Location**: `components/effects/NeuralNetworkBackground.tsx`

**Props**:
```typescript
interface NeuralNetworkBackgroundProps {
  variant?: 'canvas' | 'svg' | 'css';
  animated?: boolean;
  opacity?: number;
  nodeCount?: number;
  connectionCount?: number;
  className?: string;
}
```

**Usage**:
```tsx
<NeuralNetworkBackground
  variant="canvas"
  animated
  opacity={0.1}
  nodeCount={50}
  connectionCount={100}
/>
```

**Features**:
- Multiple rendering variants (Canvas/SVG/CSS)
- Animated flowing connections
- Responsive to mouse movement (desktop)
- Performance optimized for mobile
- Pause when tab inactive

---

### GlassCard

**Location**: `components/effects/GlassCard.tsx`

**Props**:
```typescript
interface GlassCardProps {
  blur?: 'sm' | 'md' | 'lg';
  opacity?: number;
  border?: boolean;
  children: React.ReactNode;
  className?: string;
}
```

**Usage**:
```tsx
<GlassCard blur="md" opacity={0.7} border>
  <h3>Glass Effect Card</h3>
  <p>Content with glassmorphism effect</p>
</GlassCard>
```

**Features**:
- Backdrop-filter blur effect
- Fallback for unsupported browsers
- Customizable blur intensity
- Optional border
- Hover effects

---

### Robot3D

**Location**: `components/effects/Robot3D.tsx`

**Props**:
```typescript
interface Robot3DProps {
  autoRotate?: boolean;
  interactive?: boolean;
  scale?: number;
  position?: [number, number, number];
  className?: string;
}
```

**Usage**:
```tsx
<Robot3D
  autoRotate
  interactive
  scale={1.5}
  position={[0, 0, 0]}
/>
```

**Features**:
- React Three Fiber rendering
- Auto-rotation animation
- Mouse interaction (orbit controls)
- Lazy loaded
- 2D fallback for mobile

---

### Robot2D

**Location**: `components/effects/Robot2D.tsx`

**Props**:
```typescript
interface Robot2DProps {
  animated?: boolean;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}
```

**Usage**:
```tsx
<Robot2D animated size="lg" />
```

**Features**:
- SVG illustration
- Optional subtle animation
- Responsive sizing
- Lightweight fallback for 3D

---

## Composition Patterns

### Page Layout Pattern

```tsx
import { Header, Footer } from '@/components/layout';
import { NeuralNetworkBackground } from '@/components/effects';

export default function Page() {
  return (
    <>
      <NeuralNetworkBackground variant="canvas" animated opacity={0.1} />
      <Header transparent showAuth />
      <main className="min-h-screen">
        {/* Page content */}
      </main>
      <Footer />
    </>
  );
}
```

### Form with Validation Pattern

```tsx
import { Input, Button } from '@/components/ui';
import { useState } from 'react';

export default function MyForm() {
  const [values, setValues] = useState({ email: '', password: '' });
  const [errors, setErrors] = useState({});

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    // Validation and submission logic
  };

  return (
    <form onSubmit={handleSubmit}>
      <Input
        type="email"
        value={values.email}
        onChange={(v) => setValues({ ...values, email: v })}
        label="Email"
        error={errors.email}
        required
      />
      <Input
        type="password"
        value={values.password}
        onChange={(v) => setValues({ ...values, password: v })}
        label="Password"
        error={errors.password}
        required
      />
      <Button type="submit" variant="primary" fullWidth>
        Submit
      </Button>
    </form>
  );
}
```

### Modal with Confirmation Pattern

```tsx
import { Modal, Button } from '@/components/ui';
import { useState } from 'react';

export default function DeleteButton() {
  const [isOpen, setIsOpen] = useState(false);

  const handleDelete = async () => {
    // Delete logic
    setIsOpen(false);
  };

  return (
    <>
      <Button variant="outline" onClick={() => setIsOpen(true)}>
        Delete
      </Button>
      <Modal
        isOpen={isOpen}
        onClose={() => setIsOpen(false)}
        title="Confirm Deletion"
        footer={
          <>
            <Button variant="ghost" onClick={() => setIsOpen(false)}>
              Cancel
            </Button>
            <Button variant="primary" onClick={handleDelete}>
              Delete
            </Button>
          </>
        }
      >
        <p>Are you sure you want to delete this item?</p>
      </Modal>
    </>
  );
}
```

---

## Testing Components

### Unit Test Example

```typescript
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

  it('is disabled when disabled prop is true', () => {
    render(<Button disabled>Click me</Button>);
    expect(screen.getByText('Click me')).toBeDisabled();
  });
});
```

### Accessibility Test Example

```typescript
import { render } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
import { Input } from '@/components/ui/Input';

expect.extend(toHaveNoViolations);

describe('Input Accessibility', () => {
  it('has no accessibility violations', async () => {
    const { container } = render(
      <Input
        value=""
        onChange={() => {}}
        label="Email"
        placeholder="you@example.com"
      />
    );
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
```

---

**Component API Status**: ✅ Complete
**Next Step**: Create theme-api.md and quickstart.md
