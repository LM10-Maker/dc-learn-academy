# dc-screen Repository — Archived

**Status:** READ-ONLY REFERENCE. Do not modify.
**Archived:** 16 April 2026
**Source:** github.com/LM10-Maker/dc-screen
**Reason:** Consolidated into dc-learn-academy (single source of truth).

## What moved where

| File(s) | Destination | Status |
|---------|-------------|--------|
| DC-MSTR-001, DC-CPS-001, DC-RPT-001 | `tools/pipeline/` | ACTIVE — Services-tier engine |
| DC-R-*.html (8 screeners) | `archive/dc-screen/` (here) | Superseded by DC-TOOL-001 to 014 |
| DC-DIAG-001, DC-SLD-001, DC-R-SUM-001 | `archive/dc-screen/` (here) | Internal support, no Factory rebuild |
| DC_*_v1_*.html (5 unregistered) | `archive/dc-screen/` (here) | Factory rebuilds exist for 2 (Grid, Regulatory) |
| DC_SCREEN_*.md docs | `archive/dc-screen/` (here) | Historic project docs |
| patch_rpt.py, verify_screen.py | `archive/dc-screen/` (here) | Build utilities — still usable if needed |

## Factory rebuilds — for reference

Cross-reference: `DC_TOOL_CONSOLIDATION_REPORT_v2_0.md` (repo root)

Gaps still open (no Factory rebuild yet):
- DC-R-ROI-001 Retrofit vs Rebuild   → planned DC-TOOL-015
- DC-R-FGS-001 F-Gas Phase-Down      → planned DC-TOOL-016
- DC-F-CST-001 Cost per MW Benchmark → planned DC-TOOL-017

## Source repo

`github.com/LM10-Maker/dc-screen` — to be set read-only on GitHub post-merge (manual LM step via Settings → Archive this repository).
