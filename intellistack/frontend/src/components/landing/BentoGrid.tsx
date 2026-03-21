'use client';

import React from 'react';

interface BentoItem {
  icon: React.ReactNode;
  title: string;
  description: string;
}

interface BentoGridProps {
  items: BentoItem[];
}

function BentoCard({ item }: { item: BentoItem }) {
  return (
    <div
      className="group relative rounded-2xl p-7 cursor-default transition-all duration-300"
      style={{
        background: 'rgba(22, 22, 31, 0.85)',
        border: '1px solid rgba(99, 102, 241, 0.14)',
        backdropFilter: 'blur(12px)',
      }}
      onMouseEnter={(e) => {
        const el = e.currentTarget as HTMLElement;
        el.style.boxShadow = '0 0 32px rgba(99,102,241,0.18), 0 4px 24px rgba(0,0,0,0.3)';
        el.style.borderColor = 'rgba(99,102,241,0.4)';
        el.style.transform = 'translateY(-2px)';
      }}
      onMouseLeave={(e) => {
        const el = e.currentTarget as HTMLElement;
        el.style.boxShadow = 'none';
        el.style.borderColor = 'rgba(99, 102, 241, 0.14)';
        el.style.transform = 'translateY(0)';
      }}
    >
      {/* Top gradient accent line on hover */}
      <div
        className="absolute top-0 left-8 right-8 h-px opacity-0 group-hover:opacity-100 transition-opacity duration-300"
        style={{ background: 'linear-gradient(90deg, transparent, #6366f1, transparent)' }}
      />

      <div className="space-y-4">
        {/* Icon container */}
        <div
          className="w-12 h-12 rounded-xl flex items-center justify-center mb-5"
          style={{
            background: 'linear-gradient(135deg, rgba(79,70,229,0.2), rgba(99,102,241,0.1))',
            border: '1px solid rgba(99,102,241,0.2)',
          }}
        >
          {item.icon}
        </div>

        {/* Title */}
        <h3 className="text-lg font-semibold font-heading text-text-primary leading-snug">
          {item.title}
        </h3>

        {/* Description */}
        <p className="text-text-secondary leading-relaxed text-sm">
          {item.description}
        </p>
      </div>
    </div>
  );
}

export function BentoGrid({ items }: BentoGridProps) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
      {items.map((item, index) => (
        <BentoCard key={index} item={item} />
      ))}
    </div>
  );
}
