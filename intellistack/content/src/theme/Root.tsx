import React, { useEffect } from 'react';
import { AuthProvider } from '../contexts/AuthContext';
import ChatKitWidget from '../components/ai/ChatKitWidget';

// Root wrapper for Docusaurus to provide auth context
export default function Root({ children }) {
  useEffect(() => {
    // Check if coming from personalization
    const params = new URLSearchParams(window.location.search);
    const from = params.get('from');
    if (from === 'personalization' || from === 'login') {
      // Verify session is active
      import('@site/src/lib/auth-client.ts').then(async (mod) => {
        const session = await mod.authClient.getSession();
        if (session.data?.user) {
          console.log('Session verified after personalization redirect');
          // Dispatch event to refresh ChatKit widget
          window.dispatchEvent(new Event('auth-state-changed'));
          // Clean URL
          window.history.replaceState({}, '', window.location.pathname);
        } else {
          console.warn('No session found after personalization redirect');
        }
      }).catch(err => {
        console.error('Failed to verify session:', err);
      });
    }
  }, []);

  return (
    <AuthProvider>
      {children}
      <ChatKitWidget />
    </AuthProvider>
  );
}
