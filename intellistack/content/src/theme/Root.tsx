/**
 * Global Root Component
 * Wraps the entire application to inject ChatKit widget on all pages
 */
import React, { useEffect } from 'react';
import { ChatKitErrorBoundary } from '../components/ai/ChatKitErrorBoundary';
import ChatKitWidget from '../components/ai/ChatKitWidget';

interface Props {
  children: React.ReactNode;
}

export default function Root({ children }: Props): JSX.Element {
  // Add body class for proper positioning when widget is present
  useEffect(() => {
    document.body.classList.add('has-chatkit-widget');
    return () => {
      document.body.classList.remove('has-chatkit-widget');
    };
  }, []);

  return (
    <>
      {children}
      <ChatKitErrorBoundary>
        <ChatKitWidget />
      </ChatKitErrorBoundary>
    </>
  );
}