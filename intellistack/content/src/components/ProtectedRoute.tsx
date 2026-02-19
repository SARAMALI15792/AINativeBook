import React, { useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';

interface ProtectedRouteProps {
  children: React.ReactNode;
  requireAuth?: boolean;
}

export default function ProtectedRoute({ children, requireAuth = true }: ProtectedRouteProps) {
  const { user, loading } = useAuth();

  useEffect(() => {
    if (!loading && requireAuth && !user) {
      // Redirect to Docusaurus login page with return URL
      const returnUrl = encodeURIComponent(window.location.href);
      window.location.href = `/login?returnUrl=${returnUrl}`;
    }
  }, [user, loading, requireAuth]);

  if (loading) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        minHeight: '400px' 
      }}>
        <div style={{
          width: '48px',
          height: '48px',
          border: '4px solid rgba(0, 239, 255, 0.2)',
          borderTop: '4px solid #00efff',
          borderRadius: '50%',
          animation: 'spin 1s linear infinite',
        }} />
      </div>
    );
  }

  if (requireAuth && !user) {
    return null; // Will redirect in useEffect
  }

  return <>{children}</>;
}
