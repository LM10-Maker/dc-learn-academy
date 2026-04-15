# DC-TOOL FACTORY SPEC v1.0
## Legacy Business Engineers Ltd | 13 April 2026
## Governs all AI-powered screening tool builds

---

## PURPOSE

This spec defines the repeatable pattern for building AI-powered screening tools from DC-LEARN module knowledge. Every tool follows the same architecture, the same visual language, and the same quality gates. Content differs; structure does not.

**Governing principle:** Each tool is a single-file React/Babel HTML application — same build pattern as DC-LEARN modules. The AI engine uses the Anthropic API (Sonnet) with a domain-specific system prompt extracted from the corresponding DC-LEARN module.

**Positioning principle (inherited):** LBE identifies and quantifies. Tools produce screening-level outputs. Every tool output is explicitly NOT a design deliverable, NOT a compliance determination.

---

## 1. TOOL REGISTRY

| Tool ID | Name | Source Module | Primary Persona | Status |
|---------|------|--------------|----------------|--------|
| DC-TOOL-000 | Factory Template | — | — | Template |
| DC-TOOL-001 | Power Chain Screener | DC-LEARN-001 | Mark | Build |
| DC-TOOL-002 | Cooling Chain Screener | DC-LEARN-002 | Mark | Build |
| DC-TOOL-003 | Redundancy Gap Tool | DC-LEARN-003 | Declan | Build |
| DC-TOOL-004 | Compliance Checker | DC-LEARN-004 | Sarah | Build |
| DC-TOOL-005 | UPS Adequacy Tool | DC-LEARN-005 | Mark | Build |
| DC-TOOL-006 | Grid Headroom Calculator | DC-LEARN-006 | Ann | Build |
| DC-TOOL-007 | Gap Analysis Generator | DC-LEARN-007 | Mark | Build |
| DC-TOOL-008 | Retrofit Scope Builder | DC-LEARN-008 | Ann | Build |
| DC-TOOL-009 | Investment Decision Model | DC-LEARN-009 | Ann | Extend ROI-001 |
| DC-TOOL-010 | Facility Audit Checklist | DC-LEARN-000 | Declan | Build |
| DC-TOOL-011 | Regulatory Tracker | DC-LEARN-011 | Sarah | Build |
| DC-TOOL-012 | F-Gas Phase-Down Tracker | DC-LEARN-013 | Mark | Build |
| DC-TOOL-013 | CRM Revenue Calculator | DC-LEARN-014 | Tom | Build |
| DC-TOOL-014 | Technology Roadmap Generator | DC-LEARN-015 | Ann | Build |

**Note:** DC-LEARN-010 (Carbon) and DC-LEARN-012 (CRREM/Energy Centre) are already served by CPS-001 and RPT-001. No separate tools needed.

---

## 2. FILE STRUCTURE (every tool, top to bottom)

```
<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
  ├── meta charset + viewport
  ├── <title> — "{TOOL_ID} v{VERSION} | {TOOL_NAME} | Legacy Business Engineers"
  ├── CDN scripts (React 18, ReactDOM 18, Babel 7.23) — cdnjs.cloudflare.com ONLY
  ├── Google Fonts — IBM Plex Sans + IBM Plex Mono
  └── <style> — CANONICAL CSS (inherited from DC-LEARN, Section 3)
</head>
<body>
  ├── BSG Layer 1 — window.onerror (plain JS, before root div)
  ├── <div id="root"></div>
  ├── <script> — LOGO_SRC constant (base64, plain JS — NOT inside Babel block)
  └── <script type="text/babel">
      ├── Header comment block (tool ID, version, factory spec ref)
      ├── TOOL_ID, TOOL_VERSION, TOOL_NAME constants
      ├── CANONICAL_DATA object (locked values with tier labels)
      ├── DOMAIN_PROMPT string (extracted from source module)
      ├── INPUT_SCHEMA array (field definitions for the input form)
      ├── DEMO_DATA object (Clonshaugh reference values)
      ├── PERSONAS constant (same 5 personas, tool-specific framing)
      ├── BSG Layer 2 — ErrorBoundary class
      ├── React hooks destructure
      ├── InputTab component (Section 5)
      ├── AnalysisTab component (Section 6)
      ├── ReportTab component (Section 7)
      ├── ConfidenceTab component (Section 8)
      ├── App component (Section 9)
      └── ReactDOM.render(<ErrorBoundary><App/></ErrorBoundary>, ...)
  </script>
</body>
</html>
```

---

## 3. CANONICAL CSS

Inherited from DC-LEARN Canonical Architecture v1.1 — same CSS variables, same dark/light theme, same colour usage rules. Plus these tool-specific additions:

```css
/* Tool-specific classes */
.input-group { margin-bottom: 16px; }
.input-label {
  display: block; font-size: 13px; font-weight: 600;
  color: var(--text-dim); margin-bottom: 4px;
  font-family: var(--font-mono);
}
.input-field {
  width: 100%; padding: 10px 12px; border-radius: 6px;
  border: 1px solid var(--border); background: var(--panel);
  color: var(--text); font-family: var(--font-sans); font-size: 14px;
}
.input-field:focus {
  outline: none; border-color: var(--accent);
  box-shadow: 0 0 0 2px rgba(88,166,255,0.15);
}
.input-hint {
  font-size: 11px; color: var(--text-muted); margin-top: 2px;
}
.run-btn {
  background: var(--lbe-green); color: #fff; border: none;
  padding: 12px 32px; border-radius: 6px; font-size: 15px;
  font-weight: 600; cursor: pointer; width: 100%;
  font-family: var(--font-sans);
}
.run-btn:hover { opacity: 0.9; }
.run-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.result-card {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 8px; padding: 20px; margin-bottom: 16px;
}
.traffic-light {
  display: inline-block; width: 14px; height: 14px;
  border-radius: 50%; margin-right: 8px; vertical-align: middle;
}
.tl-green { background: var(--green); box-shadow: 0 0 6px var(--green-glow); }
.tl-amber { background: var(--amber); box-shadow: 0 0 6px var(--amber-glow); }
.tl-red { background: var(--red); box-shadow: 0 0 6px var(--red-glow); }
.tier-badge {
  display: inline-block; font-size: 10px; font-weight: 700;
  padding: 1px 6px; border-radius: 3px; margin-left: 6px;
  font-family: var(--font-mono); vertical-align: middle;
}
.tier-1 { background: var(--green-dim); color: var(--green); }
.tier-2 { background: rgba(88,166,255,0.15); color: var(--accent); }
.tier-3 { background: var(--amber-dim); color: var(--amber); }
.tier-4 { background: var(--red-dim); color: var(--red); }
.confidence-bar {
  height: 8px; border-radius: 4px; background: var(--panel);
  overflow: hidden; margin-top: 4px;
}
.confidence-fill { height: 100%; border-radius: 4px; transition: width 0.5s; }
.caveat-box {
  background: var(--amber-dim); border: 1px solid var(--amber);
  border-radius: 6px; padding: 12px 16px; margin: 16px 0;
  font-size: 13px; color: var(--text);
}
.persona-lens {
  background: var(--panel); border: 1px solid var(--border);
  border-radius: 8px; padding: 16px; margin-bottom: 12px;
}
.persona-name {
  font-weight: 700; font-size: 14px; color: var(--text-bright);
}
.persona-role {
  font-size: 12px; color: var(--text-muted);
  font-family: var(--font-mono);
}
.section-divider {
  border: none; border-top: 1px solid var(--border);
  margin: 24px 0;
}
@media print {
  .no-print { display: none !important; }
  body { background: #fff; color: #000; }
  .result-card { border: 1px solid #ccc; break-inside: avoid; }
}
```

**Colour usage rules (inherited — no deviation):**
- `--lbe-green` → CTA/run buttons ONLY
- `--dc-black` → header background
- `--green/amber/red` → traffic light verdicts
- `--accent` → links, selected tabs, interactive highlights
- Three-tier depth: `--bg` (page) → `--surface` (cards) → `--panel` (nested)
- Four-tier text: `--text-bright` (headings) → `--text` (body) → `--text-dim` (secondary) → `--text-muted` (hints)

---

## 4. TAB ARCHITECTURE (4 tabs — locked)

| Position | ID | Label | Purpose |
|----------|-----|-------|---------|
| 1 | input | 📋 Input | Facility data entry — manual or JSON import |
| 2 | analysis | 🔍 Analysis | AI-powered screening — runs on submit, streams results |
| 3 | report | 📊 Report | Formatted screening report — printable, PI-safe |
| 4 | confidence | 🎯 Confidence | T1–T4 breakdown of every data point used |

**Tab flow:**
1. User enters facility data on Input tab (or loads demo/JSON)
2. User clicks "Run Screening" → switches to Analysis tab
3. AI processes via Anthropic API → results stream into Analysis tab
4. Structured results populate Report tab and Confidence tab
5. User can print Report tab or export as PDF

---

## 5. INPUT TAB

### 5.1 Input Schema

Each tool defines an INPUT_SCHEMA array. Each entry:

```javascript
const INPUT_SCHEMA = [
  {
    id: 'it_load_kw',
    label: 'IT Load (kW)',
    type: 'number',         // number | text | select | boolean
    required: true,
    default: null,           // null = no default (user must enter)
    demo: 2400,              // Clonshaugh demo value
    min: 0,
    max: 100000,
    step: 100,
    unit: 'kW',
    hint: 'Total IT load — servers, storage, networking',
    tier: 'T1',              // data tier when user provides this
    helpText: 'From your latest metered reading or UPS output'
  },
  // ... more fields
];
```

### 5.2 Demo Data Button

Every tool has a "Load Demo Data (Clonshaugh)" button that fills the form with the reference facility values. This lets Ann or Mark see what the output looks like before entering real data.

Demo data is ALWAYS Clonshaugh: 400 racks, 2.4 MW IT, PUE 1.50, 5 MVA MIC, 10 kV ESB Networks, Hall A/Hall B, built 2013.

### 5.3 JSON Import/Export

Every tool supports:
- **Import:** paste JSON from CPS-001 or another tool → auto-fills matching fields
- **Export:** download current inputs as JSON → feeds into other tools in the chain

Field IDs must be consistent across all tools so JSON flows between them.

### 5.4 Input Validation

Client-side validation before API call:
- Required fields present
- Numeric ranges respected
- At least one meaningful input (not all defaults)
- No API call fires until validation passes

---

## 6. ANALYSIS TAB (AI Engine)

### 6.1 API Call Pattern

```javascript
const runScreening = async (inputs) => {
  setLoading(true);
  setError(null);

  const response = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 4000,
      system: DOMAIN_PROMPT,
      messages: [{
        role: 'user',
        content: buildUserPrompt(inputs)
      }]
    })
  });

  const data = await response.json();
  // Parse structured JSON from response
  // Populate report and confidence tabs
};
```

### 6.2 Domain Prompt Structure

Every DOMAIN_PROMPT follows this skeleton:

```
You are an expert [DOMAIN ROLE] conducting a screening-level assessment
of a data centre facility in Ireland. You work for Legacy Business
Engineers Ltd (LBE), an independent technical advisory firm.

## YOUR EXPERTISE
[Extracted from module Grammar — key facts, standards, thresholds]

## CANONICAL DATA (use these values — do not substitute)
[Locked values with T1–T4 tiers from canonical data table]

## ASSESSMENT LOGIC
[Extracted from module Logic — cause-effect chains, decision trees]

## PERSONA PERSPECTIVES
[How each of the 5 personas would interpret the findings]

## OUTPUT FORMAT
Respond ONLY with a JSON object. No preamble, no markdown fences.
{
  "executive_summary": "string — 3-sentence fund-manager language",
  "traffic_light": "GREEN | AMBER | RED",
  "findings": [
    {
      "area": "string",
      "status": "PASS | FLAG | FAIL",
      "detail": "string — what was found",
      "implication": "string — so what",
      "indicative_action": "string — what to investigate next",
      "cost_range": "string — T3 indicative range or null",
      "source": "string — standard/regulation reference",
      "tier": "T1 | T2 | T3 | T4"
    }
  ],
  "persona_views": {
    "ann": "string — fund manager perspective",
    "declan": "string — ops manager perspective",
    "mark": "string — MEP engineer perspective",
    "sarah": "string — ESG analyst perspective",
    "tom": "string — QS/cost perspective"
  },
  "decision_gate": "DESKTOP_ASSESSMENT | MONITORING | DISPOSAL_ANALYSIS",
  "confidence_score": 0-100,
  "data_quality_notes": "string — what inputs were missing or estimated"
}

## LANGUAGE RULES (PI-SAFE — MANDATORY)
- Use "indicative" or "screening-level" for all cost figures
- Use "screening assessment" not "audit" or "report"
- Use "Misalignment Year" not "Stranding Year" for CRREM
- Never say "compliant" — use "aligned" or "readiness"
- Never say "should" or "must" to the client — use "consider" or "investigate"
- Every cost figure must state its tier (T1–T4) and basis
- State: "This screening does not constitute a design deliverable
  or compliance determination"
```

### 6.3 User Prompt Builder

The `buildUserPrompt(inputs)` function formats user inputs into a structured request:

```
Conduct a screening assessment for the following facility:

Facility name: {name}
Location: {location}
IT Load: {it_load_kw} kW
PUE (current): {pue_current}
[... all non-null inputs ...]

Inputs marked with * are user-provided. All others are estimated defaults.
Flag any findings that depend on estimated inputs.
```

### 6.4 Response Parsing

```javascript
const parseResponse = (data) => {
  const text = data.content
    .filter(item => item.type === 'text')
    .map(item => item.text)
    .join('');

  // Strip markdown fences if present
  const clean = text.replace(/```json\s*/g, '').replace(/```\s*/g, '').trim();

  try {
    return JSON.parse(clean);
  } catch (e) {
    setError('Analysis failed to parse. Raw response saved for review.');
    setRawResponse(text);
    return null;
  }
};
```

### 6.5 Loading State

While the API call is in flight, show:
- Animated progress indicator (not a spinner — a step-by-step status)
- "Checking [area]..." messages that cycle through the assessment areas
- Estimated time: "Screening typically takes 15–30 seconds"

### 6.6 Error Handling

| Error | User sees | Action |
|-------|-----------|--------|
| Network failure | "Unable to reach screening engine. Check connection." | Retry button |
| API error (4xx/5xx) | "Screening temporarily unavailable." | Retry button |
| Parse failure | "Analysis completed but output format unexpected." | Show raw text + retry |
| Timeout (>60s) | "Screening taking longer than expected." | Cancel + retry |

---

## 7. REPORT TAB

### 7.1 Report Structure

Every screening report follows this layout:

```
┌─────────────────────────────────────────┐
│ LBE LOGO + HEADER                       │
│ "DC Screening Assessment"               │
│ Tool name + version                     │
│ Date + facility name                    │
├─────────────────────────────────────────┤
│ EXECUTIVE SUMMARY                       │
│ Traffic light + 3-sentence summary      │
│ Decision gate recommendation            │
├─────────────────────────────────────────┤
│ CAVEAT BOX                              │
│ "This screening does not constitute..." │
├─────────────────────────────────────────┤
│ FINDINGS (per area)                     │
│ Status badge + area name                │
│ Detail + implication                    │
│ Indicative action + cost range          │
│ Source + tier                           │
├─────────────────────────────────────────┤
│ PERSONA PERSPECTIVES                    │
│ Ann / Declan / Mark / Sarah / Tom       │
├─────────────────────────────────────────┤
│ DATA QUALITY NOTES                      │
│ What was provided vs estimated          │
├─────────────────────────────────────────┤
│ CONFIDENCE PANEL (summary)              │
│ T1/T2/T3/T4 breakdown bar              │
├─────────────────────────────────────────┤
│ SIGN-OFF                                │
│ Les Murphy CEng MIEI                    │
│ Independent Technical Advisor           │
│ Legacy Business Engineers Ltd           │
│ PI Insurance: confirmed                 │
├─────────────────────────────────────────┤
│ NEXT STEP CTA                           │
│ Based on decision gate                  │
│ "Contact info@legacybe.ie"              │
└─────────────────────────────────────────┘
```

### 7.2 Print/Export

- Print button triggers `window.print()`
- Print stylesheet hides nav, tabs, input form
- Report renders cleanly on A4
- Footer: "Generated by {TOOL_ID} v{VERSION} | {date} | LBE"

---

## 8. CONFIDENCE TAB

### 8.1 Purpose

Shows the user exactly what data the screening relied on, what tier each data point carries, and where the analysis is strong vs weak. This is the "show your work" tab — it builds trust and protects LBE professionally.

### 8.2 Layout

For every data point used in the analysis:

| Data Point | Value | Source | Tier | Provided By |
|------------|-------|--------|------|-------------|
| IT Load | 2,400 kW | User input | T1 | User |
| Grid EF | 0.2241 kgCO₂/kWh | SEAI 2026 | T1 | Canonical |
| PUE | 1.50 | User input | T1 | User |
| Cooling type | DX split | User estimate | T3 | User |
| Retrofit CAPEX | €1,100/kW IT | Industry benchmark | T3 | Canonical |

### 8.3 Confidence Score Calculation

```
Score = (T1_count × 4 + T2_count × 3 + T3_count × 2 + T4_count × 1)
        / (total_count × 4) × 100
```

Display as:
- Bar chart showing T1/T2/T3/T4 distribution
- Overall percentage
- Plain English: "This screening is based on 65% verified data (T1/T2). Findings marked T3/T4 should be validated with site-specific data before any investment decision."

---

## 9. CANONICAL DATA (inherited — locked)

Same canonical data table as DC-LEARN modules. Stored as a constant in each tool:

```javascript
const CANONICAL_DATA = {
  grid_ef: { value: 0.2241, unit: 'kgCO₂/kWh', source: 'SEAI 2026', tier: 'T1' },
  carbon_tax_current: { value: 71, unit: '€/tCO₂', source: 'Budget 2025', tier: 'T1' },
  carbon_tax_2030: { value: 100, unit: '€/tCO₂', source: 'Finance Act', tier: 'T1' },
  crm_t4: { value: 149960, unit: '€/MW/yr', source: 'SEMO PCAR2829T-4', tier: 'T1' },
  electricity_price: { value: 0.12, unit: '€/kWh', source: 'CRU Q4 2024', tier: 'T2' },
  free_cooling_hours: { value: 7200, unit: 'hrs/yr', source: 'Met Éireann 30yr', tier: 'T1' },
  taxonomy_pue: { value: 1.3, unit: 'threshold', source: 'Delegated Act 2021/2139', tier: 'T1' },
  cru_renewable: { value: 80, unit: '%', source: 'CRU/2025236', tier: 'T1' },
  retrofit_capex: { value: 1100, unit: '€/kW IT', source: 'LBE screening estimate', tier: 'T3' },
  discount_rate: { value: 8, unit: '%', source: 'Fund standard hurdle', tier: 'T2' }
};
```

**STALE VALUE GUARD:** Every tool must include a validation check at build time:
```bash
grep -n '83,050\|83050\|0\.295\|63\.50' DC-TOOL-XXX.html
# Must return ZERO matches
```

---

## 10. QUALITY GATES

### QG-1: Babel Parse
Every tool must pass `@babel/parser` parse check. No exceptions.

### QG-2: Stale Value Sweep
grep for all known stale values (§9). Zero matches = pass.

### QG-3: PI-Safe Language
grep for banned terms:
```bash
grep -niP 'compliant|should|must|exact|guaranteed|audit|stranding.year' DC-TOOL-XXX.html
```
Zero matches outside of clearly negative contexts (e.g., "this is NOT an audit") = pass.

### QG-4: Demo Data Run
Load Clonshaugh demo data → run screening → verify report renders without errors.

### QG-5: Confidence Panel Accuracy
Every data point in the Confidence tab must match a CANONICAL_DATA entry or an INPUT_SCHEMA field. No orphan data points.

### QG-6: Print Test
Print preview → report fits A4 → no nav/input elements visible → footer present.

### QG-7: JSON Round-Trip
Export inputs as JSON → close tool → reopen → import JSON → all fields restored.

### QG-8: Error Recovery
Disconnect network → run screening → verify error message appears → reconnect → retry → verify success.

---

## 11. CC BUILD PROMPT TEMPLATE

Every CC session uses this structure:

```
# DC-TOOL-{XXX} — {TOOL NAME}
# Build Prompt v1 | {DATE}
# Paste into Claude Code (Sonnet)

## WORKSTREAM: Build {TOOL NAME} from factory template

## SCOPE FENCE — DO NOT CROSS
These items are ALREADY DONE. Do not rebuild, modify, or audit them:
| Item | Status |
|------|--------|
| Factory template CSS | DONE — inherited |
| BSG layers | DONE — inherited |
| Canonical data object | DONE — inherited |
| Tab architecture | DONE — inherited |

These items are OUT OF SCOPE:
- Other tools in the registry
- DC-LEARN module content changes
- Supabase/Stripe integration (separate session)

## DEVIATION RULE
If you change ANYTHING not in the TASKS list, STOP and report as DEVIATION.

## INPUTS PROVIDED:
- Factory template: DC-TOOL-000_v1_0_0.html
- Domain prompt: DC-TOOL-{XXX}_DOMAIN_PROMPT.md
- Input schema: DC-TOOL-{XXX}_INPUT_SCHEMA.json

## TASKS:
1. Copy factory template to DC-TOOL-{XXX}_v1_0_0.html
2. Replace TOOL_ID, TOOL_VERSION, TOOL_NAME constants
3. Insert DOMAIN_PROMPT from provided file
4. Insert INPUT_SCHEMA from provided file
5. Insert DEMO_DATA (Clonshaugh values matching input schema)
6. Verify Babel parse passes
7. Verify stale value sweep passes (QG-2)
8. Verify PI-safe language sweep passes (QG-3)
9. Commit to dc-learn-academy repo main branch
10. Append DC_LEARN_OPS_LOG.md entry

## VERIFICATION:
1. Babel check: PASS
2. Stale value grep: 0 matches
3. PI-safe grep: 0 matches (excluding negatives)
4. Demo data loads without error
5. TOOL_ID matches registry

## OUTPUT:
- DC-TOOL-{XXX}_v1_0_0.html → /mnt/user-data/outputs/
- OPS_LOG entry

## SHIP / NOT SHIP
```

---

## 12. TOOL CHAIN (JSON Flow)

Tools connect via JSON export/import. The chain:

```
DC-TOOL-010 (Facility Audit)
    ↓ JSON
DC-TOOL-001 (Power) + DC-TOOL-002 (Cooling)
    ↓ JSON
DC-TOOL-003 (Redundancy) + DC-TOOL-005 (UPS)
    ↓ JSON
DC-TOOL-004 (Compliance) + DC-TOOL-006 (Grid)
    ↓ JSON
DC-TOOL-007 (Gap Analysis)
    ↓ JSON
DC-TOOL-008 (Retrofit Scope)
    ↓ JSON
DC-TOOL-009 (Investment Decision) ← also feeds from DC-TOOL-013 (CRM Revenue)
    ↓ JSON
DC-TOOL-011 (Regulatory Tracker) — ongoing monitoring
DC-TOOL-012 (F-Gas Tracker) — ongoing monitoring
DC-TOOL-014 (Technology Roadmap) — future planning
```

### 12.1 Shared Field IDs (locked across all tools)

```javascript
// These field IDs must be consistent so JSON flows between tools
const SHARED_FIELDS = {
  facility_name: 'facility_name',
  facility_location: 'facility_location',
  it_load_kw: 'it_load_kw',
  rack_count: 'rack_count',
  pue_current: 'pue_current',
  pue_target: 'pue_target',
  mic_kva: 'mic_kva',
  voltage_kv: 'voltage_kv',
  build_year: 'build_year',
  cooling_type: 'cooling_type',
  ups_topology: 'ups_topology',
  redundancy_level: 'redundancy_level',
  generator_count: 'generator_count',
  renewable_pct: 'renewable_pct',
  hall_config: 'hall_config',
  total_floor_m2: 'total_floor_m2'
};
```

---

## 13. COMMERCIAL GATING

### 13.1 Access Tiers

| Tier | Tool Access | Run Limit |
|------|------------|-----------|
| Free (no auth) | Demo data only — Clonshaugh pre-loaded, no custom input | Unlimited demo |
| Founding/Professional | Full tool access | 3 runs/tool/year |
| Corporate | Full tool access + branded reports | Unlimited |
| Enterprise | Full + API access + white-label | Unlimited |

### 13.2 Implementation

Free tier: Input fields disabled. Demo button active. "Upgrade to enter your facility data" message on input fields.

Paid tier: Supabase auth check → if valid licence → enable inputs. Run counter stored in Supabase `tool_runs` table.

### 13.3 Auth Integration (Phase 2 — separate CC session)

```javascript
// Check auth before enabling inputs
const checkAccess = async () => {
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) return 'free';
  const { data: licence } = await supabase
    .from('licences')
    .select('plan, tool_runs_remaining')
    .eq('user_id', user.id)
    .single();
  return licence?.plan || 'free';
};
```

Auth is Phase 2. Phase 1 tools ship without auth — all features enabled. Gating added in a single batch session after all tools are built.

---

## 14. TERMINOLOGY (inherited from DC-LEARN — enforced)

| Use This | Never This |
|----------|-----------|
| Screening assessment | Audit / report / certification |
| Misalignment Year | Stranding Year |
| CRU Readiness | CRU Compliance |
| Indicative / estimated / screening-level | Exact / guaranteed / certified |
| Aligned | Compliant |
| Consider / investigate | Should / must |
| Les Murphy CEng MIEI | Les McGuinness |
| MEP Engineer (Mark) | Electrical Engineer |
| Hall A / Hall B | Hall 1 / Hall 2 |

---

## 15. DEPLOYMENT

### 15.1 File Naming
`DC-TOOL-{XXX}_v{MAJOR}_{MINOR}_{PATCH}.html`

Example: `DC-TOOL-004_v1_0_0.html`

### 15.2 Netlify
Same site as DC-LEARN: learn.legacybe.ie
Tools deployed to: learn.legacybe.ie/tools/
URL pattern: learn.legacybe.ie/tools/dc-tool-004.html

### 15.3 GitHub
Same repo: dc-learn-academy
Tools in /tools/ subdirectory

### 15.4 Version Bump
On EVERY change — 4 reference points:
1. `<title>` tag
2. TOOL_VERSION constant
3. BSG Layer 1 version string
4. BSG Layer 2 version string

---

## 16. BUILD SEQUENCE (locked)

| Priority | Tool | Sessions | Dependency |
|----------|------|----------|------------|
| 0 | Factory Template (DC-TOOL-000) | This session | None |
| 1 | Compliance Checker (DC-TOOL-004) | 1 Opus + 1 CC | Template |
| 2 | Grid Headroom (DC-TOOL-006) | 1 CC | Template + domain prompt |
| 3 | Redundancy Gap (DC-TOOL-003) | 1 CC | Template + domain prompt |
| 4 | UPS Adequacy (DC-TOOL-005) | 1 CC | Template + domain prompt |
| 5 | Retrofit Scope (DC-TOOL-008) | 1 Opus + 1 CC | Template + domain prompt |
| 6 | Gap Analysis (DC-TOOL-007) | 1 CC | Template + domain prompt |
| 7 | F-Gas Tracker (DC-TOOL-012) | 1 CC | Template + domain prompt |
| 8 | CRM Revenue (DC-TOOL-013) | 1 CC | Template + domain prompt |
| 9 | Facility Audit (DC-TOOL-010) | 1 CC | Template + domain prompt |
| 10 | Regulatory Tracker (DC-TOOL-011) | 1 Opus + 1 CC | Template + domain prompt |
| 11 | Power Screener (DC-TOOL-001) | 1 CC | Template + domain prompt |
| 12 | Cooling Screener (DC-TOOL-002) | 1 CC | Template + domain prompt |
| 13 | Investment Model (DC-TOOL-009) | 1 CC | Extend ROI-001 |
| 14 | Roadmap Generator (DC-TOOL-014) | 1 CC | Template + domain prompt |
| 15 | Auth + gating batch | 1 CC | All tools built |
| 16 | Stripe metering | 1 CC | Auth done |

Domain prompts for tools 1–4 extracted in one Opus batch session.
Domain prompts for tools 5–9 extracted in a second Opus batch session.
Domain prompts for tools 10–14 extracted in a third Opus batch session.

---

## DOCUMENT CONTROL

| Field | Value |
|-------|-------|
| Version | 1.0 |
| Date | 13 April 2026 |
| Author | LM + Claude (Opus) |
| Status | ACTIVE — governs all DC-TOOL builds |
| Companion | DC-TOOL-000_v1_0_0.html (factory template) |
| Parent | DC_LEARN_SERIES_SPEC_v1_4.md |
| Parent | DC_LEARN_CANONICAL_ARCHITECTURE_v1_1.md |

---

*DC_TOOL_FACTORY_SPEC v1.0 | 13 April 2026*
*Single source of truth for all AI-powered screening tool builds*
