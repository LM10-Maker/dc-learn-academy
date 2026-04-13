#!/usr/bin/env python3
"""
Fix B: Simplify persona selector on ChainTab.
Remove outer .card wrapper and "Viewing As" title header.
Replace with subtle inline label + buttons on same line.
Relevance rows render flush (no card padding).
Reads/writes DC-AI-001_v2_2_0.html in place.
"""

FILE = "DC-AI-001_v2_2_0.html"

OLD = """\
      {/* Persona Selector */}
      <div className="main-content" style={{paddingTop:'0.5rem'}}>
        <div className="card">
          <div className="card-header">
            <div><div className="card-title">Viewing As</div>
              <div className="card-subtitle">Select a persona to see where this chain is most relevant</div>
            </div>
          </div>
          <div style={{display:'flex',gap:'0.5rem',flexWrap:'wrap',marginBottom:'0.75rem'}}>
            {PERSONAS.map(function(p){ var active=activePersona===p.key; return (
              <button key={p.key} onClick={function(){setActivePersona(active?null:p.key);}} style={{
                padding:'5px 12px',borderRadius:'16px',fontSize:'0.78rem',fontWeight:active?600:400,cursor:'pointer',
                border:'1px solid '+(active?personaColors[p.key]:'var(--border)'),
                background:active?personaColors[p.key]+'22':'transparent',
                color:active?personaColors[p.key]:'var(--text-dim)',transition:'all 0.15s'
              }}>{p.icon} {p.name}</button>
            ); })}
          </div>
          {activePersona && (
            <div style={{maxHeight:'350px',overflowY:'auto'}}>
              <div style={{fontSize:'0.65rem',fontWeight:600,textTransform:'uppercase',letterSpacing:'0.08em',color:'var(--text-faint)',marginBottom:'0.4rem'}}>
                Where This Perspective Is Richest
              </div>
              {LEVELS.map(function(lvl,li){
                var tw = (RHETORIC_TAKEAWAYS[lvl.id]||{})[activePersona];
                if (!tw) return null;
                var sentence = tw.split(/\\.\\s+/)[0] + '.';
                return (
                  <div key={li} style={{display:'flex',alignItems:'center',gap:'0.4rem',padding:'0.25rem 0',borderBottom:'1px solid var(--border)',overflow:'hidden'}}>
                    <span style={{fontSize:'0.6rem',fontWeight:700,color:'var(--lbe-green)',flexShrink:0,background:'var(--green-dim)',borderRadius:'3px',padding:'1px 4px'}}>{lvl.id}</span>
                    <span style={{fontSize:'0.73rem',fontWeight:600,color:'var(--text-bright)',flexShrink:0,whiteSpace:'nowrap'}}>{lvl.title}</span>
                    <span style={{fontSize:'0.71rem',color:'var(--text-muted)',flex:1,overflow:'hidden',textOverflow:'ellipsis',whiteSpace:'nowrap'}}>\u2014 {sentence}</span>
                    <button onClick={function(){setSelectedLevel(li);setActiveTab('rhetoric');}} style={{flexShrink:0,fontSize:'0.62rem',padding:'1px 5px',borderRadius:'8px',border:'1px solid var(--rhetoric)',background:'transparent',color:'var(--rhetoric)',cursor:'pointer',whiteSpace:'nowrap'}}>Rhetoric \u2192</button>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>"""

NEW = """\
      {/* Persona Selector */}
      <div style={{paddingTop:'0.75rem',paddingBottom:'0.25rem'}}>
        <div style={{display:'flex',alignItems:'center',gap:'0.5rem',flexWrap:'wrap',marginBottom:'0.5rem'}}>
          <span style={{fontSize:'0.73rem',color:'var(--text-muted)',whiteSpace:'nowrap'}}>View through a professional lens:</span>
          {PERSONAS.map(function(p){ var active=activePersona===p.key; return (
            <button key={p.key} onClick={function(){setActivePersona(active?null:p.key);}} style={{
              padding:'3px 10px',borderRadius:'16px',fontSize:'0.75rem',fontWeight:active?600:400,cursor:'pointer',
              border:'1px solid '+(active?personaColors[p.key]:'var(--border)'),
              background:active?personaColors[p.key]+'22':'transparent',
              color:active?personaColors[p.key]:'var(--text-dim)',transition:'all 0.15s'
            }}>{p.icon} {p.name}</button>
          ); })}
        </div>
        {activePersona && (
          <div>
            {LEVELS.map(function(lvl,li){
              var tw = (RHETORIC_TAKEAWAYS[lvl.id]||{})[activePersona];
              if (!tw) return null;
              var sentence = tw.split(/\\.\\s+/)[0] + '.';
              return (
                <div key={li} style={{display:'flex',alignItems:'center',gap:'0.4rem',padding:'0.25rem 0',borderBottom:'1px solid var(--border)',overflow:'hidden'}}>
                  <span style={{fontSize:'0.6rem',fontWeight:700,color:'var(--lbe-green)',flexShrink:0,background:'var(--green-dim)',borderRadius:'3px',padding:'1px 4px'}}>{lvl.id}</span>
                  <span style={{fontSize:'0.73rem',fontWeight:600,color:'var(--text-bright)',flexShrink:0,whiteSpace:'nowrap'}}>{lvl.title}</span>
                  <span style={{fontSize:'0.71rem',color:'var(--text-muted)',flex:1,overflow:'hidden',textOverflow:'ellipsis',whiteSpace:'nowrap'}}>\u2014 {sentence}</span>
                  <button onClick={function(){setSelectedLevel(li);setActiveTab('rhetoric');}} style={{flexShrink:0,fontSize:'0.62rem',padding:'1px 5px',borderRadius:'8px',border:'1px solid var(--rhetoric)',background:'transparent',color:'var(--rhetoric)',cursor:'pointer',whiteSpace:'nowrap'}}>Rhetoric \u2192</button>
                </div>
              );
            })}
          </div>
        )}
      </div>"""

with open(FILE, "r", encoding="utf-8") as f:
    html = f.read()

assert OLD in html, "Fix B: persona selector block not found — check exact whitespace/chars"
html = html.replace(OLD, NEW, 1)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Fix B applied: persona selector simplified to inline label → {FILE}")
