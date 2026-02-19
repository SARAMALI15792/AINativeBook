'use client';

import React, { Suspense, useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, useGLTF } from '@react-three/drei';
import * as THREE from 'three';

interface Robot3DProps {
  className?: string;
  autoRotate?: boolean;
  enableZoom?: boolean;
}

function RobotModel() {
  const meshRef = useRef<THREE.Group>(null);

  // Auto-rotation animation
  useFrame((state, delta) => {
    if (meshRef.current) {
      meshRef.current.rotation.y += delta * 0.3;
    }
  });

  return (
    <group ref={meshRef}>
      {/* Placeholder robot geometry - Using basic materials for true colors */}
      {/* Head - Bright Cyan */}
      <mesh position={[0, 1.5, 0]}>
        <boxGeometry args={[0.6, 0.6, 0.6]} />
        <meshBasicMaterial color="#00efff" />
      </mesh>

      {/* Eyes - Bright Violet */}
      <mesh position={[-0.15, 1.6, 0.3]}>
        <sphereGeometry args={[0.08, 16, 16]} />
        <meshBasicMaterial color="#a855f7" />
      </mesh>
      <mesh position={[0.15, 1.6, 0.3]}>
        <sphereGeometry args={[0.08, 16, 16]} />
        <meshBasicMaterial color="#a855f7" />
      </mesh>

      {/* Body - Bright Teal */}
      <mesh position={[0, 0.6, 0]}>
        <boxGeometry args={[0.8, 1.2, 0.5]} />
        <meshBasicMaterial color="#14b8a6" />
      </mesh>

      {/* Left Arm - Bright Cyan */}
      <group position={[-0.5, 0.8, 0]}>
        <mesh position={[0, -0.3, 0]}>
          <cylinderGeometry args={[0.1, 0.1, 0.6, 16]} />
          <meshBasicMaterial color="#00efff" />
        </mesh>
        <mesh position={[0, -0.7, 0]}>
          <sphereGeometry args={[0.12, 16, 16]} />
          <meshBasicMaterial color="#a855f7" />
        </mesh>
      </group>

      {/* Right Arm - Bright Cyan */}
      <group position={[0.5, 0.8, 0]}>
        <mesh position={[0, -0.3, 0]}>
          <cylinderGeometry args={[0.1, 0.1, 0.6, 16]} />
          <meshBasicMaterial color="#00efff" />
        </mesh>
        <mesh position={[0, -0.7, 0]}>
          <sphereGeometry args={[0.12, 16, 16]} />
          <meshBasicMaterial color="#a855f7" />
        </mesh>
      </group>

      {/* Left Leg - Bright Teal */}
      <group position={[-0.25, -0.2, 0]}>
        <mesh position={[0, -0.4, 0]}>
          <cylinderGeometry args={[0.12, 0.12, 0.8, 16]} />
          <meshBasicMaterial color="#14b8a6" />
        </mesh>
        <mesh position={[0, -0.9, 0.1]}>
          <boxGeometry args={[0.15, 0.1, 0.25]} />
          <meshBasicMaterial color="#00efff" />
        </mesh>
      </group>

      {/* Right Leg - Bright Teal */}
      <group position={[0.25, -0.2, 0]}>
        <mesh position={[0, -0.4, 0]}>
          <cylinderGeometry args={[0.12, 0.12, 0.8, 16]} />
          <meshBasicMaterial color="#14b8a6" />
        </mesh>
        <mesh position={[0, -0.9, 0.1]}>
          <boxGeometry args={[0.15, 0.1, 0.25]} />
          <meshBasicMaterial color="#00efff" />
        </mesh>
      </group>
    </group>
  );
}

function Scene({ autoRotate, enableZoom }: { autoRotate: boolean; enableZoom: boolean }) {
  return (
    <>
      {/* Lighting - Enhanced for better color visibility */}
      <ambientLight intensity={0.8} />
      <directionalLight position={[10, 10, 5]} intensity={1.5} color="#ffffff" />
      <pointLight position={[-10, 0, -5]} intensity={1} color="#a855f7" />
      <pointLight position={[10, 0, -5]} intensity={1} color="#00efff" />
      <spotLight position={[0, 10, 0]} intensity={0.5} angle={0.6} penumbra={1} color="#ffffff" />

      {/* Robot Model */}
      <Suspense fallback={null}>
        <RobotModel />
      </Suspense>

      {/* Camera Controls */}
      <OrbitControls
        enableZoom={enableZoom}
        enablePan={false}
        autoRotate={autoRotate}
        autoRotateSpeed={2}
        minDistance={3}
        maxDistance={8}
        minPolarAngle={Math.PI / 4}
        maxPolarAngle={Math.PI / 1.5}
      />
    </>
  );
}

export function Robot3D({ className = '', autoRotate = true, enableZoom = false }: Robot3DProps) {
  return (
    <div
      className={`w-full h-full ${className}`}
      role="img"
      aria-label="3D animated humanoid robot model rotating in space"
    >
      <Canvas
        camera={{ position: [0, 1, 5], fov: 50 }}
        gl={{ antialias: true, alpha: true }}
        dpr={[1, 2]}
      >
        <Scene autoRotate={autoRotate} enableZoom={enableZoom} />
      </Canvas>
    </div>
  );
}
