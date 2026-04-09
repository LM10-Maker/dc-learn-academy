-- =============================================================================
-- DC-LEARN STAGE 5 MIGRATION
-- Supabase Auth + Content Gating
-- =============================================================================
-- Date:     09 April 2026
-- Project:  iphonednnnqhxvhypvwn.supabase.co
-- Author:   Legacy Business Engineers Ltd
--
-- Purpose:  Create learner state tables, Stripe licence mapping, RLS policies,
--           and seed admin account (lmurphy@legacybe.ie).
--
-- Idempotent: safe to re-run. Uses IF NOT EXISTS / DROP IF EXISTS patterns and
-- conditional ALTER statements for licences table evolution.
-- =============================================================================

-- -----------------------------------------------------------------------------
-- 1. TABLES
-- -----------------------------------------------------------------------------

-- learner_progress: per-user, per-module, per-level Trivium completion
CREATE TABLE IF NOT EXISTS learner_progress (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES auth.users ON DELETE CASCADE,
  module_id text NOT NULL,
  level_id text NOT NULL,
  grammar_complete boolean DEFAULT false,
  logic_complete boolean DEFAULT false,
  rhetoric_complete boolean DEFAULT false,
  assessment_tier1_score integer,
  assessment_tier2_score integer,
  assessment_tier3_score integer,
  time_spent_seconds integer,
  assessment_duration_seconds integer,
  completed_at timestamptz,
  updated_at timestamptz DEFAULT now(),
  UNIQUE(user_id, module_id, level_id)
);

-- learner_pathways: multi-module learning paths, optional company scope
CREATE TABLE IF NOT EXISTS learner_pathways (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES auth.users ON DELETE CASCADE,
  pathway_id text NOT NULL,
  company_id uuid,
  started_at timestamptz DEFAULT now(),
  completed_at timestamptz,
  certificate_issued boolean DEFAULT false
);

-- learner_certificates: issued certificates (CPD, completion, achievement)
CREATE TABLE IF NOT EXISTS learner_certificates (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES auth.users ON DELETE CASCADE,
  certificate_type text NOT NULL,
  reference_id text NOT NULL,
  issued_at timestamptz DEFAULT now(),
  learner_name text,
  assessment_score integer
);

-- learner_analytics: client-side timing events (flushed from localStorage)
CREATE TABLE IF NOT EXISTS learner_analytics (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES auth.users ON DELETE CASCADE,
  module_id text NOT NULL,
  event_type text NOT NULL,
  event_data jsonb,
  recorded_at timestamptz DEFAULT now()
);

-- companies: B2B buyers (admin-managed for now)
CREATE TABLE IF NOT EXISTS companies (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL,
  licence_tier text,
  created_at timestamptz DEFAULT now()
);

-- licences: Stripe payment → access mapping
CREATE TABLE IF NOT EXISTS licences (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES auth.users ON DELETE CASCADE,
  stripe_customer_id text,
  stripe_payment_intent_id text,
  tier text NOT NULL,                -- 'founding' | 'professional' | 'corporate' | 'enterprise' | 'admin'
  amount_cents integer,
  currency text DEFAULT 'eur',
  status text DEFAULT 'active',      -- 'active' | 'revoked' | 'expired'
  created_at timestamptz DEFAULT now(),
  expires_at timestamptz             -- NULL for one-off, set for subscriptions
);

-- Backward-compat evolution: if licences existed from Stages 1–4 with the old
-- schema (stripe_session_id / plan / amount_paid), add the new columns
-- idempotently without dropping existing data.
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns
                 WHERE table_name='licences' AND column_name='tier') THEN
    ALTER TABLE licences ADD COLUMN tier text;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns
                 WHERE table_name='licences' AND column_name='amount_cents') THEN
    ALTER TABLE licences ADD COLUMN amount_cents integer;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns
                 WHERE table_name='licences' AND column_name='status') THEN
    ALTER TABLE licences ADD COLUMN status text DEFAULT 'active';
  END IF;
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns
                 WHERE table_name='licences' AND column_name='stripe_payment_intent_id') THEN
    ALTER TABLE licences ADD COLUMN stripe_payment_intent_id text;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns
                 WHERE table_name='licences' AND column_name='expires_at') THEN
    ALTER TABLE licences ADD COLUMN expires_at timestamptz;
  END IF;
  -- Kept for webhook idempotency (lookup by Stripe session id)
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns
                 WHERE table_name='licences' AND column_name='stripe_session_id') THEN
    ALTER TABLE licences ADD COLUMN stripe_session_id text;
  END IF;
END $$;

-- Helpful indexes
CREATE INDEX IF NOT EXISTS idx_learner_progress_user     ON learner_progress(user_id);
CREATE INDEX IF NOT EXISTS idx_learner_progress_module   ON learner_progress(module_id);
CREATE INDEX IF NOT EXISTS idx_learner_analytics_user    ON learner_analytics(user_id);
CREATE INDEX IF NOT EXISTS idx_learner_analytics_module  ON learner_analytics(module_id);
CREATE INDEX IF NOT EXISTS idx_learner_certificates_user ON learner_certificates(user_id);
CREATE INDEX IF NOT EXISTS idx_licences_user             ON licences(user_id);
CREATE INDEX IF NOT EXISTS idx_licences_session          ON licences(stripe_session_id);

-- -----------------------------------------------------------------------------
-- 2. ROW LEVEL SECURITY
-- -----------------------------------------------------------------------------

ALTER TABLE learner_progress     ENABLE ROW LEVEL SECURITY;
ALTER TABLE learner_pathways     ENABLE ROW LEVEL SECURITY;
ALTER TABLE learner_certificates ENABLE ROW LEVEL SECURITY;
ALTER TABLE learner_analytics    ENABLE ROW LEVEL SECURITY;
ALTER TABLE licences             ENABLE ROW LEVEL SECURITY;
ALTER TABLE companies            ENABLE ROW LEVEL SECURITY;

-- Drop existing policies so the migration is safe to re-run
DROP POLICY IF EXISTS "Users own data"       ON learner_progress;
DROP POLICY IF EXISTS "Users own data"       ON learner_pathways;
DROP POLICY IF EXISTS "Users own data"       ON learner_certificates;
DROP POLICY IF EXISTS "Users own data"       ON learner_analytics;
DROP POLICY IF EXISTS "Users read own licences" ON licences;
DROP POLICY IF EXISTS "Admin only"           ON companies;

-- Pattern: users read/write only their own rows; admins read all.
-- Admin is detected via user_metadata.role = 'admin' in the JWT.

CREATE POLICY "Users own data" ON learner_progress
  FOR ALL USING (
    auth.uid() = user_id
    OR (auth.jwt() -> 'user_metadata' ->> 'role') = 'admin'
  );

CREATE POLICY "Users own data" ON learner_pathways
  FOR ALL USING (
    auth.uid() = user_id
    OR (auth.jwt() -> 'user_metadata' ->> 'role') = 'admin'
  );

CREATE POLICY "Users own data" ON learner_certificates
  FOR ALL USING (
    auth.uid() = user_id
    OR (auth.jwt() -> 'user_metadata' ->> 'role') = 'admin'
  );

CREATE POLICY "Users own data" ON learner_analytics
  FOR ALL USING (
    auth.uid() = user_id
    OR (auth.jwt() -> 'user_metadata' ->> 'role') = 'admin'
  );

-- Licences are written by the service role (Stripe webhook) only. Clients
-- get read-only access to their own row; admins can read all.
CREATE POLICY "Users read own licences" ON licences
  FOR SELECT USING (
    auth.uid() = user_id
    OR (auth.jwt() -> 'user_metadata' ->> 'role') = 'admin'
  );

CREATE POLICY "Admin only" ON companies
  FOR ALL USING (
    (auth.jwt() -> 'user_metadata' ->> 'role') = 'admin'
  );

-- -----------------------------------------------------------------------------
-- 3. ADMIN SEED: lmurphy@legacybe.ie
-- -----------------------------------------------------------------------------
-- Conditional: only seeds if the auth user already exists. If not, run this
-- migration again after the admin completes their first magic-link sign-in
-- (which creates their auth.users row).

DO $$
DECLARE
  admin_uuid uuid;
BEGIN
  SELECT id INTO admin_uuid FROM auth.users WHERE email = 'lmurphy@legacybe.ie';

  IF admin_uuid IS NOT NULL THEN
    UPDATE auth.users
       SET raw_user_meta_data =
             COALESCE(raw_user_meta_data, '{}'::jsonb) || '{"role":"admin"}'::jsonb
     WHERE id = admin_uuid;

    IF NOT EXISTS (
      SELECT 1 FROM licences WHERE user_id = admin_uuid AND tier = 'admin'
    ) THEN
      INSERT INTO licences (user_id, tier, status, amount_cents, currency)
      VALUES (admin_uuid, 'admin', 'active', 0, 'eur');
    END IF;
  END IF;
END $$;

-- =============================================================================
-- END OF MIGRATION
-- =============================================================================
