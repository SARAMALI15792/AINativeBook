import dotenv from 'dotenv';
import postgres from 'postgres';

dotenv.config();

const sql = postgres(process.env.DATABASE_URL);

async function migrate() {
  console.log('🔄 Creating database tables...');

  try {
    // Create tables using raw SQL
    await sql`
      CREATE TABLE IF NOT EXISTS "user" (
        "id" text PRIMARY KEY,
        "name" text NOT NULL,
        "email" text NOT NULL UNIQUE,
        "email_verified" boolean DEFAULT false NOT NULL,
        "image" text,
        "created_at" timestamp DEFAULT now() NOT NULL,
        "updated_at" timestamp DEFAULT now() NOT NULL
      );
    `;

    await sql`
      CREATE TABLE IF NOT EXISTS "session" (
        "id" text PRIMARY KEY,
        "expires_at" timestamp NOT NULL,
        "token" text NOT NULL UNIQUE,
        "created_at" timestamp DEFAULT now() NOT NULL,
        "updated_at" timestamp DEFAULT now() NOT NULL,
        "ip_address" text,
        "user_agent" text,
        "user_id" text NOT NULL REFERENCES "user"("id") ON DELETE CASCADE
      );
    `;

    await sql`
      CREATE INDEX IF NOT EXISTS "session_userId_idx" ON "session"("user_id");
    `;

    await sql`
      CREATE TABLE IF NOT EXISTS "account" (
        "id" text PRIMARY KEY,
        "account_id" text NOT NULL,
        "provider_id" text NOT NULL,
        "user_id" text NOT NULL REFERENCES "user"("id") ON DELETE CASCADE,
        "access_token" text,
        "refresh_token" text,
        "id_token" text,
        "access_token_expires_at" timestamp,
        "refresh_token_expires_at" timestamp,
        "scope" text,
        "password" text,
        "created_at" timestamp DEFAULT now() NOT NULL,
        "updated_at" timestamp DEFAULT now() NOT NULL
      );
    `;

    await sql`
      CREATE INDEX IF NOT EXISTS "account_userId_idx" ON "account"("user_id");
    `;

    await sql`
      CREATE TABLE IF NOT EXISTS "verification" (
        "id" text PRIMARY KEY,
        "identifier" text NOT NULL,
        "value" text NOT NULL,
        "expires_at" timestamp NOT NULL,
        "created_at" timestamp DEFAULT now() NOT NULL,
        "updated_at" timestamp DEFAULT now() NOT NULL
      );
    `;

    await sql`
      CREATE INDEX IF NOT EXISTS "verification_identifier_idx" ON "verification"("identifier");
    `;

    await sql`
      CREATE TABLE IF NOT EXISTS "jwks" (
        "id" text PRIMARY KEY,
        "public_key" text NOT NULL,
        "private_key" text NOT NULL,
        "created_at" timestamp NOT NULL,
        "expires_at" timestamp
      );
    `;

    await sql`
      CREATE TABLE IF NOT EXISTS "oauth_application" (
        "id" text PRIMARY KEY,
        "name" text,
        "icon" text,
        "metadata" text,
        "client_id" text UNIQUE,
        "client_secret" text,
        "redirect_urls" text,
        "type" text,
        "disabled" boolean DEFAULT false,
        "user_id" text REFERENCES "user"("id") ON DELETE CASCADE,
        "created_at" timestamp,
        "updated_at" timestamp
      );
    `;

    await sql`
      CREATE INDEX IF NOT EXISTS "oauthApplication_userId_idx" ON "oauth_application"("user_id");
    `;

    await sql`
      CREATE TABLE IF NOT EXISTS "oauth_access_token" (
        "id" text PRIMARY KEY,
        "access_token" text UNIQUE,
        "refresh_token" text UNIQUE,
        "access_token_expires_at" timestamp,
        "refresh_token_expires_at" timestamp,
        "client_id" text REFERENCES "oauth_application"("client_id") ON DELETE CASCADE,
        "user_id" text REFERENCES "user"("id") ON DELETE CASCADE,
        "scopes" text,
        "created_at" timestamp,
        "updated_at" timestamp
      );
    `;

    await sql`
      CREATE INDEX IF NOT EXISTS "oauthAccessToken_clientId_idx" ON "oauth_access_token"("client_id");
    `;

    await sql`
      CREATE INDEX IF NOT EXISTS "oauthAccessToken_userId_idx" ON "oauth_access_token"("user_id");
    `;

    await sql`
      CREATE TABLE IF NOT EXISTS "oauth_consent" (
        "id" text PRIMARY KEY,
        "client_id" text REFERENCES "oauth_application"("client_id") ON DELETE CASCADE,
        "user_id" text REFERENCES "user"("id") ON DELETE CASCADE,
        "scopes" text,
        "created_at" timestamp,
        "updated_at" timestamp,
        "consent_given" boolean
      );
    `;

    await sql`
      CREATE INDEX IF NOT EXISTS "oauthConsent_clientId_idx" ON "oauth_consent"("client_id");
    `;

    await sql`
      CREATE INDEX IF NOT EXISTS "oauthConsent_userId_idx" ON "oauth_consent"("user_id");
    `;

    console.log('✅ Database tables created successfully!');
  } catch (error) {
    console.error('❌ Migration failed:', error);
    throw error;
  } finally {
    await sql.end();
  }
}

migrate();
