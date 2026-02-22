/**
 * Better-Auth OIDC Server Entry Point
 * Provides JWT-based authentication with OIDC discovery and JWKS endpoints
 */

// Load environment variables BEFORE any other imports
// Use absolute path resolution to handle different execution contexts
import dotenv from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';

// Get directory name for absolute path resolution
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Load .env file with absolute path for reliability across different environments
dotenv.config({ path: path.resolve(__dirname, '../.env') });

import express, { Request, Response, NextFunction } from 'express';
import cors from 'cors';
import helmet from 'helmet';
import { toNodeHandler } from 'better-auth/node';

// Dynamic import so env vars are loaded before auth/db modules initialize
const { auth } = await import('./auth.js');

// Import database connection check function
const { checkDatabaseConnection } = await import('./db.js');

const app = express();
const PORT = process.env.PORT || 3001;

// ==========================================
// Middleware
// ==========================================

// Security headers
app.use(helmet());

// CORS configuration
const corsOptions = {
  origin: process.env.CORS_ORIGINS?.split(',') || [
    'http://localhost:3000',
    'http://localhost:3001',
    'http://localhost:3002',
    'http://localhost:3004',
    'http://localhost:8000',
    'https://saramali15792.github.io',
  ],
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization', 'X-Requested-With'],
};
app.use(cors(corsOptions));

// Request logging middleware
app.use((req: Request, res: Response, next: NextFunction) => {
  const start = Date.now();
  res.on('finish', () => {
    const duration = Date.now() - start;
    console.log(`[${new Date().toISOString()}] ${req.method} ${req.path} ${res.statusCode} ${duration}ms`);
  });
  next();
});

// Body parser
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// ==========================================
// Health Check
// ==========================================

app.get('/health', (_req: Request, res: Response) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// ==========================================
// OIDC Discovery & JWKS Endpoints
// ==========================================

app.get('/.well-known/openid-configuration', async (_req: Request, res: Response) => {
  const issuer = process.env.BETTER_AUTH_URL || 'http://localhost:3001';
  const oidcConfig = {
    issuer,
    authorization_endpoint: `${issuer}/api/auth/authorize`,
    token_endpoint: `${issuer}/api/auth/token`,
    userinfo_endpoint: `${issuer}/api/auth/userinfo`,
    jwks_uri: `${issuer}/.well-known/jwks.json`,
    scopes_supported: ['openid', 'profile', 'email'],
    response_types_supported: ['code', 'token', 'id_token', 'code id_token'],
    subject_types_supported: ['public'],
    id_token_signing_alg_values_supported: ['EdDSA'],
    token_endpoint_auth_methods_supported: ['client_secret_basic', 'client_secret_post'],
  };
  res.json(oidcConfig);
});

app.get('/.well-known/jwks.json', async (_req: Request, res: Response) => {
  try {
    // Proxy to Better-Auth's internal JWKS endpoint (mounted at basePath + jwksPath)
    // Use 0.0.0.0 to allow container to reach itself on the bound port
    const jwksUrl = `http://0.0.0.0:${PORT}/api/auth/.well-known/jwks.json`;
    const response = await fetch(jwksUrl);
    if (!response.ok) {
      throw new Error(`JWKS fetch failed: ${response.status}`);
    }
    const jwks = await response.json();
    res.json(jwks);
  } catch (error) {
    console.error('Error fetching JWKS:', error);
    res.status(500).json({ error: 'Failed to fetch JWKS' });
  }
});

// ==========================================
// Better-Auth API Routes
// ==========================================

// Mount all Better-Auth routes at /api/auth/*
app.all('/api/auth/*', toNodeHandler(auth));

// ==========================================
// Error Handling
// ==========================================

app.use((err: Error, _req: Request, res: Response, _next: NextFunction) => {
  console.error('Error:', err);
  res.status(500).json({
    error: 'Internal server error',
    message: process.env.NODE_ENV === 'development' ? err.message : undefined,
  });
});

app.use((_req: Request, res: Response) => {
  res.status(404).json({ error: 'Not found' });
});

// ==========================================
// Server Startup
// ==========================================

async function start() {
  try {
    // Check database connectivity before starting server
    console.log('🔍 Checking database connection...');
    const dbConnected = await checkDatabaseConnection();

    if (!dbConnected) {
      console.error('❌ Database connection failed. Server cannot start.');
      process.exit(1);
    }

    console.log('✅ Database connection successful. Starting server...');

    app.listen(PORT, () => {
      console.log(`✅ Auth server running on http://localhost:${PORT}`);
      console.log(`📋 OIDC Discovery: http://localhost:${PORT}/.well-known/openid-configuration`);
      console.log(`🔑 JWKS Endpoint: http://localhost:${PORT}/.well-known/jwks.json`);
      console.log(`📚 API Routes: http://localhost:${PORT}/api/auth/*`);
    });
  } catch (error) {
    console.error('Failed to start server:', error);
    process.exit(1);
  }
}

start();

export default app;
