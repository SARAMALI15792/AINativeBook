"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { cn } from "@/lib/utils";
import { useAuth } from "@/hooks/useAuth";

interface Chapter {
  id: string;
  title: string;
  slug: string;
  order: number;
  status: "locked" | "available" | "in_progress" | "completed";
  percentage: number;
  subsections?: { id: string; title: string; slug: string }[];
}

interface BookLayoutProps {
  children: React.ReactNode;
  title?: string;
  subtitle?: string;
  chapters?: Chapter[];
  currentChapterId?: string;
  showProgress?: boolean;
  overallProgress?: number;
}

export default function BookLayout({
  children,
  title = "IntelliStack",
  subtitle = "Physical AI & Humanoid Robotics",
  chapters = [],
  currentChapterId,
  showProgress = true,
  overallProgress = 0,
}: BookLayoutProps) {
  const pathname = usePathname();
  const router = useRouter();
  const { user, isAuthenticated, isLoading, logout } = useAuth();
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const handleLogout = async () => {
    await logout();
  };

  // Mobile: close sidebar by default
  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth < 1024) {
        setSidebarOpen(false);
      } else {
        setSidebarOpen(true);
      }
    };
    handleResize();
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return (
    <div className="min-h-screen bg-[#f5f0e8] text-slate-800 font-serif">
      {/* Book Background Texture */}
      <div className="fixed inset-0 pointer-events-none opacity-30"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM12 60c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z' fill='%23d4c5b5' fill-opacity='0.15' fill-rule='evenodd'/%3E%3C/svg%3E")`,
        }}
      />

      {/* Top Header */}
      <header className="sticky top-0 z-50 bg-[#f5f0e8]/95 backdrop-blur-sm border-b-2 border-[#8b7355] shadow-sm">
        <div className="flex items-center justify-between px-4 lg:px-6 h-16">
          {/* Left: Menu Toggle & Logo */}
          <div className="flex items-center gap-4">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="p-2 rounded-lg hover:bg-[#e8e0d5] transition-colors lg:hidden"
              aria-label="Toggle menu"
            >
              <svg className="w-6 h-6 text-[#5c4a3d]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
            <Link href="/" className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-[#8b6914] to-[#a67c52] flex items-center justify-center shadow-md">
                <span className="text-white text-lg font-bold">IS</span>
              </div>
              <div className="hidden sm:block">
                <h1 className="text-xl font-bold text-[#3d3229] font-serif">{title}</h1>
                <p className="text-xs text-[#8b7355] -mt-0.5">{subtitle}</p>
              </div>
            </Link>
          </div>

          {/* Center: Navigation */}
          <nav className="hidden lg:flex items-center gap-1">
            {[
              { href: "/dashboard", label: "Dashboard", icon: "📖" },
              { href: "/learn", label: "Learn", icon: "📚" },
              { href: "/assessments", label: "Practice", icon: "✏️" },
              { href: "/ai/chatbot", label: "AI Tutor", icon: "🎓" },
            ].map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all",
                  pathname === item.href || pathname.startsWith(item.href + "/")
                    ? "bg-[#e8e0d5] text-[#5c4a3d] shadow-inner"
                    : "text-[#6b5a4a] hover:bg-[#ebe4da] hover:text-[#3d3229]"
                )}
              >
                <span>{item.icon}</span>
                <span>{item.label}</span>
              </Link>
            ))}
          </nav>

          {/* Right: User Menu */}
          <div className="flex items-center gap-3">
            <Link
              href="/community"
              className="hidden sm:flex p-2 rounded-lg hover:bg-[#e8e0d5] transition-colors text-[#6b5a4a]"
              title="Community"
            >
              👥
            </Link>
            <div className="relative">
              <button
                onClick={() => setShowUserMenu(!showUserMenu)}
                className="flex items-center gap-2 px-3 py-1.5 rounded-lg hover:bg-[#e8e0d5] transition-colors"
              >
                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-[#8b6914] to-[#a67c52] flex items-center justify-center text-sm font-bold text-white">
                  {user?.name?.charAt(0).toUpperCase() || "U"}
                </div>
                <span className="hidden md:block text-sm font-medium text-[#5c4a3d]">
                  {user?.name?.split(" ")[0] || "User"}
                </span>
                <svg className="w-4 h-4 text-[#8b7355]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>

              {showUserMenu && (
                <>
                  <div className="fixed inset-0 z-10" onClick={() => setShowUserMenu(false)} />
                  <div className="absolute right-0 mt-2 w-56 rounded-lg shadow-xl bg-white border border-[#d4c5b5] z-20 overflow-hidden">
                    <div className="p-4 border-b border-[#e8e0d5] bg-gradient-to-r from-[#faf8f5] to-[#f5f0e8]">
                      <p className="font-semibold text-[#3d3229]">{user?.name}</p>
                      <p className="text-xs text-[#8b7355]">{user?.email}</p>
                    </div>
                    <div className="p-2">
                      <Link
                        href="/profile"
                        className="flex items-center gap-2 px-3 py-2 rounded-md text-sm text-[#5c4a3d] hover:bg-[#f5f0e8] transition-colors"
                        onClick={() => setShowUserMenu(false)}
                      >
                        <span>👤</span> Profile
                      </Link>
                      <Link
                        href="/profile/settings"
                        className="flex items-center gap-2 px-3 py-2 rounded-md text-sm text-[#5c4a3d] hover:bg-[#f5f0e8] transition-colors"
                        onClick={() => setShowUserMenu(false)}
                      >
                        <span>⚙️</span> Settings
                      </Link>
                      <hr className="my-2 border-[#e8e0d5]" />
                      <button
                        onClick={handleLogout}
                        className="w-full flex items-center gap-2 px-3 py-2 rounded-md text-sm text-red-600 hover:bg-red-50 transition-colors"
                      >
                        <span>🚪</span> Sign out
                      </button>
                    </div>
                  </div>
                </>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Main Book Layout */}
      <div className="flex min-h-[calc(100vh-64px)]">
        {/* Left Sidebar - Table of Contents (Book Style) */}
        <aside
          className={cn(
            "fixed lg:sticky top-16 left-0 z-40 h-[calc(100vh-64px)] bg-[#faf8f5] border-r-2 border-[#d4c5b5] transition-all duration-300 ease-in-out overflow-hidden",
            sidebarOpen ? "w-80 translate-x-0" : "w-0 -translate-x-full lg:w-0 lg:translate-x-0"
          )}
        >
          <div className="w-80 h-full flex flex-col">
            {/* Sidebar Header */}
            <div className="p-4 border-b border-[#e8e0d5] bg-gradient-to-r from-[#f5f0e8] to-[#faf8f5]">
              <h2 className="text-sm font-bold text-[#8b7355] uppercase tracking-wider">
                Table of Contents
              </h2>
              {showProgress && (
                <div className="mt-3">
                  <div className="flex justify-between text-xs mb-1">
                    <span className="text-[#6b5a4a]">Overall Progress</span>
                    <span className="font-semibold text-[#8b6914]">{Math.round(overallProgress)}%</span>
                  </div>
                  <div className="h-2 bg-[#e8e0d5] rounded-full overflow-hidden border border-[#d4c5b5]">
                    <div
                      className="h-full bg-gradient-to-r from-[#8b6914] to-[#a67c52] transition-all duration-500"
                      style={{ width: `${overallProgress}%` }}
                    />
                  </div>
                </div>
              )}
            </div>

            {/* Chapters List */}
            <div className="flex-1 overflow-y-auto py-4 px-3 space-y-1">
              {chapters.length === 0 ? (
                <div className="text-center py-8 text-[#8b7355] text-sm">
                  <p>No chapters available</p>
                  <p className="mt-1 text-xs">Start your learning journey!</p>
                </div>
              ) : (
                chapters.map((chapter, index) => {
                  const isActive = chapter.id === currentChapterId;
                  const isLocked = chapter.status === "locked";
                  const isCompleted = chapter.status === "completed";

                  return (
                    <div key={chapter.id}>
                      <Link
                        href={isLocked ? "#" : `/learn/${chapter.id}`}
                        className={cn(
                          "flex items-start gap-3 p-3 rounded-lg transition-all group",
                          isActive
                            ? "bg-[#f5f0e8] shadow-inner border border-[#d4c5b5]"
                            : isLocked
                            ? "opacity-50 cursor-not-allowed"
                            : "hover:bg-[#f5f0e8] hover:shadow-sm"
                        )}
                      >
                        {/* Chapter Number Badge */}
                        <div
                          className={cn(
                            "flex-shrink-0 w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold border-2",
                            isCompleted
                              ? "bg-emerald-600 border-emerald-600 text-white"
                              : isActive
                              ? "bg-[#8b6914] border-[#8b6914] text-white"
                              : isLocked
                              ? "bg-[#e8e0d5] border-[#d4c5b5] text-[#a09080]"
                              : "bg-white border-[#c4b5a5] text-[#6b5a4a] group-hover:border-[#a67c52]"
                          )}
                        >
                          {isCompleted ? "✓" : index + 1}
                        </div>

                        {/* Chapter Info */}
                        <div className="flex-1 min-w-0">
                          <p
                            className={cn(
                              "text-sm font-medium leading-tight",
                              isActive ? "text-[#3d3229]" : "text-[#5c4a3d]"
                            )}
                          >
                            {chapter.title}
                          </p>
                          {!isLocked && (
                            <div className="mt-1.5 flex items-center gap-2">
                              <div className="flex-1 h-1 bg-[#e8e0d5] rounded-full overflow-hidden">
                                <div
                                  className={cn(
                                    "h-full rounded-full transition-all",
                                    isCompleted ? "bg-emerald-500" : "bg-[#a67c52]"
                                  )}
                                  style={{ width: `${chapter.percentage}%` }}
                                />
                              </div>
                              <span className="text-[10px] text-[#8b7355]">{Math.round(chapter.percentage)}%</span>
                            </div>
                          )}
                          {isLocked && (
                            <span className="text-[10px] text-[#a09080]">🔒 Complete previous to unlock</span>
                          )}
                        </div>
                      </Link>

                      {/* Subsections (if any and if active) */}
                      {chapter.subsections && chapter.subsections.length > 0 && (isActive || chapter.percentage > 0) && (
                        <div className="ml-6 mt-1 space-y-0.5 border-l-2 border-[#e8e0d5] pl-3">
                          {chapter.subsections.map((subsection) => (
                            <Link
                              key={subsection.id}
                              href={`/learn/${chapter.id}/${subsection.slug}`}
                              className="block py-1.5 px-2 text-xs text-[#6b5a4a] hover:text-[#3d3229] hover:bg-[#f5f0e8] rounded transition-colors"
                            >
                              {subsection.title}
                            </Link>
                          ))}
                        </div>
                      )}
                    </div>
                  );
                })
              )}
            </div>

            {/* Sidebar Footer */}
            <div className="p-4 border-t border-[#e8e0d5] bg-gradient-to-r from-[#faf8f5] to-[#f5f0e8]">
              <Link
                href="/dashboard"
                className="flex items-center justify-center gap-2 px-4 py-2 rounded-lg bg-[#e8e0d5] hover:bg-[#ded5c8] text-[#5c4a3d] text-sm font-medium transition-colors"
              >
                <span>←</span> Back to Dashboard
              </Link>
            </div>
          </div>
        </aside>

        {/* Overlay for mobile when sidebar is open */}
        {sidebarOpen && (
          <div
            className="fixed inset-0 bg-black/20 z-30 lg:hidden"
            onClick={() => setSidebarOpen(false)}
          />
        )}

        {/* Right Content Area - The "Page" */}
        <main className="flex-1 min-w-0">
          <div className="max-w-4xl mx-auto p-6 lg:p-10">
            {/* Book Page Effect */}
            <div className="bg-white rounded-lg shadow-lg border border-[#e8e0d5] min-h-[calc(100vh-160px)]">
              {/* Page Header with Decorative Elements */}
              <div className="px-8 pt-8 pb-4 border-b border-[#f0e8dd]">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2 text-[#a67c52]">
                    <span className="text-lg">📖</span>
                    <span className="text-sm font-medium">IntelliStack Learning</span>
                  </div>
                  <div className="text-xs text-[#a09080]">
                    {new Date().toLocaleDateString("en-US", {
                      weekday: "long",
                      year: "numeric",
                      month: "long",
                      day: "numeric",
                    })}
                  </div>
                </div>
              </div>

              {/* Page Content */}
              <div className="px-8 py-8">
                {children}
              </div>

              {/* Page Footer */}
              <div className="px-8 py-4 border-t border-[#f0e8dd] mt-auto">
                <div className="flex items-center justify-between text-xs text-[#a09080]">
                  <span>© 2026 IntelliStack</span>
                  <span>Page generated with 💛 for learning</span>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
