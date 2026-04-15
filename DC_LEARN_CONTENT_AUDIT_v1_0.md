# DC-LEARN Content Audit — clockQuotes, Visual Guide & Clock Chapters

**Date:** 2026-04-10
**Scope:** All 16 modules (dc-learn-000 through dc-learn-015)
**Type:** Audit only — no fixes applied

---

## OUTPUT 1: CLOCKQUOTE MATRIX

**Target:** 9 per module (1 per level), 144 across fleet.

| Module | Total clockQuotes | Missing levels |
|--------|:-:|----------------|
| 000 — Anatomy of a Data Centre | 9 | None |
| 001 — Data Centre Power Chain | 9 | None |
| 002 — Cooling Systems | 9 | None |
| 003 — Resilience & Redundancy | 9 | None |
| 004 — Energy Efficiency & PUE | 9 | None |
| 005 — Backup Power & Generators | 9 | None |
| 006 — Grid Connection & Capacity | 9 | None |
| 007 — Regulatory Landscape | 9 | None |
| 008 — F-Gas & Refrigerant Compliance | 9 | None |
| 009 — Monitoring & Measurement | 9 | None |
| 010 — Net Zero & Sustainability | 9 | None |
| 011 — Physical Security & Access Control | 9 | None |
| 012 — On-Site Energy & Revenue | 9 | None |
| 013 — Commissioning & Handover | 9 | None |
| 014 — High-Density & Liquid Cooling | 9 | None |
| 015 — Programme Close-Out | 9 | None |

**Fleet total: 144 clockQuotes (9 × 16). Target MET.**

All 16 modules render clockQuotes via conditional JSX (`{lvl.clockQuote && ( ... )}`). Rendering code confirmed present in all 16.

---

## OUTPUT 2: VISUAL GUIDE MATRIX

| Module | VisualGuideTab | ChainTab | Chain Overview function | DiagramWalkthrough | SVG count | Notes |
|--------|:-:|:-:|------------------------|:-:|:-:|-------|
| 000 | Yes | Yes | **NONE** | No | 2 | No chain overview diagram. Lowest SVG count in fleet. |
| 001 | Yes | Yes | `ChainOverview` | No | 6 | |
| 002 | Yes | Yes | `ChainOverview` | No | 6 | |
| 003 | Yes | Yes | `ChainOverview` | No | 5 | |
| 004 | Yes | Yes | `VGChainOverview` | No | 6 | Different naming convention from fleet standard |
| 005 | Yes | Yes | `ChainOverview` | No | 6 | |
| 006 | Yes | Yes | `VG_ChainOverview` | No | 6 | Different naming convention (underscore variant) |
| 007 | Yes | Yes | `VG_ChainOverview` | No | 6 | Different naming convention (underscore variant) |
| 008 | Yes | Yes | `ChainOverview` | No | 6 | |
| 009 | Yes | Yes | `ChainOverview` | No | 6 | |
| 010 | Yes | Yes | `ChainOverview` | No | 6 | |
| 011 | Yes | Yes | `ChainOverviewDiagram` | Yes | 6 | Extended variant with DiagramWalkthrough |
| 012 | Yes | Yes | `ChainOverviewDiagram` | Yes | 5 | Extended variant with DiagramWalkthrough |
| 013 | Yes | Yes | `ChainOverviewDiagram` | Yes | 5 | Extended variant with DiagramWalkthrough |
| 014 | Yes | Yes | `ChainOverview` | No | 5 | |
| 015 | Yes | Yes | `ChainOverview` | No | 5 | |

### Visual Guide observations

1. **VisualGuideTab + ChainTab: CLEAN** — all 16 modules have both.
2. **Chain Overview naming inconsistency (P3):**
   - Standard `ChainOverview`: 001, 002, 003, 005, 008, 009, 010, 014, 015 (9 modules)
   - Extended `ChainOverviewDiagram` + `DiagramWalkthrough`: 011, 012, 013 (3 modules)
   - Variant `VGChainOverview`: 004 (1 module)
   - Variant `VG_ChainOverview`: 006, 007 (2 modules)
   - **Missing entirely: 000** (1 module)
3. **Module 000 has no chain overview diagram** — only 2 SVGs vs fleet typical of 5–6. This is the introductory/anatomy module so may be intentional.
4. **SVG counts vary:** 000=2, 003/012/013/014/015=5, rest=6. Not necessarily a defect — different modules have different diagram needs.

---

## OUTPUT 3: DATA CENTRE CLOCK CHAPTERS

| Module | BookTab present? | External chapter file | Chapter file exists? | File size |
|--------|:-:|----------------------|:-:|----------:|
| 000 | Yes | `dc-clock-prologue.html` | Yes | 4,275 B |
| 001 | Yes | `dc-clock-ch01.html` | Yes | 14,471 B |
| 002 | Yes | `dc-clock-ch02.html` | Yes | 24,666 B |
| 003 | Yes | `dc-clock-ch03.html` | Yes | 27,495 B |
| 004 | Yes | `dc-clock-ch04.html` | Yes | 26,796 B |
| 005 | Yes | `dc-clock-ch05.html` | Yes | 27,994 B |
| 006 | Yes | `dc-clock-ch06.html` | Yes | 24,604 B |
| 007 | Yes | `dc-clock-ch07.html` | Yes | 28,084 B |
| 008 | Yes | `dc-clock-ch08.html` | Yes | 27,205 B |
| 009 | Yes | `dc-clock-ch09.html` | Yes | 28,602 B |
| 010 | Yes | `dc-clock-ch10.html` | Yes | 27,920 B |
| 011 | Yes | `dc-clock-ch11.html` | Yes | 25,099 B |
| 012 | Yes | `dc-clock-ch12.html` | Yes | 26,428 B |
| 013 | Yes | `dc-clock-ch13.html` | Yes | 27,222 B |
| 014 | Yes | `dc-clock-ch14.html` | Yes | 28,109 B |
| 015 | Yes | `dc-clock-ch15.html` | Yes | 29,234 B |

### Clock chapter observations

1. **BookTab: CLEAN** — present in all 16 modules.
2. **StoryTab: NOT PRESENT** — 0 matches in any module. Tab may have been renamed to BookTab.
3. **All 17 chapter files exist** — prologue + ch01 through ch15.
4. **Standalone book file exists:** `dc-clock-book.html` (497,567 B / ~486 KB) — likely the full compiled book.
5. **Chapter 01 is notably smaller** (14,471 B) than chapters 02–15 (24,604–29,234 B). May be intentional (shorter opening chapter) or incomplete content.
6. **Prologue is smallest** (4,275 B) — expected for an introductory piece.
7. **clockChapter keyword: 0 matches fleet-wide** — chapters are loaded via external HTML file reference, not inline data.

---

## SUMMARY

| Category | Status | Issues |
|----------|--------|--------|
| clockQuotes | **CLEAN** | 144/144 present. No missing levels. |
| VisualGuideTab | **CLEAN** | 16/16 present. |
| ChainTab | **CLEAN** | 16/16 present. |
| Chain Overview | **P3** | 4 naming variants across fleet. Module 000 has none. |
| BookTab | **CLEAN** | 16/16 present. All chapter files exist. |
| Chapter file sizes | **NOTE** | ch01 is 50% smaller than fleet average. Prologue is expected small. |

**No P1 or P2 defects found.**
