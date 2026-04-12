#!/usr/bin/env python3
"""
polish2_05_clarify.py
ITEM 5: CLARIFY BUTTON ON GRAMMAR FACTS
- Moves "Plain English" behind a toggle
- Adds 💡 Clarify button below each fact card
- Max-height slide transition (150ms)
Reads/writes DC-AI-001_v1_2_0.html
"""

WF = 'DC-AI-001_v1_2_0.html'

with open(WF, 'r', encoding='utf-8') as f:
    html = f.read()

# ─── 1. CSS ───────────────────────────────────────────────────────────────────
CSS = r"""
    /* ─── CLARIFY BUTTON & PANEL ───────────────────────────────────── */
    .clarify-btn {
      background: none;
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 5px 12px;
      font-size: 0.78rem;
      color: var(--text-dim);
      cursor: pointer;
      margin-top: 0.6rem;
      font-family: var(--font-sans);
      transition: background var(--transition), color var(--transition);
    }
    .clarify-btn:hover { background: var(--panel); color: var(--text); }
    .clarify-panel {
      max-height: 0;
      overflow: hidden;
      transition: max-height 0.15s ease, padding 0.15s ease;
      background: var(--panel);
      border-left: 3px solid var(--grammar);
      border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
      font-size: 0.82rem;
      font-style: italic;
      color: var(--text);
      line-height: 1.6;
      margin-top: 0;
    }
    .clarify-panel.open {
      max-height: 240px;
      padding: 0.6rem 0.9rem;
      margin-top: 0.5rem;
    }
    .clarify-header {
      font-size: 0.65rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.07em;
      color: var(--grammar);
      margin-bottom: 0.35rem;
      font-style: normal;
    }
"""

html = html.replace('  </style>', CSS + '  </style>', 1)

# ─── 2. Modify GrammarTab ────────────────────────────────────────────────────
# 2a. Add clarifyOpen state after facts declaration
OLD_FACTS_LINE = "  var facts = grammar.facts || [];"
NEW_FACTS_LINE = "  var facts = grammar.facts || [];\n  var [clarifyOpen, setClarifyOpen] = React.useState({});"

html = html.replace(OLD_FACTS_LINE, NEW_FACTS_LINE, 1)

# 2b. Replace the fact-row block (Plain English + By the Numbers columns)
#     with a single-column By the Numbers block, then add Clarify toggle
OLD_FACT_ROW = r"""                <div className="fact-row">
                  <div className="fact-field">
                    <span className="fact-field-label">Plain English</span>
                    <span className="fact-field-value">{fact.plain}</span>
                  </div>
                  <div className="fact-field">
                    <span className="fact-field-label">By the Numbers</span>
                    <div className="fact-number-pill">{fact.number}</div>
                  </div>
                </div>
                <div className="so-what-box">
                  <strong>So what? </strong>{soWhat || fact.soWhat}
                </div>"""

NEW_FACT_ROW = r"""                <div className="fact-row" style={{gridTemplateColumns:'1fr'}}>
                  <div className="fact-field">
                    <span className="fact-field-label">By the Numbers</span>
                    <div className="fact-number-pill">{fact.number}</div>
                  </div>
                </div>
                <div className="so-what-box">
                  <strong>So what? </strong>{soWhat || fact.soWhat}
                </div>
                <button
                  className="clarify-btn"
                  onClick={function(){ var n=Object.assign({},clarifyOpen); n[fi]=!n[fi]; setClarifyOpen(n); }}
                >
                  &#x1F4A1; Clarify{clarifyOpen[fi] ? ' \u25be' : ''}
                </button>
                <div className={'clarify-panel' + (clarifyOpen[fi] ? ' open' : '')}>
                  <div className="clarify-header">In plain English:</div>
                  {fact.plain}
                </div>"""

assert OLD_FACT_ROW in html, "fact-row pattern not found in file"
html = html.replace(OLD_FACT_ROW, NEW_FACT_ROW, 1)

# ─── 3. Verify ────────────────────────────────────────────────────────────────
assert 'clarifyOpen' in html, "clarifyOpen state missing"
assert 'clarify-btn' in html, "clarify-btn CSS missing"
assert 'clarify-panel' in html, "clarify-panel CSS missing"
# plain field data must still exist in the source (unchanged)
assert html.count('"plain":') == 45, f"grammar facts changed: {html.count(chr(34)+'plain'+chr(34)+':')}"
assert html.count('"correct":') == 27, "assessment questions changed"

with open(WF, 'w', encoding='utf-8') as f:
    f.write(html)

print("[05] OK — Clarify button added to all grammar fact cards")
