import { NextRequest, NextResponse } from 'next/server';

// Routes that require authentication
const PROTECTED_ROUTES = ['/secure-admin'];

// Public routes within protected area (no auth needed)
const PUBLIC_ADMIN_ROUTES = ['/secure-admin/login'];

export async function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Check if the route is a public admin route (login page)
  const isPublicAdminRoute = PUBLIC_ADMIN_ROUTES.some(route => 
    pathname === route || pathname.startsWith(`${route}/`)
  );

  // Check if the route is protected
  const isProtectedRoute = PROTECTED_ROUTES.some(route => 
    pathname === route || pathname.startsWith(`${route}/`)
  );

  // If it's not a protected route, allow access
  if (!isProtectedRoute) {
    return NextResponse.next();
  }

  // Get the refresh token from cookies (indicates user is logged in)
  const refreshToken = request.cookies.get('refresh_token')?.value;

  // If it's a public admin route (login) and user has refresh token, redirect to admin
  if (isPublicAdminRoute && refreshToken) {
    // User is logged in, redirect to admin dashboard
    return NextResponse.redirect(new URL('/secure-admin', request.url));
  }

  // If it's a public admin route (login) and no token, allow access
  if (isPublicAdminRoute) {
    return NextResponse.next();
  }

  // For protected routes, check if user has refresh token
  if (!refreshToken) {
    // No refresh token, redirect to login
    const loginUrl = new URL('/secure-admin/login', request.url);
    loginUrl.searchParams.set('redirect', pathname);
    return NextResponse.redirect(loginUrl);
  }

  // User has refresh token, allow access
  // The actual token validation will happen client-side with access token
  return NextResponse.next();
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public files
     */
    '/((?!api|_next/static|_next/image|favicon.ico|.*\\..*|_next).*)',
  ],
};
