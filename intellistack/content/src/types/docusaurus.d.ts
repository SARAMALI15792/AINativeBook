declare global {
  interface Window {
    docusaurus?: {
      siteConfig: {
        customFields?: {
          betterAuthUrl?: string;
          backendUrl?: string;
          frontendUrl?: string;
        };
      };
    };
  }
}

export {};
