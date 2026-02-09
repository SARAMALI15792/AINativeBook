'use client';

import { useEffect, useState } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { useUserStore } from '@/stores/userStore';

const publicRoutes = ['/', '/login', '/register', '/forgot-password'];
const authRoutes = ['/login', '/register'];

export function AuthGuard({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const pathname = usePathname();
  const { isAuthenticated, fetchUser } = useUserStore();
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('token');
      const isPublicRoute = publicRoutes.includes(pathname);
      const isAuthRoute = authRoutes.includes(pathname);

      // If we have a token, verify it's still valid
      if (token && !isAuthenticated) {
        try {
          await fetchUser();
        } catch (error) {
          // Token is invalid, will be cleared by fetchUser
          if (!isPublicRoute) {
            router.push(`/login?from=${pathname}`);
          }
        }
      }

      // Redirect logic
      if (!token && !isPublicRoute) {
        router.push(`/login?from=${pathname}`);
      } else if (token && isAuthRoute) {
        router.push('/dashboard');
      }

      setIsLoading(false);
    };

    checkAuth();
  }, [pathname, isAuthenticated, fetchUser, router]);

  // Show loading state while checking auth
  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-900">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-slate-400">Loading...</p>
        </div>
      </div>
    );
  }

  return <>{children}</>;
}
