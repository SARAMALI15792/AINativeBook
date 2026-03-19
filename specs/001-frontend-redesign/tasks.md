# Tasks: Frontend Redesign & Experience Enhancement

**Input**: Design documents from `/specs/001-frontend-redesign/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Tests are NOT explicitly requested in the specification, so test tasks are excluded per template guidelines.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Next.js Frontend**: `intellistack/frontend/src/`
- **Docusaurus**: `intellistack/content/src/`
- **Shared Styles**: `intellistack/frontend/src/styles/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create Next.js 14 project structure in intellistack/frontend/ with TypeScript and App Router
- [x] T002 Install dependencies: Next.js 14+, React 18+, Tailwind CSS 3.4+, TypeScript 5.6+, Framer Motion 11+
- [x] T003 [P] Configure ESLint and Prettier in intellistack/frontend/.eslintrc.json and .prettierrc
- [x] T004 [P] Set up environment variables in intellistack/frontend/.env.local (AUTH_URL, API_URL, DOCUSAURUS_URL)
- [x] T005 [P] Configure Tailwind CSS in intellistack/frontend/tailwind.config.js to use CSS custom properties
- [x] T006 [P] Create design token system in intellistack/frontend/src/styles/tokens.css with AI Neural Network theme colors
- [x] T007 [P] Create global styles in intellistack/frontend/src/styles/globals.css
- [x] T008 [P] Create animation definitions in intellistack/frontend/src/styles/animations.css
- [x] T009 Configure Next.js in intellistack/frontend/next.config.js with image optimization and environment variables
- [x] T010 Create root layout in intellistack/frontend/src/app/layout.tsx importing design tokens

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T011 Create TypeScript types in intellistack/frontend/src/types/api.ts for PersonalizationPreferences, UserSession, ThemeConfig
- [x] T012 [P] Implement Better Auth client in intellistack/frontend/src/lib/auth.ts with session management
- [x] T013 [P] Implement API client in intellistack/frontend/src/lib/api-client.ts with error handling and rate limiting
- [x] T014 [P] Create AuthContext in intellistack/frontend/src/contexts/AuthContext.tsx for session state management
- [x] T015 [P] Create ThemeContext in intellistack/frontend/src/contexts/ThemeContext.tsx for theme configuration
- [x] T016 [P] Implement base Button component in intellistack/frontend/src/components/ui/Button.tsx (4 variants, 3 sizes, accessibility)
- [x] T017 [P] Implement base Input component in intellistack/frontend/src/components/ui/Input.tsx (validation, error states, accessibility)
- [x] T018 [P] Implement base Card component in intellistack/frontend/src/components/ui/Card.tsx (default, glass, elevated variants)
- [x] T019 [P] Implement base Slider component in intellistack/frontend/src/components/ui/Slider.tsx (keyboard accessible, ARIA labels)
- [x] T020 [P] Implement base Modal component in intellistack/frontend/src/components/ui/Modal.tsx (focus trap, escape key, accessibility)
- [x] T021 [P] Create component index in intellistack/frontend/src/components/ui/index.ts exporting all UI components
- [x] T022 [P] Implement GlassCard effect component in intellistack/frontend/src/components/effects/GlassCard.tsx with backdrop-filter and fallback
- [x] T023 [P] Implement Header component in intellistack/frontend/src/components/layout/Header.tsx with navigation and auth buttons
- [x] T024 [P] Implement Footer component in intellistack/frontend/src/components/layout/Footer.tsx with links and branding
- [x] T025 [P] Implement MobileMenu component in intellistack/frontend/src/components/layout/MobileMenu.tsx with hamburger menu

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - First-Time Visitor Landing Experience (Priority: P1) 🎯 MVP

**Goal**: Create engaging landing page with AI Neural Network theme, 3D robot, branding, and CTAs to convert visitors

**Independent Test**: Navigate to homepage and verify all visual elements (3D robot, branding, CTAs, neural network background) render correctly with proper theme colors and animations

### Effect Components for User Story 1

- [x] T026 [P] [US1] Implement NeuralNetworkBackground Canvas variant in intellistack/frontend/src/components/effects/NeuralNetworkBackground.tsx for desktop (50 nodes, 100 connections, 60fps)
- [x] T027 [P] [US1] Implement NeuralNetworkBackground SVG variant in intellistack/frontend/src/components/effects/NeuralNetworkBackground.tsx for mobile (20 nodes, 40 connections, 30fps)
- [x] T028 [P] [US1] Add device detection logic to NeuralNetworkBackground component to switch between Canvas/SVG based on screen size and capabilities
- [x] T029 [P] [US1] Create neural network SVG pattern in intellistack/frontend/public/img/neural-network-pattern.svg with gradient lines
- [x] T030 [P] [US1] Implement Robot3D component in intellistack/frontend/src/components/effects/Robot3D.tsx using React Three Fiber with auto-rotation and orbit controls
- [x] T031 [P] [US1] Implement Robot2D component in intellistack/frontend/src/components/effects/Robot2D.tsx as SVG fallback for mobile
- [x] T032 [P] [US1] Add lazy loading and Suspense wrapper for Robot3D component with Robot2D as fallback

### Landing Page Components for User Story 1

- [x] T033 [P] [US1] Implement Hero component in intellistack/frontend/src/components/landing/Hero.tsx with gradient background, robot model, branding, and CTAs
- [x] T034 [P] [US1] Implement FeatureCard component in intellistack/frontend/src/components/landing/FeatureCard.tsx with glass effect and hover animation
- [x] T035 [P] [US1] Implement TestimonialCarousel component in intellistack/frontend/src/components/landing/TestimonialCarousel.tsx with auto-rotation and swipe gestures
- [x] T036 [US1] Create landing page in intellistack/frontend/src/app/page.tsx integrating Hero, Features, Testimonials, and Footer
- [x] T037 [US1] Add page metadata and SEO tags to landing page in intellistack/frontend/src/app/page.tsx
- [x] T038 [US1] Optimize images for landing page (WebP with PNG fallback) in intellistack/frontend/public/images/
- [x] T039 [US1] Add reduced motion support to landing page animations respecting prefers-reduced-motion media query

**Checkpoint**: At this point, User Story 1 should be fully functional - landing page loads with AI Neural Network theme, 3D robot, and working CTAs

---

## Phase 4: User Story 3 - User Authentication Experience (Priority: P1)

**Goal**: Provide secure authentication with SSO and email/password options using Better Auth integration

**Independent Test**: Click login/register links, verify auth page opens in new tab, displays SSO options prominently, and successfully authenticates users

### Auth Components for User Story 3

- [x] T040 [P] [US3] Implement LoginForm component in intellistack/frontend/src/components/auth/LoginForm.tsx with email/password validation and show/hide password toggle
- [x] T041 [P] [US3] Implement RegisterForm component in intellistack/frontend/src/components/auth/RegisterForm.tsx with validation and password strength indicator
- [x] T042 [P] [US3] Implement SocialAuthButtons component in intellistack/frontend/src/components/auth/SocialAuthButtons.tsx for Google and GitHub OAuth
- [x] T043 [P] [US3] Create form validation schemas in intellistack/frontend/src/lib/validation.ts using Zod for email, password, and name fields
- [x] T044 [US3] Create login page in intellistack/frontend/src/app/auth/login/page.tsx integrating LoginForm and SocialAuthButtons
- [x] T045 [US3] Create register page in intellistack/frontend/src/app/auth/register/page.tsx integrating RegisterForm and SocialAuthButtons
- [x] T046 [US3] Add error handling and loading states to auth pages with user-friendly error messages
- [x] T047 [US3] Configure auth pages to open in new tab when triggered from landing page
- [x] T048 [US3] Add "Powered by Better Auth" branding to auth page footers

**Checkpoint**: At this point, User Story 3 should be fully functional - users can register and login with email/password or SSO

---

## Phase 5: User Story 2 - New User Personalization Onboarding (Priority: P1)

**Goal**: Collect user learning preferences through 4-step wizard and save to backend API

**Independent Test**: Complete registration, verify personalization flow presents all 4 steps with progress indicators, saves preferences correctly, and redirects to Docusaurus

### Personalization Components for User Story 2

- [x] T049 [P] [US2] Implement LearningGoalSelector component in intellistack/frontend/src/components/personalization/LearningGoalSelector.tsx with card-based selection
- [x] T050 [P] [US2] Implement ExperienceLevelSelector component in intellistack/frontend/src/components/personalization/ExperienceLevelSelector.tsx with visual level indicators
- [x] T051 [P] [US2] Implement WeeklyCommitmentSlider component in intellistack/frontend/src/components/personalization/WeeklyCommitmentSlider.tsx (1-20 hours range)
- [x] T052 [P] [US2] Implement InterestTagSelector component in intellistack/frontend/src/components/personalization/InterestTagSelector.tsx with multi-select and max 10 limit
- [x] T053 [US2] Implement PersonalizationWizard component in intellistack/frontend/src/components/personalization/PersonalizationWizard.tsx with 4-step flow and progress indicator
- [x] T054 [US2] Add step validation logic to PersonalizationWizard preventing progression with incomplete data
- [x] T055 [US2] Create personalization page in intellistack/frontend/src/app/personalization/page.tsx integrating PersonalizationWizard
- [x] T056 [US2] Implement API integration in PersonalizationWizard to save preferences via POST /api/v1/personalization/preferences
- [x] T057 [US2] Add progress persistence to sessionStorage allowing users to resume if they navigate away
- [x] T058 [US2] Add redirect to Docusaurus book after successful preference submission
- [x] T059 [US2] Add skip option to personalization flow with confirmation modal

**Checkpoint**: At this point, User Story 2 should be fully functional - users can complete 4-step personalization and be redirected to Docusaurus

---

## Phase 6: User Story 4 - Seamless Transition to Docusaurus Book (Priority: P1)

**Goal**: Apply AI Neural Network theme to Docusaurus and ensure seamless navigation from Next.js pages

**Independent Test**: Complete personalization, verify redirect to Docusaurus book with consistent theme and preserved auth state

### Docusaurus Theme Customization for User Story 4

- [x] T060 [US4] Copy design tokens from intellistack/frontend/src/styles/tokens.css to intellistack/content/src/css/tokens.css
- [x] T061 [US4] Update Docusaurus custom CSS in intellistack/content/src/css/custom.css to import tokens and override theme variables
- [x] T062 [US4] Apply AI Neural Network color palette to Docusaurus theme variables (--ifm-color-primary, --ifm-background-color, etc.)
- [x] T063 [US4] Add neural network background pattern to Docusaurus pages in custom.css with fixed positioning and low opacity
- [x] T064 [US4] Apply glassmorphism effects to Docusaurus cards and sidebars in custom.css
- [x] T065 [US4] Add fallback styles for browsers without backdrop-filter support in custom.css using @supports
- [x] T066 [US4] Swizzle Docusaurus Layout component with --wrap flag: npm run swizzle @docusaurus/theme-classic Layout -- --wrap
- [x] T067 [US4] Swizzle Docusaurus Navbar component with --wrap flag: npm run swizzle @docusaurus/theme-classic Navbar -- --wrap
- [x] T068 [US4] Swizzle Docusaurus Footer component with --wrap flag: npm run swizzle @docusaurus/theme-classic Footer -- --wrap
- [x] T069 [US4] Update swizzled Layout component in intellistack/content/src/theme/Layout/index.tsx to add neural network background
- [x] T070 [US4] Test Docusaurus theme on all page types (docs, blog, custom pages) verifying consistent styling
- [x] T071 [US4] Verify dark mode toggle works correctly with AI Neural Network theme

**Checkpoint**: At this point, User Story 4 should be fully functional - Docusaurus book has consistent AI Neural Network theme matching Next.js pages

---

## Phase 7: User Story 4 (continued) - Authentication State Sharing

**Goal**: Share authentication state between Next.js and Docusaurus using shared cookie domain

**Independent Test**: Login in Next.js, navigate to Docusaurus, verify auth state is preserved and user menu displays correctly

### Auth State Sharing for User Story 4

- [x] T072 [US4] Configure Better Auth cookie domain to .intellistack.com in intellistack/frontend/src/lib/auth.ts
- [x] T073 [US4] Implement AuthContext in Docusaurus Root component at intellistack/content/src/theme/Root.tsx
- [x] T074 [US4] Add Better Auth client to Docusaurus in intellistack/content/src/lib/auth.ts with same cookie domain
- [x] T075 [US4] Add session loading logic to Docusaurus Root component checking Better Auth session on mount
- [x] T076 [US4] Implement user menu in Docusaurus navbar showing authenticated user name and logout option
- [x] T077 [US4] Add protected route logic to Docusaurus redirecting unauthenticated users to Next.js login page
- [x] T078 [US4] Test logout flow from both Next.js and Docusaurus verifying session is cleared in both platforms
- [x] T079 [US4] Test session persistence across Next.js and Docusaurus by navigating between platforms

**Checkpoint**: At this point, authentication state is fully shared - users stay logged in across Next.js and Docusaurus

---

## Phase 8: User Story 5 - Navigation and Site-Wide Experience (Priority: P2)

**Goal**: Ensure consistent header/footer styling with smooth transitions and responsive design

**Independent Test**: Navigate through multiple pages verifying header/footer elements are consistently styled, responsive, and provide smooth transitions

### Navigation Enhancement for User Story 5

- [x] T080 [P] [US5] Add smooth hover transitions to Header navigation links in intellistack/frontend/src/components/layout/Header.tsx
- [x] T081 [P] [US5] Add glassmorphism effect to Header component with backdrop-filter and fallback
- [x] T082 [P] [US5] Add micro-interactions to Header buttons (hover, press states) with cyan glow effects
- [x] T083 [P] [US5] Update Footer styling in intellistack/frontend/src/components/layout/Footer.tsx with AI Neural Network theme
- [x] T084 [P] [US5] Add responsive breakpoints to Header and Footer for mobile, tablet, and desktop
- [x] T085 [US5] Test Header and Footer on all Next.js pages verifying consistent styling
- [x] T086 [US5] Test Header and Footer responsiveness on mobile devices (320px to 768px)

**Checkpoint**: At this point, User Story 5 should be complete - navigation is consistent and responsive across all pages

---

## Phase 9: User Story 6 - Seamless Integration Between Landing Page and Docusaurus Book (Priority: P2)

**Goal**: Ensure visual consistency and smooth navigation between Next.js and Docusaurus platforms

**Independent Test**: Navigate from landing page to Docusaurus book and back, verify styling is consistent, navigation works, and user context is preserved

### Integration Testing for User Story 6

- [x] T087 [US6] Test "Start Learning" CTA on landing page redirects to Docusaurus book homepage without errors
- [x] T088 [US6] Test navigation from Docusaurus back to landing page preserves session context
- [x] T089 [US6] Verify AI Neural Network theme colors match exactly between Next.js and Docusaurus (charcoal, cyan, violet, teal)
- [x] T090 [US6] Verify glassmorphism effects render consistently on both platforms
- [x] T091 [US6] Test authenticated user navigation between platforms preserves auth state
- [x] T092 [US6] Add breadcrumb or back navigation from Docusaurus to landing page if needed

**Checkpoint**: At this point, User Story 6 should be complete - seamless integration between Next.js and Docusaurus verified

---

## Phase 10: User Story 7 - Mobile User Experience (Priority: P2)

**Goal**: Optimize platform for mobile devices with touch-friendly interactions and performance

**Independent Test**: Test on mobile devices (iOS/Android) verifying touch interactions, performance, and visual rendering meet requirements

### Mobile Optimization for User Story 7

- [x] T093 [P] [US7] Implement device detection in NeuralNetworkBackground to use SVG variant on mobile
- [x] T094 [P] [US7] Implement device detection for Robot3D to show Robot2D fallback on mobile (screen width < 768px)
- [x] T095 [P] [US7] Optimize neural network animations for mobile reducing node/connection count and targeting 30fps
- [x] T096 [P] [US7] Ensure all touch targets are minimum 44x44px on mobile in all components
- [x] T097 [P] [US7] Implement hamburger menu for mobile navigation in Header component
- [x] T098 [P] [US7] Add progressive image loading for landing page on slow connections
- [x] T099 [P] [US7] Test landing page on mobile devices verifying load time < 3 seconds on 3G
- [x] T100 [P] [US7] Test personalization flow on mobile devices verifying touch interactions work smoothly
- [x] T101 [US7] Add viewport meta tags to all pages for proper mobile rendering
- [x] T102 [US7] Test animations on mobile devices verifying 30fps+ performance without battery drain

**Checkpoint**: At this point, User Story 7 should be complete - mobile experience is optimized and performant

---

## Phase 11: Error Handling & Loading States (Cross-Cutting)

**Purpose**: Comprehensive error handling and loading states across all user stories

- [x] T103 [P] Implement error boundary component in intellistack/frontend/src/components/ErrorBoundary.tsx
- [x] T104 [P] Implement toast notification system in intellistack/frontend/src/components/ui/Toast.tsx for error messages
- [x] T105 [P] Create loading skeleton components in intellistack/frontend/src/components/ui/Skeleton.tsx
- [x] T106 [P] Create 404 error page in intellistack/frontend/src/app/not-found.tsx with AI Neural Network theme
- [x] T107 [P] Create 500 error page in intellistack/frontend/src/app/error.tsx with retry option
- [x] T108 Add retry logic to API client in intellistack/frontend/src/lib/api-client.ts for failed requests
- [x] T109 Add network error detection to API client showing offline indicator
- [x] T110 Add loading states to all async operations (auth, personalization save, page transitions)
- [x] T111 Add client-side error logging to monitoring service in intellistack/frontend/src/lib/logger.ts
- [x] T112 Test error recovery flows verifying users can retry failed operations successfully

---

## Phase 12: Accessibility Compliance (Cross-Cutting)

**Purpose**: Ensure WCAG 2.1 Level AA compliance across all user stories

- [x] T113 [P] Add visible focus indicators (2px cyan outline) to all interactive elements
- [x] T114 [P] Implement skip-to-main-content link in intellistack/frontend/src/components/layout/Header.tsx
- [x] T115 [P] Add ARIA labels to all custom components (Robot3D, NeuralNetworkBackground, PersonalizationWizard)
- [x] T116 [P] Ensure proper heading hierarchy (h1 → h2 → h3) on all pages
- [x] T117 [P] Add alt text to all images in intellistack/frontend/public/images/
- [x] T118 [P] Implement screen reader announcements for dynamic content (form errors, loading states)
- [x] T119 Verify all color combinations meet 4.5:1 contrast ratio using contrast checker tool
- [x] T120 Test keyboard navigation on all pages verifying all interactive elements are accessible
- [x] T121 Test with screen readers (NVDA, JAWS, VoiceOver) verifying all content is announced correctly
- [x] T122 Run axe-core accessibility audit on all pages and fix violations
- [x] T123 Verify prefers-reduced-motion support disables all animations correctly

---

## Phase 13: Performance Optimization (Cross-Cutting)

**Purpose**: Optimize bundle size, loading performance, and runtime performance

- [x] T124 [P] Implement code splitting for heavy components (Robot3D, NeuralNetworkBackground)
- [x] T125 [P] Lazy load Robot3D component with React.lazy() and Suspense
- [x] T126 [P] Lazy load Framer Motion animations only when needed
- [x] T127 [P] Optimize images with Next.js Image component and WebP format
- [x] T128 [P] Implement font loading strategy (FOIT with 3s timeout) in intellistack/frontend/src/app/layout.tsx
- [x] T129 [P] Add resource hints (preconnect, prefetch) to critical resources
- [x] T130 Configure bundle analyzer in intellistack/frontend/next.config.js to monitor bundle size
- [x] T131 Run Lighthouse audit on landing page targeting 90+ score on desktop, 80+ on mobile
- [x] T132 Run Lighthouse audit on auth pages targeting 90+ score
- [x] T133 Run Lighthouse audit on personalization page targeting 90+ score
- [x] T134 Optimize neural network animations to pause when tab is inactive using Page Visibility API
- [x] T135 Fix any performance issues identified by Lighthouse audits

---

## Phase 14: Documentation & Deployment (Final)

**Purpose**: Complete documentation and prepare for production deployment

- [ ] T136 [P] Update README.md with setup instructions for Next.js frontend
- [ ] T137 [P] Update README.md with Docusaurus theme customization instructions
- [ ] T138 [P] Document component API in intellistack/frontend/README.md
- [ ] T139 [P] Document theming system in intellistack/frontend/THEMING.md
- [ ] T140 [P] Create deployment guide in intellistack/frontend/DEPLOYMENT.md
- [ ] T141 Configure CI/CD pipeline in .github/workflows/frontend.yml for Next.js build and deploy
- [ ] T142 Configure CI/CD pipeline in .github/workflows/docusaurus.yml for Docusaurus build and deploy
- [ ] T143 Set up staging environment for Next.js frontend
- [ ] T144 Set up staging environment for Docusaurus
- [ ] T145 Deploy Next.js frontend to production (Vercel or similar)
- [ ] T146 Deploy Docusaurus to production (Netlify or similar)
- [ ] T147 Configure production environment variables (AUTH_URL, API_URL, cookie domain)
- [ ] T148 Monitor production deployment for errors and performance issues
- [ ] T149 Run smoke tests on production verifying all user stories work end-to-end

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-10)**: All depend on Foundational phase completion
  - US1 (Landing Page): Can start after Foundational - No dependencies on other stories
  - US3 (Authentication): Can start after Foundational - No dependencies on other stories
  - US2 (Personalization): Depends on US3 (needs auth) - Can start after US3 complete
  - US4 (Docusaurus Integration): Can start after Foundational - No dependencies on other stories
  - US5 (Navigation): Can start after Foundational - Enhances existing components
  - US6 (Integration Testing): Depends on US1, US2, US3, US4 - Validates integration
  - US7 (Mobile): Can start after Foundational - Optimizes existing components
- **Cross-Cutting (Phase 11-13)**: Depends on all desired user stories being complete
- **Documentation & Deployment (Phase 14)**: Depends on all previous phases

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Depends on User Story 3 (authentication required for personalization)
- **User Story 4 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 5 (P2)**: Can start after Foundational (Phase 2) - Enhances existing components
- **User Story 6 (P2)**: Depends on User Stories 1, 2, 3, 4 - Integration testing
- **User Story 7 (P2)**: Can start after Foundational (Phase 2) - Optimizes existing components

### Within Each User Story

- Effect components before page components (e.g., NeuralNetworkBackground before Hero)
- UI components before page components (e.g., Button before LoginForm)
- Form components before page integration (e.g., LoginForm before login page)
- Core implementation before optimization (e.g., basic animations before mobile optimization)

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T003, T004, T005, T006, T007, T008)
- All Foundational UI components marked [P] can run in parallel (T016-T025)
- Once Foundational phase completes:
  - US1 (Landing Page) and US3 (Authentication) can start in parallel
  - US4 (Docusaurus Theme) can start in parallel with US1 and US3
- Within US1: All effect components marked [P] can run in parallel (T026-T032)
- Within US1: All landing components marked [P] can run in parallel (T033-T035)
- Within US3: All auth components marked [P] can run in parallel (T040-T043)
- Within US2: All personalization components marked [P] can run in parallel (T049-T052)
- Within US7: All mobile optimization tasks marked [P] can run in parallel (T093-T100)
- All cross-cutting tasks marked [P] can run in parallel within their phase

---

## Parallel Example: User Story 1 (Landing Page)

```bash
# After Foundational phase completes, launch all effect components together:
Task T026: "Implement NeuralNetworkBackground Canvas variant"
Task T027: "Implement NeuralNetworkBackground SVG variant"
Task T028: "Add device detection logic to NeuralNetworkBackground"
Task T029: "Create neural network SVG pattern"
Task T030: "Implement Robot3D component"
Task T031: "Implement Robot2D component"
Task T032: "Add lazy loading for Robot3D"

# Then launch all landing components together:
Task T033: "Implement Hero component"
Task T034: "Implement FeatureCard component"
Task T035: "Implement TestimonialCarousel component"
```

---

## Implementation Strategy

### MVP First (User Stories 1, 3, 2, 4 Only)

1. Complete Phase 1: Setup (T001-T010)
2. Complete Phase 2: Foundational (T011-T025) - CRITICAL - blocks all stories
3. Complete Phase 3: User Story 1 - Landing Page (T026-T039)
4. Complete Phase 4: User Story 3 - Authentication (T040-T048)
5. Complete Phase 5: User Story 2 - Personalization (T049-T059)
6. Complete Phase 6-7: User Story 4 - Docusaurus Integration (T060-T079)
7. **STOP and VALIDATE**: Test all P1 user stories independently
8. Deploy/demo MVP if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (Landing) → Test independently → Deploy/Demo (First impression!)
3. Add User Story 3 (Auth) → Test independently → Deploy/Demo (Users can register!)
4. Add User Story 2 (Personalization) → Test independently → Deploy/Demo (Personalized experience!)
5. Add User Story 4 (Docusaurus) → Test independently → Deploy/Demo (Complete learning platform!)
6. Add User Story 5 (Navigation) → Test independently → Deploy/Demo
7. Add User Story 6 (Integration) → Test independently → Deploy/Demo
8. Add User Story 7 (Mobile) → Test independently → Deploy/Demo
9. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T025)
2. Once Foundational is done:
   - Developer A: User Story 1 (Landing Page) - T026-T039
   - Developer B: User Story 3 (Authentication) - T040-T048
   - Developer C: User Story 4 (Docusaurus Theme) - T060-T071
3. After US3 completes:
   - Developer B: User Story 2 (Personalization) - T049-T059
4. After US1, US2, US3, US4 complete:
   - Developer A: User Story 5 (Navigation) - T080-T086
   - Developer B: User Story 6 (Integration) - T087-T092
   - Developer C: User Story 7 (Mobile) - T093-T102
5. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies - can run in parallel
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Tests are NOT included per specification (no explicit test requirements)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Total tasks: 149 tasks across 14 phases
- MVP scope: Phases 1-7 (79 tasks) covering P1 user stories
- Estimated time: 52-66 hours per plan.md (7-9 working days)
