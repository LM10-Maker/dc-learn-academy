#!/usr/bin/env python3
"""
polish_02_level_selector.py
Fix level selector: 80x72px buttons, 8px gap, grammar selected state,
L1-L9 corner badge, hover effect, progress dots, visitedStages state in App.
Reads/writes DC-AI-001_v1_1_0.html in place.
"""

TARGET = '/home/user/dc-learn-academy/DC-AI-001_v1_1_0.html'

with open(TARGET, 'r', encoding='utf-8') as f:
    html = f.read()

replaced = []

def rep(old, new, tag):
    global html
    if old not in html:
        raise ValueError(f'[MISS:{tag}]')
    html = html.replace(old, new, 1)
    replaced.append(tag)

# ==============================================================================
# 1. Level selector CSS — row gap, button sizing, selected/hover states,
#    badge, and progress dots
# ==============================================================================

rep(
    "    .level-selector-row {\n      display: flex;\n      gap: 0.4rem;\n      overflow-x: auto;\n      padding-bottom: 2px;\n      scrollbar-width: none;\n    }\n    .level-selector-row::-webkit-scrollbar { display: none; }\n    .level-btn {\n      flex-shrink: 0;\n      display: flex;\n      flex-direction: column;\n      align-items: center;\n      gap: 2px;\n      padding: 0.45rem 0.75rem;\n      border-radius: var(--radius-md);\n      background: var(--surface-2);\n      border: 1px solid var(--border);\n      color: var(--text-muted);\n      font-size: 0.72rem;\n      font-weight: 500;\n      transition: all var(--transition);\n      min-width: 70px;\n      cursor: pointer;\n    }\n    .level-btn:hover {\n      background: var(--accent-dim);\n      border-color: var(--accent);\n      color: var(--accent);\n    }\n    .level-btn.active {\n      background: var(--accent);\n      border-color: var(--accent);\n      color: #fff;\n      box-shadow: 0 2px 8px rgba(59,130,246,0.3);\n    }\n    .level-btn-icon { font-size: 1.1rem; line-height: 1; }\n    .level-btn-id { font-size: 0.62rem; opacity: 0.7; }\n    .level-btn-label { font-size: 0.68rem; text-align: center; max-width: 72px; line-height: 1.2; }",
    "    .level-selector-row {\n      display: flex;\n      gap: 8px;\n      overflow-x: auto;\n      padding-bottom: 6px;\n      scrollbar-width: none;\n      scroll-snap-type: x mandatory;\n    }\n    .level-selector-row::-webkit-scrollbar { display: none; }\n    .level-btn {\n      flex-shrink: 0;\n      display: flex;\n      flex-direction: column;\n      align-items: center;\n      justify-content: center;\n      gap: 3px;\n      width: 80px;\n      height: 72px;\n      padding: 0.35rem 0.25rem 0.3rem;\n      border-radius: var(--radius-md);\n      background: var(--panel);\n      border: 1px solid var(--border);\n      color: var(--text-dim);\n      font-size: 0.72rem;\n      font-weight: 500;\n      transition: all var(--transition-level);\n      cursor: pointer;\n      position: relative;\n      scroll-snap-align: start;\n    }\n    .level-btn:hover {\n      background: var(--surface);\n      border-color: var(--accent);\n      color: var(--text-bright);\n      box-shadow: var(--shadow);\n    }\n    .level-btn.active {\n      background: rgba(37,99,235,0.15);\n      border: 2px solid var(--grammar);\n      color: var(--text-bright);\n    }\n    .level-btn-badge {\n      position: absolute;\n      top: 4px;\n      left: 5px;\n      font-size: 0.56rem;\n      font-weight: 700;\n      color: var(--text-muted);\n      letter-spacing: 0.02em;\n      line-height: 1;\n    }\n    .level-btn.active .level-btn-badge { color: var(--grammar); }\n    .level-btn-icon { font-size: 1.1rem; line-height: 1; }\n    .level-btn-id { display: none; }\n    .level-btn-label { font-size: 0.64rem; text-align: center; max-width: 70px; line-height: 1.2; color: inherit; }\n    .level-progress-dots {\n      display: flex;\n      gap: 3px;\n      justify-content: center;\n      margin-top: 2px;\n    }\n    .level-progress-dot {\n      width: 5px;\n      height: 5px;\n      border-radius: 50%;\n      background: var(--border-2);\n      transition: background 0.2s ease;\n    }\n    .level-progress-dot.grammar.done  { background: var(--grammar); }\n    .level-progress-dot.logic.done    { background: var(--logic); }\n    .level-progress-dot.rhetoric.done { background: var(--rhetoric); }",
    'level selector CSS'
)

# ==============================================================================
# 2. LevelSelector JSX — add badge span, progress dots, visitedStages prop
# ==============================================================================

rep(
    "function LevelSelector({ selectedLevel, setSelectedLevel }) {\n  return (\n    <div className=\"level-selector-wrap\">\n      <div className=\"level-selector-label\">Select Level</div>\n      <div className=\"level-selector-row\">\n        {LEVELS.map(function(lvl, idx) {\n          return (\n            <button\n              key={lvl.id}\n              className={'level-btn' + (selectedLevel === idx ? ' active' : '')}\n              onClick={() => { setSelectedLevel(idx); safeStore('level', idx); }}\n            >\n              <span className=\"level-btn-icon\">{lvl.icon}</span>\n              <span className=\"level-btn-id\">{lvl.id}</span>\n              <span className=\"level-btn-label\">{lvl.title}</span>\n            </button>\n          );\n        })}\n      </div>\n    </div>\n  );\n}",
    "function LevelSelector({ selectedLevel, setSelectedLevel, visitedStages }) {\n  return (\n    <div className=\"level-selector-wrap\">\n      <div className=\"level-selector-label\">Select Level</div>\n      <div className=\"level-selector-row\">\n        {LEVELS.map(function(lvl, idx) {\n          var vs = (visitedStages && visitedStages[idx]) || {};\n          return (\n            <button\n              key={lvl.id}\n              className={'level-btn' + (selectedLevel === idx ? ' active' : '')}\n              onClick={() => { setSelectedLevel(idx); safeStore('level', idx); }}\n            >\n              <span className=\"level-btn-badge\">{lvl.id}</span>\n              <span className=\"level-btn-icon\">{lvl.icon}</span>\n              <span className=\"level-btn-label\">{lvl.title}</span>\n              <div className=\"level-progress-dots\">\n                <span className={'level-progress-dot grammar' + (vs.grammar  ? ' done' : '')} />\n                <span className={'level-progress-dot logic'   + (vs.logic    ? ' done' : '')} />\n                <span className={'level-progress-dot rhetoric'+ (vs.rhetoric ? ' done' : '')} />\n              </div>\n            </button>\n          );\n        })}\n      </div>\n    </div>\n  );\n}",
    'LevelSelector JSX'
)

# ==============================================================================
# 3. App component — add visitedStages state + useEffect to track stage visits
# ==============================================================================

rep(
    "function App() {\n  var [theme, setTheme] = React.useState(safeLoad('theme', 'dark'));\n  var [selectedLevel, setSelectedLevel] = React.useState(safeLoad('level', 0));\n  var [activeTab, setActiveTab] = React.useState(safeLoad('tab', 'chain'));\n\n  // Apply theme to document\n  React.useEffect(function() {\n    document.documentElement.setAttribute('data-theme', theme);\n  }, [theme]);",
    "function App() {\n  var [theme, setTheme] = React.useState(safeLoad('theme', 'dark'));\n  var [selectedLevel, setSelectedLevel] = React.useState(safeLoad('level', 0));\n  var [activeTab, setActiveTab] = React.useState(safeLoad('tab', 'chain'));\n  var [visitedStages, setVisitedStages] = React.useState(safeLoad('visitedStages', {}));\n\n  // Apply theme to document\n  React.useEffect(function() {\n    document.documentElement.setAttribute('data-theme', theme);\n  }, [theme]);\n\n  // Track stage completion dots — mark grammar/logic/rhetoric when tab visited\n  var STAGE_MAP = { grammar: 'grammar', logic: 'logic', rhetoric: 'rhetoric' };\n  var levelIdx0 = Math.max(0, Math.min(LEVELS.length - 1, selectedLevel));\n  React.useEffect(function() {\n    if (STAGE_MAP[activeTab]) {\n      setVisitedStages(function(prev) {\n        var next = Object.assign({}, prev);\n        next[levelIdx0] = Object.assign({}, next[levelIdx0] || {});\n        next[levelIdx0][STAGE_MAP[activeTab]] = true;\n        safeStore('visitedStages', next);\n        return next;\n      });\n    }\n  }, [activeTab, levelIdx0]);",
    'App visitedStages state'
)

# ==============================================================================
# 4. Pass visitedStages to LevelSelector in App render
# ==============================================================================

rep(
    "        <LevelSelector selectedLevel={levelIdx} setSelectedLevel={setSelectedLevel} />",
    "        <LevelSelector selectedLevel={levelIdx} setSelectedLevel={setSelectedLevel} visitedStages={visitedStages} />",
    'LevelSelector visitedStages prop'
)

# ==============================================================================
# Write output
# ==============================================================================
with open(TARGET, 'w', encoding='utf-8') as f:
    f.write(html)

lines = html.count('\n')
print(f"OK  {TARGET.split('/')[-1]} updated  ({lines} lines)")
print(f"    {len(replaced)} replacements applied:")
for r in replaced:
    print(f"      \u2713 {r}")
