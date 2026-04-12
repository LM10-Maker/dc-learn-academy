#!/usr/bin/env python3
"""
polish2_02_personas.py
ITEM 2: PERSONA ENTRY POINT ON CHAIN TAB
Reads/writes DC-AI-001_v1_2_0.html
"""

WF = 'DC-AI-001_v1_2_0.html'

with open(WF, 'r', encoding='utf-8') as f:
    html = f.read()

# ─── 1. CSS ───────────────────────────────────────────────────────────────────
CSS = r"""
    /* ─── PERSONA SELECTOR BAR (Chain Tab) ─────────────────────────── */
    .persona-bar {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 1rem 1.2rem;
      margin-bottom: 1.25rem;
    }
    .persona-bar-label {
      font-size: 0.78rem;
      color: var(--text-dim);
      margin-bottom: 0.75rem;
    }
    .persona-btn-row {
      display: flex;
      gap: 0.75rem;
      flex-wrap: wrap;
      align-items: flex-end;
    }
    .persona-circle-btn {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 4px;
      width: 60px;
      cursor: pointer;
      background: none;
      border: none;
      padding: 0;
    }
    .persona-circle {
      width: 42px;
      height: 42px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1rem;
      font-weight: 700;
      transition: all 0.15s ease;
      border: 2px solid transparent;
    }
    .persona-circle-name {
      font-size: 0.65rem;
      font-weight: 500;
      text-align: center;
    }
    .persona-active-bar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-top: 0.6rem;
      padding: 0.45rem 0.75rem;
      background: var(--panel);
      border-radius: var(--radius-sm);
      font-size: 0.8rem;
      color: var(--text);
      border: 1px solid var(--border);
    }
    .persona-takeaway-list {
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      overflow: hidden;
      margin-bottom: 1.25rem;
    }
    .persona-takeaway-title {
      font-size: 0.68rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--text-faint);
      padding: 0.65rem 1rem;
      border-bottom: 1px solid var(--border);
      background: var(--surface);
    }
    .persona-takeaway-row {
      display: flex;
      align-items: flex-start;
      gap: 0.75rem;
      padding: 0.6rem 1rem;
      border-bottom: 1px solid var(--border);
      font-size: 0.8rem;
    }
    .persona-takeaway-row:last-child { border-bottom: none; }
    .persona-level-badge {
      font-size: 0.62rem;
      font-weight: 700;
      font-family: var(--font-mono);
      padding: 2px 6px;
      border-radius: 4px;
      flex-shrink: 0;
      margin-top: 2px;
    }
    .persona-takeaway-text {
      flex: 1;
      color: var(--text-muted);
      line-height: 1.45;
    }
    .persona-rhetoric-link {
      font-size: 0.7rem;
      font-weight: 600;
      flex-shrink: 0;
      cursor: pointer;
      text-decoration: underline;
      text-underline-offset: 2px;
      background: none;
      border: none;
      padding: 0;
      font-family: inherit;
      margin-top: 2px;
    }
"""

html = html.replace('  </style>', CSS + '  </style>', 1)

# ─── 2. Modify ChainTab to add persona state and bar ─────────────────────────
# Add selectedPersona state after the existing state lines in ChainTab
OLD_CHAIN_STATE = """function ChainTab({ selectedLevel, setSelectedLevel, setActiveTab }) {
  var level = LEVELS[selectedLevel];
  var [expandedEnglish, setExpandedEnglish] = React.useState({});
  var [expandedRefs,    setExpandedRefs]    = React.useState({});
  return (
    <div>
      <div className="card">"""

NEW_CHAIN_STATE = r"""function ChainTab({ selectedLevel, setSelectedLevel, setActiveTab }) {
  var level = LEVELS[selectedLevel];
  var [expandedEnglish, setExpandedEnglish] = React.useState({});
  var [expandedRefs,    setExpandedRefs]    = React.useState({});
  var [selectedPersona, setSelectedPersona] = React.useState(null);

  var PERSONA_COLORS = {
    asset_management: '#2563EB',
    technology:       '#7c3aed',
    technical:        '#16a34a',
    compliance:       '#d97706',
    cost:             '#6b7280'
  };

  return (
    <div>
      {/* Persona selector bar */}
      <div className="persona-bar">
        <div className="persona-bar-label">View through the lens of:</div>
        <div className="persona-btn-row">
          {PERSONAS.map(function(p) {
            var col = PERSONA_COLORS[p.key] || 'var(--accent)';
            var active = selectedPersona && selectedPersona.key === p.key;
            return (
              <button key={p.key} className="persona-circle-btn"
                onClick={function(){ setSelectedPersona(active ? null : p); }}>
                <span className="persona-circle" style={{
                  background: active ? col : 'var(--panel)',
                  color:      active ? '#fff' : col,
                  border:     '2px solid ' + col
                }}>{p.initial}</span>
                <span className="persona-circle-name" style={{color: active ? col : 'var(--text-dim)'}}>{p.name}</span>
              </button>
            );
          })}
          {selectedPersona && (
            <button className="persona-circle-btn" onClick={function(){ setSelectedPersona(null); }}>
              <span className="persona-circle" style={{background:'var(--panel)',color:'var(--text-dim)',border:'2px solid var(--border)'}}>&#x2715;</span>
              <span className="persona-circle-name" style={{color:'var(--text-dim)'}}>Clear</span>
            </button>
          )}
        </div>
        {selectedPersona && (
          <div className="persona-active-bar">
            <span>Viewing as <strong>{selectedPersona.name}</strong> &mdash; {selectedPersona.role}</span>
          </div>
        )}
      </div>

      {/* Persona takeaway list */}
      {selectedPersona && (
        <div className="persona-takeaway-list">
          <div className="persona-takeaway-title">Where this perspective is richest</div>
          {LEVELS.map(function(lvl, li) {
            var col = PERSONA_COLORS[selectedPersona.key] || 'var(--accent)';
            var takeaway = (RHETORIC_TAKEAWAYS[lvl.id] || {})[selectedPersona.key] || '';
            return (
              <div key={li} className="persona-takeaway-row">
                <span className="persona-level-badge" style={{background: col + '22', color: col}}>{lvl.id}</span>
                <span className="persona-takeaway-text"><strong style={{color:'var(--text)'}}>{lvl.title}</strong> &middot; {takeaway}</span>
                <button
                  className="persona-rhetoric-link"
                  style={{color: col}}
                  onClick={function(){ setSelectedLevel(li); safeStore('level', li); setActiveTab('rhetoric'); safeStore('tab', 'rhetoric'); }}
                >Rhetoric &#x2192;</button>
              </div>
            );
          })}
        </div>
      )}

      <div className="card">"""

html = html.replace(OLD_CHAIN_STATE, NEW_CHAIN_STATE, 1)

# ─── 3. Verify ────────────────────────────────────────────────────────────────
assert 'selectedPersona' in html, "selectedPersona state missing"
assert 'persona-bar' in html, "persona-bar CSS missing"
assert 'persona-takeaway-list' in html, "persona-takeaway-list missing"
assert html.count('"plain":') == 45, "grammar facts changed"
assert html.count('"correct":') == 27, "assessment questions changed"

with open(WF, 'w', encoding='utf-8') as f:
    f.write(html)

print("[02] OK — persona entry point on chain tab added")
