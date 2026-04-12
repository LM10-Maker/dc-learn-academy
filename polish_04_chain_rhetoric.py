#!/usr/bin/env python3
"""
polish_04_chain_rhetoric.py
- Chain tab: plainEnglish clamped to 3 lines + "Read more...", crossRefs behind
  "See related ->", 2px left border on selected card (rhetoric for L9),
  "Select this level ->" CTA
- Chain card CSS: add active left-border rule
- Rhetoric tab: Eoin card dashed border + DIAGNOSTIC badge
- Persona avatar colours per spec
- New CSS: .persona-card-diagnostic, .diagnostic-badge, .chain-expand-btn,
  .chain-seerelated-btn
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
# 1. Chain card CSS — add left-border active rule + new expand/see-related CSS
# ==============================================================================

rep(
    "    .chain-level-card.active {\n      border-color: var(--accent);\n      background: var(--accent-dim);\n    }",
    "    .chain-level-card.active {\n      border-color: var(--grammar);\n      border-left: 2px solid var(--grammar);\n      background: var(--accent-dim);\n    }\n    .chain-level-card.l9.active {\n      border-color: var(--rhetoric);\n      border-left: 2px solid var(--rhetoric);\n    }\n    .chain-expand-btn {\n      display: inline-block;\n      margin-top: 4px;\n      font-size: 0.7rem;\n      color: var(--grammar);\n      font-weight: 600;\n      cursor: pointer;\n      background: none;\n      border: none;\n      padding: 0;\n      text-decoration: underline;\n      text-underline-offset: 2px;\n    }\n    .chain-seerelated-btn {\n      display: inline-block;\n      margin-top: 6px;\n      font-size: 0.7rem;\n      color: var(--text-dim);\n      font-weight: 500;\n      cursor: pointer;\n      background: none;\n      border: none;\n      padding: 0;\n    }\n    .chain-seerelated-btn:hover { color: var(--text); }",
    'chain card active CSS + expand CSS'
)

# ==============================================================================
# 2. Persona avatar colours per spec
# ==============================================================================

rep(
    "    .persona-avatar.conor   { background: #1e3a5f; color: #60a5fa; }\n    .persona-avatar.helena  { background: #1a3350; color: #38bdf8; }\n    .persona-avatar.eoin    { background: #1e3a2f; color: #34d399; }\n    .persona-avatar.rachel  { background: #3b2e55; color: #c084fc; }\n    .persona-avatar.padraig { background: #3b2e10; color: #fbbf24; }",
    "    .persona-avatar.conor   { background: #2563EB; color: #fff; }\n    .persona-avatar.helena  { background: #7c3aed; color: #fff; }\n    .persona-avatar.eoin    { background: #16a34a; color: #fff; }\n    .persona-avatar.rachel  { background: #d97706; color: #fff; }\n    .persona-avatar.padraig { background: #6b7280; color: #fff; }",
    'persona avatar colours'
)

# ==============================================================================
# 3. Add Eoin diagnostic card CSS after persona-takeaway block
# ==============================================================================

rep(
    "    .persona-takeaway strong { font-style: normal; color: var(--accent); font-size: 0.65rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.07em; display: block; margin-bottom: 2px; }",
    "    .persona-takeaway strong { font-style: normal; color: var(--accent); font-size: 0.65rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.07em; display: block; margin-bottom: 2px; }\n    /* Eoin diagnostic card */\n    .persona-card-diagnostic {\n      border: 1px dashed var(--text-dim) !important;\n    }\n    .diagnostic-badge {\n      display: inline-block;\n      font-size: 0.58rem;\n      font-weight: 700;\n      letter-spacing: 0.09em;\n      text-transform: uppercase;\n      padding: 1px 6px;\n      border-radius: 4px;\n      background: rgba(22,163,74,0.15);\n      color: var(--lbe-green);\n      margin-top: 3px;\n    }",
    'persona diagnostic CSS'
)

# ==============================================================================
# 4. ChainTab JSX — add expand state, clamp plainEnglish, expandable crossRefs,
#    L9 class, inline left-border on active, "Select this level ->" CTA
# ==============================================================================

rep(
    "function ChainTab({ selectedLevel, setSelectedLevel, setActiveTab }) {\n  var level = LEVELS[selectedLevel];\n  return (",
    "function ChainTab({ selectedLevel, setSelectedLevel, setActiveTab }) {\n  var level = LEVELS[selectedLevel];\n  var [expandedEnglish, setExpandedEnglish] = React.useState({});\n  var [expandedRefs,    setExpandedRefs]    = React.useState({});\n  return (",
    'ChainTab expand state'
)

rep(
    "              <div\n                key={lvl.id}\n                className={'chain-level-card' + (selectedLevel === idx ? ' active' : '')}\n                onClick={() => {\n                  setSelectedLevel(idx);\n                  safeStore('level', idx);\n                  setActiveTab('grammar');\n                  safeStore('tab', 'grammar');\n                }}\n              >\n                <div className=\"chain-level-num\">{lvl.id} \u00b7 Level {lvl.level}</div>\n                <div className=\"chain-level-icon\">{lvl.icon}</div>\n                <div className=\"chain-level-title\">{lvl.title}</div>\n                <div className=\"chain-level-subtitle\">{lvl.subtitle}</div>\n                <div className=\"chain-plain-english\">{lvl.plainEnglish}</div>\n                {lvl.retrofitRelevance && (\n                  <div style={{marginTop:'0.5rem', padding:'0.45rem 0.65rem', background:'var(--amber-dim)', borderRadius:'var(--radius-sm)', fontSize:'0.73rem', color:'var(--text-muted)', lineHeight:'1.45'}}>\n                    <strong style={{color:'var(--amber)', fontSize:'0.62rem', textTransform:'uppercase', letterSpacing:'0.07em'}}>Retrofit Relevance \u00b7 </strong>\n                    {lvl.retrofitRelevance}\n                  </div>\n                )}\n                <div className=\"chain-crossrefs\">\n                  {(lvl.crossRefs || []).map(function(ref, ri) {\n                    return <span key={ri} className=\"chain-crossref-tag\">{ref}</span>;\n                  })}\n                </div>\n                <div style={{marginTop:'0.6rem', fontSize:'0.68rem', color:'var(--accent)', fontWeight:600}}>\n                  Click to explore \u2192\n                </div>\n              </div>",
    "              <div\n                key={lvl.id}\n                className={'chain-level-card' + (selectedLevel === idx ? ' active' : '') + (lvl.id === 'L9' ? ' l9' : '')}\n                style={selectedLevel === idx ? {borderLeft: '2px solid ' + (lvl.id === 'L9' ? 'var(--rhetoric)' : 'var(--grammar)')} : {}}\n                onClick={() => {\n                  setSelectedLevel(idx);\n                  safeStore('level', idx);\n                  setActiveTab('grammar');\n                  safeStore('tab', 'grammar');\n                }}\n              >\n                <div className=\"chain-level-num\">{lvl.id} \u00b7 Level {lvl.level}</div>\n                <div className=\"chain-level-icon\">{lvl.icon}</div>\n                <div className=\"chain-level-title\">{lvl.title}</div>\n                <div className=\"chain-level-subtitle\">{lvl.subtitle}</div>\n                <div\n                  className=\"chain-plain-english\"\n                  style={expandedEnglish[idx] ? {} : {display:'-webkit-box', WebkitLineClamp:3, WebkitBoxOrient:'vertical', overflow:'hidden'}}\n                >\n                  {lvl.plainEnglish}\n                </div>\n                {!expandedEnglish[idx] && (\n                  <button className=\"chain-expand-btn\" onClick={function(e){ e.stopPropagation(); setExpandedEnglish(function(p){ var n=Object.assign({},p); n[idx]=true; return n; }); }}>\n                    Read more...\n                  </button>\n                )}\n                {lvl.retrofitRelevance && (\n                  <div style={{marginTop:'0.5rem', padding:'0.45rem 0.65rem', background:'var(--amber-dim)', borderRadius:'var(--radius-sm)', fontSize:'0.73rem', color:'var(--text-muted)', lineHeight:'1.45'}}>\n                    <strong style={{color:'var(--amber)', fontSize:'0.62rem', textTransform:'uppercase', letterSpacing:'0.07em'}}>Retrofit Relevance \u00b7 </strong>\n                    {lvl.retrofitRelevance}\n                  </div>\n                )}\n                {(lvl.crossRefs && lvl.crossRefs.length > 0) && (\n                  expandedRefs[idx] ? (\n                    <div className=\"chain-crossrefs\" style={{marginTop:'0.5rem'}}>\n                      {lvl.crossRefs.map(function(ref, ri) {\n                        return <span key={ri} className=\"chain-crossref-tag\">{ref}</span>;\n                      })}\n                    </div>\n                  ) : (\n                    <button className=\"chain-seerelated-btn\" onClick={function(e){ e.stopPropagation(); setExpandedRefs(function(p){ var n=Object.assign({},p); n[idx]=true; return n; }); }}>\n                      See related \u2192\n                    </button>\n                  )\n                )}\n                <div style={{marginTop:'0.6rem', fontSize:'0.68rem', color:'var(--grammar)', fontWeight:600}}>\n                  Select this level \u2192\n                </div>\n              </div>",
    'ChainTab card JSX'
)

# ==============================================================================
# 5. RhetoricTab JSX — Eoin card: dashed border + DIAGNOSTIC badge
# ==============================================================================

rep(
    "            return (\n              <div key={persona.key} className=\"persona-card\">\n                <div className=\"persona-header\">\n                  <div className={'persona-avatar ' + persona.avatarClass}>{persona.initial}</div>\n                  <div>\n                    <div className=\"persona-name\">{persona.icon} {persona.name}</div>\n                    <div className=\"persona-role\">{persona.role}</div>\n                  </div>\n                </div>",
    "            var isEoin = persona.key === 'technical';\n            return (\n              <div key={persona.key} className={'persona-card' + (isEoin ? ' persona-card-diagnostic' : '')}>\n                <div className=\"persona-header\">\n                  <div className={'persona-avatar ' + persona.avatarClass}>{persona.initial}</div>\n                  <div>\n                    <div className=\"persona-name\">{persona.icon} {persona.name}</div>\n                    <div className=\"persona-role\">{persona.role}</div>\n                    {isEoin && <span className=\"diagnostic-badge\">DIAGNOSTIC</span>}\n                  </div>\n                </div>",
    'RhetoricTab Eoin diagnostic JSX'
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
