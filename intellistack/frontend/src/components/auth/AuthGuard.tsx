'use client';

import { useEffect, useState } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth';

const publicRoutes = ['/', '/login', '/register', '/forgot-password', '/reset-password'];
const authRoutes = ['/login', '/register', '/forgot-password', '/reset-password'];

export function AuthGuard({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const pathname = usePathname();
  const { isAuthenticated, isLoading } = useAuth();
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    if (isLoading) return;

    const isPublicRoute = publicRoutes.includes(pathname);
    const isAuthRoute = authRoutes.includes(pathname);

    if (!isAuthenticated && !isPublicRoute) {
      router.push(`/login?from=${encodeURIComponent(pathname)}`);
    } else if (isAuthenticated && isAuthRoute) {
      router.push('/dashboard');
    }

    setIsReady(true);
  }, [pathname, isAuthenticated, isLoading, router]);

  if (isLoading || !isReady) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4" />
          <p className="text-muted-foreground">Loading...</p>
        </div>
      </div>
    );
  }

  if (authRoutes.includes(pathname) && isAuthenticated) {
    return null;
  }

  if (!publicRoutes.includes(pathname) && !isAuthenticated) {
    return null;
  }

  return <>{children}</>;
}
