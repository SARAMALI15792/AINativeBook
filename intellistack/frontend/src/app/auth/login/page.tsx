'use client';

import { useEffect } from 'react';

const docusaurusUrl = (process.env.NEXT_PUBLIC_DOCUSAURUS_URL || 'http://localhost:3005/AINativeBook').replace(/\/$/, '');

export default function LoginPage() {
  useEffect(() => {
    window.location.replace(`${docusaurusUrl}/auth/login`);
  }, []);

  return null;
}
