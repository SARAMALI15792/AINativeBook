'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import { getDocusaurusUrl } from '@/lib/docusaurus-utils';

export default function AuthCallbackPage() {
  const router = useRouter();
  const { session, refreshSession } = useAuth();
  const [status, setStatus] = useState('Validating session...');
  const [attempts, setAttempts] = useState(0);

  useEffect(() => {
    const validateAndRedirect = async () => {
      // Poll for session (max 10 attempts, 1 second intervals)
      if (attempts >= 10) {
        setStatus('Session validation failed. Redirecting to login...');
        setTimeout(() => router.push('/auth/login'), 2000);
        return;
      }

      // Refresh session
      await refreshSession();

      // Check if session is established
      if (!session.isAuthenticated) {
        setAttempts(prev => prev + 1);
        setTimeout(validateAndRedirect, 1000);
        return;
      }

      // Session established, check personalization
      setStatus('Loading preferences...');

      if (!session.hasCompletedPersonalization) {
        setStatus('Redirecting to personalization...');
        setTimeout(() => router.push('/personalization'), 500);
      } else {
        setStatus('Redirecting to learning platform...');
        const docusaurusUrl = getDocusaurusUrl('stage-1/intro', { from: 'oauth' });
        setTimeout(() => window.location.href = docusaurusUrl, 500);
      }
    };

    validateAndRedirect();
  }, [attempts, session.isAuthenticated, session.hasCompletedPersonalization, router, refreshSession]);

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-50">
      <div className="text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
        <p className="text-gray-600">{status}</p>
      </div>
    </div>
  );
}
