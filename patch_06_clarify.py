"""patch_06_clarify.py — hide plain English by default; add Clarify toggle button"""
F = "DC-AI-001_v2_0_0.html"

CSS = """
    /* ─── CLARIFY BUTTON ────────────────────────────────────────── */
    .clarify-btn {
      display: inline-flex; align-items: center; gap: 4px;
      margin-top: 0.5rem; padding: 3px 10px;
      font-size: 0.72rem; font-weight: 500; cursor: pointer;
      border: 1px solid var(--grammar); border-radius: 12px;
      background: transparent; color: var(--grammar);
      transition: all var(--transition);
    }
    .clarify-btn:hover { background: var(--accent-dim); }
    .clarify-box {
      margin-top: 0.5rem; padding: 0.6rem 0.9rem;
      background: var(--panel); border: 1px solid var(--grammar);
      border-left: 3px solid var(--grammar);
      border-radius: var(--radius-sm); font-size: 0.82rem;
      color: var(--text); line-height: 1.6;
    }
"""

# Find the exact fact-card render block in GrammarTab
OLD_FACT = r"""          {facts.map(function(fact, fi) {
            var soWhat = SO_WHAT_MAP[fact.term] || fact.soWhat || '';
            return (
              <div key={fi} className="fact-card">
                <div className="fact-term">{fact.term}</div>
                <div className="fact-standard">{fact.standard}</div>
                <div style={{fontSize:'0.83rem', color:'var(--text-muted)', lineHeight:'1.6', marginBottom:'0.6rem'}}>
                  <strong style={{color:'var(--text)', fontSize:'0.72rem', textTransform:'uppercase', letterSpacing:'0.06em'}}>Definition · </strong>
                  {fact.definition}
                </div>
                <div className="fact-row">
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
                </div>
              </div>
            );
          })}"""

NEW_FACT = r"""          {facts.map(function(fact, fi) {
            var soWhat = SO_WHAT_MAP[fact.term] || fact.soWhat || '';
            var clarifyOpen = !!(expandedEnglish && expandedEnglish[fi]);
            return (
              <div key={fi} className="fact-card">
                <div className="fact-term">{fact.term}</div>
                <div className="fact-standard">{fact.standard}</div>
                <div style={{fontSize:'0.83rem', color:'var(--text-muted)', lineHeight:'1.6', marginBottom:'0.6rem'}}>
                  <strong style={{color:'var(--text)', fontSize:'0.72rem', textTransform:'uppercase', letterSpacing:'0.06em'}}>Definition · </strong>
                  {fact.definition}
                </div>
                <div className="fact-row">
                  <div className="fact-field">
                    <span className="fact-field-label">By the Numbers</span>
                    <div className="fact-number-pill">{fact.number}</div>
                  </div>
                </div>
                {fact.plain && (
                  <>
                    <button className="clarify-btn" onClick={function(){ setExpandedEnglish(function(p){ var n=Object.assign({},p); n[fi]=!p[fi]; return n; }); }}>
                      💡 Clarify {clarifyOpen ? '▲' : '▼'}
                    </button>
                    {clarifyOpen && <div className="clarify-box">{fact.plain}</div>}
                  </>
                )}
                <div className="so-what-box">
                  <strong>So what? </strong>{soWhat || fact.soWhat}
                </div>
              </div>
            );
          })}"""

html = open(F, encoding="utf-8").read()
assert OLD_FACT in html, "Fact render block not found — check GrammarTab indentation"
html = html.replace("    /* ─── RESET & BASE", CSS + "    /* ─── RESET & BASE", 1)
html = html.replace(OLD_FACT, NEW_FACT, 1)
open(F, "w", encoding="utf-8").write(html)
print("patch_06 done — Clarify button added (plain English hidden by default)")
