#!/usr/bin/env python3
"""
polish_05_assessment_footer.py
- Assessment: tier badges (knowledge=blue/grammar, calculation=amber, judgement=purple),
  correct/wrong answer styling already in CSS — confirm q-option-btn states,
  score circle uses grammar colour
- Footer JSX: rebuild as full-width bar with copyright, CTA, contact, version
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
# 1. Assessment: score circle use grammar colour
# ==============================================================================

rep(
    "    .score-circle {\n      width: 90px; height: 90px;\n      border-radius: 50%;\n      background: var(--accent-dim);\n      border: 3px solid var(--accent);",
    "    .score-circle {\n      width: 90px; height: 90px;\n      border-radius: 50%;\n      background: var(--accent-dim);\n      border: 3px solid var(--grammar);",
    'score-circle grammar border'
)

rep(
    "    .score-num { font-size: 1.6rem; font-weight: 700; color: var(--accent); line-height: 1; }",
    "    .score-num { font-size: 1.6rem; font-weight: 700; color: var(--grammar); line-height: 1; }",
    'score-num grammar colour'
)

# ==============================================================================
# 2. Assessment: q-level-badge use grammar
# ==============================================================================

rep(
    "    .q-level-badge {\n      font-size: 0.67rem;\n      font-weight: 600;\n      background: var(--accent-dim);\n      color: var(--accent);\n      padding: 2px 8px;\n      border-radius: 4px;\n    }",
    "    .q-level-badge {\n      font-size: 0.67rem;\n      font-weight: 600;\n      font-family: var(--font-mono);\n      background: var(--accent-dim);\n      color: var(--grammar);\n      padding: 2px 8px;\n      border-radius: 4px;\n    }",
    'q-level-badge grammar colour'
)

# ==============================================================================
# 3. Assessment: selected option uses grammar border (already partially done
#    in CSS; ensure selected state uses grammar not accent)
# ==============================================================================

rep(
    "    .q-option-btn.selected    { border-color: var(--accent); background: var(--accent-dim); color: var(--text); }",
    "    .q-option-btn.selected    { border-color: var(--grammar); background: var(--accent-dim); color: var(--text); }",
    'q-option-btn selected grammar'
)

rep(
    "    .q-option-btn.selected .q-option-letter  { background: var(--accent); color: #fff; }",
    "    .q-option-btn.selected .q-option-letter  { background: var(--grammar); color: #fff; }",
    'q-option selected letter grammar'
)

# ── hover border also grammar ────────────────────────────────────────────────
rep(
    "    .q-option-btn:not(:disabled):hover {\n      border-color: var(--accent);\n      background: var(--accent-dim);\n      color: var(--text);\n    }",
    "    .q-option-btn:not(:disabled):hover {\n      border-color: var(--grammar);\n      background: var(--accent-dim);\n      color: var(--text);\n    }",
    'q-option hover grammar'
)

# ==============================================================================
# 4. Assessment tier badges — judgement/calculation use stage colours
# ==============================================================================

rep(
    "    .q-tier-badge.calculation { background: var(--amber-dim);  color: var(--amber); }\n    .q-tier-badge.judgement   { background: var(--purple-dim); color: var(--purple); }",
    "    .q-tier-badge.calculation { background: var(--amber-dim);  color: var(--logic); }\n    .q-tier-badge.judgement   { background: var(--purple-dim); color: var(--rhetoric); }",
    'q-tier badges stage colours'
)

# ==============================================================================
# 5. Nav button primary: accent -> grammar
# ==============================================================================

rep(
    "    .q-nav-btn.primary {\n      background: var(--accent);\n      color: #fff;\n      border: 1px solid var(--accent);\n    }\n    .q-nav-btn.primary:hover { background: var(--accent-hover); }",
    "    .q-nav-btn.primary {\n      background: var(--grammar);\n      color: #fff;\n      border: 1px solid var(--grammar);\n    }\n    .q-nav-btn.primary:hover { background: var(--accent-hover); }",
    'q-nav-btn primary grammar'
)

# ==============================================================================
# 6. Restart button: accent -> lbe-green (CTA colour per spec)
# ==============================================================================

rep(
    "    .restart-btn {\n      margin-top: 1.2rem;\n      padding: 0.6rem 1.6rem;\n      background: var(--accent);\n      color: #fff;\n      border-radius: var(--radius-md);\n      font-size: 0.85rem;\n      font-weight: 600;\n    }\n    .restart-btn:hover { background: var(--accent-hover); }",
    "    .restart-btn {\n      margin-top: 1.2rem;\n      padding: 0.6rem 1.6rem;\n      background: var(--lbe-green);\n      color: #fff;\n      border-radius: var(--radius-md);\n      font-size: 0.85rem;\n      font-weight: 600;\n    }\n    .restart-btn:hover { background: var(--success); }",
    'restart-btn lbe-green CTA'
)

# ==============================================================================
# 7. Footer JSX — rebuild as full-width structured bar
# ==============================================================================

rep(
    "      <footer className=\"app-footer\">\n        <span className=\"footer-text\">\n          \u00a9 2026 Legacy Business Engineers Ltd \u00b7 DC-AI Series \u00b7 Module 1 of 8\n        </span>\n        <span className=\"footer-version\">v{TOOL_VERSION}</span>\n      </footer>",
    """      <footer className="app-footer">
        <div className="footer-inner">
          <div className="footer-left">
            <span className="footer-copyright">&copy; 2026 Legacy Business Engineers Ltd &middot; DC-AI Series &middot; Module 1 of 8</span>
            <span className="footer-cta">Need to know where your facility stands on AI readiness?</span>
          </div>
          <div className="footer-right">
            <a href="mailto:lmurphy@legacybe.ie" className="footer-contact">lmurphy@legacybe.ie</a>
            <span className="footer-version">DC-AI-001 v{TOOL_VERSION}</span>
          </div>
        </div>
      </footer>""",
    'footer JSX rebuild'
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
