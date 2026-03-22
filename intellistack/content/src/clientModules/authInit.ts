/**
 * Auth initialization module for Docusaurus
 * Runs on client-side to initialize auth state and restore theme preference.
 */

import ExecutionEnvironment from '@docusaurus/ExecutionEnvironment';

if (ExecutionEnvironment.canUseDOM) {
  import('../lib/auth-client')
    .then(async ({ getAuthClient }) => {
      try {
        const client = getAuthClient();
        const session = await client.getSession();

        // Restore theme preference from user profile
        if (session?.data) {
          try {
            const backendUrl = process.env.BACKEND_URL || 'http://localhost:8000';
            const res = await fetch(`${backendUrl}/api/v1/users/preferences`, { credentials: 'include' });
            if (res.ok) {
              // Theme is stored in user.preferences on the auth server
            }
          } catch {
            // Non-critical — silently ignore
          }

          // Check theme from auth server user preferences
          try {
            const authServerUrl = process.env.BETTER_AUTH_URL || 'http://localhost:3001';
            const sessionRes = await fetch(`${authServerUrl}/api/auth/get-session`, { credentials: 'include' });
            if (sessionRes.ok) {
              const sessionData = await sessionRes.json();
              const savedTheme = sessionData?.user?.preferences?.theme;
              if (savedTheme === 'light' || savedTheme === 'dark') {
                // Docusaurus exposes setColorMode via the colorMode store
                const colorModeKey = 'docusaurus.colorMode';
                const current = localStorage.getItem(colorModeKey);
                if (current !== savedTheme) {
                  localStorage.setItem(colorModeKey, savedTheme);
                  document.documentElement.setAttribute('data-theme', savedTheme);
                }
              }
            }
          } catch {
            // Silent — non-critical
          }
        }
      } catch {
        // Auth server unreachable — silent fail
      }
    })
    .catch(() => {
      // Module load failed — silent
    });
}

export function onRouteDidUpdate({ location, previousLocation }) {
  if (location.pathname !== previousLocation?.pathname) {
    // Route changed — could refresh session here if needed
  }
}

export function onRouteUpdate({ location, previousLocation }) {
  // Can be used to show loading state
}
