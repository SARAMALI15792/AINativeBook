# Image Assets for Landing Page

This directory contains optimized images for the IntelliStack landing page.

## Required Images

### Hero Section
- `hero-robot.webp` - 3D robot hero image (WebP format, ~200KB)
  - **Alt text:** "3D rendered humanoid robot with metallic cyan and violet accents standing in neutral pose"
- `hero-robot.png` - Fallback PNG version (~500KB)
  - **Alt text:** Same as WebP version

### Features Section
- `feature-ai-tutor.webp` - AI tutor illustration
  - **Alt text:** "AI brain icon with neural network connections representing intelligent tutoring system"
- `feature-simulation.webp` - Simulation environment screenshot
  - **Alt text:** "Gazebo simulation environment showing humanoid robot in virtual testing space"
- `feature-curriculum.webp` - Curriculum visualization
  - **Alt text:** "Progressive learning path diagram showing five stages from foundations to capstone"

### Testimonials
- `avatar-placeholder.webp` - Default avatar (if not using initials)
  - **Alt text:** "Profile picture of [Name]" (replace [Name] with actual name)

## Optimization Guidelines

- **WebP Format**: Primary format for modern browsers (80-90% quality)
- **PNG Fallback**: For older browsers
- **Dimensions**:
  - Hero images: 1200x800px
  - Feature images: 600x400px
  - Avatars: 200x200px
- **Compression**: Use tools like `sharp` or `imagemin` for optimization

## Accessibility Guidelines (WCAG 2.1 Level AA)

### Alt Text Best Practices

1. **Be Descriptive:** Describe what the image shows, not just its purpose
2. **Be Concise:** Keep alt text under 125 characters when possible
3. **Avoid Redundancy:** Don't start with "Image of" or "Picture of"
4. **Context Matters:** Consider the surrounding content when writing alt text
5. **Decorative Images:** Use empty alt="" or aria-hidden="true" for purely decorative images

### Examples

**Good Alt Text:**
- "Humanoid robot with glowing cyan eyes performing object manipulation task"
- "Student using VR headset to interact with simulated robot in virtual environment"
- "Code editor showing ROS 2 Python node with syntax highlighting"

**Bad Alt Text:**
- "Image" (not descriptive)
- "robot.png" (filename, not description)
- "Click here to learn more" (describes action, not image)

## Usage in Next.js

```tsx
import Image from 'next/image';

<Image
  src="/images/hero-robot.webp"
  alt="3D rendered humanoid robot with metallic cyan and violet accents standing in neutral pose"
  width={1200}
  height={800}
  priority
/>
```

## Accessibility Checklist

- [ ] All images have descriptive alt text
- [ ] Decorative images use aria-hidden="true" or empty alt=""
- [ ] Complex images (charts, diagrams) have extended descriptions
- [ ] Text in images is also available as actual text
- [ ] Images don't rely on color alone to convey information

## TODO

Replace placeholder images with actual design assets once available.
