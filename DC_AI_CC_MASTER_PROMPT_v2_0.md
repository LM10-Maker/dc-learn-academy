# DC-AI CC MASTER PROMPT v2.0
# Builder Agent — DNA YAML + Template → Finished Module
# Paste into Claude Code (Sonnet)
# Upload: DNA YAML + Feynman JSON + DC-AI-TEMPLATE_v2_0_0.html (from repo)
# Version: 2.0 | 14 April 2026

---

## MODEL TIER: Sonnet — mechanical assembly, not content judgement

## WORKSTREAM: Build DC-AI-[NNN] v1.0.0 from DNA YAML + Feynman JSON + template

## SCOPE FENCE — DO NOT CROSS
- DO NOT modify any content from the DNA YAML — paste exactly as provided
- DO NOT rewrite, improve, or rephrase any grammar fact, persona entry, or assessment question
- DO NOT change the template architecture, CSS, or component structure
- DO NOT improvise engineering values, cost figures, or regulatory references
- DO NOT invent content that is not in the DNA YAML
- Content judgement was completed upstream. Your job is assembly.

## DEVIATION RULE
If the DNA YAML is missing a required field, STOP and report as DEVIATION.
Do not fill gaps. Content gaps go back to the SMCA (Opus).

---

## FILES REQUIRED

1. `DC-AI-TEMPLATE_v2_0_0.html` — canonical template (from repo)
2. `DNA_DC_AI_[NNN]_v[X]_[Y].yaml` — verified content (uploaded)
3. `DC_AI_[NNN]_FEYNMAN_v1_0.json` — Feynman 3-layer content (uploaded)

---

## PRE-BUILD: Parse and Count

Read the DNA YAML. Report these counts. ALL must match or STOP.

```
Levels:              9 (id L1–L9)
Grammar facts:       45 (5 per level)
soWhat entries:      45 (1 per fact)
C&E entries:         18+ (2+ per level)
Persona entries:     45 (5 personas × 9 levels)
Weakest links:       9
Field challenges:    9 (scenario per level)
Cascade checks:      9 (JavaScript function per level)
CrossRefs:           9
Assessment Qs:       27 (3 per level: 1 grammar, 1 logic, 1 rhetoric)
clockQuotes:         9 (may be empty — that's OK)
Glossary terms:      30–50
Bibliography entries: 10–20
Diagram specs:       3–5
```

Read the Feynman JSON. Verify: 45 entries, 9 levels, each with
{term, analogy, firstPrinciples, theTest}. Terms must match DNA facts.

---

## BUILD METHOD

Python file-write using r''' raw strings. NEVER f-strings for JSX.
Build script should be under 200 lines. Run incrementally — write,
verify section, continue.

---

## TASKS (in order)

### Task 1: Copy Template and Replace Metadata

```python
# Copy template
cp DC-AI-TEMPLATE_v2_0_0.html DC-AI-[NNN]_v1_0_0.html

# Replace in ALL locations (grep to find count first):
# TOOL_ID: "DC-AI-TEMPLATE" → "DC-AI-[NNN]"
# TOOL_VERSION: "2.0.0" → "1.0.0"
# Title in <title> tag
# BSG L1 window.onerror string
# BSG L2 ErrorBoundary render string
# Header subtitle
# Footer
# Tab 1 label → from DNA meta.chain_tab_label
```

Version must appear in ALL 5 reference points:
1. `<title>` tag
2. `TOOL_VERSION` constant
3. BSG L1 `window.onerror`
4. BSG L2 `ErrorBoundary` render
5. CSS comment header

### Task 2: Inject Content Data

From the DNA YAML, write these JavaScript constants:

**LEVELS array** — 9 entries. Each level object must include ALL fields:
```javascript
{
  level: 1,
  id: "L1",
  title: "...",
  icon: "...",
  subtitle: "...",
  plainEnglish: "...",
  sourceNote: "...",
  retrofitRelevance: "...",
  clockQuote: "...",
  crossRefs: [...],
  grammar: {
    facts: [
      { term:"...", definition:"...", plain:"...", number:"...", standard:"...", soWhat:"..." }
    ],
    whatItLooksLike: "...",
    siteChecklist: [...]
  },
  logic: {
    causeAndEffect: [ { cause:"...", effect:"...", insight:"..." } ],
    constraintLesson: "...",
    weakestLink: { component:"...", whyItFails:"...", whatToMeasure:"..." }
  },
  rhetoric: {
    asset_management: "...",
    technology: "...",
    technical: "...",
    compliance: "...",
    cost: "..."
  },
  scenario: {
    whoShouldCare: ["conor","eoin",...],
    title: "...",
    situation: "...",
    challenge: "...",
    fix: "..."
  },
  cascadeCheck: function(inputs) { ... }
}
```

**CRITICAL FIELD NAME RULES** (DC-AI-001 defects — prevent recurrence):

| Field in DNA | Field in JS | Notes |
|---|---|---|
| scenario.situation | scenario.situation | NOT narrative |
| scenario.challenge | scenario.challenge | NOT question |
| scenario.fix | scenario.fix | NOT answer |
| rhetoric keys | asset_management, technology, technical, compliance, cost | NOT declan/ann/mark/sarah/tom |
| assessment stage | grammar, logic, rhetoric | NOT knowledge/calculation/judgement |

**ASSESSMENT_QUESTIONS** — 27 entries:
```javascript
{
  level: 1,
  id: "QAI[NNN]-1",
  stage: "grammar",    // MUST be grammar/logic/rhetoric — NEVER knowledge/calculation/judgement
  q: "...",
  options: ["A...", "B...", "C...", "D..."],
  correct: 0,          // 0-indexed position
  explain: "..."
}
```

**FEYNMAN_DATA** — inject after LEVELS, before ASSESSMENT_QUESTIONS:
```javascript
const FEYNMAN_DATA = {
  "L1": [ {term:"...", analogy:"...", firstPrinciples:"...", theTest:"..."}, ... ],
  "L2": [ ... ],
  ...
};
```

**SO_WHAT_MAP** — from rhetoric entries per level:
```javascript
const SO_WHAT_MAP = {
  "L1": { asset_management:"...", technology:"...", technical:"...", compliance:"...", cost:"..." },
  ...
};
```

**GLOSSARY** and **BIBLIOGRAPHY** — from DNA YAML companion sections.

### Task 3: Wire Feynman into GrammarPanel

The AssistBar component renders a 3-step Clarify feature. Wire FEYNMAN_DATA:

```javascript
// Inside AssistBar({fact, level, stage}) — the clarifyContent array:
const clarifyContent = [
  {label:"Think of it like… (1/3)", text: (() => {
    const fe = FEYNMAN_DATA[level.id] && FEYNMAN_DATA[level.id].find(e => e.term === fact.term);
    return fe ? fe.analogy : (fact ? fact.plain : '');
  })()},
  {label:"From the ground up… (2/3)", text: (() => {
    const fe = FEYNMAN_DATA[level.id] && FEYNMAN_DATA[level.id].find(e => e.term === fact.term);
    return fe ? fe.firstPrinciples : (fact ? fact.number : '');
  })()},
  {label:"You understand this when… (3/3)", text: (() => {
    const fe = FEYNMAN_DATA[level.id] && FEYNMAN_DATA[level.id].find(e => e.term === fact.term);
    const question = fe ? fe.theTest : '';
    const answer = fact && fact.soWhat ? fact.soWhat : '';
    return question + (answer ? '\n\n✓ The key insight: ' + answer : '');
  })()}
];
```

**CRITICAL**: The variable is `fact` not `f`. AssistBar receives `{fact, level, stage}` as props.

The clarify text div must have `whiteSpace:'pre-line'` for line breaks to render:
```jsx
<div style={{fontSize:13,color:'var(--text)',lineHeight:1.8,whiteSpace:'pre-line'}}>
  {clarifyContent[clarifyStep].text}
</div>
```

### Task 4: Wire whoShouldCare for Field Challenges

Every scenario must include a `whoShouldCare` array with persona keys.
The FieldChallengesTab filters on this field.

DC-AI persona keys: `conor`, `helena`, `eoin`, `rachel`, `padraig`

If the DNA YAML does not include whoShouldCare, assign based on
scenario content — but flag as DEVIATION.

### Task 5: Wire Persona Colours in Field Challenges

The PERSONA_FILTERS in FieldChallengesTab must include colour and bg:
```javascript
const PERSONA_FILTERS=[
  {key:'all',     label:'All',      role:'',              color:'var(--accent)', bg:'rgba(91,155,213,.15)'},
  {key:'conor',   label:'Conor',    role:'Asset Manager', color:'var(--accent)', bg:'rgba(91,155,213,.15)'},
  {key:'helena',  label:'Helena',   role:'CTO',           color:'#e879a0',       bg:'rgba(232,121,160,.15)'},
  {key:'eoin',    label:'Eoin',     role:'MEP Engineer',  color:'var(--green)',   bg:'rgba(34,197,94,.15)'},
  {key:'rachel',  label:'Rachel',   role:'ESG Director',  color:'#2dd4bf',       bg:'rgba(45,212,191,.15)'},
  {key:'padraig', label:'Padraig',  role:'QS / Cost',     color:'#fb923c',       bg:'rgba(251,146,60,.15)'},
];
```

Active button styling:
```jsx
const isActive = filterPersona===p.key;
const activeStyle = isActive ? {borderColor:p.color, color:p.color, background:p.bg, fontWeight:600} : {};
```

### Task 6: Series Navigation

From DNA meta:
```javascript
// prev/next module links
const prevModule = meta.prev_module;  // null for first module
const nextModule = meta.next_module;  // e.g. "DC-AI-002"
const seriesPosition = meta.series_position;  // e.g. 1
const seriesTotal = meta.series_total;  // e.g. 8
```

### Task 7: Hero Section

- Module title from DNA meta.title
- Hero disclaimer from DNA meta.hero_disclaimer
- Tab 1 label from DNA meta.chain_tab_label
- Do NOT use a base64 hero image — keep the gradient placeholder from template

### Task 8: Kate Kelly Protagonist

DNA meta includes:
```yaml
protagonist: "Kate Kelly"
protagonist_role: "Fund Asset Manager"
```

If clockQuotes reference the protagonist, use this name.
If clockQuotes are empty (""), leave them empty — they will be populated
in a later content session.

---

## VERIFICATION (all must PASS before SHIP)

```bash
# 1. Babel parse
node -e "
const fs = require('fs');
const {parse} = require('@babel/parser');
const html = fs.readFileSync('DC-AI-[NNN]_v1_0_0.html','utf8');
const m = html.match(/<script type=\"text\/babel\">([\s\S]*?)<\/script>/);
try { parse(m[1], {sourceType:'module', plugins:['jsx']}); console.log('BABEL: PASS'); }
catch(e) { console.log('BABEL: FAIL — '+e.message); process.exit(1); }
"

# 2. Content counts
grep -c '"term":' DC-AI-[NNN]_v1_0_0.html          # expect ≥45 (LEVELS) + 45 (FEYNMAN)
grep -c '"stage": "grammar"' DC-AI-[NNN]_v1_0_0.html  # expect 9
grep -c '"stage": "logic"' DC-AI-[NNN]_v1_0_0.html    # expect 9
grep -c '"stage": "rhetoric"' DC-AI-[NNN]_v1_0_0.html # expect 9
grep -c 'whoShouldCare' DC-AI-[NNN]_v1_0_0.html       # expect 9

# 3. No stale field names
grep -c '"tier":' DC-AI-[NNN]_v1_0_0.html              # expect 0
grep -c 'scenario.narrative' DC-AI-[NNN]_v1_0_0.html   # expect 0
grep -c 'scenario.answer' DC-AI-[NNN]_v1_0_0.html      # expect 0
grep -c 'f\.term' DC-AI-[NNN]_v1_0_0.html              # expect 0 in FEYNMAN lookup

# 4. Version consistency
grep 'DC-AI-[NNN]' DC-AI-[NNN]_v1_0_0.html | head -6   # all 5 refs present

# 5. No template placeholders remaining
grep -c 'LEVEL_TITLE\|PLACEHOLDER\|DC-AI-TEMPLATE' DC-AI-[NNN]_v1_0_0.html  # expect 0

# 6. Stale values
grep -c '83,050\|83050' DC-AI-[NNN]_v1_0_0.html        # expect 0
grep -c 'Stranding Year' DC-AI-[NNN]_v1_0_0.html       # expect 0
grep -c 'CRU Compliance' DC-AI-[NNN]_v1_0_0.html       # expect 0
```

ALL checks must PASS. Fix any failures before presenting.

---

## DC-AI-001 DEFECT REGISTER (prevent recurrence)

These defects occurred in the DC-AI-001 build. Each is now a check above.

| # | Defect | Root Cause | Prevention |
|---|--------|-----------|------------|
| 1 | Assessment not colour-coded | Data used `tier` not `stage` | Check 3: grep for `"tier":` = 0 |
| 2 | Field challenges empty | Data used `situation/challenge/fix`, render expected `narrative/question/answer` | Render now uses correct data field names |
| 3 | Persona filter shows 0 | No `whoShouldCare` in scenario data | Check 2: grep whoShouldCare = 9 |
| 4 | Feynman showed duplicate text | FEYNMAN_DATA not injected, fallback to existing fields | Check 2: term count ≥ 90 (45 LEVELS + 45 FEYNMAN) |
| 5 | Feynman lookup failed | Used `f.term` but AssistBar prop is `fact` | Check 3: grep f\.term = 0 |
| 6 | Stage colours undefined | stageColours maps grammar/logic/rhetoric but data had knowledge/calculation/judgement | Check 3: grep "tier" = 0 |
| 7 | CC modified file in place | CC renamed v3.2.0 contents instead of creating v4.0.0 | Explicit instruction: save as new filename |
| 8 | CC pushed to branch not main | Default CC behaviour | Explicit instruction: push to main |

---

## OUTPUT FILES
- `DC-AI-[NNN]_v1_0_0.html` → push to dc-learn-academy main
- Append to DC_LEARN_OPS_LOG.md (if in repo)

## SESSION REPORT FORMAT
```
### WHAT I WAS ASKED TO DO
Build DC-AI-[NNN] from DNA YAML + Feynman JSON + template.

### WHAT I ACTUALLY DID
[list every constant injected, every component wired]

### DEVIATIONS FROM SCOPE
[anything not in the DNA — or "None"]

### VERIFICATION RESULTS
[all 6 check groups with counts]

### SHIP / NOT SHIP
```

---

## QUICK REFERENCE: DC-AI vs DC-LEARN DIFFERENCES

| Feature | DC-LEARN | DC-AI |
|---------|----------|-------|
| Personas | declan, ann, mark, sarah, tom | conor, helena, eoin, rachel, padraig |
| Persona colours | steel blue, rose, green, teal, orange | Same colours, different names |
| Technical persona | Mark (MEP Engineer) | Eoin (MEP Retrofit Engineer) |
| Primary reader | Declan (Ops) | Conor (Fund Asset Manager) |
| Reference facility | Clonshaugh — 400 racks, 2.4 MW, 6 kW/rack | Clonshaugh — Hall A legacy, Hall B AI retrofit target |
| Series size | 16 modules (000–015) | 8 modules (001–008) |
| Protagonist | None / The Data Centre Clock | Kate Kelly / The AI Clock |
| Assessment stages | grammar, logic, rhetoric | Same |
| Field challenge fields | narrative, question, answer | situation, challenge, fix |

---

*DC-AI CC Master Prompt v2.0 | 14 April 2026*
*One paste. One session. One module out.*

---

## ADDENDUM — A+ FIXES (14 April 2026)

### Git Discipline
Commit and push directly to main. Do NOT create a feature branch.
```bash
git add DC-AI-[NNN]_v1_0_0.html
git commit -m "feat: DC-AI-[NNN] v1.0.0 — [Module Title]"
git push origin main
```

### Chain Card Component Field (≤25 chars)
Every level in LEVELS may include a `component` field for the chain tab
card subtitle. This field renders as small mono text. Maximum 25 characters.
After writing LEVELS, run:
```python
for lvl in levels:
    c = lvl.get('component', '')
    if len(c) > 25:
        print(f"FAIL: L{lvl['level']} component '{c}' = {len(c)} chars (max 25)")
```
Fix any over 25 before Babel check.

### cascadeCheck is a JavaScript Function Body
The DNA YAML `cascadeCheck` field contains a raw JavaScript function.
In the LEVELS array, inject it as an actual function — NOT a string:
```javascript
// CORRECT:
cascadeCheck: function(inputs) {
  var targetKW = inputs.targetKW || 40;
  // ... function body from DNA YAML ...
  return { pass: true, reason: "..." };
}

// WRONG:
cascadeCheck: "function(inputs) { ... }"
```
Verify: `grep 'cascadeCheck: "' DC-AI-[NNN]_v1_0_0.html` must return 0 matches.
Add to verification checks:
```bash
# 7. cascadeCheck is function not string
grep -c 'cascadeCheck: "' DC-AI-[NNN]_v1_0_0.html   # expect 0
grep -c 'cascadeCheck: function' DC-AI-[NNN]_v1_0_0.html  # expect 9
```

---

*Addendum applied. Master Prompt is now A+.*
