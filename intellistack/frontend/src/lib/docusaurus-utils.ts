/**
 * Docusaurus URL utility functions
 */

/**
 * Constructs a properly formatted Docusaurus URL
 * @param path Path within Docusaurus (e.g., 'stage-1/intro')
 * @param queryParams Optional query parameters
 * @returns Full Docusaurus URL
 */
export function getDocusaurusUrl(path: string, queryParams?: Record<string, string>): string {
  const baseUrl = process.env.NEXT_PUBLIC_DOCUSAURUS_URL || 'http://localhost:3002';

  // Ensure path starts with /docs/
  const normalizedPath = path.startsWith('/docs/') ? path : `/docs/${path.replace(/^\//, '')}`;

  // Build URL
  let url = `${baseUrl}${normalizedPath}`;

  // Add query params
  if (queryParams) {
    const params = new URLSearchParams(queryParams);
    url += `?${params.toString()}`;
  }

  return url;
}
