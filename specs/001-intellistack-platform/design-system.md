# IntelliStack Design System

## Overview
This document defines the design system for the IntelliStack platform, establishing consistent visual language, components, and patterns to ensure a cohesive user experience across all interfaces.

## Color System

### Primary Palette
- **Primary**: `#2563eb` (Indigo 600) - Main brand color for CTAs and highlights
- **Primary Dark**: `#1d4ed8` (Indigo 700) - Hover states and emphasis
- **Primary Light**: `#3b82f6` (Blue 500) - Alternative primary shade
- **Secondary**: `#64748b` (Slate 500) - Supporting elements
- **Success**: `#10b981` (Emerald 500) - Positive feedback
- **Warning**: `#f59e0b` (Amber 500) - Warnings and caution
- **Danger**: `#ef4444` (Red 500) - Errors and destructive actions

### Neutral Palette
- **Background**: `#f8fafc` (Gray 50) - Main background
- **Surface**: `#ffffff` - Card and modal backgrounds
- **Surface Alt**: `#f1f5f9` (Gray 100) - Secondary surfaces
- **Text Primary**: `#1e293b` (Slate 800) - Main text
- **Text Secondary**: `#64748b` (Slate 500) - Supporting text
- **Text Muted**: `#94a3b8` (Slate 400) - Muted text
- **Border**: `#e2e8f0` (Gray 200) - Borders and dividers
- **Border Strong**: `#cbd5e1` (Gray 300) - Strong borders

### Dark Mode Palette
- **Background**: `#0f172a` (Slate 900) - Main background
- **Surface**: `#1e293b` (Slate 800) - Card and modal backgrounds
- **Surface Alt**: `#334155` (Slate 700) - Secondary surfaces
- **Text Primary**: `#f1f5f9` (Slate 100) - Main text
- **Text Secondary**: `#cbd5e1` (Slate 300) - Supporting text
- **Text Muted**: `#94a3b8` (Slate 400) - Muted text
- **Border**: `#334155` (Slate 700) - Borders and dividers
- **Border Strong**: `#475569` (Slate 600) - Strong borders

## Typography System

### Font Stack
- **Primary**: Inter, system-ui, sans-serif
- **Monospace**: JetBrains Mono, ui-monospace, monospace

### Hierarchy
- **H1**: 2.5rem (40px), Bold, Leading 8, Tracking -0.02em
- **H2**: 2rem (32px), Semi-bold, Leading 7, Tracking -0.015em
- **H3**: 1.5rem (24px), Semi-bold, Leading 6, Tracking -0.01em
- **H4**: 1.25rem (20px), Medium, Leading 6, Tracking -0.005em
- **Body Large**: 1.125rem (18px), Regular, Leading 7
- **Body**: 1rem (16px), Regular, Leading 6
- **Small**: 0.875rem (14px), Regular, Leading 5
- **Caption**: 0.75rem (12px), Regular, Leading 4
- **Code**: 0.875rem (14px), JetBrains Mono, Leading 5

### Code Typography
- **Inline Code**: 0.875rem, JetBrains Mono, Background: Gray 100, Padding: 0.2rem 0.4rem, Border-radius: 0.25rem
- **Code Blocks**: 0.875rem, JetBrains Mono, Line height: 1.5, Background: Gray 50, Padding: 1rem, Border-radius: 0.5rem

## Layout Structure

### Grid System
- **Container**: Max-width 1200px, Centered
- **Gutters**: 1.5rem (24px) on desktop, 1rem (16px) on mobile
- **Breakpoints**:
  - Mobile: 640px
  - Tablet: 768px
  - Desktop: 1024px
  - Large: 1200px

### Spacing Scale
- **xs**: 0.25rem (4px)
- **sm**: 0.5rem (8px)
- **md**: 1rem (16px)
- **lg**: 1.5rem (24px)
- **xl**: 2rem (32px)
- **2xl**: 3rem (48px)
- **3xl**: 4rem (64px)
- **4xl**: 5rem (80px)

### Z-Index Scale
- **dropdown**: 1000
- **sticky**: 1100
- **fixed**: 1200
- **modal-backdrop**: 1300
- **modal**: 1400
- **popover**: 1500
- **tooltip**: 1600

## Component Specifications

### Buttons
- **Primary**: bg-primary text-white hover:bg-primary-dark
- **Secondary**: bg-transparent border border-primary text-primary hover:bg-primary/10
- **Ghost**: bg-transparent text-primary hover:bg-primary/10
- **Danger**: bg-danger text-white hover:bg-danger-dark
- **Sizes**: sm (height: 2rem, padding: 0 0.75rem), md (height: 2.5rem, padding: 0 1rem), lg (height: 3rem, padding: 0 1.25rem)
- **Radius**: 0.375rem (6px)

### Cards
- **Background**: white (dark: slate-800)
- **Border**: 1px solid border (dark: slate-700)
- **Shadow**: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1)
- **Padding**: 1.5rem
- **Radius**: 0.5rem (8px)

### Inputs
- **Background**: white (dark: slate-800)
- **Border**: 1px solid border (dark: slate-700)
- **Focus**: ring-2 ring-primary/50
- **Padding**: 0.5rem 0.75rem
- **Radius**: 0.375rem (6px)

### Navigation
- **Top Navigation Height**: 4rem (64px)
- **Sidebar Width**: 16rem (256px)
- **Mobile Menu Height**: 4rem (64px)

## Component Library

### Core Components
- **Button**: Primary, secondary, ghost, and danger variants
- **Card**: Content containers with consistent styling
- **Input**: Text, password, textarea with validation states
- **Select**: Dropdown menus with search capability
- **Modal**: Overlay dialogs with proper focus management
- **Alert**: Information, success, warning, and error messages
- **Badge**: Status indicators and tags
- **Avatar**: User profile images with fallbacks
- **Tooltip**: Contextual information on hover
- **Spinner**: Loading indicators

### Learning Components
- **Progress Bar**: Visual representation of completion (linear and circular)
- **Badge Display**: Achievement recognition system
- **Code Block**: Syntax-highlighted code with copy functionality
- **Quiz Interface**: Interactive assessment components
- **Simulation Viewer**: Embedded simulation environments
- **Learning Path**: Visual representation of course progression
- **Content Card**: Lesson and resource cards with status indicators

### Layout Components
- **Header**: Top navigation with branding and user menu
- **Sidebar**: Collapsible navigation for dashboard sections
- **Grid**: Responsive grid system for content organization
- **Breadcrumb**: Navigation path indicator
- **Footer**: Site-wide footer with important links
- **Container**: Centered content containers with max-width

## Accessibility Standards

### Color Contrast
- Minimum 4.5:1 ratio for normal text
- Minimum 3:1 ratio for large text
- Enhanced contrast (7:1) for critical information

### Keyboard Navigation
- Visible focus indicators on all interactive elements
- Logical tab order following visual flow
- Skip links for main content
- Keyboard shortcuts for common actions

### Screen Reader Support
- Semantic HTML with proper heading structure
- ARIA labels for interactive elements
- Alternative text for all meaningful images
- Live regions for dynamic content updates

### Visual Accessibility
- Support for user's reduced motion preference
- High contrast mode support
- Text scaling up to 200% without loss of functionality
- Clear visual hierarchy and information architecture

## Responsive Design

### Breakpoints
- **Mobile**: Up to 639px
- **Tablet**: 640px to 1023px
- **Desktop**: 1024px to 1279px
- **Large**: 1280px and above

### Touch Targets
- Minimum 44px touch targets
- Adequate spacing between interactive elements
- Thumb-friendly positioning for mobile interactions

### Orientation Handling
- Proper layout adjustment for portrait/landscape
- Content remains readable in both orientations
- Navigation remains accessible in all orientations

## Animation & Micro-interactions

### Duration
- Quick: 150ms (hover states, small transitions)
- Standard: 300ms (page transitions, modal appearance)
- Slow: 500ms (complex animations, loading states)

### Easing
- Ease-out for entrance animations
- Ease-in for exit animations
- Linear for progress indicators

### Motion Preferences
- Respect user's reduced motion preference
- Provide alternatives for motion-sensitive users
- Avoid flashing or strobing effects

## Theming System

### Theme Variables
- Define all colors, spacing, typography as CSS custom properties
- Enable runtime theme switching
- Support for user preferences (prefers-color-scheme)

### Theme Provider
- Context provider for theme state
- Persistent theme preference storage
- Smooth theme transitions

## Implementation Guidelines

### CSS Architecture
- Use utility-first approach with Tailwind CSS
- Extend Tailwind with custom theme values
- Create component classes for complex compositions
- Maintain consistent naming conventions

### Component Composition
- Build components with composition in mind
- Use slots/children for flexible content
- Maintain consistent prop interfaces
- Provide sensible defaults

### Performance Considerations
- Minimize custom CSS in favor of utilities
- Use CSS containment for performance
- Optimize images and media
- Implement proper loading states

## Testing & Validation

### Visual Regression Testing
- Automated screenshot testing for component variations
- Cross-browser visual consistency checks
- Responsive design validation

### Accessibility Testing
- Automated accessibility scanning
- Keyboard navigation testing
- Screen reader compatibility checks
- Color contrast validation

### Cross-browser Compatibility
- Test in major browsers (Chrome, Firefox, Safari, Edge)
- Validate responsive behavior
- Check for CSS feature support
- Fallback for unsupported features

## Documentation & Maintenance

### Component Documentation
- Storybook-style component documentation
- Usage examples and best practices
- Props and variant documentation
- Accessibility guidelines

### Design Token Management
- Centralized design token system
- Automated token generation from design files
- Version control for design changes
- Sync between design and development teams

## Future Considerations

### Scalability
- Modular design system architecture
- Extensible component patterns
- Flexible theming capabilities
- Internationalization support

### Innovation
- Stay current with design trends
- Incorporate user feedback
- Experiment with new interaction patterns
- Evolve with platform needs