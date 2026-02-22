import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

const protectedRoutes = ['/dashboard', '/personalization', '/curriculum', '/profile'];
const authRoutes = ['/auth/login', '/auth/register'];

export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  const isProtectedRoute = protectedRoutes.some(route => pathname.startsWith(route));
  const isAuthRoute = authRoutes.some(route => pathname.startsWith(route));

  // Check for Better-Auth session cookie (try multiple possible names)
  const allCookies = request.cookies.getAll();
  const sessionCookie = request.cookies.get('better-auth.session_token') ||
                        request.cookies.get('better_auth.session_token') ||
                        request.cookies.get('session_token') ||
                        allCookies.find(c => c.name.includes('session'));

  const isAuthenticated = !!sessionCookie;

  console.log('Middleware check:', {
    pathname,
    isProtectedRoute,
    isAuthenticated,
    sessionCookie: sessionCookie?.name,
    allCookies: allCookies.map(c => c.name)
  });

  if (isProtectedRoute && !isAuthenticated) {
    const loginUrl = new URL('/auth/login', request.url);
    loginUrl.searchParams.set('redirect', pathname);
    return NextResponse.redirect(loginUrl);
  }

  if (isAuthRoute && isAuthenticated) {
    return NextResponse.redirect(new URL('/dashboard', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
};
