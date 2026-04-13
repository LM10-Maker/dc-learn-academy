# DC-AI-001 PIXEL MATCH PASS — v2.3.0
# Match DC-LEARN-002 v5.13.7 exactly in layout, spacing, colour, structure
# DC-LEARN-002 HTML file is in the repo as dc-learn-002.html — READ IT FIRST
# Input: DC-AI-001_v2_2_0.html
# Output: DC-AI-001_v2_3_0.html

---

## CC PROMPT — paste into new Claude Code session

```
You have two HTML files in the repo:
- dc-learn-002.html (THE BENCHMARK — read this first, study every component)
- DC-AI-001_v2_2_0.html (THE TARGET — make this match the benchmark)

DC-LEARN-002 is the gold standard. DC-AI-001 must match it in EVERY visual
detail: spacing, font sizes, colours, card styles, borders, padding, margins,
component layout, progressive disclosure pattern, footer structure.

DO NOT change any content, data, questions, or persona text in DC-AI.
ONLY change: CSS, component structure, layout, spacing, element ordering.

Work through 10 patches. Each is ONE Python script under 80 lines.
Run one at a time. Read dc-learn-002.html FIRST to understand the target.

PATCH 1 — CHAIN TAB
Read how dc-learn-002.html renders its chain tab (the "Cooling Chain" tab).
Match DC-AI's chain tab to this EXACTLY:
- Level rows: icon (32px) + "L1: Title" (15px, weight 600, --text-bright)
  + component subtitle (12px, mono, --text-muted) + 3 progress dots (right)
- Row background: --surface, 1px --border, border-radius 8px, padding 12px 16px
- Row gap: 4px between rows
- No expand/collapse on chain rows — they are simple navigation rows
- Click = navigate to Learn tab at that level
- Chain description card at top: plain text, no icons, 13px, --text-dim
- Persona selector below L9: flush, no card wrapper

PATCH 2 — SIDEBAR (Calculator + Facility Profile + Methodology)
Match dc-learn-002.html sidebar EXACTLY:
- Sidebar width: 320px on desktop, hidden on mobile
- Calculator: "Cascade Calculator" title (bold, 15px), inputs (label 12px mono,
  field full-width, --panel bg, 1px --border), green "Find Bottlenecks →" button
- After calc runs: results list with PASS/FAIL badges + reason per level
- Facility Profile: table with label (12px, --text-dim, mono) + value (13px,
  --text-bright, mono, bold) in two columns
- Methodology: title + description paragraphs (13px, --text-dim)

PATCH 3 — LEARN TAB: Grammar stage
Match dc-learn-002.html Grammar rendering:
- Clock quote at top: green left border (--lbe-green), --panel bg, italic quote,
  "— Level N: Title" attribution below
- Level selector: L1-L9 pill buttons, 32px height, active = --green border
- Level header card: icon + "Level N: Title" (22px, weight 700) + component
  (12px, mono) + user need statement (italic, --green, 13px) + plain English (14px)
- Stage buttons: [Grammar] [Logic] [Rhetoric] — equal width, active = filled
  with stage colour, inactive = outlined
- "Grammar — What Is It?" header in --grammar colour
- 5 fact rows: collapsed by default, show ONLY term name (15px, 600)
- Click to expand: definition, plain English, By the Numbers, So What
- "What It Looks Like On Site" section below facts
- Site Checklist with ✓ marks
- Sources footer at bottom

PATCH 4 — LEARN TAB: Logic stage
Match dc-learn-002.html Logic rendering:
- "Logic — Why Does It Matter?" header in --logic colour
- Cause & Effect cards with coloured left borders:
  - ⚡ CAUSE: bold statement (--text-bright)
  - → EFFECT line (--text-dim)
  - 💡 INSIGHT italic (--logic colour)
- Constraint Lesson box: --panel bg, amber/logic border
- Weakest Link section:
  - "Weakest Link" header
  - ✗ common mistake (red bg tint, red border)
  - ✓ correct understanding (green bg tint, green border)
  - "How To Get There" numbered steps
- Cross-references at bottom
- "I understand the consequences" button (red/logic, full width)

PATCH 5 — LEARN TAB: Rhetoric stage
Match dc-learn-002.html Rhetoric rendering:
- "Rhetoric — How Do I Explain It?" header in --rhetoric colour
- 5 persona buttons: "Declan (Ops Manager)" style — name + role in button
  DC-AI uses: Conor/Helena/Eoin/Rachel/Padraig with their roles
- Selected persona: shows quote in --panel bg card with green left border
- Key takeaway in italic below
- "I can explain it to each stakeholder" button (purple/rhetoric, full width)
- Below rhetoric: Glossary + Bibliography expandable sections

PATCH 6 — FIELD CHALLENGES TAB
Match dc-learn-002.html Field Challenges:
- Description box at top with green left border
- Level filter: [All Levels] [L1]...[L9] pill buttons
- Persona filter: [All] [Declan]...[Tom] — DC-AI uses Conor/Helena/Eoin/Rachel/Padraig
- Each challenge: card with level badge + title
  - SITUATION label (green pill) + text
  - CHALLENGE label (amber pill) + bold question
  - "Show the Fix" button (muted, outlined)
  - Fix hidden by default, revealed on click

PATCH 7 — ASSESSMENT TAB
Match dc-learn-002.html Assessment:
- Description box at top (green border, text about 27 questions, 3 tiers)
- Timer: clock circle + "15:00" display + "starts on first answer"
- Tier filter: [All] [Knowledge Check] [Eng. Calculation] [Prof. Judgement]
- Level filter: [All Levels] [L1]...[L9]
- Question cards: level icon + GRAMMAR/LOGIC/RHETORIC badge + "Level N"
- Question text: 15px, 600, --text-bright
- 4 options: cards with hover effect, 14px
- Score panel after completion: score %, tier breakdown, time

PATCH 8 — CTA + FOOTER
Match dc-learn-002.html exactly:
- Two-column CTA section: left = service description, right = feedback + button
- "Send Us a Message" button: --lbe-green bg, white text, full width of right card
- Series nav row: "← Prev Module" | "Module N of 8 · DC-AI v2.3" | "Next Module →"
- Copyright row: "© 2026 Legacy Business Engineers Ltd" | links (legacybe.ie, Tools, Contact, Services)

PATCH 9 — PROGRESS TAB
Match dc-learn-002.html Progress:
- "Overall Progress" card: "X/27 stages complete (Y%)" + progress bar
- Assessment Results (if completed): score, time, tier breakdown
- Per-level rows: icon + "Level N: Title" + Grammar dot + Logic dot + Rhetoric dot
- Dots: empty circle = not visited, filled = visited, colours match stages

PATCH 10 — VERSION BUMP + VERIFICATION
- Bump to 2.3.0 in all locations (title, TOOL_VERSION, MODULE_META, series badge)
- Verify: 27 questions, 45 facts (5 per level × 9), all tabs render
- Save as DC-AI-001_v2_3_0.html
```

---

## KEY PRINCIPLE FOR CC

DC-LEARN-002 is in the repo. Read it. Match it. Every font size, every
padding value, every border colour, every hover state. If DC-LEARN does
it one way and DC-AI does it differently, DC-AI changes to match.

The ONLY things that stay different:
- Content (DC-AI has different facts, questions, personas)
- Tab names (DC-AI: "Chain" not "Cooling Chain", "Reference" not "The Story")
- Module title and series info
- Audience bar text (DC-AI has fund-specific audience)
- No Visual Guide tab (deferred)
- No Story tab (no DC-AI narrative exists yet)

Everything else: IDENTICAL.

---

*DC-AI Pixel Match Spec v1.0 | April 2026*
