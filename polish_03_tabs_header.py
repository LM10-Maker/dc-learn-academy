#!/usr/bin/env python3
"""
polish_03_tabs_header.py
- Tab bar CSS: sticky (position:sticky, top:0, z-index:10), surface bg, bottom border
- Active tab: 2px bottom border in stage colour via data-tab attribute
- TABS JS: remove emoji prefixes, rename BSG -> Reference
- TabBar JSX: add data-tab={tab.id} to button
- Header title: use --text-bright
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
# 1. Tab bar CSS — sticky, surface background, stage-coloured active state
# ==============================================================================

rep(
    "    .tab-bar {\n      background: var(--surface);\n      border-bottom: 2px solid var(--border);\n      display: flex;\n      padding: 0 1.5rem;\n      gap: 0.1rem;\n      overflow-x: auto;\n      scrollbar-width: none;\n    }\n    .tab-bar::-webkit-scrollbar { display: none; }\n    .tab-btn {\n      flex-shrink: 0;\n      padding: 0.75rem 1.1rem;\n      font-size: 0.82rem;\n      font-weight: 500;\n      color: var(--text-muted);\n      border-bottom: 2px solid transparent;\n      margin-bottom: -2px;\n      transition: color var(--transition), border-color var(--transition);\n      white-space: nowrap;\n    }\n    .tab-btn:hover { color: var(--text); }\n    .tab-btn.active { color: var(--accent); border-bottom-color: var(--accent); font-weight: 600; }",
    "    .tab-bar {\n      background: var(--surface);\n      border-bottom: 1px solid var(--border);\n      display: flex;\n      padding: 0 1.5rem;\n      gap: 0;\n      overflow-x: auto;\n      scrollbar-width: none;\n      position: sticky;\n      top: 0;\n      z-index: 10;\n    }\n    .tab-bar::-webkit-scrollbar { display: none; }\n    .tab-btn {\n      flex-shrink: 0;\n      padding: 0.75rem 1.2rem;\n      font-size: 0.82rem;\n      font-weight: 500;\n      color: var(--text-dim);\n      border-bottom: 2px solid transparent;\n      margin-bottom: -1px;\n      transition: color var(--transition), border-color var(--transition);\n      white-space: nowrap;\n    }\n    .tab-btn:hover { color: var(--text); }\n    /* Active tab: text-bright base, then stage-coloured border+text via data-tab */\n    .tab-btn.active                         { font-weight: 600; color: var(--text-bright); }\n    .tab-btn.active[data-tab='chain']       { border-bottom-color: var(--text-dim); }\n    .tab-btn.active[data-tab='grammar']     { border-bottom-color: var(--grammar);  color: var(--grammar); }\n    .tab-btn.active[data-tab='logic']       { border-bottom-color: var(--logic);    color: var(--logic); }\n    .tab-btn.active[data-tab='rhetoric']    { border-bottom-color: var(--rhetoric); color: var(--rhetoric); }\n    .tab-btn.active[data-tab='field']       { border-bottom-color: var(--logic);    color: var(--logic); }\n    .tab-btn.active[data-tab='assessment']  { border-bottom-color: var(--grammar);  color: var(--grammar); }\n    .tab-btn.active[data-tab='bsg']         { border-bottom-color: var(--text-dim); }",
    'tab bar CSS'
)

# ==============================================================================
# 2. TABS data — remove emoji, rename BSG -> Reference
# ==============================================================================

rep(
    "var TABS = [\n  { id: 'chain',      label: '\U0001f517 Chain' },\n  { id: 'grammar',    label: '\U0001f4d6 Grammar' },\n  { id: 'logic',      label: '\u26a1 Logic' },\n  { id: 'rhetoric',   label: '\U0001f4ac Rhetoric' },\n  { id: 'field',      label: '\U0001f3d7\ufe0f Field Challenge' },\n  { id: 'assessment', label: '\u2705 Assessment' },\n  { id: 'bsg',        label: '\U0001f4da BSG' }\n];",
    "var TABS = [\n  { id: 'chain',      label: 'Chain' },\n  { id: 'grammar',    label: 'Grammar' },\n  { id: 'logic',      label: 'Logic' },\n  { id: 'rhetoric',   label: 'Rhetoric' },\n  { id: 'field',      label: 'Field Challenge' },\n  { id: 'assessment', label: 'Assessment' },\n  { id: 'bsg',        label: 'Reference' }\n];",
    'TABS data (emoji removal + BSG rename)'
)

# ==============================================================================
# 3. TabBar JSX — add data-tab attribute to each button
# ==============================================================================

rep(
    "          <button\n            key={tab.id}\n            className={'tab-btn' + (activeTab === tab.id ? ' active' : '')}\n            onClick={() => { setActiveTab(tab.id); safeStore('tab', tab.id); }}\n          >\n            {tab.label}\n          </button>",
    "          <button\n            key={tab.id}\n            data-tab={tab.id}\n            className={'tab-btn' + (activeTab === tab.id ? ' active' : '')}\n            onClick={() => { setActiveTab(tab.id); safeStore('tab', tab.id); }}\n          >\n            {tab.label}\n          </button>",
    'TabBar JSX data-tab attribute'
)

# ==============================================================================
# 4. Header title: --text -> --text-bright
# ==============================================================================

rep(
    "    .header-title-main {\n      font-size: 0.95rem;\n      font-weight: 600;\n      color: var(--text);\n      letter-spacing: -0.01em;\n    }",
    "    .header-title-main {\n      font-size: 0.95rem;\n      font-weight: 600;\n      color: var(--text-bright);\n      letter-spacing: -0.01em;\n    }",
    'header-title-main colour'
)

# ==============================================================================
# 5. Header divider: --border-2 -> --border (cleaner separator)
# ==============================================================================

rep(
    "    .header-divider {\n      width: 1px;\n      height: 28px;\n      background: var(--border-2);\n    }",
    "    .header-divider {\n      width: 1px;\n      height: 28px;\n      background: var(--border);\n    }",
    'header-divider colour'
)

# ==============================================================================
# 6. Level indicator bar (shown below tab on non-chain tabs) — use panel bg
# ==============================================================================

rep(
    "          background: 'var(--surface-2)',\n          borderBottom: '1px solid var(--border)',",
    "          background: 'var(--panel)',\n          borderBottom: '1px solid var(--border)',",
    'level indicator bar background'
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
