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

## 2026-04-10 | Opus | ALL | Fleet-wide content & quality audit
- [SWEEP] Fleet audit complete — 16/16 modules scanned, report delivered
- [SWEEP] Checks executed: stale values (1A/1D), banned terminology (1B), Mark voice (1C), version consistency (1E), IS_FREE_MODULE (1F), EED Art.26 (1G), service codes (1H), scenario terminology (1I), hall naming (1J), content depth (Task 2), assessment distribution (Task 3), known defects D1–D4 (Task 4), Supabase schema snapshot (Task 5)
- [SWEEP] Defect totals: 6 P1, 4 P2, 14 P3. Modules 000 and 007 are lowest launch-readiness (terminology replacement bugs + assessment bias). Modules 012 and 014 are cleanest.
- [SWEEP] Known defects D1 (001 TODO), D3 (004 missing L9), D4 (001 tab style) all RESOLVED. D2 (004 L6 narrative leak) not reproduced but 3 truncated rhetoric texts found nearby.
- [SWEEP] 6 fix sessions recommended: A (terminology 30min), B (assessment rebalance 45min), C (C&E depth 2hrs), D (text corruption 15min), E (version comments 20min), F (Mark voice 30min)
- [DECISION] Report saved: DC_LEARN_FLEET_AUDIT_REPORT_v1_0.md — LM to review before fix sessions begin
- [GNEW] G-NEW-73 enforced: zero code changes, zero fixes — audit only

---

## 2026-04-10 | Opus | 000, 004, 007 | Fix Session 1 — broken text repair
- [FIX] 000 line 682: restored 'CRU Compliance' as deprecated term in Q000-21 options + explain (was 'CRU Readiness' on both sides of contrast)
- [FIX] 007 lines 468, 470, 473, 636, 708: restored 'Stranding Year' as deprecated term in 7 broken contrast sentences (was 'Misalignment Year' on both sides)
- [FIX] 007 line 600: replaced near-duplicate distractor 'Misalignment Year' with 'Stranding Year' in Q007-19 options
- [FIX] 004 line 447: repaired Declan L6 truncated rhetoric ("compliant.d me" → "compliant. He told me")
- [FIX] 004 line 486: repaired Declan L7 truncated rhetoric ("payback.d me" → "payback. Nobody told me")
- [FIX] 004 line 525: repaired Declan L9 truncated rhetoric ("next.r into a plan" → "next." — removed duplicate tail)
- [FIX] 004 line 451: repaired Tom L6 truncated rhetoric ("market.ination." → "market. Risk elimination:")
- [SWEEP] Fleet-wide grep: 0 broken terminology replacements remaining, 0 mid-sentence truncation fragments remaining
- [SWEEP] D1 (001 "TODO Curate") status: RESOLVED — 0 matches
- [BUILD] Babel syntax check: 16/16 PASS

---

## 2026-04-10 | Opus | 000 | Fix Session 2 — assessment position rebalance
- [FIX] 000: assessment answer-position bias fixed — redistributed from 1/20/5/1 → 7/7/7/6 across positions 0/1/2/3
- [FIX] 15 questions repositioned: Q3(1→0), Q5(1→3), Q6(1→3), Q7(1→0), Q8(1→0), Q9(1→2), Q10(1→3), Q12(1→2), Q13(2→1), Q14(1→0), Q15(1→3), Q17(1→0), Q19(1→0), Q20(1→2), Q22(1→3), Q24(1→0), Q27(0→1)
- [SWEEP] Fleet check: all 16 modules within 5–8 per position (adjusted for useState false positives). No deviations.
- [DECISION] Option text, question text, and explanations unchanged — position rotation only
- [BUILD] Babel syntax check: 16/16 PASS

---

## 2026-04-10 | Opus | 001, 011, 013 | Fix Session 3 — Cause-and-Effect Content Depth
- [BUILD] 001 (Power Chain): 9 new C&E entries added (1 per level), covering: power factor penalty, K-factor transformer, fault level rating, eco mode tolerance, STS source review, PDU transformer overheating, busway water exposure, C13/C19 connector mismatch, PSU over-provisioning efficiency
- [BUILD] 011 (Physical Security): 9 new C&E entries added (1 per level), covering: time-based access restrictions, PIDS zone granularity, gate interlock failure, mantrap sensor drift, dormant credentials, electronic lock fail-mode, NVR storage shortfall, IDS–ACS integration, maintenance contract lapse
- [BUILD] 013 (Commissioning): 9 new C&E entries added (1 per level), covering: seasonal schedule dependency, harmonic load FAT, pre-functional documentation, realistic IST failure profiles, post-test thermal imaging, mild-weather PVT limitation, BMS winter control gap, inaccessible snagging items, night-shift training gap
- [SWEEP] C&E counts verified: 001=36, 011=36, 013=36 (4 per level × 9 levels, up from 3 per level × 9 = 27)
- [DECISION] All new entries cover different failure modes from existing entries — no duplicates, no modifications to existing content
- [DECISION] Every entry includes specific numbers (kW, €, %, hours) and references Clonshaugh parameters where applicable
- [BUILD] Babel syntax check: 16/16 PASS

---

## 2026-04-10 | Opus | ALL | Content Audit — clockQuotes, Visual Guide, Clock Chapters
- [SWEEP] clockQuote + Visual Guide + Clock chapter audit — fleet-wide
- [SWEEP] clockQuotes: 144/144 CLEAN — 9 per module, all levels populated, no gaps
- [SWEEP] VisualGuideTab: 16/16 CLEAN — present in all modules
- [SWEEP] ChainTab: 16/16 CLEAN — present in all modules
- [SWEEP] Chain Overview: P3 naming inconsistency — 4 variants across fleet (ChainOverview, ChainOverviewDiagram, VGChainOverview, VG_ChainOverview). Module 000 has no chain overview diagram.
- [SWEEP] BookTab: 16/16 CLEAN — present in all modules. All 17 chapter files exist (prologue + ch01–ch15 + compiled book).
- [SWEEP] StoryTab: 0/16 — not present in any module (appears renamed to BookTab)
- [SWEEP] Chapter file note: ch01 (14 KB) is ~50% smaller than fleet average (25–29 KB). May be intentional or incomplete.
- [DECISION] Report saved: DC_LEARN_CONTENT_AUDIT_v1_0.md — no P1 or P2 defects found. One P3 (naming inconsistency).

---

## 2026-04-12 | Sonnet | ALL | AuthButton email normalisation
- [FIX] AuthButton email normalisation | .trim().toLowerCase() added before sendMagicLink across 16 modules (29 call-sites). Prevents orphan accounts from whitespace/case mismatch. Branch: claude/normalize-authbutton-email-KRjlq
- [BUILD] Babel parse check (@babel/parser, jsx+flow plugins): **16/16 PASS** — dc-learn-000 through dc-learn-015

---

## 2026-04-14 | Sonnet | DC-TOOL-003 | Build — Redundancy Gap Tool
- [BUILD] /tools/ directory created — canonical location for DC-SCREEN tool suite
- [BUILD] DC-TOOL-003_v1_0_0.html built from DC-TOOL-000_v1_0_0.html factory template
- [BUILD] TOOL_ID = 'DC-TOOL-003', TOOL_VERSION = '1.0.0', TOOL_NAME = 'Redundancy Gap Tool'
- [BUILD] DOMAIN_PROMPT replaced — redundancy/topology screening prompt; RBD methodology; SPOF identification; Uptime Institute Tier Standard; SEAI 2026 emission factor (0.2241 kgCO₂/kWh); Irish facility norms (Clonshaugh reference)
- [BUILD] INPUT_SCHEMA replaced — 24 fields: facility identity, power supply (MIC, transformer, MSB, supply feeds), UPS & backup (UPS config, battery age, generators, fuel autonomy), cooling (type + redundancy), commercial (target tier, PPA, hall, floor area)
- [BUILD] SECTIONS replaced — 5 groups: Facility Identity, Power Supply, UPS & Backup, Cooling, Commercial
- [BUILD] LOADING_MESSAGES replaced — topology/SPOF/availability/cooling/gap-analysis sequence
- [BUILD] DEMO_DATA auto-derived from INPUT_SCHEMA demo values (Clonshaugh: 2.4MW IT, 400 racks, PUE 1.50, 5MVA MIC, N+1 UPS, 2 generators, 48hr autonomy)
- [BUILD] DEMO_DATA: explicit Clonshaugh object (2.4MW IT, 400 racks, PUE 1.50, 5MVA MIC, N+1 UPS, 2 generators, 48hr autonomy)
- [SWEEP] QG-2 stale value sweep: 0 matches for 83,050 | 0.295 | 63.50
- [SWEEP] QG-3 PI-safe sweep: 0 banned-term matches (excluding instruction text)
- [SWEEP] DC-TOOL-000 / Factory Template refs: 0 remaining
- [BUILD] Babel parse check (@babel/parser, jsx+flow plugins): **PASS** — DC-TOOL-003_v1_0_0.html
- [DECISION] No deviations from task scope — CSS, BSG architecture, tab structure, and JSON import/export inherited unchanged from factory template
- [DEPLOY] Branch: claude/build-redundancy-gap-tool-Xo2S1

---

## 2026-04-14 | Sonnet | DC-TOOL-004 | Build — Compliance Checker v1.0.0
- [BUILD] DC-TOOL-004_v1_0_0.html created from DC-TOOL-000_v1_0_0.html factory template
- [BUILD] /tools/ directory created in repo root
- [BUILD] TOOL_ID = 'DC-TOOL-004' — updated in all 4 version points (title, BSG L1, spec comment, const)
- [BUILD] TOOL_NAME = 'Compliance Checker' — replaced 'Factory Template — Facility Screener'
- [BUILD] BSG Layer 1 (window.onerror) updated: 'DC-TOOL-004 v1.0.0 — Blank Screen Guard'
- [BUILD] BSG Layer 2 (ErrorBoundary) updated: 'DC-TOOL-004 v1.0.0 — Error Boundary'
- [BUILD] DOMAIN_PROMPT: full compliance analyst prompt — EU Taxonomy, EED 2023/1791, CRU/2025236, F-Gas 2024/573, ASHRAE TC 9.9, EN 50600-4-2, EN 50600-2-3, HSA Legionella, SFDR
- [BUILD] INPUT_SCHEMA: 19 fields across Facility Identity, Energy & Efficiency, Cooling & Refrigerants, Water, Renewables & Carbon, Reporting & Compliance
- [BUILD] SECTIONS: 6 sections matching INPUT_SCHEMA (replaced 5-section Power/Cooling template)
- [BUILD] LOADING_MESSAGES: 5 compliance-specific messages (EU Taxonomy, CRU, F-Gas, carbon, EED)
- [BUILD] DEMO_DATA: auto-derived from INPUT_SCHEMA demo values (Clonshaugh DC, Dublin 17, 2013, 2.4 MW, 400 racks, PUE 1.50, DX CRAC, no free cooling, R410A, 192 kg, 45% renewable, EED not started)
- [SWEEP] Stale value sweep (QG-2): 0 matches — mic_kva, voltage_kv, redundancy_level, hall_config all removed
- [SWEEP] PI-safe sweep (QG-3): 0 output-side violations — Stranding Year and compliant references are instruction-only (inside DOMAIN_PROMPT rules)
- [BUILD] Babel check: PASS (1 block, @babel/parser jsx+flow)
- [DECISION] Primary persona: Sarah (ESG Analyst) — per DC-TOOL-004 spec
- [DECISION] OUTPUT_FORMAT includes 7 findings areas: EU Taxonomy PUE, CRU Renewables, EED Reporting, F-Gas, Carbon Cost, CRREM, Free Cooling
- [COMMIT] Branch: claude/build-compliance-checker-HaNNQ | tools/DC-TOOL-004_v1_0_0.html

---

## 2026-04-14 | Sonnet | DC-TOOL-006 | Build — Grid Headroom Calculator v1.0.0
- [BUILD] DC-TOOL-006_v1_0_0.html created from DC-TOOL-000_v1_0_0.html factory template
- [BUILD] TOOL_ID = 'DC-TOOL-006' — updated in all 4 version points (title, BSG L1, spec comment, const)
- [BUILD] TOOL_NAME = 'Grid Headroom Calculator' — replaced 'Factory Template — Facility Screener'
- [BUILD] BSG Layer 1 (window.onerror) updated: 'DC-TOOL-006 v1.0.0 — Blank Screen Guard'
- [BUILD] BSG Layer 2 (ErrorBoundary) updated: 'DC-TOOL-006 v1.0.0 — Error Boundary'
- [BUILD] DOMAIN_PROMPT: grid connection specialist — EirGrid TCP, ESB Networks MIC/MV/HV, SNSP, ECP-1/ECP-2, generation licence, CRM revenue, queue timeline 4–8 years
- [BUILD] INPUT_SCHEMA: 19 fields across Facility Identity, Load Profile, Grid Connection, On-Site Generation, Expansion Planning, Commercial
- [BUILD] SECTIONS: 6 sections — Facility Identity, Load Profile, Grid Connection, On-Site Generation, Expansion Planning, Commercial
- [BUILD] LOADING_MESSAGES: 5 grid-specific messages — MIC utilisation, headroom, voltage adequacy, generation licence, connection timeline
- [BUILD] CANONICAL_DATA: updated to grid tool — dc_grid_share 22% (CRU 2024 T1), queue_timeline 4–8 yrs (EirGrid TCP T2), gen_licence_thresh 10 MW (CRU T1), queue_total_gw 2.1 GW (EirGrid T2)
- [BUILD] DEMO_DATA: auto-derived — Clonshaugh DC, Dublin 17, 2013, 2.4 MW IT, PUE 1.50, 5000 kVA MIC, 10 kV supply, 1 feed, 2 generators 2 MW each, 4 MW total gen, 45% renewable
- [SWEEP] Stale value sweep (QG-2): 0 stale DC-TOOL-000 references, 0 Factory Template references
- [SWEEP] PI-safe sweep (QG-3): 0 output-side violations — 'should' and 'must' in caveat_box UI text only (not AI output), 'must' in DOMAIN_PROMPT instruction rules only
- [BUILD] Babel check: PASS — no JSX structure modified, all React component structure inherited from template
- [DECISION] Primary persona: Ann (Fund Manager) — per DC-TOOL-006 spec
- [DECISION] OUTPUT_FORMAT: 7 assessment areas — MIC Utilisation, Grid Headroom, Connection Voltage, Planning Risk, Generation Licence, CRM Revenue, Expansion Timeline
- [COMMIT] Branch: main | tools/DC-TOOL-006_v1_0_0.html

---

## 2026-04-14 | Sonnet | DC-TOOL-005 | Build — UPS Adequacy Tool v1.0.0
- [BUILD] DC-TOOL-005_v1_0_0.html created from DC-TOOL-004_v1_0_0.html (inherits factory CSS, BSG, tab architecture)
- [BUILD] TOOL_ID = 'DC-TOOL-005' — updated in all 4 version points (title, BSG L1, spec comment, const)
- [BUILD] TOOL_NAME = 'UPS Adequacy Tool'
- [BUILD] BSG Layer 1 (window.onerror): 'DC-TOOL-005 v1.0.0 — Blank Screen Guard'
- [BUILD] BSG Layer 2 (ErrorBoundary): 'DC-TOOL-005 v1.0.0 — Error Boundary'
- [BUILD] DOMAIN_PROMPT: UPS/backup power assessment — topology, battery tech, bridge time, generator start sequence, fuel autonomy, EPA/MCPD, carbon tax
- [BUILD] CANONICAL_DATA: 11 entries — grid_ef, carbon_tax_current, carbon_tax_2030, electricity_price, diesel_ef, gas_ef, epa_standby_limit, vrla_design_life, li_ion_design_life, diesel_sfc, gen_start_time
- [BUILD] INPUT_SCHEMA: 21 fields — Facility Identity (3), Load Profile (2), UPS System (4), Batteries (4), Generator Fleet (6), Commercial (1)
- [BUILD] SECTIONS: 6 sections — Facility Identity, Load Profile, UPS System, Batteries, Generator Fleet, Commercial
- [BUILD] LOADING_MESSAGES: 5 UPS-specific messages (UPS capacity, battery health, generator fleet, fuel autonomy, EPA/MCPD)
- [BUILD] DEMO_DATA: auto-derived from INPUT_SCHEMA demo values (Clonshaugh DC, 2.4 MW IT, PUE 1.50, 2× 1500 kVA online double-conversion N+1, VRLA 4yr, 2× 2000 kW diesel, 20,000 L tank, 200 hr/yr)
- [SWEEP] Stale value sweep: 0 matches — no DC-TOOL-004 or compliance-specific refs remaining
- [SWEEP] PI-safe sweep: 0 output-side violations (instruction-only text excluded)
- [BUILD] Primary persona: Mark (MEP Engineer) — per DC-TOOL-005 spec
- [BUILD] Findings areas: UPS Capacity, Battery Health, Generator Fleet, Fuel Chain, EPA/MCPD, Transfer Sequence
- [DECISION] No deviations from task scope — CSS, BSG, tab architecture, JSON import/export all inherited
- [COMMIT] Branch: main | tools/DC-TOOL-005_v1_0_0.html

---

## 2026-04-14 | Sonnet | DC-TOOL-007 | Build — Regulatory Gap Screener v1.0.0
- [BUILD] DC-TOOL-007_v1_0_0.html created from DC-TOOL-000_v1_0_0.html (inherits factory CSS, BSG, tab architecture)
- [BUILD] TOOL_ID = 'DC-TOOL-007' — updated in all 4 version points (title, BSG L1, spec comment, const)
- [BUILD] TOOL_NAME = 'Regulatory Gap Screener'
- [BUILD] BSG Layer 1 (window.onerror): 'DC-TOOL-007 v1.0.0 — Blank Screen Guard'
- [BUILD] BSG Layer 2 (ErrorBoundary): 'DC-TOOL-007 v1.0.0 — Error Boundary'
- [BUILD] DOMAIN_PROMPT: Expert regulatory analyst — covers EED Art.12/26, EPA/MCPD thermal threshold (50 MWth installed), EU Taxonomy PUE ≤1.3, F-Gas GWP/phase-down, CRREM Misalignment Year (LBE-derived pathway T3/T4), CRU 80% renewables, carbon cost trajectory
- [BUILD] CANONICAL_DATA in prompt: 10 entries — grid_ef (0.2241 kgCO₂/kWh), carbon_tax_current (€71), carbon_tax_2030 (€100), CRM_T4 (€149,960/MW/yr), electricity_price (€0.12/kWh), EU Taxonomy PUE threshold (≤1.3), CRU renewable obligation (80%), Dublin free cooling (7,200 hrs/yr), EPA IE Licence threshold (50 MWth), EPA standby limit (200 hrs/yr)
- [BUILD] INPUT_SCHEMA: 19 fields — Facility Identity (3), Energy Profile (4), Cooling & Refrigerants (3), Generators & EPA (5), Regulatory Status (2), Commercial (1)
- [BUILD] SECTIONS: 6 sections — Facility Identity, Energy Profile, Cooling & Refrigerants, Generators & EPA, Regulatory Status, Commercial
- [BUILD] LOADING_MESSAGES: 5 regulatory-specific messages (EED Art.12/26, EPA thermal, EU Taxonomy, F-Gas, CRREM)
- [BUILD] DEMO_DATA: auto-derived — Clonshaugh DC, 2013, 2.4 MW IT, 400 racks, PUE 1.50, 45% renewables, DX CRAC, R410A 192 kg, 2× 2000 kW diesel, 200 hrs/yr, EED not started, waste heat assessment no, no EPA licence, 1800 m²
- [SWEEP] QG-2 stale value sweep: 0 matches — rack_density_kw, mic_kva, voltage_kv, redundancy_level, hall_config all removed
- [SWEEP] QG-3 PI-safe sweep: 0 output-side violations — "Stranding Year" appears only in DOMAIN_PROMPT instruction (negative rule); all PI-safe elements present (indicative, Misalignment Year, LBE-derived disclosure, screening caveat)
- [SWEEP] Babel check: PASS — 1 text/babel block parsed clean (jsx + flow plugins)
- [DECISION] No deviations from task scope — CSS, BSG, tab architecture, JSON import/export all inherited unchanged
- [COMMIT] Branch: claude/build-regulatory-gap-screener-uHjDO | tools/DC-TOOL-007_v1_0_0.html
## 2026-04-14 | Sonnet | DC-TOOL-008 | Build — Fire Safety Screener v1.0.0
- [BUILD] DC-TOOL-008_v1_0_0.html created from DC-TOOL-000_v1_0_0.html factory template
- [BUILD] TOOL_ID = 'DC-TOOL-008' — updated in all 4 version points (title, BSG L1, spec comment, const)
- [BUILD] TOOL_NAME = 'Fire Safety Screener' — replaced 'Factory Template — Facility Screener'
- [BUILD] BSG Layer 1 (window.onerror): 'DC-TOOL-008 v1.0.0 — Blank Screen Guard'
- [BUILD] BSG Layer 2 (ErrorBoundary): 'DC-TOOL-008 v1.0.0 — Error Boundary'
- [BUILD] DOMAIN_PROMPT: fire safety engineer — VESDA, FM-200/Novec 1230, EN 15004, ISO 14520, IS 3218, BS 6266, NFPA 75/76, F-Gas Reg 2024/573, Li-ion thermal runaway, BESS compartmentation
- [BUILD] INPUT_SCHEMA: 17 fields — Facility Identity (3), IT Environment (3), Detection (2), Suppression (3), Battery & BESS (2), Commercial (1), plus hall_config and total_floor_m2
- [BUILD] SECTIONS: 6 sections — Facility Identity, IT Environment, Detection, Suppression, Battery & BESS, Commercial
- [BUILD] LOADING_MESSAGES: 5 fire safety messages (detection adequacy, suppression alignment, room integrity, Li-ion/BESS, gap analysis)
- [BUILD] CANONICAL_DATA: updated to fire safety domain — grid_ef (SEAI 2026 T1), electricity_price (CRU Q4 2024 T2), fm200_gwp 3220 (F-Gas T1), novec_gwp <1 (F-Gas T1), hold_time 10 min (EN 15004 T1), li_ion_risk thermal runaway (NFPA 75 T1)
- [SWEEP] Stale value sweep (QG-2): 0 matches — inputs.pue removed, CANONICAL_DATA updated to fire safety domain, all removed schema fields (pue, mic_kva, voltage_kv, cooling_type, redundancy_level, generator_fuel, generator_hours) purged
- [SWEEP] PI-safe sweep (QG-3): 0 output-side violations — 'compliant', 'should', 'must' references are instruction-only (inside DOMAIN_PROMPT rules)
- [BUILD] Babel check: PASS — JSX structure unchanged, all React component architecture inherited from template
- [DECISION] Primary persona: Mark (MEP Engineer) — fire protection engineering perspective
- [DECISION] OUTPUT_FORMAT: findings areas — Detection System, Suppression Agent, Room Integrity, Li-ion/BESS Risk, Sub-Floor Protection, Sprinkler Adequacy
- [COMMIT] Branch: claude/fire-safety-screener-iRNJN | tools/DC-TOOL-008_v1_0_0.html

---
## 2026-04-14 | Sonnet | DC-TOOL-012 | Build — Commissioning Readiness Tool v1.0.0
- [BUILD] DC-TOOL-012_v1_0_0.html created from DC-TOOL-000_v1_0_0.html factory template
- [BUILD] TOOL_ID = 'DC-TOOL-012' — updated in all 4 version points (title, BSG L1, spec comment, const)
- [BUILD] TOOL_NAME = 'Commissioning Readiness Tool' — replaced 'Factory Template — Facility Screener'
- [BUILD] BSG Layer 1 (window.onerror): 'DC-TOOL-012 v1.0.0 — Blank Screen Guard'
- [BUILD] BSG Layer 2 (ErrorBoundary): 'DC-TOOL-012 v1.0.0 — Error Boundary'
- [BUILD] DOMAIN_PROMPT: commissioning engineer — Cx Plan, CxA independence, FAT/SAT/IST, ATS transfer test, full-chain proving, PUE verification, O&M handover, ORR; CIBSE/RICS benchmark 2–5% M&E contract; electricity price €0.12/kWh (CRU Q4 2024 T2)
- [BUILD] INPUT_SCHEMA: 20 fields — Facility Identity (4), Commissioning Programme (2), Testing (5), Performance Verification (3), Handover (4), Commercial (1) — ppa_pct retained; old factory fields (rack_count, rack_density_kw, mic_kva, voltage_kv, cooling_type, redundancy_level, generator_fuel, generator_hours, hall_config, total_floor_m2) removed
- [BUILD] SECTIONS: 6 sections — Facility Identity, Commissioning Programme, Testing, Performance Verification, Handover, Commercial
- [BUILD] LOADING_MESSAGES: 5 commissioning messages (commissioning programme, FAT/SAT documentation, integrated systems testing, PUE verification, operational readiness)
- [BUILD] buildUserPrompt: updated framing to commissioning readiness; findings cover all 7 commissioning phases (Cx Plan, FAT, SAT, IST, PUE verification, O&M handover, operational readiness)
- [SWEEP] Stale value sweep (QG-2): 0 matches — all factory template fields and messages replaced
- [SWEEP] PI-safe sweep (QG-3): 0 output-side violations — 'should' in caveat boxes replaced with 'warrant validation'; 'compliant'/'must'/'should' in DOMAIN_PROMPT are instruction-only
- [BUILD] Babel check: PASS — JSX structure unchanged, all React component architecture inherited from template
- [DECISION] OUTPUT_FORMAT: findings areas — Cx Plan, FAT Documentation, SAT Completion, IST/Transfer Testing, PUE Verification, O&M Handover, Operational Readiness
- [COMMIT] Branch: claude/build-commissioning-tool-uxWAX | tools/DC-TOOL-012_v1_0_0.html

## 2026-04-14 | Sonnet | DC-TOOL-013 | Build — AI-Ready Cooling Screener v1.0.0
- [BUILD] DC-TOOL-013_v1_0_0.html created from DC-TOOL-000_v1_0_0.html factory template
- [BUILD] TOOL_ID = 'DC-TOOL-013' — updated in all 4 version points (title, BSG L1, spec comment, BSG L2)
- [BUILD] TOOL_NAME = 'AI-Ready Cooling Screener' — replaced 'Factory Template — Facility Screener'
- [BUILD] BSG Layer 1 (window.onerror): 'DC-TOOL-013 v1.0.0 — Blank Screen Guard'
- [BUILD] BSG Layer 2 (ErrorBoundary): 'DC-TOOL-013 v1.0.0 — Error Boundary'
- [BUILD] DOMAIN_PROMPT: liquid cooling retrofit specialist — DLC cold plates, immersion (single/two-phase), ASHRAE TC 9.9, OCP, EN 50600-2-3, NVIDIA DGX/HGX; physics of high density (water 3,500× air heat capacity); CDU architecture; Clonshaugh reference (400 racks, 6 kW/rack, 2.4 MW IT, PUE 1.50, target 40-rack AI pod at 40 kW/rack)
- [BUILD] INPUT_SCHEMA: 19 fields — Facility Identity (3: name, location, build_year), Current State (6: it_load_mw, rack_count, rack_density_kw, pue, cooling_type, has_containment), AI Workload Target (3: target_density_kw, target_rack_count, preferred_cooling), Infrastructure Constraints (5: chiller_capacity_kw, mic_kva, floor_type, ceiling_height_m, slab_load_kpa), Commercial (2: ppa_pct, total_floor_m2)
- [BUILD] SECTIONS: 5 sections — Facility Identity, Current State, AI Workload Target, Infrastructure Constraints, Commercial
- [BUILD] LOADING_MESSAGES: 5 cooling-specific messages — heat load at target density, cooling plant headroom, power distribution, structural constraints, retrofit roadmap
- [BUILD] DEMO_DATA: auto-derived from INPUT_SCHEMA demo values (Clonshaugh DC, Dublin 17, 2013, 2.4 MW IT, 400 racks, 6 kW/rack current, 40 kW/rack target, 40 target racks, PUE 1.50, DX CRAC, no containment, 2000 kW chiller, 5000 kVA MIC, raised floor, 3.0 m ceiling, 5 kPa slab, DLC preferred, 45% renewable, 1800 m²)
- [SWEEP] Stale value sweep (QG-2): 0 matches — DC-TOOL-000, Factory Template, old fields (voltage_kv, redundancy_level, generator_fuel, generator_hours, hall_config) all purged
- [SWEEP] PI-safe sweep (QG-3): 0 output-side violations — 'should'/'must' in UI caveat-box boilerplate only (inherited template); 'report' in tab labels only; DOMAIN_PROMPT instruction rules correctly scoped
- [BUILD] Babel check: PASS (@babel/parser, jsx+flow plugins)
- [DECISION] No deviations from task scope — CSS, BSG architecture, tab structure, JSON import/export inherited unchanged from factory template
- [DEPLOY] Branch: claude/build-cooling-screener-qw6Hd | tools/DC-TOOL-013_v1_0_0.html

---

## 2026-04-14 | Sonnet | DC-TOOL-010 | Build — Facility Audit Checklist v1.0.0
- [BUILD] DC-TOOL-010_v1_0_0.html created from DC-TOOL-000_v1_0_0.html factory template
- [BUILD] TOOL_ID = 'DC-TOOL-010' — updated in all 4 version points (title tag, BSG L1 window.onerror, spec comment header, BSG L2 ErrorBoundary)
- [BUILD] TOOL_NAME = 'Facility Audit Checklist' — replaced 'Factory Template'
- [BUILD] BSG Layer 1 (window.onerror): 'DC-TOOL-010 v1.0.0 — Blank Screen Guard'
- [BUILD] BSG Layer 2 (ErrorBoundary): 'DC-TOOL-010 v1.0.0 — Error Boundary'
- [BUILD] DOMAIN_PROMPT: expert data centre engineer conducting screening-level facility walkthrough in Ireland for LBE; covers full anatomy (power chain utility→rack, cooling chain server→atmosphere, redundancy topology, fire safety, physical security EN 50600-2-5, BMS/EPMS, environmental PUE/F-Gas/water, compliance CRU/EED/EU Taxonomy/EPA, commercial); canonical data locked (SEAI 2026 0.2241 kgCO₂/kWh, carbon tax €71/tCO₂, CRM T-4 €149,960/MW/yr, electricity €0.12/kWh, EU Taxonomy PUE ≤1.3, CRU 80% renewable, Dublin free cooling 7,200 hrs/yr); 8-system walkthrough; PI-safe output rules
- [BUILD] INPUT_SCHEMA: 19 fields — Facility Identity (3: facility_name, location, build_year), Power & IT (5: it_load_mw, rack_count, rack_density_kw, mic_kva, voltage_kv), Cooling (2: pue, cooling_type), Redundancy & Backup (3: redundancy_level, generator_fuel, generator_hours), Fire Safety (2: detection_type, suppression_type), Commercial & ESG (4: ppa_pct, hall_config, total_floor_m2) — total 19 fields, IDs match DC-Screen MSTR-001 shared standard
- [BUILD] SECTIONS: 6 sections — Facility Identity, Power & IT, Cooling, Redundancy & Backup, Fire Safety, Commercial & ESG
- [BUILD] LOADING_MESSAGES: 5 facility-audit-specific messages — power chain utility to rack, cooling chain adequacy, redundancy and resilience, fire safety and security, facility condition profile
- [BUILD] DEMO_DATA: auto-derived from INPUT_SCHEMA demo values (Clonshaugh DC, Dublin 17, 2013, 2.4 MW IT, 400 racks, 6 kW/rack, PUE 1.50, 5000 kVA MIC, 10 kV, DX CRAC, N+1, diesel, 200 hrs/yr, 45% renewable, Hall A/B, 1800 m²)
- [SWEEP] Stale value sweep (QG-2): 0 matches — DC-TOOL-000 and 'Factory Template' purged from all 4 version points
- [SWEEP] PI-safe sweep (QG-3): 0 output-side violations — language rules enforced in DOMAIN_PROMPT; 'should'/'must' in UI caveat-box boilerplate only (inherited template)
- [BUILD] Babel check: PASS
- [NOTE] Primary intake tool — JSON export feeds DC-Screen MSTR-001; field IDs verified against shared standard
- [DECISION] No deviations from task scope
- [DEPLOY] Branch: claude/facility-audit-checklist-HUcGi | tools/DC-TOOL-010_v1_0_0.html

---

## 2026-04-14 | Sonnet | DC-TOOL-001 | Build — Power Chain Screener v1.0.0
- [BUILD] DC-TOOL-001_v1_0_0.html created from DC-TOOL-000_v1_0_0.html factory template
- [BUILD] TOOL_ID = 'DC-TOOL-001' — updated in all 4 version points (title tag, BSG L1 window.onerror, spec comment header, BSG L2 ErrorBoundary)
- [BUILD] TOOL_NAME = 'Power Chain Screener' — replaced 'Factory Template — Facility Screener'
- [BUILD] BSG Layer 1 (window.onerror): 'DC-TOOL-001 v1.0.0 — Blank Screen Guard'
- [BUILD] BSG Layer 2 (ErrorBoundary): 'DC-TOOL-001 v1.0.0 — Error Boundary'
- [BUILD] DOMAIN_PROMPT: expert data centre electrical engineer — full power chain utility→rack; MIC/ESB Networks, HV/MV transformers (oil-immersed/cast-resin, K-factor), LV MSB (single bus/split bus, fault level, STS), UPS (online double-conversion, modular), PDU (floor/busway, intelligent metering); standards EN 50600-2-2, IEC 62040-3, IS 10101, IEEE 493; canonical data SEAI 2026 0.2241 kgCO₂/kWh, carbon tax €71/tCO₂, electricity €0.12/kWh, CRM T-4 €149,960/MW/yr
- [BUILD] INPUT_SCHEMA: 19 fields — Facility Identity (3: facility_name, location, build_year), Grid Connection (5: it_load_mw, pue, mic_kva, voltage_kv, supply_feeds), Transformers & Switchgear (3: transformer_config, transformer_age, msb_config), UPS (4: ups_count, ups_capacity_kva, ups_topology, redundancy_level), Distribution & Racks (3: pdu_type, rack_count, rack_density_kw), Commercial (1: ppa_pct)
- [BUILD] SECTIONS: 6 sections — Facility Identity, Grid Connection, Transformers & Switchgear, UPS, Distribution & Racks, Commercial
- [BUILD] LOADING_MESSAGES: 5 power-chain-specific messages (grid/MIC, transformer, UPS, distribution, risk profile)
- [BUILD] DEMO_DATA: auto-derived — Clonshaugh DC, Dublin 17, 2013, 2.4 MW IT, PUE 1.50, 5000 kVA MIC, 10 kV, 1 supply feed, 2 × 2MVA transformer, 12 yr age, 3200A single bus MSB, 2× 1500 kVA UPS (online double), N+1, floor PDU, 400 racks, 6 kW/rack, 45% renewable
- [SWEEP] QG-2 stale value sweep: 0 matches — DC-TOOL-000, Factory Template, cooling_type, generator_fuel, generator_hours, hall_config, total_floor_m2 all purged
- [SWEEP] QG-3 PI-safe sweep: 0 output-side violations — 'should'/'must' in DOMAIN_PROMPT instruction rules and UI caveat-box boilerplate only (inherited template); all PI-safe elements present (indicative, screening-level, LBE disclosure)
- [BUILD] Babel check: PASS — brace balance 523:523, JSX structure unchanged, all React component architecture inherited from template
- [DECISION] No deviations from task scope — CSS, BSG architecture, tab structure, JSON import/export all inherited unchanged
- [COMMIT] Branch: claude/build-power-chain-screener-Xzf4L | tools/DC-TOOL-001_v1_0_0.html
## 2026-04-14 | Sonnet | DC-TOOL-002 | Build — Cooling Chain Screener v1.0.0
- [BUILD] DC-TOOL-002_v1_0_0.html created from DC-TOOL-000_v1_0_0.html factory template
- [BUILD] TOOL_ID = 'DC-TOOL-002' — updated in all 4 version points (title, BSG L1, spec comment, const)
- [BUILD] TOOL_NAME = 'Cooling Chain Screener' — replaced 'Factory Template — Facility Screener'
- [BUILD] BSG Layer 1 (window.onerror): 'DC-TOOL-002 v1.0.0 — Blank Screen Guard'
- [BUILD] BSG Layer 2 (ErrorBoundary): 'DC-TOOL-002 v1.0.0 — Error Boundary'
- [BUILD] DOMAIN_PROMPT: cooling chain expert — server→rack→room→plant→atmosphere; ASHRAE TC 9.9 A1–A4 thermal envelope; CRAC vs CRAH; free cooling (7,200 hrs/yr Dublin); adiabatic cooling; chiller COP; cooling towers (Legionella); F-Gas 2024/573 phase-down; EN 50600-2-3; CIBSE Guide B2; HSA Legionella
- [BUILD] CANONICAL_DATA: grid_ef 0.2241 kgCO₂/kWh (SEAI 2026 T1), carbon_tax €71/tCO₂ (Budget 2025 T1), electricity_price €0.12/kWh (CRU Q4 2024 T2), EU Taxonomy PUE ≤1.3 (T1), Dublin free cooling 7,200 hrs/yr (Met Éireann T1)
- [BUILD] INPUT_SCHEMA: 19 fields — Facility Identity (3), IT Load (4: it_load_mw, rack_count, rack_density_kw, pue), Room Cooling (4: cooling_type, has_free_cooling, has_containment, supply_temp_c), Plant (3: chiller_count, chiller_kw_each, chiller_type), Refrigerants & Water (3: refrigerant_type, refrigerant_charge_kg, has_water_meter), Commercial (2: ppa_pct, total_floor_m2)
- [BUILD] SECTIONS: 6 sections — Facility Identity, IT Load, Room Cooling, Plant, Refrigerants & Water, Commercial
- [BUILD] LOADING_MESSAGES: 5 cooling-specific messages — airflow/containment, free cooling potential, chiller plant capacity, F-Gas exposure, cooling chain risk profile
- [BUILD] DEMO_DATA: auto-derived from INPUT_SCHEMA demo values (Clonshaugh DC, Dublin 17, 2013, 2.4 MW IT, 400 racks, 6 kW/rack, PUE 1.50, DX CRAC, no free cooling, no containment, 18°C supply, 3 chillers × 500 kW, air-cooled, R410A 192 kg, no water meter, 45% renewable, 1800 m²)
- [SWEEP] Stale value sweep (QG-2): 0 matches — DC-TOOL-000, Factory Template, mic_kva, voltage_kv, redundancy_level, generator_fuel, generator_hours, hall_config all purged
- [SWEEP] PI-safe sweep (QG-3): 0 output-side violations — 'should'/'must' in UI caveat-box boilerplate only (inherited template); DOMAIN_PROMPT instruction rules correctly scoped
- [BUILD] Babel check: PASS (1 text/babel block, @babel/parser jsx+flow)
- [DECISION] No deviations from task scope — CSS, BSG architecture, tab structure, JSON import/export inherited unchanged from factory template
- [DEPLOY] Branch: claude/setup-cooling-chain-screener-QwRVQ | tools/DC-TOOL-002_v1_0_0.html

---

## 2026-04-14 | Sonnet 4.6 | DC-TOOL-014 | Build CRU Readiness Screener
- [BUILD] tools/DC-TOOL-014_v1_0_0.html created from DC-TOOL-000 factory template
- [BUILD] TOOL_ID: DC-TOOL-014 | TOOL_VERSION: 1.0.0 | TOOL_NAME: CRU Readiness Screener
- [BUILD] 4 static version reference points updated: title, BSG guard, script header comment, ErrorBoundary
- [BUILD] DOMAIN_PROMPT: CRU/2025236 specialist — three pillars (grid security, 80% renewable, reporting), tier classification (de minimis / autoproducer 1–10 MVA / full 10 MVA+), MIC policy, CRM T-4 revenue, PPA/GOs/solar procurement, carbon trajectory
- [BUILD] CANONICAL_DATA: grid_ef 0.2241 kgCO₂/kWh (SEAI 2026 T1), carbon_tax_current €71/tCO₂ (T1), carbon_tax_2030 €100/tCO₂ (T1), crm_t4 €149,960/MW/yr (SEMO PCAR2829T-4 T1), electricity_price €0.12/kWh (T2), cru_renewable 80% (CRU/2025236 T1), free_cooling 7200 hrs/yr (T1)
- [BUILD] INPUT_SCHEMA: 18 fields — facility_name, location, build_year, it_load_mw, pue, mic_kva, ppa_pct, ppa_type (5 options), generator_count, generator_kw_each, generator_fuel (4 options), has_bess (3 options), bess_mw, expansion_planned, planned_it_mw, crm_participating (3 options), rack_count, total_floor_m2
- [BUILD] SECTIONS: 5 sections — Facility Identity, Energy Profile, Renewables, On-Site Generation, Expansion & CRM
- [BUILD] LOADING_MESSAGES: 5 CRU-specific messages — Classifying CRU tier, Calculating renewable energy gap, Assessing on-site generation potential, Modelling CRM revenue opportunity, Evaluating grid expansion risk
- [BUILD] DEMO_DATA: auto-derived from INPUT_SCHEMA demo values (Clonshaugh DC, Dublin 17, 2013, 2.4 MW IT, PUE 1.50, MIC 5000 kVA, 45% renewable, grid average, 2 generators × 2000 kW diesel, no BESS, no expansion, no CRM, 400 racks, 1800 m²)
- [SWEEP] Stale value sweep (QG-2): 0 matches — DC-TOOL-000, Factory Template, rack_density_kw, voltage_kv, cooling_type, redundancy_level, generator_hours, hall_config all purged
- [SWEEP] PI-safe sweep (QG-3): 0 output-side violations — 'compliant'/'CRU Compliance' appear only inside DOMAIN_PROMPT LANGUAGE RULES (instructing AI not to use them); no UI-side violations
- [BUILD] Babel check: PASS — 1 text/babel block, 522/522 brace balance, 28 backticks (even), all new field IDs and constants verified
- [DECISION] No deviations from task scope — CSS, BSG architecture, tab structure, JSON import/export, PERSONAS, CANONICAL_DATA inherited unchanged from factory template
- [DEPLOY] Branch: claude/build-cru-screener-XPxB4 | tools/DC-TOOL-014_v1_0_0.html
## 2026-04-14 | Sonnet | DC-TOOL-011 | Build — Security Assessment Tool v1.0.0
- [BUILD] DC-TOOL-011_v1_0_0.html created from DC-TOOL-000_v1_0_0.html factory template
- [BUILD] TOOL_ID = 'DC-TOOL-011' — updated in all 4 version points (title, BSG L1, spec comment, const)
- [BUILD] TOOL_NAME = 'Security Assessment Tool' — replaced 'Factory Template — Facility Screener'
- [BUILD] BSG Layer 1 (window.onerror): 'DC-TOOL-011 v1.0.0 — Blank Screen Guard'
- [BUILD] BSG Layer 2 (ErrorBoundary): 'DC-TOOL-011 v1.0.0 — Error Boundary'
- [BUILD] DOMAIN_PROMPT: physical security consultant — EN 50600-2-5 zones (1–4) and protection classes (1–4); HVM (PAS 68/IWA 14-1 bollards/barriers); PIDS (fence sensors, CCTV analytics); mantrap/airlock; biometric; anti-passback; NIS2 Directive (EU) 2022/2555 essential entity obligations; 24/7 SOC; CCTV retention 90 days; visitor management
- [BUILD] INPUT_SCHEMA: 18 fields — Facility Identity (5: facility_name, location, build_year, it_load_mw, rack_count), Target Standard (1: target_protection_class), Perimeter Zone 1 (5: fence_type, fence_height_m, has_anticlimb, has_hvm, has_pids), Building & Data Hall Access Zones 2–4 (3: building_entry, datahall_entry, visitor_policy), Surveillance (3: cctv_coverage, cctv_retention_days, has_soc), Commercial (1: ppa_pct)
- [BUILD] SECTIONS: 6 sections — Facility Identity, Target Standard, Perimeter (Zone 1), Building & Data Hall Access (Zones 2–4), Surveillance, Commercial
- [BUILD] LOADING_MESSAGES: 5 security-specific messages — perimeter, access control, CCTV, NIS2 alignment, security gap profile
- [BUILD] DEMO_DATA: auto-derived from INPUT_SCHEMA demo values — Clonshaugh DC, Dublin 17, 2013, 2.4 MW IT, Class 2, steel palisade 2.4m, no anti-climb, no HVM, no PIDS, card entry (building + data hall), partial CCTV, 30 days retention, no SOC, log book visitor policy, 400 racks, 45% renewable
- [SWEEP] QG-2 stale value sweep: 0 matches — DC-TOOL-000, Factory Template, cooling_type, generator_fuel, generator_hours, hall_config, total_floor_m2, rack_density_kw, mic_kva, voltage_kv, redundancy_level all purged; inputs.pue replaced with inputs.target_protection_class in report header
- [SWEEP] QG-3 PI-safe sweep: 0 output-side violations — 'should'/'must' in DOMAIN_PROMPT instruction rules and UI caveat-box boilerplate only (inherited template); all PI-safe elements present (indicative, screening-level, LBE disclosure)
- [BUILD] Babel check: PASS — 1 text/babel block, @babel/parser jsx+flow, brace balance verified
- [DECISION] No deviations from task scope — CSS, BSG architecture, tab structure, JSON import/export inherited unchanged from factory template
- [COMMIT] Branch: claude/setup-security-tool-nBZST | tools/DC-TOOL-011_v1_0_0.html

---

---

## 2026-04-14 | Sonnet 4.6 | DC-AI-001 | Defect fixes v4.0.1
- [DEFECT-1] Assessment option colours: `.assess-option` used `var(--surface)` — same as enclosing `.card` container — making option boxes invisible/flat. Fixed: changed to `var(--panel)` background; hover gains `var(--surface)` lift. Matches DC-LEARN-002 assessment styling.
- [DEFECT-2] Field Challenges persona filter: `PERSONA_FILTERS` used narrative keys (conor/helena/eoin/rachel/padraig) and filtered on non-existent `l.scenario.whoShouldCare`, returning "0 of 9 challenges". Fixed: updated to DC-AI rhetoric takeaway keys (asset_management/technology/technical/compliance/cost); filter condition checks `RHETORIC_TAKEAWAYS[l.id][filterPersona]`.
- [BUILD] DC-AI-001_v4_0_0.html patched in-place (9 lines changed).
- [DEPLOY] Branch: claude/fix-assessment-colors-Bwlnj | commit 96cebe7

---

## 2026-04-14 | Sonnet 4.6 | DC-TOOL-004 v2.0.0 | Build — Compliance Checker
- [BUILD] tools/DC-TOOL-004_v2_0_0.html — copied from DC-TOOL-000_v2_0_0.html factory template; all engines replaced for compliance-specific use case
- [BUILD] TOOL_ID: DC-TOOL-004 | TOOL_NAME: Compliance Checker | TOOL_VERSION: 2.0.0 | All 4 version points updated (title tag, TOOL_VERSION const, BSG L1, BSG L2, ErrorBoundary)
- [BUILD] CALC_ENGINE: 22 deterministic calculations — facility_load_mw, annual_energy_mwh, it_energy_mwh, overhead_mwh, annual_energy_cost, pue_gap, taxonomy_aligned, overhead_cost_at_target, renewable_gap_pct, unmatched_mwh, co2_scope2, carbon_cost_now, carbon_cost_2030, carbon_escalation, carbon_10yr_incremental, fgas_co2eq, fgas_leak_check_freq, fgas_annual_leak_cost, wue, cooling_upgrade_min, cooling_upgrade_max, pue_payback_years
- [BUILD] FINDINGS_ENGINE: 6 rule-based findings — pue_taxonomy (EU Taxonomy Delegated Act 2021/2139), cru_renewable (CRU/2025236), carbon_trajectory (SEAI 2026; Finance Act), fgas_exposure (F-Gas Regulation EU 2024/573), eed_reporting (EED 2023/1791 Art 12), free_cooling (Met Éireann 30-yr; EN 50600-2-3)
- [BUILD] INPUT_SCHEMA: 19 fields — Facility Identity (3: facility_name, location, build_year), Energy & Efficiency (5: it_load_mw, rack_count, rack_density_kw, pue, pue_measurement), Cooling & Refrigerants (4: cooling_type, has_free_cooling, refrigerant_type, refrigerant_charge_kg), Water (2: has_water_meter, water_litres_yr), Renewables & Carbon (3: ppa_pct, generator_fuel, generator_hours), Reporting & Compliance (2: eed_reporting, total_floor_m2)
- [BUILD] SECTIONS: 6 sections matching INPUT_SCHEMA groups above
- [BUILD] INTERPRETATION_PROMPT: compliance-scoped — EU Taxonomy, CRU/2025236, EED 2023/1791, F-Gas (EU) 2024/573, CRREM, ASHRAE TC 9.9, EN 50600; DO NOT perform any arithmetic rule included
- [BUILD] LOADING_MESSAGES: 6 compliance-specific messages — energy profile, EU Taxonomy PUE, CRU renewable, F-Gas, carbon trajectory, AI interpretation
- [SWEEP] Stale value sweep: 0 matches — 83,050 | 0.295 | 63.50 purged
- [SWEEP] DC-TOOL-000 reference sweep: 0 matches — all replaced
- [SWEEP] Clonshaugh reference sweep: 0 matches
- [SWEEP] PI-safe sweep: 0 output-side violations — 'compliant'/'should'/'must' in INTERPRETATION_PROMPT instruction text only
- [BUILD] Babel check: PASS — brace depth 0, 53,534 chars, text/babel block valid
- [BUILD] CalculationsTab and ReportTab calc ID references updated (carbon_cost_current→carbon_cost_now, co2_tonnes→co2_scope2)
- [DECISION] WHY: v2.0 deterministic calc engine — LLM never calculates; numbers are JavaScript, narrative is AI
- [COMMIT] Branch: claude/copy-dc-tool-template-jTJoJ | commit bb1d070 | tools/DC-TOOL-004_v2_0_0.html

---
## 2026-04-16 — [DEPLOY] Repo consolidation (dc-screen → dc-learn-academy)

Session: Claude Code cloud (Sonnet)
Prompt: SCREEN_SITE_CC_PROMPT_v8_CLOUD.md (simplified consolidation)

Shipped:
- archive/dc-screen/ : full dc-screen contents preserved as read-only reference
- tools/pipeline/    : MSTR + CPS + RPT active here (Services-tier engine)

dc-learn-academy is now the single source of truth.

Deferred to later sessions:
- DC-TOOL-009 v2.0.0 commit (requires upload)
- screen/ v8 bundle staging (requires upload)
- Netlify + Cloudflare setup

Pending LM manual step:
- github.com/LM10-Maker/dc-screen → Settings → Archive repository (read-only)

Verdict: SHIP

---
## 2026-04-20 — DC-Screen P2: Pipeline Wiring [BUILD] [DEPLOY]

Session: Claude Code (claude/wire-dc-screen-pipeline-4SLAO)
Tasks completed: CPS v1.1.0 commit, MSTR JSON export (all 14 fields), CPS import wiring (zero manual re-entry), CPS-to-RPT wiring verified, Clonshaugh sample run, intake form

**MSTR → CPS schema:**
MSTR exports: project.{name,ref,county,build_year,hall_names}, it_load.{total_it_mw,rack_count,rack_density_kw}, design_criteria.{pue_target}, electrical.{utility_kv,ppa_pct,generator_hours,mic_mva,fuel}, cooling.{strategy}, screening.{current_pue,grid_operator,redundancy_level,lease_end_year}
CPS importJSON maps all of the above → inputs.{facilityName,itLoadMW,pue,coolingType,genFuel,genConfig,numRacks,rackDensity,ppaPercent,genHours,facilityAge,micMva,hallNames} ✓

**CPS → RPT schema:**
CPS exportJSON._aimep_lineage.tool_id = "DC-CPS-001" ✓ (validated by RPT processImport)
CPS inputs block → RPT inputs block: direct pass-through, all required fields present ✓

**Canonical values verified in DC-CPS-001 v1.1.0:**
- Grid EF: 0.2241 kgCO2/kWh (SEAI 2026) ✓
- Gas EF: 0.205 kgCO2/kWh (SEAI 2026) ✓
- Carbon tax current: €71/tCO2 (Budget 2025) ✓
- Carbon tax 2030: €100/tCO2 (Finance Act) ✓
- CRM T-4 clearing price: €149,960/MW/yr (SEMO PCAR2829T-4) ✓ — ADDED
- Electricity price: €0.12/kWh (CRU Q4 2024) ✓ — ADDED
- EU Taxonomy PUE: 1.30 (Delegated Act 2021/2139) ✓
- CRU renewable obligation: 80% (CRU/2025236) ✓
- Dublin free cooling hours: 7,200 hrs/yr (Met Éireann 30-yr) ✓ — ADDED

**Stale value sweep:** 0 matches — 83050 | 0.295 | 63.50 | 56 (as carbon tax) | 110 kV (Clonshaugh context) ✓

**Clonshaugh results (ppa=0%, diesel 200 hrs/yr, air CRAC, N+1, MIC 5 MVA, 10 kV ESB Networks):**
- CRREM misalignment year: 2027
- Carbon intensity: 336 kgCO2/MWh_IT (HIGH band, 300–400 range)
- Location CO2: 7,067 tCO2/yr | Generator CO2 (Scope 1): 521 tCO2/yr
- EU Taxonomy PUE: FAIL (1.50 vs 1.30)
- CRU 80% renewable: FAIL (0% PPA, 80% gap)
- Indicative retrofit cost range: €1.9M – €3.6M
- Indicative 10-yr cost of inaction: ~€3.4M (NPV foregone energy savings, no CRM)
- 10-yr NPV with CRM: +€3.16M | Without CRM: +€746k | Simple payback: 3.1 / 5.2 yrs
- Traffic-light: POWER=AMBER | COOLING=RED | REDUNDANCY=AMBER | REGULATORY=RED | CARBON=RED

**Intake form (screen.legacybe.ie):**
- 14 fields, Netlify forms (data-netlify="true", name=screening-intake), honeypot
- Required: facility_name, contact_email, location, build_year, it_load_mw, rack_count, rack_density_kw, pue, cooling_type, ppa_pct, voltage_kv, mic_kva, generator_fuel, generator_hours
- Confirmation: "Thank you. Your facility data has been received. We will send an invoice for the Screening Report (€3,500 plus VAT) and deliver your report within 5 working days."
- No Stripe. Invoice-based.

**Deviations:** None. No DC-LEARN modules touched. No Supabase auth/schema touched. No Stripe webhook touched.

Commits: a56f7ab | 1bd0870 | 670c977 | f58ac3d
Branch: claude/wire-dc-screen-pipeline-4SLAO

Verdict: SHIP

## [2026-04-20] DC-Screen Hero + RPT A+ Fix
[FIX] RPT: CEng MIEI → CEng MEI throughout
[FIX] RPT: CRREM LBE-derivation disclosure moved to Executive Summary page
[FIX] RPT: ROBUST badge → "Indicative: ROBUST" (PI-safe qualifier added)
[FIX] RPT: Stressed case grid EF corrected to 0.2241 (SEAI 2026 canonical)
[FIX] RPT: DC-S01 service code removed from client-facing CTA
[FIX] screen/index.html: Calendly link wired to Talk to Les card
[FIX] screen/index.html: Screening Report card routes to intake form
[FIX] screen/index.html: Sample PDF link wired at page bottom
SHIP

## 2026-04-20 | DC-Screen | [DEPLOY]
Corrected screen/ folder: replaced v4.12 hero with v4.13, added
sample-screening-report.pdf and netlify.toml (missing from branch).
Merged claude/add-screen-deploy-files-YxtjV to main, branch deleted.
WHY: Branch had wrong hero version (no Calendly, old pricing). All 6
deploy files now correct on main. Netlify publish dir: screen/
Commit: 79b77e6
SHIP
