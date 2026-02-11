/**
 * Better-Auth Configuration
 * OIDC server with JWT RS256 signing, email/password, OAuth providers
 */

import { betterAuth } from 'better-auth';
import { drizzleAdapter } from 'better-auth/adapters/drizzle';
import { jwt } from 'better-auth/plugins';
import { oidcProvider } from 'better-auth/plugins';
import { db } from './db';

// Validate required environment variables
const validateEnv = () => {
  const required = ['DATABASE_URL', 'BETTER_AUTH_SECRET', 'BETTER_AUTH_URL'];
  const missing = required.filter((key) => !process.env[key]);

  if (missing.length > 0) {
    throw new Error(`Missing required environment variables: ${missing.join(', ')}`);
  }
};

validateEnv();

/**
 * Initialize Better-Auth with:
 * - JWT plugin for RS256 token signing
 * - OIDC Provider plugin for OpenID Connect discovery
 * - Email/password authentication
 * - Google OAuth
 * - GitHub OAuth
 * - Role-based access control (student, instructor, admin)
 */
export const auth = betterAuth({
  // Database adapter
  database: drizzleAdapter(db, {
    provider: 'pg',
    schema: {
      user: 'user',
      session: 'session',
      verification: 'verification',
      account: 'account',
    },
  }),

  // Base URL for OIDC discovery and callbacks
  baseURL: process.env.BETTER_AUTH_URL || 'http://localhost:3001',
  basePath: '/api/auth',
  secret: process.env.BETTER_AUTH_SECRET || 'your-secret-key-min-32-characters',

  // Trust proxy headers (for reverse proxy deployment)
  trustHost: process.env.BETTER_AUTH_TRUST_HOST === 'true',

  // Email configuration
  emailAndPassword: {
    enabled: true,
    autoSignInAfterVerification: false, // Require email verification before login
    minPasswordLength: 12,
    maxPasswordLength: 128,
  },

  // Session configuration
  session: {
    expiresIn: 6 * 60 * 60, // 6 hours for access token
    updateAgeSession: 60 * 60, // Refresh token after 1 hour
    absoluteExpiresIn: 7 * 24 * 60 * 60, // 7 days absolute expiry
  },

  // Social OAuth providers
  socialProviders: {
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID || '',
      clientSecret: process.env.GOOGLE_CLIENT_SECRET || '',
      redirectURI: `${process.env.BETTER_AUTH_URL}/api/auth/callback/google`,
    },
    github: {
      clientId: process.env.GITHUB_CLIENT_ID || '',
      clientSecret: process.env.GITHUB_CLIENT_SECRET || '',
      redirectURI: `${process.env.BETTER_AUTH_URL}/api/auth/callback/github`,
    },
  },

  // Plugins for extended functionality
  plugins: [
    // JWT Plugin: RS256 signing for token verification at JWKS endpoint
    jwt({
      name: 'jwt', // Name for the plugin
      jwks: {
        jwksPath: '/.well-known/jwks.json', // Standard OIDC JWKS endpoint
      },
      alg: 'RS256', // RS256 (asymmetric) - can be verified without calling auth server
      iss: 'iss', // Issuer claim
      aud: 'aud', // Audience claim
      keyPairConfig: {
        alg: 'RS256',
        crv: 'P-256', // NIST P-256 elliptic curve
      },
    }),

    // OIDC Provider Plugin: OpenID Connect discovery endpoint
    oidcProvider({
      useJWTPlugin: true, // Integrate with JWT plugin
      metadata: {
        issuer: process.env.BETTER_AUTH_URL || 'http://localhost:3001',
        authorization_endpoint: `${process.env.BETTER_AUTH_URL}/api/auth/authorize`,
        token_endpoint: `${process.env.BETTER_AUTH_URL}/api/auth/token`,
        userinfo_endpoint: `${process.env.BETTER_AUTH_URL}/api/auth/userinfo`,
        jwks_uri: `${process.env.BETTER_AUTH_URL}/.well-known/jwks.json`,
        scopes_supported: ['openid', 'profile', 'email'],
        response_types_supported: ['code', 'token', 'id_token'],
        subject_types_supported: ['public'],
        id_token_signing_alg_values_supported: ['RS256'],
      },
    }),
  ],

  // Callbacks for auth events (logging, analytics, etc.)
  callbacks: {
    async signIn({ user, account, profile, isNewUser }) {
      // Log sign-in event
      console.log(`Sign in: user=${user.email}, provider=${account?.provider}, new=${isNewUser}`);
      return true; // Allow sign-in
    },

    async jwt({ token, user, account }) {
      // Add custom claims to JWT
      if (user) {
        token.id = user.id;
        token.email = user.email;
        token.role = user.role || 'student'; // Default role
      }
      return token;
    },

    async session({ session, user, token }) {
      // Add custom fields to session
      session.user.role = user.role || 'student';
      return session;
    },
  },

  // Security headers
  headers: {
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'DENY',
    'X-XSS-Protection': '1; mode=block',
  },
});

export type Session = typeof auth.$Infer.Session;
export type User = typeof auth.$Infer.User;
export type Auth = typeof auth;
