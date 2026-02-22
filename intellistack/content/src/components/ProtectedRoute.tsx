import React, { useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useLocation, useNavigate } from '@docusaurus/router';

interface ProtectedRouteProps {
  children: React.ReactNode;
  requireAuth?: boolean;
}

export default function ProtectedRoute({ children, requireAuth = true }: ProtectedRouteProps) {
  const { user, loading } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    if (!loading && requireAuth && !user) {
      // Navigate to login page with return URL using Docusaurus router
      const returnUrl = encodeURIComponent(location.pathname + location.search);
      navigate(`/login?returnUrl=${returnUrl}`);
    }
  }, [user, loading, requireAuth, navigate, location]);

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
