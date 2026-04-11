# DC-AI AESTHETICS & UI/UX SECOND PASS
# Role: World-Class UI/UX Reviewer
# Benchmark: DC-LEARN-002 v5.8.6+ (canonical template)
# Input: DC-AI-001_v1_0_0.html (functional, content-verified)
# Output: DC-AI-001_v1_1_0.html (world-class, client-ready)

---

## ROLE ASSIGNMENT

You are the WC UI/UX Reviewer for DC-AI. Your benchmark is DC-LEARN-002
— a module that has been through 6 weeks and 74 G-NEW production rules
of refinement. DC-AI-001 v1.0.0 is functionally correct but was assembled
mechanically by a builder agent. Your job is to bring it to the same
visual and interaction standard as the DC-LEARN fleet.

The audience is fund managers, CTOs, and asset owners making €50M+
decisions. Every pixel must communicate: "This was built by professionals
who understand engineering, not by a template generator."

---

## SECTION 1: CSS DESIGN SYSTEM (port from DC-LEARN-002)

### 1.1 Theme Variables — MUST MATCH DC-LEARN

The DC-LEARN CSS system uses a precise three-tier depth model and
four-tier text hierarchy. DC-AI-001 must adopt these EXACTLY:

```css
:root, [data-theme="dark"] {
  --bg: #0F1117;           /* page background — deepest */
  --surface: #181C20;      /* card background — mid depth */
  --panel: #1E2228;        /* nested panel — shallowest dark */
  --border: #2A2F38;       /* subtle dividers */
  --text: #C8CCD4;         /* body text */
  --text-bright: #F0F2F5;  /* headings, emphasis */
  --text-dim: #8B919A;     /* secondary info */
  --text-muted: #5A6170;   /* labels, hints, timestamps */
  --grammar: #2563EB;      /* blue — facts, definitions */
  --logic: #d97706;        /* amber — cause/effect */
  --rhetoric: #7c3aed;     /* purple — professional judgement */
  --lbe-green: #16a34a;    /* CTA buttons ONLY — never headings */
  --success: #16a34a;
  --warn: #d97706;
  --error: #dc2626;
  --font-sans: 'IBM Plex Sans', system-ui, sans-serif;
  --font-mono: 'IBM Plex Mono', monospace;
}

[data-theme="light"] {
  --bg: #F5F5F5;
  --surface: #FFFFFF;
  --panel: #F0F0F0;
  --border: #E0E0E0;
  --text: #2D3748;
  --text-bright: #1A202C;
  --text-dim: #718096;
  --text-muted: #A0AEC0;
}
```

### 1.2 Spacing System
- Card padding: 24px
- Card gap: 16px
- Section gap: 32px
- Border radius: 12px (cards), 8px (inner panels), 6px (badges)
- Max content width: 960px (centred)

### 1.3 Typography Scale
- Module title (hero): 28px, 700 weight, --text-bright
- Level title: 20px, 600 weight, --text-bright
- Section header (Grammar, Logic, etc.): 16px, 600 weight, stage colour
- Body text: 15px, 400 weight, --text, line-height 1.6
- Mono text (numbers, standards): 13px, 400 weight, --font-mono
- Labels/badges: 11px, 500 weight, uppercase, letter-spacing 0.05em

---

## SECTION 2: COMPONENT-BY-COMPONENT PUNCH LIST

### 2.1 Header
**Current:** Logo + title + subtitle in a row. No series nav visible.
**Target:**
- Logo (48px circle, border-radius 50%)
- Module title: "DC-AI-001: Power Density" (20px, 600, --text-bright)
- Subtitle: "AI-Ready Data Centre Investment Intelligence" (13px, --text-dim)
- Series nav right-aligned: "Module 1 of 8 · DC-AI v1.0" (12px, --text-muted)
- Theme toggle: sun/moon icon button, 36px, top-right
- Thin 1px bottom border in --border

### 2.2 Level Selector
**Current:** 9 cramped boxes with small text, hard to distinguish selected state.
**Target:**
- Horizontal scroll on narrow screens, no wrap
- Each button: 80px wide, 72px tall, border-radius 12px
- Icon: 24px centred above label
- Label: 11px, 2 lines max, centred, --text-dim (unselected), --text-bright (selected)
- Selected state: --grammar background at 15% opacity, 2px solid --grammar border
- Hover: --surface background, subtle shadow
- Unselected: --panel background, 1px --border border
- 8px gap between buttons
- Level number badge (L1–L9): 10px, top-left corner, --text-muted

### 2.3 Tab Bar
**Current:** Working but icons are inconsistent and spacing is tight.
**Target:**
- Tab icons: consistent emoji set or Lucide-style text labels
- Active tab: bottom 2px border in stage colour (grammar=blue for Grammar tab, etc.)
- Inactive tabs: no border, --text-dim colour
- Tab labels: 13px, 500 weight
- 24px horizontal padding per tab
- Sticky at top when scrolling (position: sticky, top: 0, z-index: 10)

### 2.4 Chain Tab
**Current:** 9 cards with dense text — wall of content.
**Target:**
- 3-column grid (desktop), 1-column (mobile)
- Each card: --surface background, 1px --border, border-radius 12px
- Level badge (L1–L9): top-left, stage-coloured pill
- Title: 16px, 600, --text-bright
- Subtitle: 13px, --text-dim, italic
- Plain English: 14px, --text, max 3 lines with "Read more..." expand
- Retrofit Relevance: collapsed by default, expandable with chevron
- Cross-refs: hidden by default, expandable "See related →" link
- "Click to explore →" button: --grammar colour, 13px
- Selected card (current level): 2px --grammar left border, subtle shadow
- L9 card: --rhetoric left border (final decision level)

### 2.5 Grammar Tab
**Current:** Good structure — standard, definition, plain, numbers, soWhat.
**Improvements:**
- Standard reference: --grammar background at 8% opacity, mono font, 12px
- "So what?" card: --grammar background at 12% opacity, left border 3px --grammar
- "By the Numbers" box: --panel background, mono font, border-radius 8px
- "What It Looks Like On Site" section: italic, --text-dim, with 👁️ icon
- Site Checklist: green checkmarks (--success colour), 14px
- Each fact card: 1px left border in --grammar, 16px left padding
- Fact term as heading: 16px, 600, --text-bright
- Sources footer: --text-muted, 12px, mono, separated by thin border

### 2.6 Logic Tab
**Current:** Good — Fundamental Constraint in purple, C&E with colour labels.
**Improvements:**
- Fundamental Constraint: --rhetoric background at 10% opacity, 3px left border --rhetoric
- CAUSE label: 12px, --error colour, uppercase, letter-spacing 0.1em
- EFFECT label: 12px, --warn colour, uppercase
- INSIGHT label: 12px, --success colour, uppercase
- Each C&E pair in a card with --surface background, 12px border-radius
- Weakest Link section:
  - ✗ COMMON MISTAKE: --error background at 8%, --error left border
  - ✓ CORRECT UNDERSTANDING: --success background at 8%, --success left border
  - → HOW TO GET THERE: numbered steps with --panel background, 1px --border between steps
  - Each step: cost indications right-aligned in mono, --text-dim

### 2.7 Rhetoric Tab
**Current:** 5 persona cards in 2+2+centre layout. Working but flat.
**Improvements:**
- 3-column top row (Conor, Helena, Eoin), 2-column bottom row (Rachel, Padraig)
- Each persona card: --surface background, 12px radius
- Avatar circle: 40px, coloured by persona:
  - Conor (C): #2563EB (fund blue)
  - Helena (H): #7c3aed (tech purple)
  - Eoin (E): #16a34a (engineering green) with 🔍 diagnostic badge
  - Rachel (R): #d97706 (regulatory amber)
  - Padraig (P): #6b7280 (cost grey)
- Name: 15px, 600, --text-bright
- Role: 12px, --text-dim
- Entry text: 14px, --text, line-height 1.6
- Key Takeaway: pill at bottom, persona colour at 12% opacity, 13px, italic
- Eoin's card: subtle dashed border (not solid) to visually distinguish diagnostic-only voice. Small "DIAGNOSTIC" badge under role label.

### 2.8 Field Challenge Tab
**Current:** Excellent — best tab design. Keep as-is with minor tweaks.
**Improvements:**
- SITUATION label: --grammar colour
- CHALLENGE: --logic colour, bold question text in --text-bright
- STEP-BY-STEP SOLUTION: --rhetoric colour, numbered steps in cards
- Each step: --panel background with left border in graduated colour (step 1 = light, step 5 = dark)
- Cross-ref pills at bottom: clickable style (cursor pointer, hover effect) even if not yet linked
- Clonshaugh disclaimer: retain in amber italic below situation

### 2.9 Assessment Tab
**Current:** Working — 27 questions, level/tier badges, A/B/C/D options.
**Improvements:**
- Question card: --surface, 16px padding, 12px radius
- Level badge: --grammar background, 10px, mono
- Tier badge: coloured by tier (knowledge=blue, calculation=amber, judgement=purple)
- Options: --panel background, hover: --surface with subtle border
- Selected option (before submit): 2px border in --grammar
- Correct answer (after submit): --success background at 10%, ✓ icon
- Wrong answer (after submit): --error background at 10%, ✗ icon
- Explanation: expandable card below question after answering
- Progress bar at top: gradient from --grammar to --rhetoric across 27 questions
- Score: right-aligned, "Score: X / Y" in --text-bright, large font
- Navigation: Previous / Next buttons, 36px height, --grammar colour
- End state: summary card with per-tier breakdown

### 2.10 BSG Tab
**Current:** Good — glossary with search, bibliography with tier badges.
**Improvements:**
- Sub-tabs (Glossary / Bibliography): underline active, not background
- Glossary search: --panel background, 1px --border, 14px, full width, border-radius 8px
- Glossary terms: alternating --surface / --panel rows for readability
- Term: 14px, 600, --text-bright
- Definition: 14px, --text
- Bibliography: cards grouped by tier (T1 first, then T2, T3)
- Tier badge: left-aligned, coloured (T1=blue, T2=amber, T3=grey)
- Usage note: --text-muted, 12px, italic

### 2.11 Footer
**Target:**
- Full-width, --panel background, 1px top border
- "© 2026 Legacy Business Engineers Ltd · DC-AI Series · Module 1 of 8"
- CTA: "Need to know where your facility stands on AI readiness?" with subtle link style
- Contact: lmurphy@legacybe.ie (12px, --text-muted)
- Version: "DC-AI-001 v1.0.0" (10px, --text-muted, right-aligned)

### 2.12 Progress/Completion Indicators (MISSING — add)
**Current:** No progress tracking visible.
**Target:**
- Per-level dot indicator on the level selector (grammar=blue dot, logic=amber, rhetoric=purple)
- Dots appear below each level button as stages are completed
- Module completion percentage in header: "Progress: 33%" (appears after first tab visit)
- Assessment score badge on Assessment tab (after completion)

---

## SECTION 3: INTERACTION POLISH

### 3.1 Transitions
- Tab switch: 150ms opacity fade
- Level switch: 200ms slide or fade
- Theme toggle: 200ms transition on all colour properties
- Card hover: 150ms shadow + border change
- No animations on page load (professional, not playful)

### 3.2 Scroll Behaviour
- Tab bar sticky on scroll
- "Back to top" appears after scrolling 500px
- Level selector scrolls horizontally on mobile with snap points
- Long content sections (Grammar 5 facts): consider lazy render

### 3.3 Responsive
- Desktop (>1024px): full layout as described
- Tablet (768–1024px): 2-column chain cards, persona cards stack 2+2+1
- Mobile (<768px): single column everything, level selector horizontal scroll, tabs in hamburger or horizontal scroll

---

## SECTION 4: THINGS TO REMOVE OR FIX

1. **No emojis in tab bar** — use text labels only (Chain, Grammar, Logic, Rhetoric, Field Challenge, Assessment, BSG). The emoji before each tab name is inconsistent with the DC-LEARN professional standard. Keep emojis ONLY on level selector icons.

2. **"BSG" label is unclear** — rename to "Reference" or "Glossary & Sources" for the DC-AI audience. Fund managers don't know what BSG means.

3. **Chain tab "Click to explore →"** — change to "Select this level →" with a visual affordance (arrow icon, cursor:pointer)

4. **Hero heading "Can This Facility Handle AI Workloads?"** — excellent. Keep.

5. **Disclaimer text** — currently small but visible. Good. Keep exactly as-is.

---

## SECTION 5: CC PROMPT FOR THE POLISH PASS

Paste this into Claude Code with DC-AI-001_v1_0_0.html attached:

```
Read DC-AI-001_v1_0_0.html from the repo. This is a working learning module
that needs a UI/UX polish pass to match the DC-LEARN fleet quality standard.

DO NOT change any content, data, questions, or persona text.
ONLY change: CSS, layout, spacing, colours, transitions, component structure.

Apply these changes:

1. CSS THEME VARIABLES — replace the existing CSS variables with the locked
   DC-LEARN system (exact hex values provided in the spec). Both dark and
   light themes must use the three-tier depth model (--bg, --surface, --panel)
   and four-tier text hierarchy (--text, --text-bright, --text-dim, --text-muted).

2. LEVEL SELECTOR — increase button size to 80×72px, add 8px gap, add
   selected state highlight (--grammar at 15% opacity + 2px solid border),
   add hover effect, add L1–L9 badge in corner. Horizontal scroll on mobile.

3. CHAIN TAB — collapse plainEnglish to 3 lines with "Read more...",
   hide crossRefs behind expandable "See related →", add 2px left border
   on selected level card, L9 card gets --rhetoric left border.

4. TAB BAR — remove emoji prefixes, text labels only. Make sticky on
   scroll. Active tab: 2px bottom border in stage colour.

5. RHETORIC EOIN CARD — add dashed border and "DIAGNOSTIC" badge under
   role to visually distinguish from prescriptive personas.

6. PERSONA AVATAR COLOURS — Conor #2563EB, Helena #7c3aed, Eoin #16a34a,
   Rachel #d97706, Padraig #6b7280.

7. ASSESSMENT — add coloured tier badges (knowledge=blue, calculation=amber,
   judgement=purple). Add progress bar at top. Correct/wrong answer styling
   after selection.

8. RENAME "BSG" TAB to "Reference" in the tab bar.

9. ADD PROGRESS DOTS — small coloured dots below each level selector button
   showing grammar (blue), logic (amber), rhetoric (purple) completion.

10. FOOTER — full-width bar with copyright, series nav, CTA, version, contact.

11. TRANSITIONS — 150ms tab switch, 200ms level switch, 200ms theme toggle.
    No load animations.

12. STICKY TAB BAR — position:sticky, top:0, z-index:10, with --surface
    background and bottom border.

Use Python to apply changes. Save as DC-AI-001_v1_1_0.html.
Version bump to 1.1.0 across all 4 reference points.
```

---

## SECTION 6: FACTORY INTEGRATION

This aesthetics pass becomes a STANDARD STEP in the DC-AI factory:

| Step | Agent | Model | Input | Output |
|------|-------|-------|-------|--------|
| 1 | SMCA | Opus | Vertical Config + Schema | DNA YAML |
| 2 | Builder | Sonnet (CC) | DNA + Builder Prompt | v1.0.0 HTML (functional) |
| 3 | QA | Opus | v1.0.0 HTML + screenshots | Technical QA report |
| **4** | **Polish** | **Sonnet (CC)** | **v1.0.0 HTML + this spec** | **v1.1.0 HTML (WC)** |
| 5 | Review | Opus (cold) | v1.1.0 HTML | SHIP / NOT SHIP |

Step 4 is new. It runs AFTER technical QA passes and BEFORE independent review.
The spec in Section 5 is the reusable prompt — same for every DC-AI module.

---

*DC-AI Aesthetics & UI/UX Standard v1.0 | LBE | April 2026*
*Benchmark: DC-LEARN-002 v5.8.6+ canonical template*
