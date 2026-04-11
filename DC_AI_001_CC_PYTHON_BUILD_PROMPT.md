# DC-AI-001 — Python Build Prompt
# Paste this into Claude Code. Attach all 5 .md files alongside it.

## WHAT YOU ARE BUILDING

A single-file interactive **learning module** called DC-AI-001.
NOT a calculator. NOT a screening tool. NOT an agent.
A learning module with 6 tabs, 9 levels, and 264 KB of pre-written content.

The output file is: `DC-AI-001_v1_0_0.html`
Expected size: 3,000–5,000 lines, 400–800 KB.

## WHAT YOU HAVE

5 files are attached:

1. **DC_AI_001_BUILDER_PROMPT_v1_0.md** — architecture spec (read this for component structure)
2. **DNA_DC_AI_001_v1_0.md** — ALL content: 9 levels, 45 facts, 27 questions, 5 personas/level, 9 scenarios, 40 glossary, 16 bibliography. This is 2,040 lines of pre-written content. You embed it. You do NOT rewrite it.
3. **DC_AI_VERTICAL_CONFIG_v1_3.md** — branding, colours, fonts, persona definitions
4. **DC_AI_DNA_SCHEMA_v1_0.md** — field contract
5. **LBE_LOGO_CONST.md** — base64 logo string

## HOW TO BUILD IT

Use Python to assemble the HTML file. This is how all 16 DC-LEARN modules were built.

### Phase 1: Extract content from DNA into Python dicts/lists

Read DNA_DC_AI_001_v1_0.md and extract into Python data structures:
- `levels` — list of 9 dicts, each containing grammar.facts, logic.causeAndEffect, rhetoric entries, scenario, cascadeCheck
- `so_what_map` — dict of 45 entries
- `rhetoric_takeaways` — nested dict (L1–L9, 5 personas each)
- `assessment_questions` — list of 27 question dicts
- `glossary` — list of 40 term dicts
- `bibliography` — list of 16 source dicts

### Phase 2: Write HTML sections as Python raw strings

Each section is a Python `r'''...'''` block. NEVER use f-strings for JSX.

**Section A — HTML head + CSS** (~300 lines)
```python
html_head = r'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>DC-AI-001: Power Density | DC-AI v1.0</title>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/react/18.2.0/umd/react.production.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.2.0/umd/react-dom.production.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/babel-standalone/7.23.9/babel.min.js"></script>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    /* ALL CSS HERE — dark/light theme variables, layout, tabs, cards */
  </style>
</head>
<body>
<div id="root"></div>
'''
```

**Section B — Logo + base64 constants** (~50 lines)
```python
# Read from LBE_LOGO_CONST.md
# Place in a plain <script> tag BEFORE the Babel block
logo_script = '<script>\nconst LOGO_SRC = "' + logo_base64 + '";\n</script>\n'
```

**Section C — Data constants as JS** (~1,500+ lines)
```python
# Convert the Python data structures from Phase 1 into JavaScript
# Use json.dumps() for safe serialisation, then wrap in const declarations
data_script = '<script type="text/babel">\n'
data_script += 'const TOOL_VERSION = "1.0.0";\n'
data_script += 'const LEVELS = ' + json.dumps(levels, ensure_ascii=False, indent=2) + ';\n'
data_script += 'const SO_WHAT_MAP = ' + json.dumps(so_what_map, ensure_ascii=False, indent=2) + ';\n'
# ... etc for all constants
```

**Section D — React components** (~1,500 lines)
```python
components_jsx = r'''
// ═══ UTILITY FUNCTIONS ═══
function safeStore(key, val) { ... }
function safeLoad(key, fallback) { ... }
function shuffleArray(arr) { /* Fisher-Yates — copy only, never mutate source */ }

// ═══ COMPONENTS ═══
function Header({ theme, setTheme }) { ... }
function LevelSelector({ levels, selectedLevel, setSelectedLevel }) { ... }
function TabBar({ stage, setStage }) { ... }
function ChainTab({ levels, selectedLevel, setSelectedLevel }) { ... }
function GrammarTab({ level }) { ... }
function LogicTab({ level }) { ... }
function RhetoricTab({ level }) { ... }
function FieldChallenge({ scenario }) { ... }
function AssessmentTab({ questions }) { ... }
function BSGTab({ glossary, bibliography }) { ... }

// ═══ APP ═══
function App() {
  const [selectedLevel, setSelectedLevel] = React.useState(0);
  const [stage, setStage] = React.useState('chain');
  const [theme, setTheme] = React.useState('dark');
  // ... render with all tabs
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
'''
```

**Section E — Close tags**
```python
html_close = '\n</script>\n</body>\n</html>'
```

### Phase 3: Assemble

```python
full_html = html_head + logo_script + data_script + components_jsx + html_close

with open('DC-AI-001_v1_0_0.html', 'w', encoding='utf-8') as f:
    f.write(full_html)
```

### Phase 4: Verify

```python
import subprocess
# Babel parse check
result = subprocess.run(['node', '-e', '''
  const babel = require("@babel/standalone");
  const fs = require("fs");
  const html = fs.readFileSync("DC-AI-001_v1_0_0.html", "utf8");
  const match = html.match(/<script type="text\\/babel">([\s\S]*?)<\\/script>/);
  if (!match) { console.log("FAIL: no babel block found"); process.exit(1); }
  try { babel.transform(match[1], {presets:["react"]}); console.log("PASS: Babel parse OK"); }
  catch(e) { console.log("FAIL:", e.message); process.exit(1); }
'''])
```

Also verify:
- Line count (target 3,000–5,000)
- `grep -c '"term":' DC-AI-001_v1_0_0.html` → should be 45
- `grep -c '"q":' DC-AI-001_v1_0_0.html` → should be 27
- `grep -c 'asset_management' DC-AI-001_v1_0_0.html` → should be ≥18

### Phase 5: Copy to outputs
```
cp DC-AI-001_v1_0_0.html /mnt/user-data/outputs/
```

## CRITICAL RULES
- CDN: cdnjs.cloudflare.com ONLY (never unpkg)
- Python r''' raw strings for JSX — NEVER f-strings (G-NEW-55)
- Base64 strings in plain <script> BEFORE the Babel block
- json.dumps() with ensure_ascii=False for UTF-8 characters
- Fisher-Yates shuffle in RENDER PATH only — never mutate source array
- Every word of content comes from the DNA. Zero fabrication.
- 5 personas: Conor (asset_management), Helena (technology), Eoin (technical), Rachel (compliance), Padraig (cost)
- 6 tabs: Chain, Grammar, Logic, Rhetoric, Assessment, BSG
- 9 levels with icons from the DNA
- Series nav: "Module 1 of 8 · DC-AI v1.0"
- Dark/light theme toggle

## DO NOT
- Build a calculator or screening tool
- Invent content, calculations, or golden tests
- Call it DC-AGENT-anything — it is DC-AI-001
- Use unpkg
- Skip any of the 45 facts, 27 questions, or 45 persona entries
- Put base64 inside the Babel block

## START
Read the DNA file first. Extract all content into Python data structures.
Then build section by section. Assemble. Verify. Ship.
