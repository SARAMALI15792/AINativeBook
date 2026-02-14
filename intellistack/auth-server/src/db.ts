/**
 * Database Configuration with Drizzle ORM
 * Connects to PostgreSQL via Neon for Better-Auth
 */

import { drizzle } from 'drizzle-orm/postgres-js';
import postgres from 'postgres';

const databaseUrl = process.env.DATABASE_URL;

if (!databaseUrl) {
  throw new Error('DATABASE_URL environment variable is required');
}

// Create PostgreSQL connection pool
const client = postgres(databaseUrl, {
  // Connection pool settings for better performance
  max: 25, // Maximum number of connections
  idle_timeout: 30, // Close idle connections after 30s
  connect_timeout: 10, // Connection timeout in seconds
  prepare: false, // Disable prepared statements for Neon compatibility
});

// Initialize Drizzle ORM
export const db = drizzle(client, {
  logger: process.env.NODE_ENV === 'development',
});

// Health check function
export async function checkDatabaseConnection(): Promise<boolean> {
  try {
    await client`SELECT 1`;
    console.log('✅ Database connection successful');
    return true;
  } catch (error) {
    console.error('❌ Database connection failed:', error);
    return false;
  }
}

// Close database connection
export async function closeDatabase(): Promise<void> {
  try {
    await client.end();
    console.log('📴 Database connection closed');
  } catch (error) {
    console.error('Error closing database:', error);
  }
}

export { client };
