/**
 * Better-Auth Configuration
 * OIDC server with JWT RS256 signing, email/password, OAuth providers
 */

import { betterAuth } from 'better-auth';
import { drizzleAdapter } from 'better-auth/adapters/drizzle';
import { jwt } from 'better-auth/plugins';
import { oidcProvider } from 'better-auth/plugins';
import { db } from './db.js';
import * as schema from './auth-schema.js';

// Validate required environment variables
const validateEnv = () => {
  const required = ['DATABASE_URL', 'BETTER_AUTH_SECRET', 'BETTER_AUTH_URL'];
  const missing = required.filter((key) => !process.env[key]);

  if (missing.length > 0) {
    console.error('❌ Missing required environment variables:', missing.join(', '));
    console.error('💡 Make sure your .env file contains all required variables');
    console.error('📋 Required variables:', required.join(', '));
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
    schema,
  }),

  // Base URL for OIDC discovery and callbacks
  baseURL: process.env.BETTER_AUTH_URL!,
  basePath: '/api/auth',
  secret: process.env.BETTER_AUTH_SECRET!,

  // Trust proxy headers (for reverse proxy deployment)
  trustHost: process.env.BETTER_AUTH_TRUST_HOST === 'true',

  // Trusted origins for cross-origin requests (frontend → auth server)
  trustedOrigins: process.env.CORS_ORIGINS?.split(',') || [],

  // Email configuration
  emailAndPassword: {
    enabled: true,
    autoSignInAfterVerification: true, // For development - auto sign in after email verification
    requireEmailVerification: false, // Disable email verification for development
    minPasswordLength: 8,
    maxPasswordLength: 128,
  },

  // Session configuration
  session: {
    expiresIn: 24 * 60 * 60, // 24 hours for session token
    updateAgeSession: 60 * 60, // Refresh session after 1 hour of activity
    absoluteExpiresIn: 7 * 24 * 60 * 60, // 7 days absolute expiry
    cookieCache: {
      enabled: true,
      maxAge: 5 * 60, // 5 minutes
    },
  },

  // Advanced configuration for cookie handling across localhost ports
  advanced: {
    // Apply domain to ALL cookies (session_token, session_data, etc.)
    // so they are shared across localhost:3000, :3001, :3002, :3004
    defaultCookieAttributes: {
      sameSite: 'lax' as const,
      secure: process.env.NODE_ENV === 'production',
      path: '/',
      domain: process.env.COOKIE_DOMAIN || (process.env.NODE_ENV === 'production' ? undefined : 'localhost'),
    },
  },

  // Social OAuth providers
  socialProviders: {
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID || '',
      clientSecret: process.env.GOOGLE_CLIENT_SECRET || '',
      redirectURI: `${process.env.BETTER_AUTH_URL!}/api/auth/callback/google`,
    },
    github: {
      clientId: process.env.GITHUB_CLIENT_ID || '',
      clientSecret: process.env.GITHUB_CLIENT_SECRET || '',
      redirectURI: `${process.env.BETTER_AUTH_URL!}/api/auth/callback/github`,
    },
  },

  // Plugins for extended functionality
  plugins: [
    // JWT Plugin: EdDSA (Ed25519) signing for token verification at JWKS endpoint
    jwt({
      jwks: {
        jwksPath: '/.well-known/jwks.json', // Standard OIDC JWKS endpoint
        keyPairConfig: {
          alg: 'EdDSA', // EdDSA (Ed25519) - Better-Auth default, asymmetric
          crv: 'Ed25519',
        },
      },
      expiresIn: 24 * 60 * 60, // JWT expires in 24 hours (matches session)
    }),

    // OIDC Provider Plugin: OpenID Connect discovery endpoint
    oidcProvider({
      useJWTPlugin: true, // Integrate with JWT plugin
      loginPage: `${process.env.BETTER_AUTH_URL!}/login`,
      metadata: {
        issuer: process.env.BETTER_AUTH_URL!,
        authorization_endpoint: `${process.env.BETTER_AUTH_URL!}/api/auth/authorize`,
        token_endpoint: `${process.env.BETTER_AUTH_URL!}/api/auth/token`,
        userinfo_endpoint: `${process.env.BETTER_AUTH_URL!}/api/auth/userinfo`,
        jwks_uri: `${process.env.BETTER_AUTH_URL!}/.well-known/jwks.json`,
        scopes_supported: ['openid', 'profile', 'email'],
        response_types_supported: ['code', 'id_token'] as any,
        subject_types_supported: ['public'],
        id_token_signing_alg_values_supported: ['EdDSA'],
      },
    }),
  ],

  // Callbacks for auth events (logging, analytics, etc.)
  callbacks: {
    async signIn({ user, account, isNewUser }: any) {
      // Log sign-in event
      console.log(`Sign in: user=${user.email}, provider=${account?.provider}, new=${isNewUser}`);
      return true; // Allow sign-in
    },

    async jwt({ token, user }: any) {
      // Add custom claims to JWT
      if (user) {
        token.id = user.id;
        token.email = user.email;
        token.role = user.role || 'student'; // Default role
      }
      return token;
    },

    async session({ session, user }: any) {
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
export type User = typeof auth.$Infer.Session.user;
export type Auth = typeof auth;
