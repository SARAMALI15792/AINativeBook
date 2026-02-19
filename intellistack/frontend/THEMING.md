# IntelliStack Theming System

## Design Tokens

All design tokens are defined in `src/styles/tokens.css` as CSS custom properties.

### Color Palette

| Token | Value | Usage |
|-------|-------|-------|
| `--color-bg-primary` | `#1a1a2e` | Main background |
| `--color-bg-secondary` | `#16213e` | Card/section backgrounds |
| `--color-bg-tertiary` | `#0f3460` | Input fields, elevated surfaces |
| `--color-text-primary` | `#ffffff` | Headings, primary text |
| `--color-text-secondary` | `#e0e0e0` | Body text |
| `--color-text-tertiary` | `#a0a0a0` | Muted/helper text |
| `--color-accent-cyan` | `#00efff` | Primary accent, CTAs |
| `--color-accent-violet` | `#a855f7` | Secondary accent, gradients |
| `--color-accent-teal` | `#14b8a6` | Tertiary accent, success |

### Glassmorphism

```css
.glass {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}
```

### Glow Effects

```css
.shadow-glow-cyan { box-shadow: 0 0 20px rgba(0, 239, 255, 0.3); }
.shadow-glow-violet { box-shadow: 0 0 20px rgba(168, 85, 247, 0.3); }
```

### Animation Durations

| Token | Value | Reduced Motion |
|-------|-------|----------------|
| `--duration-fast` | `150ms` | `0.01ms` |
| `--duration-normal` | `300ms` | `0.01ms` |
| `--duration-slow` | `500ms` | `0.01ms` |

## Theme Mode

Controlled via `ThemeContext`:

```tsx
import { useTheme } from '@/contexts/ThemeContext';

function MyComponent() {
  const { theme, toggleMode, setTheme } = useTheme();
  // theme.mode: ThemeMode.DARK | ThemeMode.LIGHT
  // theme.reducedMotion: boolean
  // theme.highContrast: boolean
}
```

## Tailwind Integration

Custom utilities map to design tokens in `tailwind.config.js`:

```
bg-bg-primary      -> var(--color-bg-primary)
text-accent-cyan    -> var(--color-accent-cyan)
shadow-glow-cyan    -> glow box-shadow
animate-fade-in-up  -> fade + slide animation
```

## Accessibility

- All color combinations meet WCAG 2.1 Level AA (4.5:1 contrast ratio)
- `prefers-reduced-motion` automatically disables animations
- `prefers-color-scheme` sets initial theme mode
- High contrast mode available via `ThemeContext`
