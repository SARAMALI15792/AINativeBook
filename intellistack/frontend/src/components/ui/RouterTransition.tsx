'use client';

import { usePathname } from 'next/navigation';
import { useEffect, useRef, useState } from 'react';

export function RouterTransition() {
  const pathname = usePathname();
  const [progress, setProgress] = useState(0);
  const [visible, setVisible] = useState(false);
  const timersRef = useRef<ReturnType<typeof setTimeout>[]>([]);
  const prevPath = useRef(pathname);

  useEffect(() => {
    if (pathname === prevPath.current) return;
    prevPath.current = pathname;

    // Clear any previous timers
    timersRef.current.forEach(clearTimeout);
    timersRef.current = [];

    setVisible(true);
    setProgress(10);

    const t1 = setTimeout(() => setProgress(40), 100);
    const t2 = setTimeout(() => setProgress(72), 350);
    const t3 = setTimeout(() => setProgress(90), 600);
    const t4 = setTimeout(() => {
      setProgress(100);
      const t5 = setTimeout(() => {
        setVisible(false);
        setProgress(0);
      }, 300);
      timersRef.current.push(t5);
    }, 900);

    timersRef.current = [t1, t2, t3, t4];

    return () => {
      timersRef.current.forEach(clearTimeout);
    };
  }, [pathname]);

  if (!visible && progress === 0) return null;

  return (
    <div
      aria-hidden="true"
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        height: '3px',
        width: `${progress}%`,
        background: 'linear-gradient(90deg, #4f46e5 0%, #6366f1 50%, #a78bfa 100%)',
        transition: progress === 0 ? 'none' : 'width 0.35s cubic-bezier(0.4,0,0.2,1), opacity 0.3s ease',
        opacity: visible ? 1 : 0,
        zIndex: 9999,
        pointerEvents: 'none',
      }}
    />
  );
}
