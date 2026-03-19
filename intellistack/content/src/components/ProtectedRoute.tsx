import React, { useEffect, useState } from 'react';
import { useAuth } from '../contexts/AuthContext';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export default function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { user, loading } = useAuth();
  const [checking, setChecking] = useState(true);

  useEffect(() => {
    if (!loading) {
      // Check authentication only — onboarding is handled by individual pages
      if (!user) {
        const baseUrl = (window as any).docusaurus?.siteConfig?.baseUrl || '/AINativeBook/';
        const returnUrl = encodeURIComponent(window.location.pathname + window.location.search);
        window.location.href = `${baseUrl}auth/login?returnUrl=${returnUrl}`;
        return;
      }

      // User is authenticated — allow access
      setChecking(false);
    }
  }, [user, loading]);

  // Show loading state while checking authentication
  if (loading || checking) {
    return (
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '400px',
      }}>
        <div style={{
          width: '60px',
          height: '60px',
          border: '4px solid var(--ifm-color-emphasis-300)',
          borderTop: '4px solid var(--ifm-color-primary)',
          borderRadius: '50%',
          animation: 'spin 1s linear infinite',
        }} />
        <style>{`
          @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }
        `}</style>
      </div>
    );
  }

  // Render protected content
  return <>{children}</>;
}
