# DC-AI-001 POLISH PASS 2 — B+ to A+
# Four items. Zero content changes. CSS + component additions only.
# Input: DC-AI-001_v1_1_0.html from repo
# Output: DC-AI-001_v1_2_0.html

---

## ITEM 1: CASCADE CALCULATOR SIDEBAR

The DNA contains 9 `cascadeCheck` functions — one per level. These are
JavaScript function bodies stored as strings. They take an inputs object
and return `{pass: boolean, reason: string}`.

### What to build:
A collapsible right sidebar panel (or modal on mobile) titled
"⚡ AI Readiness Calculator" that:

1. Shows input fields for Clonshaugh defaults (pre-filled, editable):
   - Target kW/rack (default: 40)
   - Number of racks (default: 50)
   - MIC MVA (default: 5)
   - MIC utilisation % (default: 85)
   - Bus section amps (default: 1600)
   - Bus utilisation % (default: 73)
   - Voltage (default: 415)
   - Power factor (default: 0.85)
   - Floor rating PSF (default: 150)
   - Rack weight lbs (default: 3200)
   - Lease years (default: 12)
   - Electricity price €/kWh (default: 0.12)

2. "Find Bottlenecks →" button (--lbe-green background, white text)

3. On click: runs the cascadeCheck function for the CURRENTLY SELECTED
   LEVEL and displays the result:
   - PASS: green card with reason text
   - FAIL: red card with reason text

4. Below the result: "Test all 9 levels →" button that runs all 9
   cascade functions and shows a summary grid:
   - L1–L9 as rows
   - PASS (green dot) / FAIL (red dot) per level
   - Click any row to see the full reason string

### Styling:
- Sidebar: 320px wide, --surface background, 1px --border left
- On desktop: always visible right of main content (main content max-width reduces to 640px)
- On mobile (<768px): hidden, accessible via floating "⚡" button bottom-right
- Input labels: 12px, --text-dim, mono
- Input fields: --panel background, 1px --border, 14px
- Pre-filled with Clonshaugh defaults from VERTICAL_CONFIG

### Data source:
The cascadeCheck strings are already in the LEVELS array. Use:
```javascript
const fn = new Function('inputs', level.cascadeCheck);
const result = fn(inputValues);
```

---

## ITEM 2: PERSONA ENTRY POINT ON CHAIN TAB

### What to build:
A persona selector bar that appears ABOVE the chain cards, showing:

"View through the lens of:"
[C Conor] [H Helena] [E Eoin] [R Rachel] [P Padraig] [Clear]

When a persona is selected:
1. The bar shows "Viewing as Conor — Asset Manager (Fund)" with Clear button
2. Below the persona bar, show a "WHERE THIS PERSPECTIVE IS RICHEST" section
3. List all 9 levels with the rhetoric_takeaway for the selected persona
4. Each row: "L1 · Legacy Density" → one-sentence takeaway → "Rhetoric →" link
5. Clicking "Rhetoric →" navigates to that level's Rhetoric tab

### Data source:
rhetoric_takeaways already exists in the JS constants:
```javascript
RHETORIC_TAKEAWAYS.L1.asset_management // Conor's L1 takeaway
RHETORIC_TAKEAWAYS.L1.technology       // Helena's L1 takeaway
// etc.
```

### Persona mapping:
- Conor → asset_management → #2563EB
- Helena → technology → #7c3aed
- Eoin → technical → #16a34a
- Rachel → compliance → #d97706
- Padraig → cost → #6b7280

### Styling:
- Persona buttons: 60px wide, coloured circle with initial + name below
- Selected: full colour background, white text
- Unselected: --panel background, coloured text
- Takeaway list: --panel background cards, 1px --border, level badge left
- Match DC-LEARN-000's persona selector layout (screenshots provided)

---

## ITEM 3: CTA SECTION ABOVE FOOTER

### What to build:
A two-column section between the main content and the footer:

**Left column (60%):**
- Heading: "Need to know where your facility stands on AI readiness?"
- Body: "From desktop screening (€8,500) to full programme management
  (€360,000) — LBE's service ladder starts where the platform stops."
- Button: "Learn about AI Readiness Assessment →" (--lbe-green, links to legacybe.ie)

**Right column (40%):**
- Heading: "Questions or feedback on this content?"
- Body: "Technical corrections, suggestions, or industry perspective welcome."
- Button: "Send Us a Message →" (--grammar colour, mailto:lmurphy@legacybe.ie)

### Styling:
- Full-width section, --panel background, 48px vertical padding
- Cards within: --surface background, 24px padding, 12px border-radius
- Desktop: 2 columns with 24px gap
- Mobile: single column, stacked
- Match DC-LEARN's CTA box styling

---

## ITEM 4: FACILITY PROFILE PANEL

### What to build:
A persistent reference panel showing Clonshaugh parameters. Position:
- Desktop: inside the cascade calculator sidebar, below the calculator
- Mobile: collapsible panel accessible from the "⚡" button

### Content:
```
🏢 Facility Profile
Clonshaugh Reference DC (2012)

Racks:              400
Current density:    8 kW/rack
IT load:            2.4 MW
Current PUE:        1.50
Target PUE:         1.20
MIC:                5 MVA (85% utilised)
Voltage:            10 kV ESB Networks MV
Hall A:             200 racks, air-cooled, 8 kW avg
Hall B:             200 racks, retrofit candidate
Floor loading:      150 psf (raised floor)
Ceiling height:     3.2m
Generator:          3.0 MW
UPS:                2.8 MW
Lease remaining:    12 years
```

### Styling:
- --surface background, 1px --border, 12px border-radius
- Title: 16px, 600, --text-bright
- Labels: 13px, --text-dim
- Values: 13px, 600, --text-bright, right-aligned
- Parameter rows: alternating --surface / --panel for readability

---

---

## ITEM 5: CLARIFY BUTTON ON GRAMMAR FACTS

### What to build:
A "Clarify" toggle button below each grammar fact that expands/collapses
an additional plain-language explanation panel. This is the Feynman
explainer — the same pattern used in DC-LEARN.

### Behaviour:
1. Below each grammar fact card (after the "So what?" section), add a
   small button: "💡 Clarify" (13px, --text-dim, cursor:pointer)
2. On click, toggle visibility of an expanded panel showing:
   - The `plain` field text (already in the data — every fact has it)
   - Styled as: --panel background, 12px padding, 12px border-radius,
     italic, --text colour, 14px, left border 3px --grammar
   - Header: "In plain English:" (12px, --grammar, uppercase)
3. Second click collapses it
4. The plain text is ALREADY DISPLAYED in the fact card layout —
   so the Clarify button should show it in an ALTERNATIVE presentation:
   - Hide the inline "PLAIN ENGLISH" section from the default fact layout
   - Move it behind the Clarify toggle instead
   - This declutters the default fact view and makes the Clarify reveal feel purposeful
5. Default state: collapsed (plain text hidden)

### Styling:
- Button: no background, 1px --border, 6px border-radius, 8px 12px padding
- Hover: --panel background
- Expanded panel: slides down with 150ms transition (max-height trick)
- Close state: "💡 Clarify" — Open state: "💡 Clarify ▾" (or toggle icon)

### Data source:
Already in LEVELS[n].grammar.facts[n].plain — no new data needed.

---

## ITEM 6: PROGRESS TAB

### What to build:
A dedicated Progress tab (add to tab bar after Assessment, before Reference)
that shows completion status across the module.

### Content:

**Section 1: Overall Progress**
- "X/27 stages complete (Y%)" with progress bar
- 27 stages = 9 levels × 3 stages (Grammar, Logic, Rhetoric)
- A stage is "complete" when the learner has visited that tab for that level
- Track in state: `visitedStages` object (already exists from v1.1.0 progress dots)

**Section 2: Assessment Results** (if assessment completed)
- "Score: X/27 (Y%)"
- Per-tier breakdown: Knowledge X/9, Calculation X/9, Judgement X/9
- "Completed in MM:SS"
- Green progress bar

**Section 3: Per-Level Completion Grid**
- 9 rows, one per level
- Each row: Level icon + title + 3 dots (Grammar=blue, Logic=amber, Rhetoric=purple)
- Filled dot = visited, empty dot = not visited
- Same data as the progress dots on the level selector

**Section 4: Module Information**
- Module: DC-AI-001 Power Density
- Version: 1.2.0
- Series: DC-AI · Module 1 of 8
- Publisher: Legacy Business Engineers Ltd
- Contact: lmurphy@legacybe.ie

### Styling:
- Match DC-LEARN Progress tab layout
- Progress bar: gradient from --grammar to --rhetoric
- Per-level rows: alternating --surface / --panel
- Assessment score: large text (24px), --text-bright
- Tier breakdown: coloured labels (Knowledge=--grammar, Calculation=--logic, Judgement=--rhetoric)

### State management:
- Use the existing `visitedStages` state from v1.1.0
- Track assessment completion in state: `assessmentResult` object
  with fields: {score, total, time, tierScores}
- Persist to localStorage via safeStore

---

## BUILD METHOD

Break into 6 Python scripts (one per item), run sequentially:
1. `polish2_01_calculator.py` — cascade calculator sidebar
2. `polish2_02_personas.py` — persona entry point on chain tab
3. `polish2_03_cta.py` — CTA section above footer
4. `polish2_04_facility.py` — facility profile panel
5. `polish2_05_clarify.py` — Clarify button on grammar facts
6. `polish2_06_progress.py` — Progress tab

Final step in script 6: bump version to 1.2.0 across all 4 reference
points and run verification (27 questions, 45 facts, all tabs rendering).

## RULES
- ZERO content changes — do not modify any grammar facts, persona text,
  assessment questions, or logic entries
- CDN: cdnjs.cloudflare.com ONLY
- Python r''' raw strings for JSX
- Test dark AND light themes after each script
- Verify 27 questions and 45 facts still present after each script
