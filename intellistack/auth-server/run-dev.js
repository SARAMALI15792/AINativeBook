// Force fetch() to use IPv4 — IPv6 is unreachable on this network, causing
// 10s connect timeouts when Node.js calls external OAuth APIs (GitHub, Google).
// This only affects undici/fetch; Neon's WebSocket uses its own transport.
import { Agent, setGlobalDispatcher } from 'undici';
setGlobalDispatcher(new Agent({ connect: { family: 4 } }));

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
