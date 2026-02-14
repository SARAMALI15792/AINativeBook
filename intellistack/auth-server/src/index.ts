/**
 * Better-Auth OIDC Server Entry Point
 * Provides JWT-based authentication with OIDC discovery and JWKS endpoints
 */

import express, { Request, Response, NextFunction } from 'express';
import cors from 'cors';
import helmet from 'helmet';
import dotenv from 'dotenv';
import { toNodeHandler } from 'better-auth/node';
import { auth } from './auth';

// Load environment variables
dotenv.config();

const app = express();
const PORT = process.env.PORT || 3001;

// ==========================================
// Middleware
// ==========================================

// Security headers
app.use(helmet());

// CORS configuration
const corsOptions = {
  origin: process.env.CORS_ORIGINS?.split(',') || ['http://localhost:3001'],
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

app.get('/health', (req: Request, res: Response) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// ==========================================
// OIDC Discovery & JWKS Endpoints
// ==========================================

app.get('/.well-known/openid-configuration', async (req: Request, res: Response) => {
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
    id_token_signing_alg_values_supported: ['RS256'],
    token_endpoint_auth_methods_supported: ['client_secret_basic', 'client_secret_post'],
  };
  res.json(oidcConfig);
});

app.get('/.well-known/jwks.json', async (req: Request, res: Response) => {
  try {
    // Better-Auth provides JWKS data - this will be populated after better-auth migrate
    const jwksData = {
      keys: [
        // Will be populated by Better-Auth
        // RS256 public key for token verification
      ],
    };
    res.json(jwksData);
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

app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  console.error('Error:', err);
  res.status(500).json({
    error: 'Internal server error',
    message: process.env.NODE_ENV === 'development' ? err.message : undefined,
  });
});

app.use((req: Request, res: Response) => {
  res.status(404).json({ error: 'Not found' });
});

// ==========================================
// Server Startup
// ==========================================

async function start() {
  try {
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
