'use client';

import React, { Suspense, lazy } from 'react';
import { Robot2D } from './Robot2D';

const Robot3D = lazy(() =>
  import('./Robot3D').then((mod) => ({ default: mod.Robot3D }))
);

interface RobotDisplayProps {
  className?: string;
  autoRotate?: boolean;
  enableZoom?: boolean;
  force2D?: boolean;
}

export function RobotDisplay({
  className = '',
  autoRotate = true,
  enableZoom = false,
  force2D = false,
}: RobotDisplayProps) {
  const [use3D, setUse3D] = React.useState(false);

  React.useEffect(() => {
    // Check if device supports WebGL and is not mobile
    const checkCapabilities = () => {
      if (force2D) {
        setUse3D(false);
        return;
      }

      const isMobile = window.innerWidth < 768 ||
                       /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);

      if (isMobile) {
        setUse3D(false);
        return;
      }

      // Check WebGL support
      const canvas = document.createElement('canvas');
      const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');

      if (gl && gl instanceof WebGLRenderingContext) {
        setUse3D(true);
      } else {
        setUse3D(false);
      }
    };

    checkCapabilities();
  }, [force2D]);

  if (!use3D) {
    return <Robot2D className={className} animate={true} />;
  }

  return (
    <Suspense fallback={<Robot2D className={className} animate={true} />}>
      <Robot3D
        className={className}
        autoRotate={autoRotate}
        enableZoom={enableZoom}
      />
    </Suspense>
  );
}
