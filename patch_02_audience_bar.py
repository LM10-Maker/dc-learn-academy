"""patch_02_audience_bar.py — add audience bar CSS + JSX (additive only)"""
F = "DC-AI-001_v2_0_0.html"

CSS = '''
    /* ─── AUDIENCE BAR ──────────────────────────────────────────── */
    .audience-bar {
      width: 100%;
      background: var(--panel);
      border-bottom: 1px solid var(--border);
      padding: 5px 1.5rem;
      font-size: 11px;
      font-family: var(--font-mono);
      color: var(--lbe-green);
      text-transform: uppercase;
      letter-spacing: 0.1em;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
'''

JSX_DIV = '      <div className="audience-bar">AUDIENCE: Fund Managers · Asset Owners · Colocation Executives · CTOs · Technical Advisors</div>\n'

ANCHOR_CSS = "    /* ─── RESET & BASE"
ANCHOR_JSX = '    <div className="app-container">\n      <Header'

html = open(F, encoding="utf-8").read()

assert ANCHOR_CSS in html, "CSS anchor not found"
assert ANCHOR_JSX in html, "JSX anchor not found"

html = html.replace(ANCHOR_CSS, CSS + "    /* ─── RESET & BASE", 1)
html = html.replace(
    '    <div className="app-container">\n      <Header',
    '    <div className="app-container">\n' + JSX_DIV + '      <Header',
    1
)

open(F, "w", encoding="utf-8").write(html)
print("patch_02 done — audience bar added")
