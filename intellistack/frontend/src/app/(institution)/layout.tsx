/**
 * Institution Admin Layout
 *
 * Layout for institution administrators with navigation
 * to cohorts, branding, and analytics.
 */

import { ReactNode } from 'react';
import Link from 'next/link';
import { BarChart3, Building2, Palette, Users } from 'lucide-react';

interface InstitutionLayoutProps {
  children: ReactNode;
}

export default function InstitutionLayout({ children }: InstitutionLayoutProps) {
  const navItems = [
    { href: '/cohorts', label: 'Cohorts', icon: Users },
    { href: '/analytics', label: 'Analytics', icon: BarChart3 },
    { href: '/branding', label: 'Branding', icon: Palette },
  ];

  return (
    <div className="flex min-h-screen bg-gray-50">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-gray-200">
        <div className="p-6">
          <div className="flex items-center gap-2 mb-8">
            <Building2 className="h-6 w-6 text-primary" />
            <h2 className="text-lg font-semibold">Institution Admin</h2>
          </div>

          <nav className="space-y-2">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className="flex items-center gap-3 px-4 py-3 rounded-lg text-gray-700 hover:bg-gray-100 hover:text-primary transition-colors"
              >
                <item.icon className="h-5 w-5" />
                <span className="font-medium">{item.label}</span>
              </Link>
            ))}
          </nav>
        </div>
      </aside>

      {/* Main content */}
      <main className="flex-1 overflow-auto">
        <div className="max-w-7xl mx-auto p-8">
          {children}
        </div>
      </main>
    </div>
  );
}
