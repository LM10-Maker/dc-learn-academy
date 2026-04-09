# DC-LEARN Stage 5 — Supabase Schema & Data Flow

**Version:** 1.0
**Date:** 09 April 2026
**Author:** Legacy Business Engineers Ltd
**Scope:** Supabase schema, Stripe webhook, content gating for DC-LEARN Professional

---

## 1. Architecture Principles

| Principle | Applied |
|-----------|---------|
| Layer 1 (localStorage) never depends on Layer 2 (Supabase) | AuthGate falls through to localStorage mode on any Supabase failure |
| Admin is a first-class role, not a payment bypass | `role: admin` stored in `auth.users.raw_user_meta_data`; RLS + AuthGate both check it |
| Idempotent migrations | Migration uses `IF NOT EXISTS` / `DROP POLICY IF EXISTS` / conditional `ALTER` so it can be re-run |
| Row Level Security on every learner table | A user can never see another user's progress, analytics, certificates, or licences |

---

## 2. Tables

All tables live in the `public` schema of Supabase project
`iphonednnnqhxvhypvwn.supabase.co`.

### 2.1 `learner_progress`

Per-user, per-module, per-level Trivium completion state plus assessment
scores. This is the source of truth when the learner is signed in; localStorage
is kept as a cache for the offline/anonymous case.

| Column | Type | Notes |
|---|---|---|
| `id` | `uuid` | PK |
| `user_id` | `uuid` | FK → `auth.users`, `ON DELETE CASCADE` |
| `module_id` | `text` | e.g. `DC-LEARN-002` |
| `level_id` | `text` | Free-form; modules use level numbers or IDs |
| `grammar_complete` | `boolean` | Grammar stage done |
| `logic_complete` | `boolean` | Logic stage done |
| `rhetoric_complete` | `boolean` | Rhetoric stage done |
| `assessment_tier1_score` | `integer` | Tier 1 score, nullable |
| `assessment_tier2_score` | `integer` | Tier 2 score, nullable |
| `assessment_tier3_score` | `integer` | Tier 3 score, nullable |
| `time_spent_seconds` | `integer` | Cumulative module time |
| `assessment_duration_seconds` | `integer` | Time on the final assessment |
| `completed_at` | `timestamptz` | First time all three stages passed |
| `updated_at` | `timestamptz` | Last write |

**Unique constraint:** `(user_id, module_id, level_id)` — allows upsert.

### 2.2 `learner_pathways`

Multi-module learning paths. Supports the B2B company-scoped pathway feature.

| Column | Type | Notes |
|---|---|---|
| `id` | `uuid` | PK |
| `user_id` | `uuid` | FK → `auth.users` |
| `pathway_id` | `text` | Free-form path identifier |
| `company_id` | `uuid` | Optional FK → `companies.id` |
| `started_at` | `timestamptz` | Default `now()` |
| `completed_at` | `timestamptz` | Null until done |
| `certificate_issued` | `boolean` | Flipped on certificate issue |

### 2.3 `learner_certificates`

Certificates (completion, achievement, CPD). Legal disclaimer on the
certificate itself satisfies the current legal review (09/04/2026).

| Column | Type | Notes |
|---|---|---|
| `id` | `uuid` | PK |
| `user_id` | `uuid` | FK → `auth.users` |
| `certificate_type` | `text` | `Completion` / `Achievement` / `CPD` |
| `reference_id` | `text` | LBE serial, e.g. `LBE-002-2026-ABCD` |
| `issued_at` | `timestamptz` | Default `now()` |
| `learner_name` | `text` | Printed on the certificate |
| `assessment_score` | `integer` | Percentage |

### 2.4 `learner_analytics`

Client-side timing events flushed from `localStorage` by `PlatformSync`. Sparse
schema intentionally — raw event data lives in `event_data` jsonb so we can
evolve instrumentation without schema churn.

| Column | Type | Notes |
|---|---|---|
| `id` | `uuid` | PK |
| `user_id` | `uuid` | FK → `auth.users` |
| `module_id` | `text` | e.g. `DC-LEARN-002` |
| `event_type` | `text` | `tab_switch` / `level_change` / `assess_q_submit` / ... |
| `event_data` | `jsonb` | Full event payload including `ts` |
| `recorded_at` | `timestamptz` | Derived from `event_data.ts` when flushed |

### 2.5 `companies`

B2B buyers. Admin-managed for now; no self-serve.

| Column | Type |
|---|---|
| `id` | `uuid` PK |
| `name` | `text` |
| `licence_tier` | `text` |
| `created_at` | `timestamptz` |

### 2.6 `licences`

Stripe payment → access mapping. One row per Stripe checkout session.

| Column | Type | Notes |
|---|---|---|
| `id` | `uuid` | PK |
| `user_id` | `uuid` | FK → `auth.users` |
| `stripe_customer_id` | `text` | Stripe customer ID |
| `stripe_payment_intent_id` | `text` | Stripe PaymentIntent ID (for refund traceability) |
| `stripe_session_id` | `text` | Stripe Checkout Session ID (used for webhook idempotency) |
| `tier` | `text` | `founding` \| `professional` \| `corporate` \| `enterprise` \| `admin` |
| `amount_cents` | `integer` | `session.amount_total` |
| `currency` | `text` | Default `eur` |
| `status` | `text` | `active` \| `revoked` \| `expired` |
| `created_at` | `timestamptz` | Default `now()` |
| `expires_at` | `timestamptz` | NULL for one-off; subscription period-end for corporate |

---

## 3. Row Level Security

RLS is **enabled on every table above**.

### 3.1 Learner-owned tables

`learner_progress`, `learner_pathways`, `learner_certificates`,
`learner_analytics` all share the same policy:

```sql
CREATE POLICY "Users own data" ON <table>
  FOR ALL USING (
    auth.uid() = user_id
    OR (auth.jwt() -> 'user_metadata' ->> 'role') = 'admin'
  );
```

A learner can only read and write their own rows; the admin
(`lmurphy@legacybe.ie`) reads all rows.

### 3.2 `licences`

`SELECT`-only for the owner; the service-role Stripe webhook bypasses RLS to
insert rows.

```sql
CREATE POLICY "Users read own licences" ON licences
  FOR SELECT USING (
    auth.uid() = user_id
    OR (auth.jwt() -> 'user_metadata' ->> 'role') = 'admin'
  );
```

### 3.3 `companies`

Admin only for now. B2B self-serve is deferred.

```sql
CREATE POLICY "Admin only" ON companies
  FOR ALL USING (
    (auth.jwt() -> 'user_metadata' ->> 'role') = 'admin'
  );
```

---

## 4. Admin Seed

```sql
UPDATE auth.users
   SET raw_user_meta_data = COALESCE(raw_user_meta_data,'{}'::jsonb)
                          || '{"role":"admin"}'::jsonb
 WHERE email = 'lmurphy@legacybe.ie';

INSERT INTO licences (user_id, tier, status, amount_cents, currency)
SELECT id, 'admin', 'active', 0, 'eur'
  FROM auth.users WHERE email = 'lmurphy@legacybe.ie';
```

The migration runs this inside a `DO $$ ... $$` block that only fires if the
auth.users row already exists. First-time setup:

1. Deploy migration → tables + RLS + empty seed no-op.
2. Visit `/login.html`, enter `lmurphy@legacybe.ie`, click magic link.
3. Re-run `stage5_migration.sql` — the seed block now elevates the user and
   inserts the admin licence.

---

## 5. Stripe → Licence Data Flow

```
  Learner pays on legacybe.ie
         │
         ▼
  Stripe Checkout ─ checkout.session.completed
         │
         ▼
  Netlify Function  stripe-webhook.js
    1. Verify Stripe signature
    2. Resolve tier from line-items price id
       (fallback to amount-based inference)
    3. Find or create Supabase auth.users row for customer email
    4. Idempotency guard on stripe_session_id
    5. INSERT into licences (tier, amount_cents, ...)
    6. For subscription mode: store subscription period_end → expires_at
    7. supabase.auth.admin.generateLink('magiclink')
         │
         ▼
  Learner receives magic-link email → signs in
         │
         ▼
  Module loads → AuthGate reads session → queries licences
     ├── session.user.user_metadata.role === 'admin'   → full access
     ├── active licence row exists                    → full access
     └── no session or no licence                     → free modules only
         │
         ▼
  PlatformSync (invisible) flushes localStorage:
     • DC_TIMING_KEY    → learner_analytics (batch insert)
     • dc{NNN}_progress → learner_progress  (upsert)
```

### 5.1 Price → tier mapping (env vars)

| Env var | Tier | List price |
|---|---|---|
| `STRIPE_PRICE_FOUNDING`     | `founding`     | €995 one-off |
| `STRIPE_PRICE_PROFESSIONAL` | `professional` | €1,995 one-off |
| `STRIPE_PRICE_CORPORATE`    | `corporate`    | €9,500 / yr subscription |
| `STRIPE_PRICE_ENTERPRISE`   | `enterprise`   | €18,000+ one-off / sub |

VAT: 23% Irish B2B is applied at checkout. Tier mapping uses Stripe's pre-VAT
price IDs, so the amount-based fallback thresholds are forgiving.

### 5.2 Idempotency

Stripe retries webhooks. The webhook looks up `licences.stripe_session_id`
before inserting. Duplicate deliveries return `200 {received:true,duplicate:true}`.

---

## 6. Failure Modes (Layer 1 never depends on Layer 2)

| Failure | Module behaviour |
|---|---|
| Supabase CDN blocked (`window.supabase` undefined) | Module runs on localStorage; `console.warn` only |
| `getSession()` throws | Falls through to `IS_FREE_MODULE || localStorage.dc_learn_paid` |
| `licences` query fails (network, RLS misconfig, etc.) | Same fallthrough, `console.warn` |
| Magic link email never arrives | Learner can retry from `/login.html` |
| Webhook fails after Stripe payment | Stripe retries automatically; LM receives failure alert via Stripe dashboard |

**No user-visible auth error ever displaces module content.** This is the
cardinal Stage-5 rule.

---

## 7. Files

| Path | Purpose |
|---|---|
| `supabase/stage5_migration.sql` | Idempotent migration: tables, RLS, admin seed |
| `netlify/functions/stripe-webhook.js` | Stripe → Supabase licences bridge |
| `docs/STAGE5_SCHEMA_DOC.md` | This document |
| `netlify/dc-learn-0NN.html` | Modules with embedded `AuthGate` + `PlatformSync` (Session 2) |
| `netlify/login.html` | Magic-link sign-in page |

---

## 8. Document Control

| Field | Value |
|---|---|
| Version | 1.0 |
| Date | 09 April 2026 |
| Supersedes | Stage 4 `learner_tiers` schema (deprecated) |
| Blockers cleared | VAT (23%), Legal (disclaimer), Positioning — 09/04/2026 |
| Companion | `DC_LEARN_PLATFORM_BUILD_PROMPT_v1_0.md` |
| Companion | `DC_LEARN_EVOLUTION_ROADMAP_v1_0.md` |
