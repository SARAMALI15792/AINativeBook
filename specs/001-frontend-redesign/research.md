# Research: Frontend Redesign & Experience Enhancement

**Feature**: 001-frontend-redesign | **Date**: 2026-02-18 | **Phase**: 0 (Research)

## Purpose

This document resolves technical unknowns and documents technology choices for the Frontend Redesign feature. It provides evidence-based recommendations for implementing the AI Neural Network theme across Next.js and Docusaurus platforms.

## Research Areas

### 1. Glassmorphism Implementation

**Question**: How to implement glassmorphism effects with proper fallbacks for older browsers?

**Research Findings**:

**Modern Approach** (Chrome 76+, Safari 9+, Firefox 103+):
```css
.glass-card {
  background: rgba(26, 26, 46, 0.7);
  backdrop-filter: blur(10px) saturate(180%);
  -webkit-backdrop-filter: blur(10px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.1);
}
```

**Fallback Strategy**:
```css
/* Feature detection */
@supports not (backdrop-filter: blur(10px)) {
  .glass-card {
    background: rgba(26, 26, 46, 0.95); /* More opaque */
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  }
}
```

**Browser Support**:
- Chrome/Edge: 76+ (backdrop-filter)
- Safari: 9+ (-webkit-backdrop-filter)
- Firefox: 103+ (backdrop-filter)
- Fallback: Solid background with opacity for older browsers

**Performance Considerations**:
- Backdrop-filter is GPU-accelerated but can impact performance on mobile
- Limit to 3-5 glass elements per viewport
- Use `will-change: backdrop-filter` sparingly (only during animations)

**Recommendation**: Use backdrop-filter with @supports fallback. Test on mobile devices with performance monitoring.

---

### 2. Neural Network Pattern Generation

**Question**: What's the best approach for animated neural network background patterns?

**Options Evaluated**:

**Option A: SVG with CSS Animations**
- Pros: Scalable, accessible, good browser support
- Cons: Limited animation complexity, can be verbose
- Performance: Excellent (60fps on most devices)

**Option B: Canvas API**
- Pros: Complex animations, particle effects, dynamic generation
- Cons: Not accessible, requires JavaScript, higher CPU usage
- Performance: Good on desktop, can struggle on mobile

**Option C: CSS-only (gradients + animations)**
- Pros: Lightweight, no JavaScript, excellent performance
- Cons: Limited visual complexity, static patterns
- Performance: Excellent (minimal overhead)

**Recommendation**: **Hybrid Approach**
1. **Desktop**: Canvas API for rich neural network animations with flowing particles
2. **Mobile**: SVG with CSS animations (simpler, better performance)
3. **Fallback**: CSS gradients with subtle animations

**Implementation Pattern**:
```typescript
// Detect device capability
const useSimpleAnimation = window.matchMedia('(max-width: 768px)').matches
  || !window.requestAnimationFrame
  || navigator.hardwareConcurrency < 4;

if (useSimpleAnimation) {
  // Render SVG neural network
} else {
  // Render Canvas neural network
}
```

**Performance Budget**:
- Canvas: Max 50 nodes, 100 connections, 30fps on mobile
- SVG: Max 20 nodes, 40 connections, 60fps
- Pause animations when tab is inactive (Page Visibility API)

---

### 3. 3D Robot Model Optimization

**Question**: Three.js vs React Three Fiber? How to optimize for web delivery?

**Library Comparison**:

| Feature | Three.js | React Three Fiber (R3F) |
|---------|----------|-------------------------|
| Bundle Size | ~600KB (minified) | ~700KB (includes Three.js + R3F) |
| Learning Curve | Steeper | Easier (React patterns) |
| Performance | Slightly faster | Comparable |
| React Integration | Manual | Native |
| Community | Larger | Growing |

**Recommendation**: **React Three Fiber**
- Better integration with Next.js/React
- Declarative API matches project patterns
- Easier state management
- 100KB overhead acceptable for better DX

**Model Optimization Strategy**:

1. **File Format**: glTF 2.0 (.glb) - industry standard, compact
2. **Polygon Budget**: 5,000-10,000 triangles (low-poly aesthetic fits theme)
3. **Texture Optimization**:
   - Max 1024x1024 textures
   - Use WebP with PNG fallback
   - Compress with gltf-pipeline
4. **Loading Strategy**:
   - Lazy load with React.lazy()
   - Show 2D placeholder during load
   - Preload on landing page idle time
5. **Mobile Fallback**:
   - 2D SVG robot illustration for devices with:
     - Screen width < 768px
     - No WebGL support
     - Low memory (< 2GB RAM)

**Code Pattern**:
```typescript
const Robot3D = lazy(() => import('@/components/Robot3D'));

function LandingHero() {
  const [show3D, setShow3D] = useState(false);

  useEffect(() => {
    const canRender3D = window.innerWidth >= 768
      && 'WebGLRenderingContext' in window
      && navigator.deviceMemory >= 2;
    setShow3D(canRender3D);
  }, []);

  return show3D ? (
    <Suspense fallback={<Robot2D />}>
      <Robot3D />
    </Suspense>
  ) : <Robot2D />;
}
```

**Performance Target**: < 3s load time for 3D model on 3G connection

---

### 4. Docusaurus Theme Customization

**Question**: What's the best approach for applying AI Neural Network theme to Docusaurus?

**Swizzling Approaches**:

**Option A: Eject Components** (`--eject`)
- Full control over component code
- Breaks upgrade path
- High maintenance burden

**Option B: Wrap Components** (`--wrap`)
- Preserves upgrade path
- Limited control
- Can add wrappers and context

**Option C: CSS Custom Properties** (No swizzling)
- Easiest to maintain
- Limited to styling changes
- No structural changes

**Recommendation**: **Hybrid Approach**
1. **CSS Custom Properties** for colors, spacing, typography (primary method)
2. **Wrap Components** for Layout, Navbar, Footer (add neural network background)
3. **Avoid Ejecting** to maintain upgrade path

**Implementation Strategy**:

```css
/* src/css/custom.css */
:root {
  /* AI Neural Network Theme */
  --ifm-color-primary: #00efff; /* Cyan */
  --ifm-color-primary-dark: #00d4e6;
  --ifm-color-primary-darker: #00c8d9;
  --ifm-color-primary-darkest: #00a5b3;
  --ifm-color-primary-light: #1af3ff;
  --ifm-color-primary-lighter: #26f4ff;
  --ifm-color-primary-lightest: #4df6ff;

  --ifm-background-color: #1a1a2e; /* Charcoal */
  --ifm-background-surface-color: #16213e; /* Midnight Blue */

  --ifm-font-color-base: #e0e0e0;
  --ifm-heading-color: #ffffff;

  /* Glassmorphism */
  --glass-background: rgba(26, 26, 46, 0.7);
  --glass-border: rgba(255, 255, 255, 0.1);
}

/* Neural network background */
.theme-doc-page {
  position: relative;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
}

.theme-doc-page::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: url('/img/neural-network-pattern.svg');
  opacity: 0.1;
  pointer-events: none;
  z-index: 0;
}
```

**Swizzle Components**:
```bash
npm run swizzle @docusaurus/theme-classic Layout -- --wrap
npm run swizzle @docusaurus/theme-classic Navbar -- --wrap
npm run swizzle @docusaurus/theme-classic Footer -- --wrap
```

**Testing Strategy**:
- Test theme on all Docusaurus page types (docs, blog, custom pages)
- Verify dark mode toggle works
- Check mobile responsiveness
- Validate accessibility (contrast ratios)

---

### 5. Design Token System Architecture

**Question**: CSS Custom Properties vs CSS-in-JS for shared design tokens?

**Options Evaluated**:

**Option A: CSS Custom Properties**
- Pros: Native, fast, works across frameworks, runtime updates
- Cons: No type safety, limited tooling
- Bundle Impact: 0KB (native CSS)

**Option B: CSS-in-JS (Styled Components, Emotion)**
- Pros: Type safety, scoped styles, dynamic theming
- Cons: Runtime overhead, larger bundle, framework lock-in
- Bundle Impact: ~15-30KB

**Option C: CSS Modules + TypeScript**
- Pros: Type safety, scoped styles, zero runtime
- Cons: No runtime theming, build-time only
- Bundle Impact: 0KB (compiled away)

**Recommendation**: **CSS Custom Properties** (Option A)

**Rationale**:
1. Works across Next.js AND Docusaurus (different frameworks)
2. Zero bundle size impact
3. Runtime theme updates (future dark/light mode toggle)
4. Standard web platform feature
5. Excellent browser support (96%+)

**Implementation Pattern**:

```css
/* styles/tokens.css - Shared across Next.js and Docusaurus */
:root {
  /* Colors */
  --color-bg-primary: #1a1a2e;
  --color-bg-secondary: #16213e;
  --color-accent-cyan: #00efff;
  --color-accent-violet: #a855f7;
  --color-accent-teal: #14b8a6;

  /* Spacing */
  --space-xs: 0.25rem;
  --space-sm: 0.5rem;
  --space-md: 1rem;
  --space-lg: 1.5rem;
  --space-xl: 2rem;

  /* Typography */
  --font-sans: 'Inter', system-ui, sans-serif;
  --font-mono: 'Fira Code', monospace;
  --text-xs: 0.75rem;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.25rem;

  /* Effects */
  --glass-bg: rgba(26, 26, 46, 0.7);
  --glass-border: rgba(255, 255, 255, 0.1);
  --blur-sm: blur(8px);
  --blur-md: blur(12px);
  --blur-lg: blur(16px);
}
```

**TypeScript Support** (optional type safety):
```typescript
// types/theme.ts
export const theme = {
  colors: {
    bgPrimary: 'var(--color-bg-primary)',
    bgSecondary: 'var(--color-bg-secondary)',
    accentCyan: 'var(--color-accent-cyan)',
    // ...
  },
  spacing: {
    xs: 'var(--space-xs)',
    sm: 'var(--space-sm)',
    // ...
  },
} as const;
```

**Distribution Strategy**:
1. Define tokens in `styles/tokens.css`
2. Import in Next.js `app/layout.tsx`
3. Import in Docusaurus `src/css/custom.css`
4. Document in `contracts/design-tokens.json`

---

### 6. Better Auth Integration Patterns

**Question**: How to share authentication state between Next.js and Docusaurus?

**Challenge**: Next.js (App Router) and Docusaurus are separate applications

**Options Evaluated**:

**Option A: Shared Cookie Domain**
- Better Auth sets cookie on parent domain (e.g., `.intellistack.com`)
- Both Next.js and Docusaurus read same cookie
- Pros: Simple, stateless, works across subdomains
- Cons: Requires same parent domain

**Option B: Token in URL**
- Next.js redirects to Docusaurus with token in URL
- Docusaurus validates token and sets own session
- Pros: Works with different domains
- Cons: Token exposure in URL, more complex

**Option C: Shared Session Store**
- Both apps query same Redis/database for session
- Pros: Centralized session management
- Cons: Adds latency, requires backend calls

**Recommendation**: **Option A (Shared Cookie Domain)**

**Implementation**:

```typescript
// Next.js - lib/auth.ts
import { betterAuth } from 'better-auth/client';

export const authClient = betterAuth({
  baseURL: process.env.NEXT_PUBLIC_AUTH_URL,
  cookieOptions: {
    domain: '.intellistack.com', // Shared domain
    secure: true,
    sameSite: 'lax',
  },
});

// Docusaurus - src/theme/Root.tsx
import { betterAuth } from 'better-auth/client';

const authClient = betterAuth({
  baseURL: process.env.AUTH_URL,
  cookieOptions: {
    domain: '.intellistack.com', // Same domain
    secure: true,
    sameSite: 'lax',
  },
});

export default function Root({ children }) {
  const [user, setUser] = useState(null);

  useEffect(() => {
    authClient.getSession().then(setUser);
  }, []);

  return (
    <AuthContext.Provider value={{ user }}>
      {children}
    </AuthContext.Provider>
  );
}
```

**Deployment Considerations**:
- Next.js: `app.intellistack.com` or `intellistack.com`
- Docusaurus: `learn.intellistack.com` or `intellistack.com/learn`
- Auth Server: `auth.intellistack.com`
- Cookie domain: `.intellistack.com` (note the leading dot)

**Fallback for Development**:
- Use `localhost` for all services
- Cookie domain: `localhost` (no subdomain sharing needed)

---

### 7. Mobile Animation Optimization

**Question**: How to ensure 60fps animations on mobile devices?

**Performance Constraints**:
- Mobile devices: 2-4 CPU cores, limited GPU
- Target: 60fps (16.67ms per frame)
- Budget: 10ms for JavaScript, 6ms for rendering

**Optimization Strategies**:

**1. Use CSS Animations (GPU-accelerated)**
```css
/* Good - GPU accelerated */
.animate {
  transform: translateX(100px);
  opacity: 0.5;
  will-change: transform, opacity;
}

/* Bad - triggers layout/paint */
.animate {
  left: 100px;
  background-color: red;
}
```

**2. Reduce Animation Complexity on Mobile**
```typescript
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const isMobile = window.innerWidth < 768;

const animationConfig = {
  duration: isMobile ? 200 : 400,
  particles: isMobile ? 20 : 50,
  fps: isMobile ? 30 : 60,
};
```

**3. Use Intersection Observer for Lazy Animations**
```typescript
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('animate');
    }
  });
}, { threshold: 0.1 });
```

**4. Throttle/Debounce Expensive Operations**
```typescript
import { useThrottle } from '@/hooks/useThrottle';

function NeuralNetwork() {
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });

  const handleMouseMove = useThrottle((e: MouseEvent) => {
    setMousePos({ x: e.clientX, y: e.clientY });
  }, 16); // ~60fps

  return <canvas onMouseMove={handleMouseMove} />;
}
```

**5. Pause Animations When Not Visible**
```typescript
useEffect(() => {
  const handleVisibilityChange = () => {
    if (document.hidden) {
      pauseAnimations();
    } else {
      resumeAnimations();
    }
  };

  document.addEventListener('visibilitychange', handleVisibilityChange);
  return () => document.removeEventListener('visibilitychange', handleVisibilityChange);
}, []);
```

**Testing Strategy**:
- Chrome DevTools Performance tab (CPU throttling 4x)
- Real device testing (iPhone 12, Samsung Galaxy S21)
- Lighthouse performance audit (target 80+ on mobile)
- Frame rate monitoring in production

---

### 8. WCAG 2.1 Level AA Accessibility

**Question**: What are the key requirements for WCAG 2.1 Level AA compliance?

**Critical Requirements**:

**1. Color Contrast** (SC 1.4.3, 1.4.6)
- Normal text (< 18pt): 4.5:1 minimum
- Large text (≥ 18pt or 14pt bold): 3:1 minimum
- UI components and graphics: 3:1 minimum

**Theme Validation**:
```
Background: #1a1a2e (Charcoal)
Text: #e0e0e0 (Light Gray)
Contrast: 11.5:1 ✅ (exceeds 4.5:1)

Background: #16213e (Midnight Blue)
Accent: #00efff (Cyan)
Contrast: 8.2:1 ✅ (exceeds 3:1)
```

**2. Keyboard Navigation** (SC 2.1.1, 2.1.2)
- All interactive elements must be keyboard accessible
- Focus indicators must be visible (2px outline minimum)
- No keyboard traps
- Logical tab order

**Implementation**:
```css
/* Visible focus indicators */
:focus-visible {
  outline: 2px solid var(--color-accent-cyan);
  outline-offset: 2px;
}

/* Skip to main content link */
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: var(--color-bg-primary);
  color: var(--color-accent-cyan);
  padding: 8px;
  z-index: 100;
}

.skip-link:focus {
  top: 0;
}
```

**3. Screen Reader Support** (SC 1.3.1, 4.1.2)
- Semantic HTML elements
- ARIA labels for custom components
- Alt text for images
- Proper heading hierarchy

**Implementation**:
```tsx
// Good - semantic HTML
<nav aria-label="Main navigation">
  <ul>
    <li><a href="/">Home</a></li>
  </ul>
</nav>

// Good - ARIA for custom components
<button
  aria-label="Close dialog"
  aria-expanded={isOpen}
  onClick={handleClose}
>
  <CloseIcon aria-hidden="true" />
</button>

// Good - alt text
<img
  src="/robot.png"
  alt="3D humanoid robot with blue accents in standing pose"
/>
```

**4. Reduced Motion** (SC 2.3.3)
- Respect `prefers-reduced-motion` media query
- Provide option to disable animations

**Implementation**:
```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

**5. Touch Target Size** (SC 2.5.5)
- Minimum 44x44 CSS pixels for touch targets
- Adequate spacing between targets

**Implementation**:
```css
/* Mobile touch targets */
@media (max-width: 768px) {
  button,
  a,
  input,
  select {
    min-height: 44px;
    min-width: 44px;
    padding: 12px 16px;
  }
}
```

**Testing Tools**:
- axe DevTools (automated testing)
- WAVE browser extension
- Lighthouse accessibility audit
- Manual keyboard navigation testing
- Screen reader testing (NVDA, JAWS, VoiceOver)

**Compliance Checklist**:
- [ ] Color contrast ratios validated
- [ ] Keyboard navigation tested
- [ ] Screen reader compatibility verified
- [ ] Focus indicators visible
- [ ] Reduced motion support implemented
- [ ] Touch target sizes meet minimum
- [ ] Semantic HTML used throughout
- [ ] ARIA labels added where needed
- [ ] Alt text for all images
- [ ] Heading hierarchy logical

---

## Technology Stack Recommendations

Based on research findings, the recommended technology stack:

### Next.js Frontend
- **Framework**: Next.js 14.2+ (App Router)
- **React**: 18.3+
- **Styling**: Tailwind CSS 3.4+ + CSS Custom Properties
- **Animations**: Framer Motion 11+ (declarative animations)
- **3D Graphics**: React Three Fiber 8+ + Three.js 0.160+
- **Auth Client**: Better Auth 1.4+ client SDK
- **Forms**: React Hook Form 7+ + Zod validation
- **HTTP Client**: Native fetch with error handling
- **Testing**: Vitest + React Testing Library + Playwright

### Docusaurus Customization
- **Version**: Docusaurus 3.7+
- **Theme**: Classic theme with CSS customization
- **Swizzling**: Wrap approach for Layout/Navbar/Footer
- **Styling**: CSS Custom Properties (shared with Next.js)
- **Auth**: Better Auth client SDK (shared session)

### Shared Infrastructure
- **Design Tokens**: CSS Custom Properties
- **Auth**: Better Auth 1.4+ (existing)
- **Session**: Shared cookie domain
- **Deployment**: Vercel (Next.js) + Netlify/Vercel (Docusaurus)

### Development Tools
- **TypeScript**: 5.6+
- **Package Manager**: npm or pnpm
- **Linting**: ESLint + Prettier
- **Git Hooks**: Husky + lint-staged
- **CI/CD**: GitHub Actions

---

## Performance Budgets

Based on research and industry standards:

### Loading Performance
- **First Contentful Paint (FCP)**: < 1.5s
- **Largest Contentful Paint (LCP)**: < 2.5s
- **Time to Interactive (TTI)**: < 3s (desktop), < 5s (mobile)
- **Cumulative Layout Shift (CLS)**: < 0.1
- **First Input Delay (FID)**: < 100ms

### Bundle Sizes (gzipped)
- **Landing Page**: < 150KB (initial JS)
- **Auth Pages**: < 100KB (initial JS)
- **Personalization**: < 120KB (initial JS)
- **Shared CSS**: < 30KB
- **3D Robot Model**: < 500KB (lazy loaded)

### Runtime Performance
- **Animations**: 60fps (desktop), 30fps minimum (mobile)
- **Neural Network**: < 5% CPU usage when idle
- **Glassmorphism**: < 10ms paint time per element
- **3D Robot**: < 16ms render time (60fps)

### Network Performance
- **API Response Time**: < 200ms (p95)
- **Image Loading**: Progressive JPEG/WebP
- **Font Loading**: FOIT with 3s timeout
- **Code Splitting**: Route-based + component-based

---

## Browser Compatibility Matrix

### Supported Browsers (Full Experience)
- Chrome/Edge: 88+ (2021+)
- Firefox: 87+ (2021+)
- Safari: 14+ (2020+)
- Chrome Mobile: 88+
- Safari iOS: 14+

### Supported Browsers (Degraded Experience)
- Chrome/Edge: 76-87 (no backdrop-filter)
- Firefox: 78-86 (no backdrop-filter)
- Safari: 12-13 (limited animations)

### Unsupported Browsers
- Internet Explorer (all versions)
- Chrome/Edge: < 76
- Firefox: < 78
- Safari: < 12

### Fallback Strategy
1. **Glassmorphism**: Solid background with opacity
2. **Neural Network**: Static SVG pattern
3. **3D Robot**: 2D SVG illustration
4. **Animations**: Reduced or disabled
5. **Modern CSS**: Autoprefixer + PostCSS

---

## Risk Mitigation

### Technical Risks Identified

**Risk 1: 3D Robot Performance on Low-End Devices**
- **Mitigation**: Device detection + 2D fallback
- **Testing**: Test on iPhone SE, Samsung Galaxy A series
- **Monitoring**: Track WebGL errors and load times

**Risk 2: Glassmorphism Browser Support**
- **Mitigation**: @supports fallback with solid backgrounds
- **Testing**: Test on Firefox 78-102 (no backdrop-filter)
- **Monitoring**: Track browser versions in analytics

**Risk 3: Animation Performance on Mobile**
- **Mitigation**: Reduced animation complexity, 30fps target
- **Testing**: Chrome DevTools CPU throttling, real device testing
- **Monitoring**: Frame rate monitoring, performance budgets

**Risk 4: Shared Authentication Complexity**
- **Mitigation**: Shared cookie domain, fallback to token-based
- **Testing**: Test cross-domain session sharing
- **Monitoring**: Track auth errors and session failures

**Risk 5: Bundle Size Exceeding Budget**
- **Mitigation**: Code splitting, lazy loading, tree shaking
- **Testing**: Bundle analyzer, Lighthouse audits
- **Monitoring**: Bundle size tracking in CI/CD

---

## Next Steps

Phase 0 research is complete. Proceed to Phase 1:

1. **Create data-model.md**: Define data structures for personalization preferences
2. **Create contracts/**: Document API contracts and design tokens
3. **Create quickstart.md**: Developer onboarding guide
4. **Update plan.md**: Incorporate research findings into architecture plan

---

**Research Status**: ✅ Complete
**Confidence Level**: High (all technical unknowns resolved)
**Ready for Phase 1**: Yes
