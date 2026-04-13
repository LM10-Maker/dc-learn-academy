#!/usr/bin/env python3
"""
Fix A: Remove "Currently Selected" expanded detail card from ChainTab.
Reads DC-AI-001_v2_1_0.html, writes DC-AI-001_v2_2_0.html.
"""

SRC = "DC-AI-001_v2_1_0.html"
DST = "DC-AI-001_v2_2_0.html"

OLD = """\
      {/* Currently selected level highlight */}
      <div className="card">
        <div className="card-header">
          <div>
            <div className="card-title">Currently Selected: {level.id} \u2014 {level.title}</div>
            <div className="card-subtitle">{level.subtitle}</div>
          </div>
        </div>
        <p style={{fontSize:'0.83rem', color:'var(--text-muted)', lineHeight:'1.65', marginBottom:'0.75rem'}}>{level.plainEnglish}</p>
        <div style={{marginBottom:'0.75rem'}}>
          <div className="section-label">Source Note</div>
          <p style={{fontSize:'0.78rem', color:'var(--text-faint)', fontStyle:'italic', lineHeight:'1.5'}}>{level.sourceNote}</p>
        </div>
        <div>
          <div className="section-label">Cross-References</div>
          <div className="crossrefs-row">
            {(level.crossRefs || []).map(function(ref, ri) {
              return <span key={ri} className="crossref-tag">{shortRef(ref)}</span>;
            })}
          </div>
        </div>
      </div>"""

NEW = ""  # remove entirely

with open(SRC, "r", encoding="utf-8") as f:
    html = f.read()

assert OLD in html, "Fix A: target block not found — check exact whitespace/chars"
html = html.replace(OLD, NEW, 1)

with open(DST, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Fix A applied: 'Currently Selected' detail card removed → {DST}")
