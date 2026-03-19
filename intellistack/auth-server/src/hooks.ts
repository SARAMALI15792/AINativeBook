/**
 * Authentication Event Logging Hooks
 * Logs all auth events for security audit and analytics (FR-028, FR-029)
 */

import { Request } from 'express';

/**
 * Extract user IP address from request
 * Handles proxies and X-Forwarded-For headers
 */
export function getClientIp(req: Request): string {
  const xForwardedFor = req.headers['x-forwarded-for'];
  if (typeof xForwardedFor === 'string') {
    return xForwardedFor.split(',')[0].trim();
  }
  if (Array.isArray(xForwardedFor)) {
    return xForwardedFor[0];
  }
  return req.socket.remoteAddress || 'unknown';
}

/**
 * Get user agent from request
 */
export function getUserAgent(req: Request): string {
  return req.headers['user-agent'] || 'unknown';
}

/**
 * Log authentication event to database
 * Called by Better-Auth hooks
 */
export async function logAuthEvent(
  eventType: 'login_success' | 'login_failed' | 'register' | 'logout' | 'password_reset' | 'oauth_link' | 'oauth_unlink',
  userId: string | null,
  email: string | null,
  req: Request,
  metadata?: Record<string, any>
): Promise<void> {
  try {
    const ipAddress = getClientIp(req);
    const userAgent = getUserAgent(req);

    // In production, persist to database
    // For now, log to console
    console.log('[AUTH EVENT]', {
      eventType,
      userId,
      email,
      ipAddress,
      userAgent,
      timestamp: new Date().toISOString(),
      metadata,
    });

    // TODO: Persist to auth_event_log table in FastAPI backend
    // await db.insert(auth_event_log).values({...})
  } catch (error) {
    console.error('Failed to log auth event:', error);
    // Don't fail the auth operation if logging fails
  }
}

/**
 * Hook handlers for Better-Auth events
 * These are called by the auth library during various auth flows
 */
export const authHooks = {
  /**
   * Called after successful sign-in
   */
  async onSignInSuccess(req: Request, user: any) {
    await logAuthEvent('login_success', user.id, user.email, req, {
      provider: 'email',
    });
  },

  /**
   * Called after failed sign-in attempt
   */
  async onSignInFailure(req: Request, email: string | null, reason: string) {
    await logAuthEvent('login_failed', null, email, req, {
      reason,
    });
  },

  /**
   * Called after successful registration
   */
  async onSignUpSuccess(req: Request, user: any) {
    await logAuthEvent('register', user.id, user.email, req, {
      provider: 'email',
    });
  },

  /**
   * Called after sign-out
   */
  async onSignOutSuccess(req: Request, userId: string) {
    await logAuthEvent('logout', userId, null, req);
  },

  /**
   * Called after password reset
   */
  async onPasswordResetSuccess(req: Request, userId: string, email: string) {
    await logAuthEvent('password_reset', userId, email, req);
  },

  /**
   * Called after OAuth account is linked
   */
  async onOAuthLinkSuccess(req: Request, userId: string, provider: string) {
    await logAuthEvent('oauth_link', userId, null, req, {
      provider,
    });
  },

  /**
   * Called after OAuth account is unlinked
   */
  async onOAuthUnlinkSuccess(req: Request, userId: string, provider: string) {
    await logAuthEvent('oauth_unlink', userId, null, req, {
      provider,
    });
  },
};

/**
 * Middleware to attach request context to Express
 * Allows hooks to access request details
 */
export function createAuthHooksMiddleware(req: Request, _res: any, next: any) {
  // Attach logging utilities to request
  (req as any).authHooks = authHooks;
  (req as any).logAuthEvent = logAuthEvent;
  next();
}
