"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { cn } from "@/lib/utils";
import { useUserStore } from "@/stores/userStore";

const navItems = [
  { href: "/learn", label: "Learning Path", icon: "📚" },
  { href: "/assessments", label: "Assessments", icon: "📝" },
  { href: "/ai/chatbot", label: "AI Assistant", icon: "🤖" },
  { href: "/community", label: "Community", icon: "👥" },
  { href: "/profile", label: "Profile", icon: "👤" },
];

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const router = useRouter();
  const { user, isAuthenticated, fetchUser, logout } = useUserStore();
  const [showUserMenu, setShowUserMenu] = useState(false);

  useEffect(() => {
    // Fetch user data on mount if not already loaded
    if (!user && typeof window !== 'undefined') {
      fetchUser();
    }
  }, [user, fetchUser]);

  const handleLogout = async () => {
    await logout();
    router.push('/login');
  };

  return (
    <div className="min-h-screen bg-slate-900">
      {/* Top Navigation */}
      <header className="sticky top-0 z-50 border-b border-slate-800 bg-slate-900/95 backdrop-blur">
        <div className="container mx-auto px-4">
          <div className="flex h-16 items-center justify-between">
            <Link href="/" className="flex items-center gap-2">
              <span className="text-xl font-bold text-blue-400">
                IntelliStack
              </span>
            </Link>

            <nav className="hidden md:flex items-center gap-6">
              {navItems.map((item) => (
                <Link
                  key={item.href}
                  href={item.href}
                  className={cn(
                    "flex items-center gap-2 text-sm font-medium transition-colors",
                    pathname.startsWith(item.href)
                      ? "text-blue-400"
                      : "text-slate-400 hover:text-white"
                  )}
                >
                  <span>{item.icon}</span>
                  <span>{item.label}</span>
                </Link>
              ))}
            </nav>

            <div className="flex items-center gap-4">
              <button className="p-2 text-slate-400 hover:text-white">
                🔔
              </button>

              {/* User Menu */}
              <div className="relative">
                <button
                  onClick={() => setShowUserMenu(!showUserMenu)}
                  className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center text-sm font-medium hover:bg-blue-700 transition-colors"
                >
                  {user?.name?.charAt(0).toUpperCase() || 'U'}
                </button>

                {showUserMenu && (
                  <>
                    <div
                      className="fixed inset-0 z-10"
                      onClick={() => setShowUserMenu(false)}
                    />
                    <div className="absolute right-0 mt-2 w-48 rounded-md shadow-lg bg-slate-800 border border-slate-700 z-20">
                      <div className="py-1">
                        <div className="px-4 py-2 text-sm text-slate-400 border-b border-slate-700">
                          <div className="font-medium text-white">{user?.name}</div>
                          <div className="text-xs">{user?.email}</div>
                        </div>
                        <Link
                          href="/profile"
                          className="block px-4 py-2 text-sm text-slate-300 hover:bg-slate-700"
                          onClick={() => setShowUserMenu(false)}
                        >
                          Profile
                        </Link>
                        <Link
                          href="/profile/settings"
                          className="block px-4 py-2 text-sm text-slate-300 hover:bg-slate-700"
                          onClick={() => setShowUserMenu(false)}
                        >
                          Settings
                        </Link>
                        <button
                          onClick={handleLogout}
                          className="block w-full text-left px-4 py-2 text-sm text-red-400 hover:bg-slate-700"
                        >
                          Sign out
                        </button>
                      </div>
                    </div>
                  </>
                )}
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Mobile Navigation */}
      <nav className="fixed bottom-0 left-0 right-0 z-50 border-t border-slate-800 bg-slate-900 md:hidden">
        <div className="flex justify-around py-2">
          {navItems.slice(0, 4).map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex flex-col items-center gap-1 p-2",
                pathname.startsWith(item.href)
                  ? "text-blue-400"
                  : "text-slate-400"
              )}
            >
              <span className="text-xl">{item.icon}</span>
              <span className="text-xs">{item.label}</span>
            </Link>
          ))}
        </div>
      </nav>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-6 pb-24 md:pb-6">
        {children}
      </main>
    </div>
  );
}
