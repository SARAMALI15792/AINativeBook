/**
 * Session utility functions for handling authentication state
 */

/**
 * Polls for session cookie establishment
 * @param maxAttempts Maximum number of polling attempts
 * @param intervalMs Interval between attempts in milliseconds
 * @returns Promise<boolean> True if session cookie found, false otherwise
 */
export async function waitForSession(
  maxAttempts: number = 5,
  intervalMs: number = 1000
): Promise<boolean> {
  for (let i = 0; i < maxAttempts; i++) {
    // Check if session cookie exists
    const cookies = document.cookie.split(';');
    const hasSessionCookie = cookies.some(cookie =>
      cookie.trim().startsWith('better-auth.session_token=') ||
      cookie.trim().startsWith('better_auth.session_token=') ||
      cookie.trim().startsWith('session_token=')
    );

    if (hasSessionCookie) {
      return true;
    }

    // Wait before next attempt
    await new Promise(resolve => setTimeout(resolve, intervalMs));
  }

  return false;
}
