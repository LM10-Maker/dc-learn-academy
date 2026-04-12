"""patch_03_pill_tabs.py — replace underline tab style with pill style"""
F = "DC-AI-001_v2_0_0.html"

html_tmp = open(F, encoding="utf-8").read()
# Extract exact tab bar block using reliable anchors
TB_START = html_tmp.index("    /* ─── TAB BAR")
TB_END   = html_tmp.index("    .tab-btn.active[data-tab='bsg']") + len("    .tab-btn.active[data-tab='bsg']         { border-bottom-color: var(--text-dim); }")
OLD = html_tmp[TB_START:TB_END]

NEW = """    /* ─── TAB BAR — pill style ─────────────────────────────────── */
    .tab-bar {
      background: var(--surface);
      border-bottom: 1px solid var(--border);
      display: flex;
      padding: 0.55rem 1.5rem;
      gap: 0.4rem;
      overflow-x: auto;
      scrollbar-width: none;
    }
    .tab-bar::-webkit-scrollbar { display: none; }
    .tab-btn {
      flex-shrink: 0;
      padding: 5px 14px;
      font-size: 0.8rem;
      font-weight: 500;
      color: var(--text-dim);
      border: 1px solid var(--border);
      border-radius: 20px;
      background: transparent;
      transition: all var(--transition);
      white-space: nowrap;
    }
    .tab-btn:hover { background: var(--panel); color: var(--text); border-color: var(--border-2); }
    .tab-btn.active { font-weight: 600; background: var(--panel); color: var(--text-bright); }
    .tab-btn.active[data-tab='chain']      { border-color: var(--text-dim); }
    .tab-btn.active[data-tab='learn']      { border-color: var(--grammar); color: var(--grammar); }
    .tab-btn.active[data-tab='grammar']    { border-color: var(--grammar); color: var(--grammar); }
    .tab-btn.active[data-tab='logic']      { border-color: var(--logic);   color: var(--logic); }
    .tab-btn.active[data-tab='rhetoric']   { border-color: var(--rhetoric);color: var(--rhetoric); }
    .tab-btn.active[data-tab='field']      { border-color: var(--logic);   color: var(--logic); }
    .tab-btn.active[data-tab='assessment'] { border-color: var(--grammar); color: var(--grammar); }
    .tab-btn.active[data-tab='progress']   { border-color: var(--lbe-green);color: var(--lbe-green); }
    .tab-btn.active[data-tab='bsg']        { border-color: var(--text-dim); }
    .tab-btn.active[data-tab='reference']  { border-color: var(--text-dim); }"""

html = open(F, encoding="utf-8").read()
assert OLD in html, "Tab bar CSS block not found"
html = html.replace(OLD, NEW, 1)
open(F, "w", encoding="utf-8").write(html)
print("patch_03 done — pill tab style applied")
