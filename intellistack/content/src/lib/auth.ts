// Simple auth client for Docusaurus (browser-only)
// Uses fetch API to communicate with Better Auth server

// Get config from Docusaurus customFields (available in browser)
const getConfig = () => {
  if (typeof window !== 'undefined' && window.docusaurus) {
    return {
      betterAuthUrl: window.docusaurus.siteConfig.customFields?.betterAuthUrl as string || 'http://localhost:3001',
      isProduction: window.location.hostname !== 'localhost',
    };
  }
  return {
    betterAuthUrl: 'http://localhost:3001',
    isProduction: false,
  };
};

const config = getConfig();

// Auth client object
export const authClient = {
  baseURL: config.betterAuthUrl,

  async getSession() {
    try {
      const response = await fetch(`${this.baseURL}/api/auth/session`, {
        credentials: 'include',
      });

      if (!response.ok) {
        return null;
      }

      const data = await response.json();
      return data.user || null;
    } catch (error) {
      console.error('Get session error:', error);
      return null;
    }
  },

  async signOut() {
    try {
      const response = await fetch(`${this.baseURL}/api/auth/signout`, {
        method: 'POST',
        credentials: 'include',
      });

      if (!response.ok) {
        throw new Error('Logout failed');
      }

      return await response.json();
    } catch (error) {
      console.error('Logout error:', error);
      throw error;
    }
  },
};

// Helper functions for backward compatibility
export async function getSession() {
  return authClient.getSession();
}

export async function signOut() {
  return authClient.signOut();
}
