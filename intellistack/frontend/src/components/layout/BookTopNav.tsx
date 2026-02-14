'use client';

import Link from 'next/link';
import { useAuth } from '@/hooks/useAuth';
import { Bell, ChevronDown, Menu, Settings, User, LogOut } from 'lucide-react';
import { useState } from 'react';

interface BookTopNavProps {
  onSidebarToggle: () => void;
  sidebarOpen: boolean;
}

export function BookTopNav({ onSidebarToggle, sidebarOpen }: BookTopNavProps) {
  const { user, logout } = useAuth();
  const [showUserMenu, setShowUserMenu] = useState(false);

  const handleLogout = async () => {
    setShowUserMenu(false);
    await logout();
  };

  return (
    <header className="sticky top-0 z-50 bg-card/95 backdrop-blur-sm border-b-2 border-secondary shadow-md">
      <div className="px-4">
        <div className="flex h-16 items-center justify-between">
          {/* Left: Hamburger + Logo */}
          <div className="flex items-center gap-3">
            <button
              onClick={onSidebarToggle}
              className="p-2 rounded-lg hover:bg-muted transition-colors text-muted-foreground"
              aria-label="Toggle sidebar"
            >
              <Menu className="w-5 h-5" />
            </button>

            <Link href="/" className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-primary to-primary-400 flex items-center justify-center shadow-md border border-primary-600">
                <span className="text-white text-lg font-bold">IS</span>
              </div>
              <div className="hidden sm:block">
                <h1 className="text-xl font-bold text-foreground font-serif m-0">
                  IntelliStack
                </h1>
                <p className="text-xs text-secondary -mt-0.5 font-medium m-0">
                  Physical AI & Humanoid Robotics
                </p>
              </div>
            </Link>
          </div>

          {/* Right: Notifications + User */}
          <div className="flex items-center gap-3">
            <button className="p-2 rounded-lg hover:bg-muted transition-colors text-muted-foreground relative">
              <Bell className="w-5 h-5" />
              <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-destructive rounded-full" />
            </button>

            <div className="relative">
              <button
                onClick={() => setShowUserMenu(!showUserMenu)}
                className="flex items-center gap-2 px-3 py-1.5 rounded-lg hover:bg-muted transition-colors"
              >
                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-primary to-primary-400 flex items-center justify-center text-sm font-bold text-white border-2 border-card shadow-sm">
                  {user?.name?.charAt(0).toUpperCase() || 'U'}
                </div>
                <span className="hidden sm:block text-sm font-medium text-foreground">
                  {user?.name?.split(' ')[0] || 'User'}
                </span>
                <ChevronDown className="w-4 h-4 text-secondary" />
              </button>

              {showUserMenu && (
                <>
                  <div
                    className="fixed inset-0 z-10"
                    onClick={() => setShowUserMenu(false)}
                  />
                  <div className="absolute right-0 mt-2 w-56 rounded-lg shadow-xl bg-card border border-border z-20 overflow-hidden">
                    <div className="p-4 border-b border-muted bg-gradient-to-r from-card to-background">
                      <p className="font-semibold text-foreground text-sm">
                        {user?.name || 'User'}
                      </p>
                      <p className="text-xs text-muted-foreground">
                        {user?.email || ''}
                      </p>
                    </div>
                    <div className="p-2">
                      <Link
                        href="/profile"
                        className="flex items-center gap-2 px-3 py-2 rounded-md text-sm text-foreground hover:bg-muted transition-colors"
                        onClick={() => setShowUserMenu(false)}
                      >
                        <User className="w-4 h-4" /> Profile
                      </Link>
                      <Link
                        href="/profile/settings"
                        className="flex items-center gap-2 px-3 py-2 rounded-md text-sm text-foreground hover:bg-muted transition-colors"
                        onClick={() => setShowUserMenu(false)}
                      >
                        <Settings className="w-4 h-4" /> Settings
                      </Link>
                      <hr className="my-2 border-muted" />
                      <button
                        onClick={handleLogout}
                        className="w-full flex items-center gap-2 px-3 py-2 rounded-md text-sm text-destructive hover:bg-destructive/10 transition-colors"
                      >
                        <LogOut className="w-4 h-4" /> Sign out
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
  );
}
