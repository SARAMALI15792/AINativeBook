/**
 * Swizzled DocPage Layout
 * Wraps the default DocPage layout to inject ChatKit widget and protect routes
 */

import React from 'react';
import Layout from '@theme-original/DocPage/Layout';
import type LayoutType from '@theme/DocPage/Layout';
import type { WrapperProps } from '@docusaurus/types';
import ChatKitWidget from '@site/src/components/ai/ChatKitWidget';
import ProtectedRoute from '@site/src/components/ProtectedRoute';

type Props = WrapperProps<typeof LayoutType>;

export default function LayoutWrapper(props: Props): JSX.Element {
  return (
    <ProtectedRoute>
      <Layout {...props} />
      <ChatKitWidget />
    </ProtectedRoute>
  );
}
