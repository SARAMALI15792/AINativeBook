import React, { useEffect } from 'react';
import { AuthProvider } from '../contexts/AuthContext';
import ChatKitWidget from '../components/ai/ChatKitWidget';

// Root wrapper for Docusaurus to provide auth context
export default function Root({ children }) {
  useEffect(() => {
    // Check if coming from personalization or login
    const params = new URLSearchParams(window.location.search);
    const from = params.get('from');
    if (from === 'personalization' || from === 'login') {
      // Verify session is active
      import('../lib/auth').then(async (mod) => {
        const session = await mod.authClient.getSession();
        if (session.data) {
          console.log('Session verified after redirect');
          // Dispatch event to refresh components
          window.dispatchEvent(new Event('auth-state-changed'));
          // Clean URL
          window.history.replaceState({}, '', window.location.pathname);
        } else {
          console.warn('No session found after redirect');
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
