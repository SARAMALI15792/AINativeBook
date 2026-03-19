'use client';

import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react';

interface AnnouncementContextValue {
  announce: (message: string, priority?: 'polite' | 'assertive') => void;
}

const AnnouncementContext = createContext<AnnouncementContextValue | undefined>(undefined);

export function useAnnouncement() {
  const context = useContext(AnnouncementContext);
  if (!context) {
    throw new Error('useAnnouncement must be used within AnnouncementProvider');
  }
  return context;
}

interface AnnouncementProviderProps {
  children: ReactNode;
}

export function AnnouncementProvider({ children }: AnnouncementProviderProps) {
  const [politeMessage, setPoliteMessage] = useState('');
  const [assertiveMessage, setAssertiveMessage] = useState('');

  const announce = useCallback((message: string, priority: 'polite' | 'assertive' = 'polite') => {
    if (priority === 'assertive') {
      setAssertiveMessage(message);
      // Clear after announcement
      setTimeout(() => setAssertiveMessage(''), 100);
    } else {
      setPoliteMessage(message);
      // Clear after announcement
      setTimeout(() => setPoliteMessage(''), 100);
    }
  }, []);

  return (
    <AnnouncementContext.Provider value={{ announce }}>
      {children}

      {/* Screen reader live regions */}
      <div
        role="status"
        aria-live="polite"
        aria-atomic="true"
        className="sr-only"
      >
        {politeMessage}
      </div>

      <div
        role="alert"
        aria-live="assertive"
        aria-atomic="true"
        className="sr-only"
      >
        {assertiveMessage}
      </div>
    </AnnouncementContext.Provider>
  );
}

/**
 * Hook to announce form errors to screen readers
 */
export function useFormErrorAnnouncement() {
  const { announce } = useAnnouncement();

  const announceError = useCallback((fieldName: string, errorMessage: string) => {
    announce(`Error in ${fieldName}: ${errorMessage}`, 'assertive');
  }, [announce]);

  const announceErrors = useCallback((errors: Record<string, string>) => {
    const errorCount = Object.keys(errors).length;
    if (errorCount === 0) return;

    const message = errorCount === 1
      ? `1 error found: ${Object.values(errors)[0]}`
      : `${errorCount} errors found. Please review the form.`;

    announce(message, 'assertive');
  }, [announce]);

  return { announceError, announceErrors };
}

/**
 * Hook to announce loading states to screen readers
 */
export function useLoadingAnnouncement() {
  const { announce } = useAnnouncement();

  const announceLoading = useCallback((message: string = 'Loading') => {
    announce(`${message}...`, 'polite');
  }, [announce]);

  const announceLoaded = useCallback((message: string = 'Content loaded') => {
    announce(message, 'polite');
  }, [announce]);

  const announceError = useCallback((message: string = 'An error occurred') => {
    announce(message, 'assertive');
  }, [announce]);

  return { announceLoading, announceLoaded, announceError };
}

/**
 * Hook to announce navigation changes to screen readers
 */
export function useNavigationAnnouncement() {
  const { announce } = useAnnouncement();

  const announceNavigation = useCallback((pageName: string) => {
    announce(`Navigated to ${pageName}`, 'polite');
  }, [announce]);

  const announceStepChange = useCallback((currentStep: number, totalSteps: number, stepName: string) => {
    announce(`Step ${currentStep} of ${totalSteps}: ${stepName}`, 'polite');
  }, [announce]);

  return { announceNavigation, announceStepChange };
}
