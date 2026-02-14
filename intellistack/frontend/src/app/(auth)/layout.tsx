import { ReactNode } from 'react';

export default function AuthLayout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen bg-background paper-texture">
      <div className="relative z-10">
        {children}
      </div>
    </div>
  );
}
