# DC-AI TEMPLATE STANDARD v1.0
# Definitive spec for DC-LEARN parity (or better)
# Every feature listed here goes into the template ONCE
# Then modules 2–8 inherit it automatically
# Deferred items are explicitly marked DEFER with reason
#
# Input: DC-AI-001_v1_1_0.html
# Output: DC-AI-001_v2_0_0.html (major version — template rewrite)
# This replaces DC_AI_POLISH_PASS_2_v1_0.md

---

## GAP ANALYSIS: DC-LEARN vs DC-AI

### MUST HAVE (include in v2.0.0 template)

| # | Feature | DC-LEARN | DC-AI v1.1.0 | Action |
|---|---------|----------|--------------|--------|
| 1 | Audience bar | Green mono text at top | Missing | ADD |
| 2 | Cascade Calculator | Right sidebar with inputs → bottleneck results | Missing | ADD |
| 3 | Facility Profile | Right sidebar panel with Clonshaugh params | Missing | ADD |
| 4 | Persona entry on Chain | "Viewing as X" with persona buttons + relevance map | Missing | ADD |
| 5 | CTA section | Two-column above footer: service CTA + feedback CTA | Single line text | REPLACE |
| 6 | Footer (2-tier) | Series nav row + copyright/links row | Single line | REPLACE |
| 7 | Clarify button | Toggle on each grammar fact | Missing | ADD |
| 8 | Field Challenge reveal | "Show the Fix" button, fix hidden by default | Fix shown inline | CHANGE |
| 9 | Progress tab | Overall %, per-level dots, assessment score | Missing tab | ADD |
| 10 | Assessment timer | Countdown/countup timer with display | No timer | ADD |
| 11 | Assessment score panel | Score + tier breakdown + "under time" badge | Basic score only | UPGRADE |
| 12 | Assessment filters | Filter by tier (Knowledge/Calc/Judgement) + level (L1–L9) | No filters | ADD |
| 13 | Assessment feedback | Green/red answer highlighting + explanation reveal | Basic correct/wrong | UPGRADE |
| 14 | Methodology card | Trivium Method, Feynman Clarify, Weakest Link explained | Missing | ADD |
| 15 | Tab styling | Pill-style buttons with border-radius, active=filled | Underline style | CHANGE to match |
| 16 | Glossary/Bib expandable | Collapsible sections with term count | Separate sub-tabs | KEEP (DC-AI approach is fine) |
| 17 | Series nav links | Prev/Next module links in footer | Text only | ADD links (disabled for module 1) |

### DEFER (not in v2.0.0 — separate workstream)

| Feature | Reason | When |
|---------|--------|------|
| Hero image | Needs Clonshaugh photo asset or generated visual | v2.1.0 or batch |
| Visual Guide tab | 4 SVG diagrams need individual Opus design sessions | v3.0.0 batch |
| The Story tab | No DC-AI companion narrative exists | Only if written |
| Sign in button | Supabase Stage 5 decision pending | After VAT/legal |
| Achievement Certificate | Needs design session | v2.1.0 |
| Clock quotes | Intentionally empty — no narrative | Only if written |
| Assessment clock face SVG | Nice-to-have, not essential | v2.1.0 |

---

## TEMPLATE ARCHITECTURE

### Tab structure (7 tabs):
```
Chain | Learn | Field Challenges | Assessment | Progress | Reference
```

**KEY CHANGE:** Merge Grammar + Logic + Rhetoric into a single "Learn"
tab with stage selector buttons (Grammar | Logic | Rhetoric) — matching
DC-LEARN's architecture. This is more intuitive and reduces tab count.

Current DC-AI: Chain | Grammar | Logic | Rhetoric | Field Challenge | Assessment | Reference (7 tabs, 3 are sub-tabs of Learn)

New DC-AI: Chain | Learn | Field Challenges | Assessment | Progress | Reference (6 tabs)

The Learn tab contains:
- Level header (icon, title, subtitle, retrofitRelevance)
- Stage buttons: [Grammar] [Logic] [Rhetoric] — same as DC-LEARN
- Grammar stage: 5 facts with Clarify toggle
- Logic stage: C&E pairs, Fundamental Constraint, Weakest Link
- Rhetoric stage: 5 persona cards with takeaways

This matches DC-LEARN exactly and makes the platform feel like one product family.

### Layout (2-column on desktop):

```
┌─────────────────────────────────────────────────────────┐
│ AUDIENCE BAR (green mono text)                          │
├──────────────────────────────────┬──────────────────────┤
│ Logo · Title · Subtitle          │ Module 1 of 8 · v2.0 │
├──────────────────────────────────┴──────────────────────┤
│ DC-AI-001 · POWER DENSITY                               │
│ Can This Facility Handle AI Workloads?                  │
│ Fictional reference facility...                         │
├─────────────────────────────────────────────────────────┤
│ [Chain] [Learn] [Field Challenges] [Assessment]         │
│ [Progress] [Reference]                     — pill style │
├────────────────────────────────┬────────────────────────┤
│                                │ ⚡ AI Readiness         │
│   MAIN CONTENT AREA            │   Calculator           │
│   (Chain / Learn / etc.)       │                        │
│                                │ 🏢 Facility Profile    │
│                                │                        │
│                                │ 📋 Methodology         │
│                                │                        │
├────────────────────────────────┴────────────────────────┤
│ CTA: Service Ladder    │  CTA: Feedback               │
├─────────────────────────────────────────────────────────┤
│ ← Prev Module  │  Module 1 of 8  │  Next Module →      │
├─────────────────────────────────────────────────────────┤
│ © 2026 LBE · legacybe.ie · Contact · Tools · Services  │
└─────────────────────────────────────────────────────────┘
```

---

## COMPONENT SPECIFICATIONS

### 1. AUDIENCE BAR
```
AUDIENCE: Fund Managers, Asset Owners, Colocation Executives, CTOs, Technical Advisors
```
- Full width, --panel background, 1px bottom border
- Text: 11px, --lbe-green, mono font, uppercase, letter-spacing 0.1em
- Matches DC-LEARN exactly

### 2. HEADER
- Logo: 40px circle, border-radius 50%
- Title: "DC-AI-001: Power Density" — 18px, 700, --text-bright
- Subtitle: "AI-Ready Data Centre Investment Intelligence" — 12px, --text-dim
- Right: "Module 1 of 8 · DC-AI v2.0.0" — 12px, --text-muted, mono
- Theme toggle: sun/moon, 32px, top-right corner
- 1px --border bottom

### 3. HERO SECTION
- Series badge: "DC-AI-001 · POWER DENSITY" — 12px, --grammar, mono, uppercase
- Title: "Can This Facility Handle AI Workloads?" — 28px, 700, --text-bright
- Disclaimer: "Fictional reference facility..." — 13px, --text-muted, italic

### 4. TAB BAR (pill style — match DC-LEARN)
- Pill buttons: 12px padding horizontal, 8px vertical, border-radius 20px
- Active: 1px solid --grammar (or stage colour), --text-bright text
- Inactive: transparent background, --text-dim, 1px solid --border
- Hover: --panel background
- NOT sticky (DC-LEARN doesn't use sticky tabs)
- Tab order: Chain | Learn | Field Challenges | Assessment | Progress | Reference

### 5. CHAIN TAB
**Level selector / persona entry combined:**
- "Select a level to explore, or use the Cascade Calculator to find bottlenecks at target density."
- 9 level rows (NOT cards — match DC-LEARN list format):
  - Each row: icon + "L1: Legacy Density" + subtitle in mono + 3 progress dots
  - --surface background, 1px --border, hover effect
  - Click → navigates to Learn tab at that level

**Persona selector below levels:**
- "Viewing as Conor — Asset Manager (Fund)" with [Clear]
- 5 persona buttons (Conor | Helena | Eoin | Rachel | Padraig)
- When selected: "WHERE THIS PERSPECTIVE IS RICHEST" section
- 9 rows showing the rhetoric_takeaway for selected persona at each level
- "Rhetoric →" link on each row to jump to that level's rhetoric stage

### 6. LEARN TAB (merged Grammar + Logic + Rhetoric)
**Level header:**
- Icon + "Level 1: Legacy Density" (20px, 600)
- Subtitle in mono (13px, --text-dim)
- retrofitRelevance in amber/orange card

**Stage selector buttons:**
- [Grammar] [Logic] [Rhetoric] — 3 equal-width buttons
- Active: filled with stage colour
- Inactive: outlined
- Match DC-LEARN's stage button styling exactly

**Grammar stage content:**
- 5 fact cards, each with:
  - Term (16px, 600, --text-bright)
  - Standard reference (mono, --grammar background at 8%)
  - DEFINITION (14px, --text)
  - 💡 Clarify button → toggles plain English panel (hidden by default)
  - BY THE NUMBERS box (mono, --panel background, orange border)
  - So what? card (--grammar background at 12%, green "So what?" label)
- "What It Looks Like On Site" section with 👁️ icon
- Site Checklist with green ✓ marks
- Sources footer (mono, --text-muted)

**Logic stage content:**
- FUNDAMENTAL CONSTRAINT card (--rhetoric background at 10%, purple border)
- Cause & Effect pairs (CAUSE=red label, EFFECT=amber, INSIGHT=green)
- The Weakest Link section (✗ mistake, ✓ correct, → how to get there with costed steps)

**Rhetoric stage content:**
- 5 persona cards (3 top + 2 bottom)
- Avatar circles with persona colours
- Eoin: dashed border + "DIAGNOSTIC" badge
- KEY TAKEAWAY pill at bottom of each card

### 7. FIELD CHALLENGES TAB
- Level filter: [All Levels] [L1] [L2] ... [L9]
- Persona filter: [All] [Conor] [Helena] [Eoin] [Rachel] [Padraig]
- Each challenge:
  - Level badge + challenge title
  - SITUATION label (--grammar) + text
  - CHALLENGE label (--logic) + bold question
  - "Show the Fix" button (collapsed by default)
  - On click: reveals STEP-BY-STEP SOLUTION with numbered steps
  - Cross-ref pills at bottom

### 8. ASSESSMENT TAB
**Pre-start state:**
- Description: "27 questions across three Trivium stages — 9 per stage..."
- "Knowledge Check (Grammar): can you recall the key facts? 60s"
- "Eng. Calculation (Logic): can you work through the consequences? 120s"
- "Prof. Judgement (Rhetoric): can you explain it to each stakeholder? 90s"
- [Start Assessment] button

**During assessment:**
- Timer: countup from 00:00 (displayed prominently)
- Question card with level badge + tier badge (coloured by stage)
- Question ID in top-right (QAI001-N)
- 4 options as cards (A/B/C/D)
- Selected: 2px --grammar border
- After selection: immediate feedback
  - Correct: green background at 10%, ✓ icon
  - Wrong: red background at 10%, ✗ icon
  - Correct answer highlighted in green if wrong was selected
  - Explanation card reveals below

**Filters (after completion):**
- Tier filter: [All] [Knowledge Check] [Eng. Calculation] [Prof. Judgement]
- Level filter: [All Levels] [L1] [L2] ... [L9]

**Score panel (after completion):**
- "Score: X/27 (Y%)" — large text
- Progress bar (green gradient)
- "Completed in MM:SS (under/over time)"
- Tier breakdown: Knowledge X/9, Calculation X/9, Judgement X/9
- [Reset Assessment] button

### 9. PROGRESS TAB
- Overall: "X/27 stages complete (Y%)" with progress bar
- Assessment Results (if completed): score, time, tier breakdown
- Per-level grid: 9 rows with icon + title + 3 dots (G/L/R)
- Module info block: ID, version, series, publisher, contact

### 10. REFERENCE TAB (was BSG)
- Sub-tabs: Glossary (40 terms) | Bibliography (16 sources)
- Glossary: searchable, alternating row colours
- Bibliography: grouped by tier, cards with usage notes

### 11. CASCADE CALCULATOR (right sidebar)
- Title: "⚡ AI Readiness Calculator"
- Input fields pre-filled with Clonshaugh defaults
- "Find Bottlenecks →" button (--lbe-green)
- Result: PASS (green) / FAIL (red) with reason
- "Test all 9 levels →" grid: L1–L9 with dots
- Below: "How to read the results" explainer

### 12. FACILITY PROFILE (right sidebar, below calculator)
- "🏢 Facility Profile — Clonshaugh Reference DC (2012)"
- Parameter table: Racks, Density, IT Load, PUE, MIC, Voltage, etc.
- Static data from VERTICAL_CONFIG

### 13. METHODOLOGY CARD (right sidebar, below facility)
- "Trivium Method: Grammar → Logic → Rhetoric"
- "Feynman Clarify: every fact has three layers..."
- "Weakest Link: each level identifies the most common misconception..."
- "Five Personas: same finding — five different professional perspectives"
- Match DC-LEARN's methodology card text

### 14. CTA SECTION (above footer)
- Two-column:
  - Left: "Need to know where your facility stands on AI readiness?"
    Service ladder teaser. Button: "Learn about AI Readiness Assessment →"
  - Right: "Questions or feedback on this content?"
    Button: "Send Us a Message" (mailto:lmurphy@legacybe.ie)

### 15. FOOTER (2-tier)
- Row 1: "← First module" | "Module 1 of 8 · DC-AI v2.0" | "DC-AI-002: Cooling →"
- Row 2: "© 2026 Legacy Business Engineers Ltd" | legacybe.ie · Tools · Contact · Services

---

## BUILD METHOD

This is a template rewrite — v2.0.0, not a patch.

CC should:
1. Read this spec completely
2. Read DC-AI-001_v1_1_0.html for the existing data constants (LEVELS, ASSESSMENT_QUESTIONS, etc.)
3. Build a NEW HTML file using Python, reusing the data constants but rewriting all components
4. The data (45 facts, 27 questions, etc.) is UNCHANGED — only the components and CSS change

Break into 8 Python scripts:
1. `template_01_css.py` — complete CSS with DC-LEARN theme, 2-column layout, pill tabs, sidebar
2. `template_02_data.py` — extract all data constants from v1.1.0, write to section file
3. `template_03_header.py` — audience bar, header, hero, tab bar
4. `template_04_chain.py` — chain tab with level list + persona selector
5. `template_05_learn.py` — merged learn tab with stage buttons, grammar clarify, logic, rhetoric
6. `template_06_challenges_assessment.py` — field challenges with reveal, assessment with timer/filters
7. `template_07_sidebar_footer.py` — calculator, facility profile, methodology, CTA, footer
8. `template_08_assemble_verify.py` — assemble, version bump to 2.0.0, verify all counts

## RULES
- ALL content from v1.1.0 data constants — zero fabrication
- CDN: cdnjs.cloudflare.com ONLY
- Python r''' raw strings for JSX — never f-strings
- Base64 in plain <script> before Babel block
- Dark AND light themes must work
- 27 questions, 45 facts, 5 personas, 9 levels — verify after build
- This is the TEMPLATE for modules 2–8 — make it clean, modular, and easy to reskin

---

*DC-AI Template Standard v1.0 | April 2026*
*Benchmark: DC-LEARN-000 v2.4.6*
*This document supersedes DC_AI_POLISH_PASS_2_v1_0.md*
