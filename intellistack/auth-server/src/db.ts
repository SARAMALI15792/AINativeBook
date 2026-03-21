/**
 * Database Configuration with Drizzle ORM
 * Connects to PostgreSQL via standard pg driver (works with local and cloud Postgres)
 */

import { drizzle } from 'drizzle-orm/node-postgres';
import pkg from 'pg';
const { Pool } = pkg;

const databaseUrl = process.env.DATABASE_URL;

if (!databaseUrl) {
  console.error('❌ DATABASE_URL environment variable is missing!');
  console.error('💡 Make sure your .env file is in the auth-server directory and contains DATABASE_URL');
  console.error('📋 Example: DATABASE_URL=postgresql://username:password@localhost:5432/database_name');
  throw new Error('DATABASE_URL environment variable is required');
}

// Create standard pg connection pool (connects via TCP — works with local and Neon Postgres)
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
