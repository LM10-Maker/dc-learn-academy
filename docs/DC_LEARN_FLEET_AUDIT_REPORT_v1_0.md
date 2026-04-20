# DC-LEARN Fleet Audit Report
# 10 April 2026
# Auditor: Claude Opus 4.6 | Branch: claude/audit-modules-quality-dUeF3

---

## SUMMARY

- Total defects found: **24**
- P1 (must fix before launch): **6**
- P2 (fix soon): **4**
- P3 (nice to have): **14**
- Known defects verified: D1 RESOLVED, D2 no narrative leak found, D3 RESOLVED, D4 RESOLVED

---

## P1 DEFECTS (must fix before launch)

| # | Module | Check | Line | Description | Fix Method |
|---|--------|-------|------|-------------|------------|
| 1 | 000 | 1C / 3A | 662–688 | Assessment answer-position bias: 20 of 27 correct answers at position 1 (74%). Learnable tell breaks assessment integrity. | Re-shuffle option order across all 27 questions to balance positions 0–3 (target 6–8 each). |
| 2 | 000 | 1B | 682 | Broken terminology replacement in Q000-21: `'CRU Readiness', not 'CRU Readiness'` — both sides identical. Should contrast with banned term `'CRU Compliance'`. Same bug in `explain:` field. | Replace second `'CRU Readiness'` with `'CRU Compliance'` in both `options[1]` and `explain`. |
| 3 | 007 | 1B | 468, 470, 473, 636, 708 | Systemic broken terminology replacement: `'Misalignment Year'` appears on BOTH sides of contrast sentences (5 locations). Should contrast new term with old banned term `'Stranding Year'`. Teaching point is destroyed. | Restore `'Stranding Year'` as the deprecated-term side of each contrast. 5 edits in one file. |
| 4 | 007 | 3B | 600 | Q007-19 grammar: options 0 (`Misalignment Year`) and 3 (`CRREM Misalignment Year`) are near-duplicates. Ambiguous distractor. | Replace option 0 with a genuinely wrong term (e.g. `Depreciation Year`). |
| 5 | 001 | 2 | — | Content depth: only 9 cause-and-effect pairs (target: 18+, i.e. 2 per level). | Add 1 additional C&E per level (9 new pairs). |
| 6 | 011 | 2 | — | Content depth: only 9 cause-and-effect pairs (target: 18+). | Add 1 additional C&E per level (9 new pairs). |

---

## P2 DEFECTS (fix soon)

| # | Module | Check | Line | Description | Fix Method |
|---|--------|-------|------|-------------|------------|
| 7 | 013 | 2 | — | Content depth: only 9 cause-and-effect pairs (target: 18+). | Add 1 additional C&E per level (9 new pairs). |
| 8 | 004 | 4 / manual | 447 | Truncated Declan L6 rhetoric: `"...to get compliant.d me ignoring it is not an option."` — fragment from prior edit. | Restore clean sentence (likely: `"...to get compliant. He told me ignoring it is not an option."`). |
| 9 | 004 | 4 / manual | 486 | Truncated Declan L7 rhetoric: `"...immediate payback.d me the servers could handle warmer air."` | Restore clean sentence. |
| 10 | 004 | 4 / manual | 525 | Truncated Declan L9 rhetoric: `"...funds the next.r into a plan the board would approve."` | Restore clean sentence. |

---

## P3 DEFECTS (nice to have)

| # | Module | Check | Line | Description | Fix Method |
|---|--------|-------|------|-------------|------------|
| 11 | 001 | 1E | 177 | Stale self-version in architecture comment: `v7.0.7` (current: `v7.4.6`) | Update comment. |
| 12 | 003 | 1E | 182 | Stale self-version in architecture comment: `v2.0.2` (current: `v2.4.7`) | Update comment. |
| 13 | 004 | 1E | ~177 | Stale self-version in architecture comment: `v6.0.6` (current: `v6.4.8`) | Update comment. |
| 14 | 006 | 1E | 184 | Stale self-version in architecture comment: `v6.7.2` (current: `v6.11.10`) | Update comment. |
| 15 | 008 | 1E | ~177 | Stale self-version in architecture comment: `v4.0.2` (current: `v4.4.8`) | Update comment. |
| 16 | 009 | 1E | ~177 | Stale self-version in architecture comment: `v4.0.3` (current: `v4.4.8`) | Update comment. |
| 17 | 010 | 1E | ~177 | Stale self-version in architecture comment: `v4.0.6` (current: `v4.4.7`) | Update comment. |
| 18 | 011 | 1E | 182 | Stale self-version in architecture comment: `v2.1.2` (current: `v2.5.8`) | Update comment. |
| 19 | 013 | 1E | ~177 | Stale self-version in architecture comment: `v3.0.2` (current: `v3.4.8`) | Update comment. |
| 20 | 015 | 1E | 180 | Stale self-version in architecture comment: `v2.0.4` (current: `v2.4.8`) | Update comment. |
| 21 | 010 | 1G | 1067 | Minor EED Art.26 wording: `"1 MW rated thermal input"` should be `"total rated energy input"`. Threshold value correct (1 MW). | Change `thermal` to `energy`. |
| 22 | 002 | 1C | 273, 503, 595, 641 | Mark prescriptive voice in rhetoricTakeaways: `"Design starts at..."`, `"Design for 12–14°C..."`, `"Specify open protocols..."`, `"Design the cooling chain..."` | Rewrite to diagnostic voice (check/verify/review). |
| 23 | 005 | 1C | 273 | Mark prescriptive voice: `"Calculate thermal input at concept design stage"` | Rewrite to diagnostic. |
| 24 | 013 | 1C | 287 | Mark prescriptive voice: `"Specify type test reports AND routine test certificates"` | Rewrite to diagnostic. |

---

## CLEAN CHECKS (no defects found)

| Check | Description | Result |
|-------|-------------|--------|
| 1A | Stale canonical values (83,050 / 0.295 / €63.50) | **CLEAN** — 0 matches across 16 modules. All substring hits verified as false positives (e.g. €567k, €56,000 PIDS calc). |
| 1D | Stale CRM value (83,050 / 83050) | **CLEAN** — 0 matches. |
| 1F | IS_FREE_MODULE flag | **CLEAN** — all 16 modules use identical runtime derivation: `(TOOL_ID === 'DC-LEARN-000' \|\| '001' \|\| '002')`. Free for 000–002, paid for 003–015. |
| 1G | EED Article 26 threshold | **CLEAN** — all references say "1 MW" (not "500 kW IT"). One minor wording variant flagged as P3 #21. |
| 1H | Service codes in content (DC-S01–S07) | **CLEAN** — 0 matches in any module. |
| 1I | "Scenario" terminology | **CLEAN** — 0 matches for `Scenario Preview`, `View full scenario`, `scenario-card`. |
| 1J | Hall naming (Hall 1 / Hall 2) | **CLEAN** — 0 Clonshaugh-specific Hall 1/2 references. One false positive in 013:472 (`"data hall 22°C"`). Hall A / Hall B used consistently. |
| 1E (titles) | Title vs TOOL_VERSION consistency | **CLEAN** — all 16 modules match between `<title>` tag, `TOOL_VERSION` const, fatal-error fallback, and React footer badge. |

---

## KNOWN DEFECT VERIFICATION

| # | Module | Defect | Status | Evidence |
|---|--------|--------|--------|----------|
| D1 | 001 | "TODO — Curate" in scenario titles | **RESOLVED** | `grep -i TODO dc-learn-001.html` returns 0 matches. |
| D2 | 004 | L6 scenario title narrative text leak | **NOT REPRODUCED** | L6 scenario title is `"The SEAI Letter"` — clean. However, 3 truncated rhetoric texts found nearby (P2 #8–10). |
| D3 | 004 | Only 8 scenarios (missing L9) | **RESOLVED** | `grep -c 'scenario:{' dc-learn-004.html` = 9. All levels present. |
| D4 | 001 | Tab active style wrong | **RESOLVED** | `.tab-btn.active` CSS in 001 matches canonical 002 exactly. |

---

## CONTENT DEPTH MATRIX

| Module | Version | Levels | clockQ | crossRef | C&E | FC | AssessQ | VG | Persona |
|--------|---------|--------|--------|----------|-----|----|---------|----|---------|
| 000 | 2.4.6 | 9 | 9 | 9 | 27 | 9 | 27 | 0 | 182 |
| 001 | 7.4.6 | 9 | 9 | 9 | **9** | 9 | 27 | 0 | 155 |
| 002 | 5.13.7 | 9 | 9 | 9 | 27 | 9 | 27 | 0 | 241 |
| 003 | 2.4.7 | 9 | 9 | 9 | 29 | 9 | 27 | 0 | 202 |
| 004 | 6.4.8 | 9 | 9 | 9 | 27 | 9 | 27 | 0 | 238 |
| 005 | 6.6.10 | 9 | 9 | 9 | 27 | 9 | 27 | 0 | 201 |
| 006 | 6.11.10 | 9 | 9 | 9 | 27 | 9 | 27 | 0 | 202 |
| 007 | 4.4.9 | 9 | 9 | 9 | 27 | 9 | 27 | 0 | 198 |
| 008 | 4.4.8 | 9 | 9 | 9 | 22 | 9 | 27 | 0 | 242 |
| 009 | 4.4.8 | 9 | 9 | 9 | 25 | 9 | 27 | 0 | 234 |
| 010 | 4.4.7 | 9 | 9 | 9 | 27 | 9 | 27 | 0 | 242 |
| 011 | 2.5.8 | 9 | 9 | 9 | **9** | 9 | 27 | 1 | 173 |
| 012 | 2.4.8 | 9 | 9 | 9 | 26 | 9 | 27 | 1 | 214 |
| 013 | 3.4.8 | 9 | 9 | 9 | **9** | 9 | 27 | 1 | 247 |
| 014 | 2.4.9 | 9 | 9 | 9 | 27 | 9 | 27 | 0 | 170 |
| 015 | 2.4.8 | 9 | 9 | 9 | 27 | 9 | 27 | 0 | 230 |

**Bold** = below target (C&E target: 18+). All other metrics meet or exceed targets.

---

## ASSESSMENT DISTRIBUTION MATRIX

Counts include `correct:N` in assessment arrays. Raw grep totals are 29 per module (27 assessment + 2 `useState({correct:0})` false positives in framework code — deduct 2 from Pos 0 for true assessment counts).

| Module | Pos 0 | Pos 1 | Pos 2 | Pos 3 | Bias? |
|--------|-------|-------|-------|-------|-------|
| 000 | 1 | **20** | 5 | 1 | **YES — P1. 74% at Pos 1.** |
| 001 | 8 | 6 | 7 | 6 | No |
| 002 | 6 | 8 | 6 | 7 | No |
| 003 | 7 | 5 | 7 | 8 | No |
| 004 | 7 | 6 | 7 | 7 | No |
| 005 | 6 | 8 | 7 | 6 | No |
| 006 | 7 | 7 | 7 | 6 | No |
| 007 | 7 | 7 | 7 | 6 | No |
| 008 | 7 | 7 | 7 | 6 | No |
| 009 | 6 | 8 | 6 | 7 | No |
| 010 | 7 | 7 | 7 | 6 | No |
| 011 | 7 | 7 | 7 | 6 | No |
| 012 | 6 | 8 | 7 | 6 | No |
| 013 | 7 | 7 | 7 | 6 | No |
| 014 | 7 | 6 | 8 | 6 | No |
| 015 | 7 | 8 | 6 | 6 | No |

Longest-answer bias: **Not detected.** Correct answers across all modules tend to be shorter/crisper than distractors — reverse pattern, no learnable tell.

---

## SUPABASE SCHEMA SNAPSHOT

Schema manually verified during Stage 5 deployment on 09/04/2026 (per OPS_LOG entry). Not re-verified from CC — no SQL editor access.

| Table | Purpose | RLS |
|-------|---------|-----|
| learner_progress | Per-module, per-level completion state | Users own data + admin bypass |
| learner_pathways | Recommended learning sequences | Users own data + admin bypass |
| learner_certificates | Issued certificate records | Users own data + admin bypass |
| learner_analytics | Timing/engagement telemetry (from PlatformSync) | Users own data + admin bypass |
| companies | Organisation records | Admin-only |
| licences | Stripe payment → access tier mapping | Service-role insert; client SELECT own rows |

Admin accounts confirmed: lmurphy@legacybe.ie, antomurph@hotmail.com, keithmurphy1983@gmail.com.

---

## MODULES RANKED BY LAUNCH READINESS

| Rank | Module | Version | P1 | P2 | P3 | Notes |
|------|--------|---------|----|----|----|----|
| 1 | 002 | 5.13.7 | 0 | 0 | 4 | Canonical template. Mark voice P3 only. |
| 2 | 003 | 2.4.7 | 0 | 0 | 1 | Clean. |
| 3 | 005 | 6.6.10 | 0 | 0 | 1 | Mark voice P3 only. |
| 4 | 006 | 6.11.10 | 0 | 0 | 1 | Clean. |
| 5 | 008 | 4.4.8 | 0 | 0 | 1 | C&E at 22 (above 18 threshold). |
| 6 | 009 | 4.4.8 | 0 | 0 | 1 | C&E at 25 (above 18 threshold). |
| 7 | 010 | 4.4.7 | 0 | 0 | 2 | Minor Art.26 wording. |
| 8 | 012 | 2.4.8 | 0 | 0 | 0 | Clean. |
| 9 | 014 | 2.4.9 | 0 | 0 | 0 | Clean. |
| 10 | 015 | 2.4.8 | 0 | 0 | 1 | Clean. |
| 11 | 001 | 7.4.6 | 1 | 0 | 1 | C&E depth gap. |
| 12 | 011 | 2.5.8 | 1 | 0 | 1 | C&E depth gap. |
| 13 | 013 | 3.4.8 | 0 | 1 | 2 | C&E depth gap (P2) + Mark voice. |
| 14 | 004 | 6.4.8 | 0 | 3 | 1 | 3 truncated rhetoric texts. |
| 15 | 007 | 4.4.9 | 2 | 0 | 0 | Systemic terminology replacement bug. |
| 16 | 000 | 2.4.6 | 2 | 0 | 0 | Assessment bias + terminology bug. |

---

## RECOMMENDED FIX SESSIONS

### Session A — Terminology Repair (000 + 007)
**Effort: ~30 min | Priority: P1**
- Fix 000:682 — restore `'CRU Compliance'` as the deprecated term in Q000-21 options + explain
- Fix 007:468, 470, 473, 636, 708 — restore `'Stranding Year'` as the deprecated term in all contrast sentences
- Fix 007:600 — replace near-duplicate distractor in Q007-19

### Session B — Assessment Rebalance (000)
**Effort: ~45 min | Priority: P1**
- Re-shuffle option positions across all 27 questions in dc-learn-000
- Target: 6–8 correct answers per position (0, 1, 2, 3)
- Verify no longest-answer bias introduced during shuffle

### Session C — Cause-and-Effect Depth (001, 011, 013)
**Effort: ~2 hrs | Priority: P1/P2**
- Add 9 new C&E pairs to each of 001, 011, 013 (1 additional per level)
- Follow existing format: `{cause:"...", effect:"...", insight:"..."}`
- Source content from existing grammar facts + rhetoric takeaways

### Session D — Text Corruption Repair (004)
**Effort: ~15 min | Priority: P2**
- Fix 3 truncated rhetoric texts at lines 447, 486, 525
- Restore clean sentence endings (fragments visible: `.d me`, `.r into`)

### Session E — Version Comment Hygiene (10 modules)
**Effort: ~20 min | Priority: P3**
- Update stale self-version in architecture comments across 001, 003, 004, 006, 008, 009, 010, 011, 013, 015
- Single sed/grep-replace per file

### Session F — Mark Voice Review (002, 005, 013)
**Effort: ~30 min | Priority: P3**
- Rewrite ~8 Mark rhetoricTakeaway lines from prescriptive to diagnostic voice
- Change "Design X" / "Specify Y" / "Calculate Z" to "Check X" / "Verify Y" / "Review Z"

---

## AUDIT METHODOLOGY

### Checks executed (all against base64-stripped copies in /tmp/dc-audit/)
1. **1A** Stale canonical values — grep `83,050|83050|€83|0.295|€56|€63.50`
2. **1B** Banned terminology — grep `Ballycoolin|Aoife|Marcus|Síle|Stranding Year|JTBD|DEAP|CRU Compliance|Les McGuinness|Electrical Engineer|Hall 1|Hall 2`
3. **1C** Mark prescriptive voice — grep `Mark.{0,40}(specif|design|prescrib|recommend|should install|must install|advises installing)`
4. **1D** Stale CRM value — grep `83,050|83050`
5. **1E** Version consistency — extract `<title>`, `TOOL_VERSION`, architecture comment, React footer per module
6. **1F** IS_FREE_MODULE flag — grep + verify logic
7. **1G** EED Article 26 threshold — grep `Article 26` + context verify
8. **1H** Service codes — grep `DC-S0[1-7]`
9. **1I** Scenario terminology — grep `Scenario Preview|View full scenario|scenario-card`
10. **1J** Hall naming — grep `Hall 1|Hall 2` + context verify
11. **Task 2** Content depth — count `clockQuote:`, `crossRefs:[`, `{cause:`, `scenario:{`, assessment Qs, persona refs
12. **Task 3A** Answer position distribution — count `correct:N` per module
13. **Task 3B** Longest answer bias — manual sample L1/L5/L9 grammar in 4 modules
14. **Task 4** Known defect verification — D1 through D4
15. **Task 5** Supabase schema snapshot — documented from OPS_LOG

### G-NEW rules applied
- **G-NEW-49**: Every grep match was read in context before classifying. False positives documented.
- **G-NEW-71**: Every finding checked across all 16 modules (e.g. truncation pattern in 004 checked fleet-wide — only 004 affected).
- **G-NEW-73**: Audit only. Zero code changes. Zero fixes applied.

---

*Report generated 10/04/2026. Audit session: claude/audit-modules-quality-dUeF3. Fix sessions to follow after LM review.*
