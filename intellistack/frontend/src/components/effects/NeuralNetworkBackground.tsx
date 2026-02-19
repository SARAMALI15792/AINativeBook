'use client';

import React, { useEffect, useRef, useState } from 'react';

interface Node {
  x: number;
  y: number;
  vx: number;
  vy: number;
}

interface Connection {
  from: number;
  to: number;
  opacity: number;
}

interface NeuralNetworkBackgroundProps {
  className?: string;
}

export function NeuralNetworkBackground({ className = '' }: NeuralNetworkBackgroundProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const svgRef = useRef<SVGSVGElement>(null);
  const [isMobile, setIsMobile] = useState(false);
  const [isVisible, setIsVisible] = useState(true);
  const nodesRef = useRef<Node[]>([]);
  const connectionsRef = useRef<Connection[]>([]);
  const animationFrameRef = useRef<number>();

  // Page Visibility API - pause animations when tab is inactive
  useEffect(() => {
    const handleVisibilityChange = () => {
      setIsVisible(!document.hidden);
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);
    return () => document.removeEventListener('visibilitychange', handleVisibilityChange);
  }, []);

  // Device detection
  useEffect(() => {
    const checkDevice = () => {
      const mobile = window.innerWidth < 768 ||
                     /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
      setIsMobile(mobile);
    };

    checkDevice();
    window.addEventListener('resize', checkDevice);
    return () => window.removeEventListener('resize', checkDevice);
  }, []);

  // Canvas implementation for desktop
  useEffect(() => {
    if (isMobile || !canvasRef.current) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Set canvas size
    const updateSize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    updateSize();
    window.addEventListener('resize', updateSize);

    // Initialize nodes (50 for desktop)
    const nodeCount = 50;
    const nodes: Node[] = [];
    for (let i = 0; i < nodeCount; i++) {
      nodes.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        vx: (Math.random() - 0.5) * 0.5,
        vy: (Math.random() - 0.5) * 0.5,
      });
    }
    nodesRef.current = nodes;

    // Initialize connections (100 for desktop)
    const connections: Connection[] = [];
    for (let i = 0; i < 100; i++) {
      connections.push({
        from: Math.floor(Math.random() * nodeCount),
        to: Math.floor(Math.random() * nodeCount),
        opacity: Math.random() * 0.3 + 0.1,
      });
    }
    connectionsRef.current = connections;

    // Animation loop (60fps)
    let lastTime = performance.now();
    const animate = (currentTime: number) => {
      // Pause animation if tab is not visible
      if (!isVisible) {
        animationFrameRef.current = requestAnimationFrame(animate);
        return;
      }

      const deltaTime = currentTime - lastTime;

      // Target 60fps (16.67ms per frame)
      if (deltaTime < 16.67) {
        animationFrameRef.current = requestAnimationFrame(animate);
        return;
      }

      lastTime = currentTime;

      // Clear canvas
      ctx.fillStyle = 'rgba(26, 26, 46, 0.1)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Update and draw nodes
      nodes.forEach((node) => {
        // Update position
        node.x += node.vx;
        node.y += node.vy;

        // Bounce off edges
        if (node.x < 0 || node.x > canvas.width) node.vx *= -1;
        if (node.y < 0 || node.y > canvas.height) node.vy *= -1;

        // Draw node
        ctx.beginPath();
        ctx.arc(node.x, node.y, 2, 0, Math.PI * 2);
        ctx.fillStyle = '#00efff';
        ctx.fill();
      });

      // Draw connections
      connections.forEach((conn) => {
        const from = nodes[conn.from];
        const to = nodes[conn.to];

        ctx.beginPath();
        ctx.moveTo(from.x, from.y);
        ctx.lineTo(to.x, to.y);
        ctx.strokeStyle = `rgba(0, 239, 255, ${conn.opacity})`;
        ctx.lineWidth = 1;
        ctx.stroke();
      });

      animationFrameRef.current = requestAnimationFrame(animate);
    };

    animationFrameRef.current = requestAnimationFrame(animate);

    return () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
      window.removeEventListener('resize', updateSize);
    };
  }, [isMobile, isVisible]);

  // SVG implementation for mobile
  useEffect(() => {
    if (!isMobile || !svgRef.current) return;

    const svg = svgRef.current;
    const width = window.innerWidth;
    const height = window.innerHeight;

    // Initialize nodes (20 for mobile)
    const nodeCount = 20;
    const nodes: Node[] = [];
    for (let i = 0; i < nodeCount; i++) {
      nodes.push({
        x: Math.random() * width,
        y: Math.random() * height,
        vx: (Math.random() - 0.5) * 0.3,
        vy: (Math.random() - 0.5) * 0.3,
      });
    }
    nodesRef.current = nodes;

    // Initialize connections (40 for mobile)
    const connections: Connection[] = [];
    for (let i = 0; i < 40; i++) {
      connections.push({
        from: Math.floor(Math.random() * nodeCount),
        to: Math.floor(Math.random() * nodeCount),
        opacity: Math.random() * 0.3 + 0.1,
      });
    }
    connectionsRef.current = connections;

    // Animation loop (30fps for mobile)
    let lastTime = performance.now();
    const animate = (currentTime: number) => {
      // Pause animation if tab is not visible
      if (!isVisible) {
        animationFrameRef.current = requestAnimationFrame(animate);
        return;
      }

      const deltaTime = currentTime - lastTime;

      // Target 30fps (33.33ms per frame)
      if (deltaTime < 33.33) {
        animationFrameRef.current = requestAnimationFrame(animate);
        return;
      }

      lastTime = currentTime;

      // Update nodes
      nodes.forEach((node) => {
        node.x += node.vx;
        node.y += node.vy;

        if (node.x < 0 || node.x > width) node.vx *= -1;
        if (node.y < 0 || node.y > height) node.vy *= -1;
      });

      // Update SVG elements
      const circles = svg.querySelectorAll('circle');
      circles.forEach((circle, i) => {
        if (nodes[i]) {
          circle.setAttribute('cx', nodes[i].x.toString());
          circle.setAttribute('cy', nodes[i].y.toString());
        }
      });

      const lines = svg.querySelectorAll('line');
      lines.forEach((line, i) => {
        if (connections[i]) {
          const from = nodes[connections[i].from];
          const to = nodes[connections[i].to];
          if (from && to) {
            line.setAttribute('x1', from.x.toString());
            line.setAttribute('y1', from.y.toString());
            line.setAttribute('x2', to.x.toString());
            line.setAttribute('y2', to.y.toString());
          }
        }
      });

      animationFrameRef.current = requestAnimationFrame(animate);
    };

    animationFrameRef.current = requestAnimationFrame(animate);

    return () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
    };
  }, [isMobile, isVisible]);

  return (
    <div className={`fixed inset-0 -z-10 overflow-hidden ${className}`}>
      {!isMobile ? (
        <canvas
          ref={canvasRef}
          className="w-full h-full"
          aria-hidden="true"
        />
      ) : (
        <svg
          ref={svgRef}
          className="w-full h-full"
          aria-hidden="true"
        >
          {/* Connections */}
          {connectionsRef.current.map((conn, i) => (
            <line
              key={`line-${i}`}
              stroke="#00efff"
              strokeWidth="1"
              opacity={conn.opacity}
            />
          ))}
          {/* Nodes */}
          {nodesRef.current.map((_, i) => (
            <circle
              key={`node-${i}`}
              r="2"
              fill="#00efff"
            />
          ))}
        </svg>
      )}
    </div>
  );
}
