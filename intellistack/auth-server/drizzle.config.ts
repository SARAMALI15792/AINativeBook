import { defineConfig } from 'drizzle-kit';
import path from 'path';
import { fileURLToPath } from 'url';

// Get directory name for absolute path resolution
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export default defineConfig({
  schema: path.resolve(__dirname, './src/auth-schema.ts'),
  dialect: 'postgresql',
  dbCredentials: {
    url: process.env.DATABASE_URL!,
  },
  out: path.resolve(__dirname, './drizzle'),
});
