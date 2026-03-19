// Load dotenv first with absolute path, then import the main app
import dotenv from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';

// Get directory name for absolute path resolution
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Load .env file with absolute path for reliability across different environments
dotenv.config({ path: path.resolve(__dirname, './.env') });

const app = await import('./src/index.ts');
