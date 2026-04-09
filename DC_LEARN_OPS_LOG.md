# DC-LEARN Operations Log

**Repository:** dc-learn-academy
**Started:** 06 April 2026
**Rule:** Append only — never edit previous entries. Every session adds one block before SHIP/NOT SHIP verdict.

---

## Entry Format

```
## YYYY-MM-DD | Model | Module(s) | Session Type
- [TAG] Description
```

**Tags:** `[FIX]` defect resolved, `[GNEW]` new G-NEW item logged, `[SWEEP]` audit/sweep finding, `[BUILD]` new feature or component, `[DEPLOY]` pushed to Netlify, `[NOTSHIP]` blocking reason, `[BLOCKED]` dependency or external blocker, `[DECISION]` architecture or content decision recorded

**Grep cheatsheet:**
- Last deployed version per module: `grep DEPLOY DC_LEARN_OPS_LOG.md`
- Outstanding blockers: `grep NOTSHIP DC_LEARN_OPS_LOG.md`
- All G-NEW items raised: `grep GNEW DC_LEARN_OPS_LOG.md`
- Sessions per module: `grep "DC-LEARN-008" DC_LEARN_OPS_LOG.md`

---

## 2026-04-06 | Opus | ALL | Ops log creation
- [BUILD] DC_LEARN_OPS_LOG.md created — persistent append-only session log
- [DECISION] Inspired by Karpathy LLM Wiki log.md pattern, adapted for build-and-ship workflow
- [DECISION] Scope: DC-LEARN project only (16 modules). Separate LBE_OPS_LOG.md for other workstreams if needed later
- [DECISION] Karpathy Obsidian + Claude Code wiki pattern logged as post-launch candidate for regulatory monitoring (CRU, EirGrid, F-Gas, CRREM)

---

## 2026-04-09 | Opus | ALL | Stage 5 Session 1 — Schema + Stripe webhook
- [DECISION] Blockers cleared 09/04/2026: VAT (23% Irish B2B, required), Legal (disclaimer on certificates/modules sufficient), Positioning (intelligence layer only, locked 02/04/2026)
- [BUILD] supabase/stage5_migration.sql — idempotent migration with 6 tables: learner_progress, learner_pathways, learner_certificates, learner_analytics, companies, licences
- [BUILD] RLS enabled on all tables; "Users own data" + admin bypass via user_metadata.role='admin'; companies admin-only
- [BUILD] Conditional ALTER TABLE block preserves pre-Stage-5 licences columns while adding new columns (tier, amount_cents, stripe_payment_intent_id, status, expires_at, stripe_session_id)
- [BUILD] Admin seed for lmurphy@legacybe.ie inside DO $$ block — only fires if auth.users row exists; re-runnable after first magic-link sign-in
- [BUILD] netlify/functions/stripe-webhook.js extended — 4-tier PRICE_MAP (founding/professional/corporate/enterprise), subscription period-end → expires_at, amount-based tier inference fallback, idempotency guard via stripe_session_id
- [BUILD] docs/STAGE5_SCHEMA_DOC.md — table docs, RLS policy summary, Stripe→licence flow, failure-mode matrix
- [DECISION] Price→tier via env vars (STRIPE_PRICE_FOUNDING/PROFESSIONAL/CORPORATE/ENTERPRISE) — LM to paste IDs from Stripe dashboard before live deploy
- [DECISION] Licences table: service-role webhook inserts; client SELECT-only on own rows via RLS. Prevents client tampering with licence state.
- [GNEW] G-NEW-56: Stage 5 supersedes earlier learner_tiers schema — modules 000/003-015 still reference learner_tiers in dcAuth._loadTier; Session 2 replaces with licences query

---

## 2026-04-09 | Opus | ALL | Stage 5 Session 2 — AuthGate + PlatformSync batch roll
- [BUILD] /tmp/stage5-build/new_auth_block.txt — unified Stage 5 auth + sync block (~360 lines): dcAuth, AuthButton, LockedOverlay, useAuth, PlatformSync
- [DECISION] IS_FREE_MODULE derived from TOOL_ID at runtime — no per-file edit required, single source of truth: `(TOOL_ID === '000' || '001' || '002')`
- [DECISION] dcAuth.checkLicence(userId) queries new `licences` table where status='active'; returns null on any error so module falls through to IS_FREE_MODULE || dcAuth.isPaid() localStorage cache (Layer 1 never depends on Layer 2)
- [DECISION] Admin bypass: dcAuth.isAdminUser(user) checks user.user_metadata.role === 'admin' BEFORE licence query — admins get full access without licence row
- [BUILD] useAuth() hook: session → admin check → licence check → fall-through; all error paths console.warn only, never user-visible
- [BUILD] PlatformSync({user, progress}): flushes safeStore(DC_TIMING_KEY) → learner_analytics batch insert (≤500 rows, clears on success); upserts progress → learner_progress with onConflict user_id,module_id,level_id
- [BUILD] /tmp/stage5-build/transform.js — Node.js batch transformer with balanced-brace useAuth end detection; handles both basic (001/002) and extended (000/003-015) variants; idempotent via <PlatformSync user={authState.user}/ JSX guard
- [FIX] G-NEW-56 resolved: transform replaces extended variant's inner `const supa = null;` stub with `const supa = (typeof supabase !== 'undefined') ? supabase.createClient(SUPA_URL, SUPA_KEY) : null;` — Supabase now actually works in modules 003-015 (previously the inner const null shadowed the outer var supa createClient)
- [DECISION] dc-learn-000's duplicate outer `var SUPA_URL` + inner `const SUPA_URL` coexists safely: outer `var` goes to window, inner `const` is script-scoped to Babel block — no runtime conflict, no edit needed
- [BUILD] Batch transform applied: 16/16 modules replaced auth block, 13/16 replaced supa stub, 16/16 inserted `<PlatformSync user={authState.user} progress={progress}/>` after `<LockedOverlay/>` JSX line
- [BUILD] Babel syntax-check via @babel/standalone + preset-react: **16/16 PASS**
- [SWEEP] Post-transform audit: 0 lingering `learner_tiers` refs, 0 lingering `authState.loggedIn/email/tier` refs, 0 lingering `dcAuth._loadTier/isLoggedIn/userEmail` refs, 16/16 have `dcAuth.checkLicence` + `function PlatformSync` + BookTab intact
- [GNEW] G-NEW-57: LockedOverlay references `LOGO_SRC` — verified present in all 16 modules (inner Babel const); no fix needed
- [GNEW] G-NEW-58: PlatformSync depends on `safeStore`, `DC_TIMING_KEY`, `TOOL_ID` — all three present in every module (confirmed by grep)
- [DECISION] No separate "outer Supabase init block" added — all 16 modules already have working supa client (002/001 via inner `const supa = createClient`, 000/003-015 via outer `var supa = createClient` + now-fixed inner re-init). Per Stage 5 rule "Layer 1 never depends on Layer 2" — no behavioural change if Supabase CDN is blocked.
- [DEPLOY] Branch: claude/supabase-auth-content-gating-vJVFr
- [SHIP] Stage 5 Session 2 ready to ship — 16/16 Babel pass, all failure modes fall through to localStorage, no user-visible regressions.

---
