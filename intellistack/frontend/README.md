# IntelliStack Frontend

Next.js 14 frontend for the IntelliStack AI-Native Learning Platform.

## Prerequisites

- Node.js 18+
- npm 9+

## Quick Start

```bash
# Install dependencies
npm install --legacy-peer-deps

# Copy environment variables
cp .env.example .env.local

# Start development server
npm run dev
```

The app runs at `http://localhost:3004` by default.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `NEXT_PUBLIC_AUTH_URL` | `http://localhost:3001` | Better-Auth OIDC server |
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000` | FastAPI backend |
| `NEXT_PUBLIC_DOCUSAURUS_URL` | `http://localhost:3002` | Docusaurus content site |
| `PORT` | `3004` | Dev server port |

## Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server |
| `npm run build` | Production build |
| `npm run start` | Start production server |
| `npm run lint` | Run ESLint |
| `npm run type-check` | TypeScript type checking |
| `npm run test` | Run unit tests (vitest) |
| `npm run format` | Format code with Prettier |

## Project Structure

```
src/
├── app/                    # Next.js App Router pages
│   ├── layout.tsx          # Root layout with Providers
│   ├── page.tsx            # Landing page (/)
│   ├── providers.tsx       # Client-side context providers
│   ├── not-found.tsx       # 404 page
│   ├── error.tsx           # Error boundary page
│   ├── auth/
│   │   ├── login/page.tsx  # Login page
│   │   └── register/page.tsx # Registration page
│   └── personalization/
│       └── page.tsx        # Onboarding wizard
├── components/
│   ├── ui/                 # Reusable UI primitives
│   ├── effects/            # Visual effects (Robot, Glass, Neural Network)
│   ├── layout/             # Header, Footer, MobileMenu
│   ├── landing/            # Landing page sections
│   ├── auth/               # Auth forms and social buttons
│   └── personalization/    # Onboarding wizard components
├── contexts/               # React Context providers
│   ├── AuthContext.tsx      # Authentication state
│   └── ThemeContext.tsx     # Theme configuration
├── lib/                    # Utilities and clients
│   ├── auth.ts             # Auth API client
│   └── api-client.ts       # Backend API client
├── styles/
│   ├── globals.css         # Global styles and Tailwind
│   ├── tokens.css          # Design tokens (colors, spacing)
│   └── animations.css      # Animation keyframes
└── types/
    └── api.ts              # Shared TypeScript types
```

## Architecture

### Cross-Site Integration

IntelliStack uses two frontends:

- **Next.js** (this project): Landing page, auth, personalization, dashboard
- **Docusaurus** (`intellistack/content/`): Learning content, documentation

Links between sites use environment variables:
- Next.js links to Docusaurus via `NEXT_PUBLIC_DOCUSAURUS_URL`
- Docusaurus links back via `FRONTEND_URL` custom field in `docusaurus.config.ts`

### Authentication

Auth is handled by Better-Auth OIDC server. Both frontends share cookies via the same auth server at `NEXT_PUBLIC_AUTH_URL`. The `AuthProvider` in `providers.tsx` wraps the entire app.

### Theming

Uses CSS custom properties defined in `tokens.css` with a dark-first design. See `THEMING.md` for details.
