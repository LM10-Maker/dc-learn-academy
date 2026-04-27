# DC-SCREEN VERIFICATION SCRIPT — Claude Code Prompt
# Model: Sonnet | Repo: dc-learn-academy
# Date: 12 April 2026
# Scope: Build verify_screen.py — automated QA across all 20 DC-Screen tools

## CONTEXT
DC-LEARN has `verify_port.py` that runs 50+ automated checks across 16 modules
before anything ships. DC-Screen has 20 tools and ZERO automated verification.
Build the equivalent.

## TASK
Create `verify_screen.py` in the repo root. It scans every HTML file matching
`DC-*-001*.html` in the repo (CPS, RPT, DIAG, MSTR, ROI, SLD, SUM, etc.)
and runs the checks below. Output: PASS/FAIL per check per tool, summary at end.

## CHECKS TO IMPLEMENT

### S01 — Stale Canonical Values (FAIL = instant block)
Reject on sight — these values are wrong and must never appear:
- `83,050` or `83050` (old CRM — correct: 149,960)
- `0.295` (old grid EF — correct: 0.2241)
- `0.185` (old gas EF — correct: 0.205)
- `56` as carbon tax (correct: 71) — match `€56` or `EUR 56` patterns
- `63.50` or `63.5` as carbon tax
- `Les McGuinness` (correct: Les Murphy)

### S02 — Banned Terminology (FAIL = must fix before ship)
- `stranding` (anywhere — must be misalignment)
- `Stranding Year` (must be Misalignment Year)
- `compliance` when preceded by `CRU` (must be CRU Readiness)
- `DEAP` (residential only — must be NEAP for commercial)
- `exact` or `100% accurate` (must be indicative/screening-level)
- `quiz` (must be assessment)
- `Electrical Engineer` for Mark persona (must be MEP Engineer)
- `Hall 1` or `Hall 2` (must be Hall A / Hall B)
- `Aoife` or `Marcus` or `Síle` (retired personas)
- `Ballycoolin` (retired facility)

### S03 — CRREM Derivation Disclosure (FAIL = PI exposure)
Every file that references CRREM must contain at least one of:
- `LBE-derived`
- `derived by LBE`
- `not CRREM-published`
- `not published by CRREM`
If the file mentions `CRREM` but has none of these → FAIL

### S04 — Disclaimer Present (FAIL = PI exposure)
Every tool must contain either:
- `INDICATIVE SCREENING ASSESSMENT`
- `independent desktop screening`
- `not a certified energy audit`
- `not.*investment recommendation`
If none found → FAIL

### S05 — PI Statement Present
Every tool should contain:
- `Professional Indemnity` or `professional indemnity`
If absent → WARN (not blocking, but flag)

### S06 — Version Consistency
For each file, extract all version strings matching `DC-[A-Z]+-001 v[0-9.]+`
All instances must match. If mixed versions (e.g., v1.0.0 and v1.0.2) → FAIL

### S07 — Contact Email
If file contains an email address, it must be:
- `info@legacybe.ie` or `lmurphy@legacybe.ie`
NOT: `les@legacybe.ie` (wrong address)
If wrong email found → FAIL

### S08 — Unicode Escapes
Count literal `\uXXXX` escape sequences (not inside comments).
If count > 0 → WARN with count

### S09 — Clonshaugh Reference Consistency
If file contains `Clonshaugh`, check for consistent parameters:
- `2.4` (MW IT load)
- `1.50` or `1.5` (current PUE)
- `400` (racks)
- `5 MVA` or `5MVA` (MIC)
If Clonshaugh is mentioned but key params are inconsistent → WARN

### S10 — Source Tier Coverage
Count instances of T1, T2, T3, T4 tier markers.
If a file has calculations/data but zero tier markers → WARN
Report: `T1: N, T2: N, T3: N, T4: N`

### S11 — Intelligence Layer Language
Check that positioning language is correct:
- Should NOT contain: `we'll design`, `we will design`, `we deliver`, `install`, `specify`
  (in CTA or marketing text — not in engineering descriptions of actions)
- Should contain: `identify`, `quantify`, or `intelligence` (at least one)
If prescriptive delivery language found in CTA/marketing sections → WARN

### S12 — Current Canonical Values Present
For files containing calculations, verify correct values are used:
- Grid EF: `0.2241` — at least one instance
- Carbon tax: `71` — at least one instance
- CRM: `149960` or `149,960` — at least one instance (if CRM-relevant)
Report which canonical values are present/absent per file.

## OUTPUT FORMAT
```
DC-SCREEN VERIFICATION REPORT
Date: [timestamp]
Files scanned: [N]
═══════════════════════════════════════

DC-CPS-001_v1_0_2.html
  S01 Stale Values      PASS
  S02 Banned Terms      PASS
  S03 CRREM Disclosure   PASS
  S04 Disclaimer         PASS
  S05 PI Statement       PASS
  S06 Version Match      PASS
  S07 Contact Email      PASS
  S08 Unicode Escapes    WARN (12 instances)
  S09 Clonshaugh Params  PASS
  S10 Source Tiers       T1:4 T2:2 T3:1 T4:0
  S11 Intel Language     PASS
  S12 Canonical Values   Grid:✓ Tax:✓ CRM:✓

[repeat for each file]

═══════════════════════════════════════
SUMMARY
  PASS: 18/20 tools clean
  FAIL: 2 tools have blocking issues
  WARN: 5 tools have non-blocking flags

BLOCKING FAILURES:
  DC-DIAG-001: S08 Unicode (329 escapes)
  DC-SLD-001: S06 Version mismatch (v1.0.0 vs v1.0.1)

SHIP CONDITION: NOT MET — 2 blocking failures
```

## ALSO CREATE: DC_SCREEN_OPS_LOG.md
Same format as DC_LEARN_OPS_LOG.md. Tags: [FIX], [GNEW], [SWEEP], [BUILD],
[DEPLOY], [NOTSHIP], [BLOCKED], [DECISION]. First entry = this session.

## ALSO CREATE: DC_SCREEN_SWEEP_CHECKLIST_v1_0.md
Markdown file listing all 12 checks above with pass/fail criteria.
This becomes the reusable governance doc for all future sweep sessions.

## RUN IMMEDIATELY AFTER BUILDING
Execute `python3 verify_screen.py` against whatever DC-Screen tools exist
in the repo. Report results. Do NOT fix anything — report only.

Commit and push directly to main. Do NOT create feature branches.
