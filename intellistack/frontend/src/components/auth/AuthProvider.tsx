/**
 * Auth provider wrapper for IntelliStack
 *
 * This is a simple wrapper that provides the auth context to the app.
 * The actual auth logic is in the useAuth hook and auth-client.
 */
"use client";

import { ReactNode } from "react";

interface AuthProviderProps {
  children: ReactNode;
}

export default function AuthProvider({ children }: AuthProviderProps) {
  // The actual authentication is handled by useAuth hook and auth-client
  // This provider is kept for future auth context expansion if needed
  return <>{children}</>;
}
