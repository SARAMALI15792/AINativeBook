# Implementation Plan: Frontend Redesign & Experience Enhancement

**Branch**: `001-frontend-redesign` | **Date**: 2026-02-17 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-frontend-redesign/spec.md`

## Summary

Redesign the platform's frontend with an AI Neural Network futuristic dark theme, creating a cohesive visual experience across landing page, authentication, personalization flow, and existing Docusaurus book. The implementation uses Next.js for new standalone pages (landing, auth, personalization) while preserving the existing Docusaurus content platform. Key features include glassmorphism effects, animated neural network patterns, mobile optimization, comprehensive error handling, and WCAG 2.1 Level AA accessibility compliance.

**Primary Requirement**: Create visually stunning, accessible, and performant frontend experience that guides users from landing page → authentication → personalization → Docusaurus book with consistent AI Neural Network theme.

**Technical Approach**:
- Next.js 14+ (App Router) for landing page, auth pages, and personalization flow
- Docusaurus 3.7+ theme customization for content platform
- Shared design token system (CSS custom properties)
- Better Auth integration for authentication
- Mobile-first responsive design with progressive enhancement

## Technical Context

**Language/Version**: TypeScript 5.6+, Node.js 18+
**Primary Dependencies**:
- Next.js 14+ (App Router)
- React 18+
- Docusaurus 3.7+
- Better Auth 1.4+
- Framer Motion (animations)
- Three.js or React Three Fiber (3D robot model)
- Tailwind CSS (styling)

**Storage**:
- User preferences: Backend API (existing)
- Session state: Better Auth (existing)
- Theme tokens: CSS custom properties

**Testing**:
- Vitest (unit tests)
- Playwright (E2E tests)
- React Testing Library (component tests)
- Lighthouse CI (performance)
- axe-core (accessibility)

**Target Platform**:
- Web browsers (Chrome 88+, Firefox 87+, Safari 14+)
- Mobile browsers (iOS Safari 14+, Chrome Mobile)
- Responsive: 320px (mobile) to 2560px (desktop)

**Project Type**: Web application (frontend + existing backend)

**Performance Goals**:
- Landing page FCP < 1.5s
- TTI < 3s (desktop), < 5s (mobile)
- 60fps animations
- Lighthouse score 90+ (desktop), 80+ (mobile)
- Bundle size < 200KB (gzipped) per page

**Constraints**:
- Must not modify existing Docusaurus content structure
- Must integrate with existing Better Auth backend
- Must maintain authentication state across Next.js and Docusaurus
- Glassmorphism fallback for older browsers
- WCAG 2.1 Level AA compliance required

**Scale/Scope**:
- 3 new Next.js pages (landing, auth, personalization)
- 1 Docusaurus theme customization
- ~50 reusable components
- Design token system
- Mobile + tablet + desktop layouts

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Note**: No project constitution file found. Applying general best practices:

✅ **Separation of Concerns**: Next.js pages separate from Docusaurus content
✅ **Reusability**: Shared design token system and component library
✅ **Testing**: Unit, integration, E2E, performance, and accessibility tests planned
✅ **Performance**: Explicit performance budgets and optimization strategies
✅ **Accessibility**: WCAG 2.1 Level AA compliance required
✅ **Mobile-First**: Responsive design with mobile optimization
✅ **Error Handling**: Comprehensive error states and recovery flows

**No violations identified** - proceeding with standard web application architecture.

## Project Structure

### Documentation (this feature)

```text
specs/001-frontend-redesign/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   ├── design-tokens.json
│   ├── theme-api.md
│   └── component-api.md
├── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
├── GAP_ANALYSIS.md      # Gap analysis report (completed)
└── checklists/
    └── requirements.md  # Specification validation checklist
```

### Source Code (repository root)

```text
intellistack/
├── frontend/                    # NEW: Next.js application
│   ├── src/
│   │   ├── app/                # App Router pages
│   │   │   ├── page.tsx        # Landing page
│   │   │   ├── auth/
│   │   │   │   ├── login/page.tsx
│   │   │   │   └── register/page.tsx
│   │   │   └── personalization/page.tsx
│   │   ├── components/         # Reusable components
│   │   │   ├── ui/            # Base UI components
│   │   │   ├── landing/       # Landing page components
│   │   │   ├── auth/          # Auth components
│   │   │   ├── personalization/ # Personalization components
│   │   │   ├── layout/        # Header, Footer
│   │   │   └── effects/       # Neural network, glassmorphism
│   │   ├── lib/               # Utilities
│   │   │   ├── auth.ts        # Better Auth client
│   │   │   ├── api.ts         # API client
│   │   │   └── theme.ts       # Theme utilities
│   │   ├── styles/            # Global styles
│   │   │   ├── globals.css    # Global CSS + design tokens
│   │   │   └── animations.css # Animation definitions
│   │   └── types/             # TypeScript types
│   ├── public/                # Static assets
│   │   ├── robot-model/       # 3D robot assets
│   │   └── images/            # Images, icons
│   ├── tests/                 # Tests
│   │   ├── unit/
│   │   ├── integration/
│   │   └── e2e/
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   └── tsconfig.json
│
├── content/                     # EXISTING: Docusaurus
│   ├── src/
│   │   ├── theme/              # MODIFIED: Theme customization
│   │   │   ├── Root.tsx        # Theme provider
│   │   │   ├── Layout/         # Layout overrides
│   │   │   └── styles/         # Custom styles
│   │   └── css/                # MODIFIED: Custom CSS
│   │       └── custom.css      # AI Neural Network theme
│   ├── docs/                   # UNCHANGED: Content
│   ├── docusaurus.config.ts    # MODIFIED: Theme config
│   └── package.json            # MODIFIED: Add dependencies
│
├── auth-server/                 # EXISTING: Better Auth
│   └── [unchanged]
│
└── backend/                     # EXISTING: FastAPI
    └── [unchanged]
```

**Structure Decision**: Web application with separate Next.js frontend for new pages and Docusaurus theme customization for existing content. This approach:
- Preserves existing Docusaurus content and structure (FR-043)
- Uses Next.js only for new standalone pages (FR-044)
- Enables shared design token system across both platforms
- Maintains clear separation of concerns
- Supports independent deployment if needed

## Complexity Tracking

> **No Constitution violations - this section is empty**

---

## Phase 0: Research Findings

**Status**: ✅ Complete | **Document**: [research.md](./research.md)

### Key Technical Decisions

**1. Glassmorphism Implementation**
- **Decision**: Use `backdrop-filter` with `@supports` fallback
- **Rationale**: Native CSS feature with excellent performance, graceful degradation for older browsers
- **Fallback**: Solid background with higher opacity for browsers without backdrop-filter support

**2. Neural Network Pattern**
- **Decision**: Hybrid approach - Canvas API (desktop) + SVG (mobile)
- **Rationale**: Rich animations on capable devices, lightweight fallback for mobile
- **Performance**: Max 50 nodes/100 connections on desktop, 20 nodes/40 connections on mobile

**3. 3D Robot Model**
- **Decision**: React Three Fiber with 2D SVG fallback
- **Rationale**: Better React integration, declarative API, acceptable bundle size overhead (~100KB)
- **Optimization**: glTF 2.0 format, 5K-10K polygons, lazy loading, 2D fallback for mobile

**4. Docusaurus Theme Customization**
- **Decision**: CSS Custom Properties + Wrap Components (no ejecting)
- **Rationale**: Maintains upgrade path, sufficient control for styling needs
- **Approach**: Swizzle Layout/Navbar/Footer with `--wrap` flag only

**5. Design Token System**
- **Decision**: CSS Custom Properties (not CSS-in-JS)
- **Rationale**: Works across Next.js and Docusaurus, zero runtime overhead, native browser feature
- **Distribution**: Single `tokens.css` file imported by both platforms

**6. Better Auth Integration**
- **Decision**: Shared cookie domain (`.intellistack.com`)
- **Rationale**: Simple, stateless, works across subdomains
- **Deployment**: Next.js + Docusaurus on same parent domain

**7. Mobile Animation Optimization**
- **Decision**: Reduced complexity + CSS animations + Intersection Observer
- **Rationale**: 60fps target on mobile requires lighter animations
- **Strategy**: 30fps fallback, pause when tab inactive, throttle expensive operations

**8. WCAG 2.1 Level AA Compliance**
- **Decision**: All color combinations meet 4.5:1 contrast ratio minimum
- **Rationale**: Legal compliance and inclusive design
- **Implementation**: Validated color palette, keyboard navigation, screen reader support, reduced motion

---

## Phase 1: Design Artifacts

**Status**: ✅ Complete

### Data Model

**Document**: [data-model.md](./data-model.md)

**Key Entities**:
1. **PersonalizationPreferences**: User learning preferences (PostgreSQL)
2. **UserSession**: Client-side session state (React Context + Better Auth)
3. **ThemeConfig**: Theme settings (CSS Custom Properties + localStorage)
4. **PersonalizationFormState**: Temporary form state (React state)

**API Endpoints**:
- `POST /api/v1/personalization/preferences` - Save preferences
- `GET /api/v1/personalization/preferences` - Get preferences
- `PATCH /api/v1/personalization/preferences` - Update preferences
- `DELETE /api/v1/personalization/preferences` - Delete preferences

**State Management**: React Context (AuthContext, ThemeContext)

### Contracts

**Documents**:
- [design-tokens.json](./contracts/design-tokens.json) - Design token specification
- [api-contracts.md](./contracts/api-contracts.md) - API request/response formats
- [component-api.md](./contracts/component-api.md) - Component props and usage
- [theme-api.md](./contracts/theme-api.md) - Theming system API

**Design Tokens**:
- 15 color tokens (background, accent, text, semantic, glassmorphism)
- 7 spacing tokens (xs to 3xl)
- Typography tokens (font families, sizes, weights)
- Effect tokens (blur, shadow, border radius, animation)
- Breakpoints and z-index layers

**Component Categories**:
- UI Components (Button, Input, Card, Slider, Modal)
- Landing Components (Hero, FeatureCard, TestimonialCarousel)
- Auth Components (LoginForm, RegisterForm, SocialAuthButtons)
- Personalization Components (PersonalizationWizard, selectors)
- Layout Components (Header, Footer, MobileMenu)
- Effect Components (NeuralNetworkBackground, GlassCard, Robot3D/2D)

### Quickstart Guide

**Document**: [quickstart.md](./quickstart.md)

**Setup Time**: ~5 minutes
**Prerequisites**: Node.js 18+, npm/pnpm 8+, Git 2.30+
**Development Servers**: 4 terminals (Next.js, Docusaurus, Auth Server, Backend API)
**Common Tasks**: Component creation, page creation, API integration, form validation

---

## Architecture Decisions

### Decision 1: Next.js App Router vs Pages Router

**Options Considered**:
- App Router (Next.js 13+)
- Pages Router (Next.js 12)

**Decision**: App Router

**Rationale**:
- Server Components for better performance
- Improved data fetching patterns
- Better TypeScript support
- Future-proof (recommended by Next.js team)
- Nested layouts support

**Trade-offs**:
- Steeper learning curve
- Some third-party libraries not yet compatible
- More complex mental model

**Mitigation**: Use Client Components where needed, comprehensive documentation

---

### Decision 2: Styling Approach

**Options Considered**:
- Tailwind CSS + CSS Custom Properties
- CSS-in-JS (Styled Components, Emotion)
- CSS Modules
- Vanilla CSS

**Decision**: Tailwind CSS + CSS Custom Properties

**Rationale**:
- Tailwind: Rapid development, consistent spacing, utility-first
- CSS Custom Properties: Runtime theming, works across frameworks, zero overhead
- Best of both worlds: Tailwind for layout, CSS vars for theming

**Trade-offs**:
- Larger HTML (utility classes)
- Learning curve for Tailwind
- No type safety for CSS variables

**Mitigation**: PurgeCSS removes unused classes, TypeScript wrapper for theme tokens

---

### Decision 3: Animation Library

**Options Considered**:
- Framer Motion
- React Spring
- CSS Animations only
- GSAP

**Decision**: Framer Motion + CSS Animations

**Rationale**:
- Framer Motion: Declarative API, gesture support, layout animations
- CSS Animations: Performance-critical animations (60fps)
- Hybrid approach: Use CSS for simple animations, Framer Motion for complex

**Trade-offs**:
- Bundle size (~30KB for Framer Motion)
- Two animation systems to maintain

**Mitigation**: Code splitting, lazy load Framer Motion, use CSS for critical path

---

### Decision 4: 3D Graphics Library

**Options Considered**:
- Three.js (vanilla)
- React Three Fiber
- Babylon.js
- 2D only (no 3D)

**Decision**: React Three Fiber with 2D fallback

**Rationale**:
- Better React integration than vanilla Three.js
- Declarative API matches project patterns
- Active community and ecosystem
- 2D fallback ensures mobile compatibility

**Trade-offs**:
- Bundle size (~700KB total)
- Performance impact on low-end devices

**Mitigation**: Lazy loading, device detection, 2D SVG fallback for mobile

---

### Decision 5: Form Management

**Options Considered**:
- React Hook Form + Zod
- Formik + Yup
- Vanilla React state
- TanStack Form

**Decision**: React Hook Form + Zod

**Rationale**:
- Excellent performance (uncontrolled inputs)
- TypeScript-first with Zod
- Small bundle size (~9KB)
- Great DX with type inference

**Trade-offs**:
- Learning curve for Zod schemas
- Less flexible than Formik

**Mitigation**: Comprehensive examples in quickstart, reusable validation schemas

---

### Decision 6: Testing Strategy

**Options Considered**:
- Jest + React Testing Library
- Vitest + React Testing Library
- Cypress (E2E)
- Playwright (E2E)

**Decision**: Vitest + React Testing Library + Playwright

**Rationale**:
- Vitest: Faster than Jest, Vite-native, ESM support
- React Testing Library: Best practices for component testing
- Playwright: Better cross-browser support than Cypress

**Trade-offs**:
- Vitest less mature than Jest
- Playwright steeper learning curve

**Mitigation**: Vitest API compatible with Jest, Playwright has excellent docs

---

## Implementation Phases

### Phase 0: Setup & Infrastructure (2-3 hours)

**Tasks**:
1. Create `intellistack/frontend/` directory structure
2. Initialize Next.js 14 with TypeScript and Tailwind CSS
3. Configure environment variables (`.env.local`)
4. Set up ESLint, Prettier, and Git hooks
5. Create design token system (`styles/tokens.css`)
6. Configure Tailwind to use CSS custom properties
7. Set up testing infrastructure (Vitest, Playwright, React Testing Library)
8. Create base layout components (Header, Footer)

**Deliverables**:
- Next.js project initialized
- Design tokens implemented
- Development environment configured
- Base layout structure

**Acceptance Criteria**:
- `npm run dev` starts Next.js on port 3000
- Design tokens accessible via Tailwind classes
- ESLint and Prettier configured
- Tests run with `npm run test`

---

### Phase 1: UI Component Library (4-5 hours)

**Tasks**:
1. Implement base UI components:
   - Button (4 variants, 3 sizes)
   - Input (text, email, password, with validation)
   - Card (default, glass, elevated variants)
   - Slider (for weekly commitment)
   - Modal (with focus trap and accessibility)
2. Implement glassmorphism effect component (GlassCard)
3. Write unit tests for all components
4. Write accessibility tests (axe-core)
5. Create Storybook stories (optional)

**Deliverables**:
- 5 base UI components with tests
- GlassCard effect component
- Component documentation

**Acceptance Criteria**:
- All components pass unit tests
- All components pass accessibility tests (WCAG 2.1 AA)
- Components support keyboard navigation
- Focus indicators visible

---

### Phase 2: Effect Components (5-6 hours)

**Tasks**:
1. Implement NeuralNetworkBackground:
   - Canvas variant (desktop)
   - SVG variant (mobile)
   - CSS fallback
   - Device detection logic
2. Implement Robot3D component:
   - React Three Fiber setup
   - glTF model loading
   - Auto-rotation and orbit controls
   - Lazy loading
3. Implement Robot2D component (SVG fallback)
4. Create neural network SVG pattern
5. Optimize performance (60fps target)
6. Add reduced motion support

**Deliverables**:
- NeuralNetworkBackground component (3 variants)
- Robot3D component with lazy loading
- Robot2D fallback component
- Neural network SVG pattern

**Acceptance Criteria**:
- Neural network animates at 60fps on desktop, 30fps on mobile
- 3D robot loads in < 3s on 3G connection
- 2D fallback displays on mobile devices
- Animations pause when tab inactive
- Respects `prefers-reduced-motion`

---

### Phase 3: Landing Page (6-7 hours)

**Tasks**:
1. Implement Hero section:
   - Animated gradient background
   - Neural network overlay
   - 3D robot model (desktop) / 2D illustration (mobile)
   - CTA button
2. Implement Features section (3-4 feature cards)
3. Implement Testimonials carousel
4. Implement Footer with links
5. Add page metadata and SEO
6. Optimize images (WebP with PNG fallback)
7. Write E2E tests for landing page flow

**Deliverables**:
- Complete landing page (`app/page.tsx`)
- Hero, Features, Testimonials, Footer components
- E2E tests

**Acceptance Criteria**:
- Landing page loads in < 1.5s (FCP)
- Lighthouse score 90+ (desktop), 80+ (mobile)
- All links functional
- Responsive on all breakpoints (320px to 2560px)
- E2E tests pass

---

### Phase 4: Authentication Pages (5-6 hours)

**Tasks**:
1. Implement Better Auth client integration
2. Implement LoginForm component:
   - Email and password validation
   - Show/hide password toggle
   - Remember me checkbox
   - Error handling
3. Implement RegisterForm component:
   - Email, password, name validation
   - Password strength indicator
   - Terms of service checkbox
   - Error handling
4. Implement SocialAuthButtons (Google, GitHub)
5. Create login page (`app/auth/login/page.tsx`)
6. Create register page (`app/auth/register/page.tsx`)
7. Add form validation with React Hook Form + Zod
8. Write E2E tests for auth flows

**Deliverables**:
- Login and register pages
- LoginForm and RegisterForm components
- Better Auth integration
- E2E tests for auth flows

**Acceptance Criteria**:
- Users can register with email/password
- Users can login with email/password
- Social auth buttons functional (if configured)
- Form validation works correctly
- Error messages display properly
- Session persists across page reloads
- E2E tests pass

---

### Phase 5: Personalization Flow (6-7 hours)

**Tasks**:
1. Implement PersonalizationWizard component (4-step wizard)
2. Implement step components:
   - LearningGoalSelector (card-based selection)
   - ExperienceLevelSelector (card-based selection)
   - WeeklyCommitmentSlider (slider with marks)
   - InterestTagSelector (multi-select tags)
3. Implement progress indicator
4. Implement step validation
5. Implement API integration (save preferences)
6. Create personalization page (`app/personalization/page.tsx`)
7. Add redirect to Docusaurus after completion
8. Write E2E tests for personalization flow

**Deliverables**:
- Personalization page with 4-step wizard
- 4 step components
- API integration
- E2E tests

**Acceptance Criteria**:
- Users can complete all 4 steps
- Step validation prevents invalid progression
- Preferences saved to backend API
- Users redirected to Docusaurus after completion
- Skip option available
- E2E tests pass

---

### Phase 6: Docusaurus Theme Customization (4-5 hours)

**Tasks**:
1. Import design tokens into Docusaurus (`src/css/custom.css`)
2. Override Docusaurus theme variables
3. Swizzle Layout component (wrap mode)
4. Swizzle Navbar component (wrap mode)
5. Swizzle Footer component (wrap mode)
6. Add neural network background to Docusaurus pages
7. Apply glassmorphism to cards and sidebars
8. Test theme on all Docusaurus page types
9. Verify dark mode toggle works
10. Test mobile responsiveness

**Deliverables**:
- Docusaurus theme customization
- Neural network background on all pages
- Glassmorphism effects
- Mobile-responsive theme

**Acceptance Criteria**:
- AI Neural Network theme applied consistently
- All Docusaurus pages styled correctly
- Dark mode toggle functional
- Mobile responsive (320px to 2560px)
- No visual regressions
- Contrast ratios meet WCAG 2.1 AA

---

### Phase 7: Authentication State Sharing (3-4 hours)

**Tasks**:
1. Configure Better Auth cookie domain (`.intellistack.com`)
2. Implement AuthContext in Next.js
3. Implement AuthContext in Docusaurus (Root.tsx)
4. Test session sharing between Next.js and Docusaurus
5. Implement protected routes in Docusaurus
6. Add user menu in Docusaurus navbar
7. Test logout flow across both platforms

**Deliverables**:
- Shared authentication state
- Protected routes in Docusaurus
- User menu in Docusaurus

**Acceptance Criteria**:
- Session persists from Next.js to Docusaurus
- Users see same auth state in both platforms
- Protected routes redirect to login if not authenticated
- Logout works from both platforms
- Cookie domain configured correctly

---

### Phase 8: Error Handling & Loading States (3-4 hours)

**Tasks**:
1. Implement error boundary components
2. Add loading skeletons for async content
3. Implement error pages (404, 500)
4. Add retry logic for failed API calls
5. Implement toast notifications for errors
6. Add network error detection
7. Implement graceful degradation for service unavailability
8. Add client-side error logging

**Deliverables**:
- Error boundary components
- Loading skeletons
- Error pages
- Toast notification system

**Acceptance Criteria**:
- Errors caught and displayed gracefully
- Loading states shown during async operations
- Users can retry failed operations
- Network errors detected and communicated
- Error logging functional
- 90%+ error recovery success rate

---

### Phase 9: Mobile Optimization (4-5 hours)

**Tasks**:
1. Implement hamburger menu for mobile navigation
2. Optimize 3D robot for mobile (2D fallback)
3. Reduce animation complexity on mobile
4. Implement touch-friendly interactions (44x44px targets)
5. Optimize images for mobile (responsive images)
6. Test on real mobile devices (iOS, Android)
7. Implement progressive loading on slow connections
8. Add viewport meta tags

**Deliverables**:
- Mobile-optimized navigation
- 2D robot fallback
- Touch-friendly UI
- Responsive images

**Acceptance Criteria**:
- All touch targets meet 44x44px minimum
- Animations run at 30fps+ on mobile
- Images load progressively
- Hamburger menu functional
- Tested on iOS Safari and Chrome Mobile
- Mobile task completion within 10% of desktop

---

### Phase 10: Accessibility Compliance (4-5 hours)

**Tasks**:
1. Implement keyboard navigation for all interactive elements
2. Add visible focus indicators (2px outline)
3. Implement skip-to-main-content link
4. Add ARIA labels for custom components
5. Ensure proper heading hierarchy
6. Add alt text for all images
7. Implement screen reader announcements for dynamic content
8. Test with screen readers (NVDA, JAWS, VoiceOver)
9. Run axe-core accessibility audit
10. Fix all WCAG 2.1 Level AA violations

**Deliverables**:
- Keyboard navigation support
- Screen reader compatibility
- WCAG 2.1 Level AA compliance

**Acceptance Criteria**:
- 100% keyboard accessible
- All color combinations meet 4.5:1 contrast ratio
- Screen reader announces all content correctly
- Focus indicators visible on all interactive elements
- axe-core audit passes with 0 violations
- Manual screen reader testing passes

---

### Phase 11: Performance Optimization (3-4 hours)

**Tasks**:
1. Implement code splitting (route-based + component-based)
2. Lazy load heavy components (Robot3D, animations)
3. Optimize images (WebP, responsive sizes)
4. Implement font loading strategy (FOIT with 3s timeout)
5. Add resource hints (preconnect, prefetch)
6. Optimize bundle size (tree shaking, minification)
7. Implement caching strategy
8. Run Lighthouse audits
9. Fix performance issues

**Deliverables**:
- Optimized bundle sizes
- Lazy loading implemented
- Caching strategy

**Acceptance Criteria**:
- Landing page FCP < 1.5s
- TTI < 3s (desktop), < 5s (mobile)
- Bundle size < 200KB per page (gzipped)
- Lighthouse score 90+ (desktop), 80+ (mobile)
- CLS < 0.1
- FID < 100ms

---

### Phase 12: Testing & QA (4-5 hours)

**Tasks**:
1. Write comprehensive unit tests (80%+ coverage)
2. Write integration tests for API interactions
3. Write E2E tests for all user flows
4. Run accessibility tests (axe-core)
5. Run performance tests (Lighthouse CI)
6. Test on multiple browsers (Chrome, Firefox, Safari, Edge)
7. Test on multiple devices (desktop, tablet, mobile)
8. Fix all failing tests
9. Document test coverage

**Deliverables**:
- Comprehensive test suite
- Test coverage report
- Browser compatibility matrix

**Acceptance Criteria**:
- Unit test coverage 80%+
- All E2E tests pass
- All accessibility tests pass
- All performance tests pass
- Tested on Chrome 88+, Firefox 87+, Safari 14+
- Tested on iOS Safari 14+, Chrome Mobile

---

### Phase 13: Documentation & Deployment (3-4 hours)

**Tasks**:
1. Update README with setup instructions
2. Document component API
3. Document theming system
4. Create deployment guide
5. Configure CI/CD pipeline (GitHub Actions)
6. Set up staging environment
7. Deploy to production
8. Monitor for errors

**Deliverables**:
- Complete documentation
- CI/CD pipeline
- Production deployment

**Acceptance Criteria**:
- README complete with setup instructions
- All components documented
- Deployment guide complete
- CI/CD pipeline functional
- Staging environment deployed
- Production deployment successful
- No critical errors in production

---

## Risk Analysis

### Risk 1: 3D Robot Performance on Low-End Devices

**Probability**: Medium | **Impact**: High

**Description**: 3D robot model may cause performance issues on low-end mobile devices, leading to poor user experience.

**Mitigation**:
- Implement device detection (screen size, WebGL support, memory)
- Provide 2D SVG fallback for low-end devices
- Lazy load 3D model (not on critical path)
- Optimize model (< 10K polygons, compressed textures)
- Test on low-end devices (iPhone SE, budget Android)

**Contingency**: If performance issues persist, default to 2D illustration for all mobile devices.

---

### Risk 2: Glassmorphism Browser Compatibility

**Probability**: Low | **Impact**: Medium

**Description**: Older browsers may not support `backdrop-filter`, causing visual inconsistencies.

**Mitigation**:
- Use `@supports` feature detection
- Provide solid background fallback
- Test on Firefox 78-102 (no backdrop-filter)
- Document browser support requirements

**Contingency**: If fallback is insufficient, provide alternative design without glassmorphism for unsupported browsers.

---

### Risk 3: Animation Performance on Mobile

**Probability**: Medium | **Impact**: Medium

**Description**: Complex animations may cause frame drops on mobile devices, degrading user experience.

**Mitigation**:
- Reduce animation complexity on mobile (fewer nodes/connections)
- Target 30fps on mobile (vs 60fps on desktop)
- Use CSS animations for critical animations (GPU-accelerated)
- Pause animations when tab inactive
- Throttle expensive operations (mouse tracking)

**Contingency**: Disable animations on low-end devices, provide static neural network pattern.

---

### Risk 4: Shared Authentication Complexity

**Probability**: Low | **Impact**: High

**Description**: Sharing authentication state between Next.js and Docusaurus may be complex, causing login issues.

**Mitigation**:
- Use shared cookie domain (`.intellistack.com`)
- Test session sharing thoroughly
- Implement fallback to token-based auth if cookie sharing fails
- Document deployment requirements (same parent domain)

**Contingency**: If cookie sharing fails, implement token-based auth with URL parameter passing.

---

### Risk 5: Bundle Size Exceeding Budget

**Probability**: Medium | **Impact**: Medium

**Description**: Heavy dependencies (React Three Fiber, Framer Motion) may cause bundle size to exceed 200KB budget.

**Mitigation**:
- Implement aggressive code splitting
- Lazy load heavy components
- Use tree shaking and minification
- Monitor bundle size in CI/CD
- Consider lighter alternatives if needed

**Contingency**: Remove 3D robot or use lighter animation library if bundle size cannot be reduced.

---

## Success Metrics

### Performance Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| First Contentful Paint (FCP) | < 1.5s | Lighthouse |
| Largest Contentful Paint (LCP) | < 2.5s | Lighthouse |
| Time to Interactive (TTI) | < 3s (desktop), < 5s (mobile) | Lighthouse |
| Cumulative Layout Shift (CLS) | < 0.1 | Lighthouse |
| First Input Delay (FID) | < 100ms | Lighthouse |
| Bundle Size (per page) | < 200KB (gzipped) | webpack-bundle-analyzer |
| Lighthouse Score | 90+ (desktop), 80+ (mobile) | Lighthouse CI |

### Accessibility Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| WCAG 2.1 Level | AA | axe-core |
| Keyboard Accessibility | 100% | Manual testing |
| Screen Reader Compatibility | 100% | Manual testing (NVDA, JAWS, VoiceOver) |
| Color Contrast Ratio | 4.5:1 (normal text), 3:1 (large text) | Contrast checker |
| Touch Target Size | 44x44px minimum | Manual testing |

### User Experience Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Task Completion Rate | 90%+ | Analytics |
| Mobile Task Completion Parity | Within 10% of desktop | Analytics |
| Error Recovery Success Rate | 90%+ | Analytics |
| User Satisfaction | 4.0+ / 5.0 | User surveys |

### Code Quality Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Unit Test Coverage | 80%+ | Vitest coverage report |
| E2E Test Coverage | All critical flows | Playwright |
| TypeScript Coverage | 100% | TypeScript compiler |
| ESLint Violations | 0 | ESLint |
| Accessibility Violations | 0 | axe-core |

---

## Timeline Estimate

| Phase | Duration | Dependencies |
|-------|----------|--------------|
| Phase 0: Setup & Infrastructure | 2-3 hours | None |
| Phase 1: UI Component Library | 4-5 hours | Phase 0 |
| Phase 2: Effect Components | 5-6 hours | Phase 0, Phase 1 |
| Phase 3: Landing Page | 6-7 hours | Phase 1, Phase 2 |
| Phase 4: Authentication Pages | 5-6 hours | Phase 1 |
| Phase 5: Personalization Flow | 6-7 hours | Phase 1, Phase 4 |
| Phase 6: Docusaurus Theme | 4-5 hours | Phase 0 |
| Phase 7: Auth State Sharing | 3-4 hours | Phase 4, Phase 6 |
| Phase 8: Error Handling | 3-4 hours | Phase 3, Phase 4, Phase 5 |
| Phase 9: Mobile Optimization | 4-5 hours | Phase 3, Phase 4, Phase 5 |
| Phase 10: Accessibility | 4-5 hours | All previous phases |
| Phase 11: Performance | 3-4 hours | All previous phases |
| Phase 12: Testing & QA | 4-5 hours | All previous phases |
| Phase 13: Documentation & Deployment | 3-4 hours | All previous phases |

**Total Estimated Time**: 52-66 hours (~7-9 working days)

---

## Next Steps

1. ✅ Phase 0 Research: Complete (see [research.md](./research.md))
2. ✅ Phase 1 Design: Complete (see [data-model.md](./data-model.md), [contracts/](./contracts/))
3. ⏭️ **Phase 2 Tasks**: Run `/sp.tasks` to generate actionable task list
4. 🚀 **Implementation**: Execute tasks in dependency order

---

**Plan Status**: ✅ Complete
**Ready for Tasks Generation**: Yes
**Last Updated**: 2026-02-18

