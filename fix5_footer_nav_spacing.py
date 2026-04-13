#!/usr/bin/env python3
"""Fix 5: Footer nav spacing — add gap:24px to series nav and copyright row containers."""

src = '/home/user/dc-learn-academy/DC-AI-001_v2_3_0 (3).html'
with open(src, 'r', encoding='utf-8') as f:
    html = f.read()

# 5a: Add gap to series nav container (already has 3 flex items with 1 1 33%)
OLD5a = """      <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',padding:'16px 24px',margin:'12px auto 0',maxWidth:1200,width:'100%',borderTop:'1px solid var(--border)',boxSizing:'border-box'}} className="no-print">
        <div style={{flex:'1 1 33%',textAlign:'left'}}><span style={{color:'var(--text-muted)',fontSize:13}}>First module</span></div>
        <div style={{flex:'1 1 33%',textAlign:'center'}}><span style={{color:'var(--text-muted)',fontSize:12}}>Module 1 of 8 · DC-AI v{TOOL_VERSION}</span></div>
        <div style={{flex:'1 1 33%',textAlign:'right'}}><a href="#" style={{color:'var(--green)',textDecoration:'none',fontSize:13}}>DC-AI-002: Cooling →</a></div>
      </div>"""
NEW5a = """      <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',gap:'24px',padding:'16px 24px',margin:'12px auto 0',maxWidth:1200,width:'100%',borderTop:'1px solid var(--border)',boxSizing:'border-box'}} className="no-print">
        <div style={{flex:'1 1 33%',textAlign:'left'}}><span style={{color:'var(--text-muted)',fontSize:13}}>First module</span></div>
        <div style={{flex:'1 1 33%',textAlign:'center'}}><span style={{color:'var(--text-muted)',fontSize:12}}>Module 1 of 8 · DC-AI v{TOOL_VERSION}</span></div>
        <div style={{flex:'1 1 33%',textAlign:'right'}}><a href="#" style={{color:'var(--green)',textDecoration:'none',fontSize:13}}>DC-AI-002: Cooling →</a></div>
      </div>"""
assert OLD5a in html, "Fix5a: series nav row not found"
html = html.replace(OLD5a, NEW5a, 1)

# 5b: Add gap:24px to copyright row container and ensure 3-column layout
OLD5b = """      <div style={{borderTop:'1px solid var(--border)',padding:'16px 24px',margin:'0 auto',maxWidth:1200,width:'100%',display:'flex',justifyContent:'space-between',alignItems:'center',flexWrap:'wrap',gap:8,fontSize:12,color:'var(--text-muted)',boxSizing:'border-box'}} className="no-print">
        <span>© 2026 Legacy Business Engineers Ltd</span>
        <div style={{display:'flex',gap:16}}>
          <a href="https://legacybe.ie" target="_blank" rel="noopener" style={{color:'var(--green)',textDecoration:'none'}}>legacybe.ie</a>
          <a href="https://legacybe.ie/tools/" target="_blank" rel="noopener" style={{color:'var(--green)',textDecoration:'none'}}>Tools</a>
          <a href="mailto:lmurphy@legacybe.ie" style={{color:'var(--green)',textDecoration:'none'}}>Contact</a>
          <a href="https://legacybe.ie/services/" target="_blank" rel="noopener" style={{color:'var(--green)',textDecoration:'none'}}>Services</a>
        </div>
      </div>"""
NEW5b = """      <div style={{borderTop:'1px solid var(--border)',padding:'16px 24px',margin:'0 auto',maxWidth:1200,width:'100%',display:'flex',justifyContent:'space-between',alignItems:'center',flexWrap:'wrap',gap:'24px',fontSize:12,color:'var(--text-muted)',boxSizing:'border-box'}} className="no-print">
        <div style={{flex:'1 1 33%',textAlign:'left'}}><span>© 2026 Legacy Business Engineers Ltd</span></div>
        <div style={{flex:'1 1 33%',textAlign:'center'}}></div>
        <div style={{flex:'1 1 33%',textAlign:'right',display:'flex',gap:16,justifyContent:'flex-end'}}>
          <a href="https://legacybe.ie" target="_blank" rel="noopener" style={{color:'var(--green)',textDecoration:'none'}}>legacybe.ie</a>
          <a href="https://legacybe.ie/tools/" target="_blank" rel="noopener" style={{color:'var(--green)',textDecoration:'none'}}>Tools</a>
          <a href="mailto:lmurphy@legacybe.ie" style={{color:'var(--green)',textDecoration:'none'}}>Contact</a>
          <a href="https://legacybe.ie/services/" target="_blank" rel="noopener" style={{color:'var(--green)',textDecoration:'none'}}>Services</a>
        </div>
      </div>"""
assert OLD5b in html, "Fix5b: copyright row not found"
html = html.replace(OLD5b, NEW5b, 1)

with open(src, 'w', encoding='utf-8') as f:
    f.write(html)
print("Fix 5 applied: Footer nav spacing updated with gap:24px on both rows.")
