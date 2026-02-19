-- Migration: Change user IDs from UUID to VARCHAR(255) for Better-Auth compatibility
-- Better-Auth generates string IDs like 'UESK5D9vQUvwU2d17u4fQoavPWWl19er'
-- This script drops foreign keys, changes column types, and recreates constraints

BEGIN;

-- Step 1: Drop all foreign key constraints referencing users.id
ALTER TABLE certificates DROP CONSTRAINT IF EXISTS certificates_user_id_fkey;
ALTER TABLE cohort_enrollments DROP CONSTRAINT IF EXISTS cohort_enrollments_enrolled_by_fkey;
ALTER TABLE cohort_enrollments DROP CONSTRAINT IF EXISTS cohort_enrollments_user_id_fkey;
ALTER TABLE cohort_instructors DROP CONSTRAINT IF EXISTS cohort_instructors_assigned_by_fkey;
ALTER TABLE cohort_instructors DROP CONSTRAINT IF EXISTS cohort_instructors_user_id_fkey;
ALTER TABLE cohorts DROP CONSTRAINT IF EXISTS cohorts_created_by_fkey;
ALTER TABLE content DROP CONSTRAINT IF EXISTS content_created_by_fkey;
ALTER TABLE content_reviews DROP CONSTRAINT IF EXISTS content_reviews_reviewer_id_fkey;
ALTER TABLE content DROP CONSTRAINT IF EXISTS content_updated_by_fkey;
ALTER TABLE content_versions DROP CONSTRAINT IF EXISTS content_versions_created_by_fkey;
ALTER TABLE content_versions DROP CONSTRAINT IF EXISTS content_versions_reviewed_by_fkey;
ALTER TABLE institution_members DROP CONSTRAINT IF EXISTS institution_members_user_id_fkey;
ALTER TABLE oauth_accounts DROP CONSTRAINT IF EXISTS oauth_accounts_user_id_fkey;
ALTER TABLE password_reset_tokens DROP CONSTRAINT IF EXISTS password_reset_tokens_user_id_fkey;
ALTER TABLE progress DROP CONSTRAINT IF EXISTS progress_user_id_fkey;
ALTER TABLE rag_conversations DROP CONSTRAINT IF EXISTS rag_conversations_user_id_fkey;
ALTER TABLE rag_messages DROP CONSTRAINT IF EXISTS rag_messages_user_id_fkey;
ALTER TABLE sessions DROP CONSTRAINT IF EXISTS sessions_user_id_fkey;
ALTER TABLE tutor_session_items DROP CONSTRAINT IF EXISTS tutor_session_items_user_id_fkey;
ALTER TABLE user_badges DROP CONSTRAINT IF EXISTS user_badges_user_id_fkey;
ALTER TABLE user_roles DROP CONSTRAINT IF EXISTS user_roles_granted_by_fkey;
ALTER TABLE user_roles DROP CONSTRAINT IF EXISTS user_roles_user_id_fkey;

-- Step 2: Change users.id from UUID to VARCHAR(255)
ALTER TABLE users ALTER COLUMN id TYPE VARCHAR(255);

-- Step 3: Change all foreign key columns from UUID to VARCHAR(255)
ALTER TABLE certificates ALTER COLUMN user_id TYPE VARCHAR(255);
ALTER TABLE cohort_enrollments ALTER COLUMN enrolled_by TYPE VARCHAR(255);
ALTER TABLE cohort_enrollments ALTER COLUMN user_id TYPE VARCHAR(255);
ALTER TABLE cohort_instructors ALTER COLUMN assigned_by TYPE VARCHAR(255);
ALTER TABLE cohort_instructors ALTER COLUMN user_id TYPE VARCHAR(255);
ALTER TABLE cohorts ALTER COLUMN created_by TYPE VARCHAR(255);
ALTER TABLE content ALTER COLUMN created_by TYPE VARCHAR(255);
ALTER TABLE content_reviews ALTER COLUMN reviewer_id TYPE VARCHAR(255);
ALTER TABLE content ALTER COLUMN updated_by TYPE VARCHAR(255);
ALTER TABLE content_versions ALTER COLUMN created_by TYPE VARCHAR(255);
ALTER TABLE content_versions ALTER COLUMN reviewed_by TYPE VARCHAR(255);
ALTER TABLE institution_members ALTER COLUMN user_id TYPE VARCHAR(255);
ALTER TABLE oauth_accounts ALTER COLUMN user_id TYPE VARCHAR(255);
ALTER TABLE password_reset_tokens ALTER COLUMN user_id TYPE VARCHAR(255);
ALTER TABLE progress ALTER COLUMN user_id TYPE VARCHAR(255);
ALTER TABLE rag_conversations ALTER COLUMN user_id TYPE VARCHAR(255);
ALTER TABLE rag_messages ALTER COLUMN user_id TYPE VARCHAR(255);
ALTER TABLE sessions ALTER COLUMN user_id TYPE VARCHAR(255);
ALTER TABLE tutor_session_items ALTER COLUMN user_id TYPE VARCHAR(255);
ALTER TABLE user_badges ALTER COLUMN user_id TYPE VARCHAR(255);
ALTER TABLE user_roles ALTER COLUMN granted_by TYPE VARCHAR(255);
ALTER TABLE user_roles ALTER COLUMN user_id TYPE VARCHAR(255);

-- Step 4: Recreate foreign key constraints
ALTER TABLE certificates ADD CONSTRAINT certificates_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id);
ALTER TABLE cohort_enrollments ADD CONSTRAINT cohort_enrollments_enrolled_by_fkey FOREIGN KEY (enrolled_by) REFERENCES users(id);
ALTER TABLE cohort_enrollments ADD CONSTRAINT cohort_enrollments_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id);
ALTER TABLE cohort_instructors ADD CONSTRAINT cohort_instructors_assigned_by_fkey FOREIGN KEY (assigned_by) REFERENCES users(id);
ALTER TABLE cohort_instructors ADD CONSTRAINT cohort_instructors_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id);
ALTER TABLE cohorts ADD CONSTRAINT cohorts_created_by_fkey FOREIGN KEY (created_by) REFERENCES users(id);
ALTER TABLE content ADD CONSTRAINT content_created_by_fkey FOREIGN KEY (created_by) REFERENCES users(id);
ALTER TABLE content_reviews ADD CONSTRAINT content_reviews_reviewer_id_fkey FOREIGN KEY (reviewer_id) REFERENCES users(id);
ALTER TABLE content ADD CONSTRAINT content_updated_by_fkey FOREIGN KEY (updated_by) REFERENCES users(id);
ALTER TABLE content_versions ADD CONSTRAINT content_versions_created_by_fkey FOREIGN KEY (created_by) REFERENCES users(id);
ALTER TABLE content_versions ADD CONSTRAINT content_versions_reviewed_by_fkey FOREIGN KEY (reviewed_by) REFERENCES users(id);
ALTER TABLE institution_members ADD CONSTRAINT institution_members_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id);
ALTER TABLE oauth_accounts ADD CONSTRAINT oauth_accounts_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id);
ALTER TABLE password_reset_tokens ADD CONSTRAINT password_reset_tokens_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;
ALTER TABLE progress ADD CONSTRAINT progress_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id);
ALTER TABLE rag_conversations ADD CONSTRAINT rag_conversations_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id);
ALTER TABLE rag_messages ADD CONSTRAINT rag_messages_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id);
ALTER TABLE sessions ADD CONSTRAINT sessions_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id);
ALTER TABLE tutor_session_items ADD CONSTRAINT tutor_session_items_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL;
ALTER TABLE user_badges ADD CONSTRAINT user_badges_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id);
ALTER TABLE user_roles ADD CONSTRAINT user_roles_granted_by_fkey FOREIGN KEY (granted_by) REFERENCES users(id);
ALTER TABLE user_roles ADD CONSTRAINT user_roles_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id);

COMMIT;
