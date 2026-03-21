/**
 * Database Configuration with Drizzle ORM
 * Connects to PostgreSQL via Neon for Better-Auth
 */

import { drizzle } from 'drizzle-orm/neon-serverless';
import { Pool } from '@neondatabase/serverless';
// Node.js 22 has a native WebSocket global — @neondatabase/serverless uses it automatically

const databaseUrl = process.env.DATABASE_URL;

if (!databaseUrl) {
  console.error('❌ DATABASE_URL environment variable is missing!');
  console.error('💡 Make sure your .env file is in the auth-server directory and contains DATABASE_URL');
  console.error('📋 Example: DATABASE_URL=postgresql://username:password@localhost:5432/database_name');
  throw new Error('DATABASE_URL environment variable is required');
}

// Create Neon serverless connection pool (connects via WebSocket on port 443)
const client = new Pool({ connectionString: databaseUrl });

// Initialize Drizzle ORM
export const db = drizzle(client, {
  logger: process.env.NODE_ENV === 'development',
});

// Health check function
export async function checkDatabaseConnection(): Promise<boolean> {
  try {
    await client.query('SELECT 1');
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
