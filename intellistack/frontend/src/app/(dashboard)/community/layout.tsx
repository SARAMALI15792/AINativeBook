'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { MessageSquare, Users, Heart } from 'lucide-react';

const communityLinks = [
  {
    href: '/community/forums',
    label: 'Forums',
    icon: MessageSquare,
    description: 'Q&A and discussions',
  },
  {
    href: '/community/groups',
    label: 'Study Groups',
    icon: Users,
    description: 'Collaborate with peers',
  },
  {
    href: '/community/mentorship',
    label: 'Mentorship',
    icon: Heart,
    description: 'Get guided by experts',
  },
];

export default function CommunityLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-lg p-8">
        <h1 className="text-3xl font-bold mb-2">Community</h1>
        <p className="text-purple-100">
          Connect with peers, get mentored, and grow together
        </p>
      </div>

      {/* Navigation Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {communityLinks.map(({ href, label, icon: Icon, description }) => (
          <Link key={href} href={href}>
            <div
              className={`p-4 rounded-lg border-2 transition-all cursor-pointer ${
                pathname.startsWith(href)
                  ? 'border-purple-500 bg-purple-50'
                  : 'border-gray-200 hover:border-purple-300'
              }`}
            >
              <Icon className="w-6 h-6 mb-2 text-purple-600" />
              <h3 className="font-semibold text-gray-900">{label}</h3>
              <p className="text-sm text-gray-600">{description}</p>
            </div>
          </Link>
        ))}
      </div>

      {/* Content */}
      <div>{children}</div>
    </div>
  );
}
