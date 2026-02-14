/**
 * Authentication hook using IntelliStack's Better-Auth compatible backend
 */
import { useState, useEffect, useCallback } from "react";
import { useRouter } from "next/navigation";
import { authClient, AuthUser } from "@/lib/auth-client";

interface UseAuthReturn {
  user: AuthUser | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, name: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  refetchUser: () => Promise<void>;
}

export function useAuth(): UseAuthReturn {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  // Fetch user on mount
  const fetchUser = useCallback(async () => {
    try {
      const userData = await authClient.getUser();
      setUser(userData);
    } catch (err) {
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchUser();
  }, [fetchUser]);

  const login = useCallback(
    async (email: string, password: string) => {
      setIsLoading(true);
      setError(null);

      try {
        const result = await authClient.signInWithCredentials(email, password);
        setUser(result.user);
        router.push("/learn");
        router.refresh();
      } catch (err) {
        const message = err instanceof Error ? err.message : "Login failed";
        setError(message);
        throw err;
      } finally {
        setIsLoading(false);
      }
    },
    [router]
  );

  const register = useCallback(
    async (email: string, name: string, password: string) => {
      setIsLoading(true);
      setError(null);

      try {
        const result = await authClient.signUp(email, name, password);
        setUser(result.user);
        router.push("/learn");
        router.refresh();
      } catch (err) {
        const message = err instanceof Error ? err.message : "Registration failed";
        setError(message);
        throw err;
      } finally {
        setIsLoading(false);
      }
    },
    [router]
  );

  const logout = useCallback(async () => {
    setIsLoading(true);

    try {
      await authClient.signOut();
      setUser(null);
      router.push("/login");
      router.refresh();
    } catch (err) {
      const message = err instanceof Error ? err.message : "Logout failed";
      setError(message);
    } finally {
      setIsLoading(false);
    }
  }, [router]);

  const refetchUser = useCallback(async () => {
    await fetchUser();
  }, [fetchUser]);

  return {
    user,
    isAuthenticated: !!user,
    isLoading,
    error,
    login,
    register,
    logout,
    refetchUser,
  };
}
