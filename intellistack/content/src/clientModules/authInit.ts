/**
 * Auth initialization module for Docusaurus
 * Runs on client-side to initialize auth state
 */

import ExecutionEnvironment from '@docusaurus/ExecutionEnvironment';

// Only run on client side
if (ExecutionEnvironment.canUseDOM) {
  // Initialize auth client when module loads
  import('../lib/auth-client')
    .then(async ({ getAuthClient }) => {
      try {
        const client = getAuthClient();
        await client.getSession();
      } catch {
        // Auth server unreachable — silent fail, user not logged in
      }
    })
    .catch(() => {
      // Module load failed — silent
    });
}

/**
 * Called on route change
 * Can be used to refresh auth state or track page views
 */
export function onRouteDidUpdate({ location, previousLocation }) {
  // Only refresh if route actually changed
  if (location.pathname !== previousLocation?.pathname) {
    // Could refresh session here if needed
    // authClient.getSession();
  }
}

/**
 * Called when route update starts
 */
export function onRouteUpdate({ location, previousLocation }) {
  // Can be used to show loading state
}
