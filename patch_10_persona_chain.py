"""patch_10_persona_chain.py — upgrade ChainTab with persona selector + RHETORIC_TAKEAWAYS map"""
F = "DC-AI-001_v2_0_0.html"

OLD_OPEN = "function ChainTab({ selectedLevel, setSelectedLevel, setActiveTab }) {\n  var level = LEVELS[selectedLevel];\n  var [expandedEnglish, setExpandedEnglish] = React.useState({});\n  var [expandedRefs,    setExpandedRefs]    = React.useState({});\n  return ("

NEW_OPEN = r"""function ChainTab({ selectedLevel, setSelectedLevel, setActiveTab }) {
  var level = LEVELS[selectedLevel];
  var [expandedEnglish, setExpandedEnglish] = React.useState({});
  var [expandedRefs,    setExpandedRefs]    = React.useState({});
  var [activePersona, setActivePersona] = React.useState(null);

  var personaColors = { asset_management:'#2563EB',technology:'#7c3aed',technical:'#d97706',compliance:'#16a34a',cost:'#dc2626' };

  return ("""

# Find the closing of ChainTab return — inject persona selector before closing </div>
# The ChainTab return closes with `    </div>\n  );\n}\n\n// ═══...GRAMMAR`
OLD_CHAIN_END = """      </div>
    </div>
  );
}

// ═══════════════════════════════════════════════════════════════
// GRAMMAR TAB COMPONENT"""

NEW_CHAIN_END = r"""      </div>

      {/* Persona Selector */}
      <div className="main-content" style={{paddingTop:'0.5rem'}}>
        <div className="card">
          <div className="card-header">
            <div className="card-icon green">👤</div>
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
            <div>
              <div style={{fontSize:'0.7rem',fontWeight:600,textTransform:'uppercase',letterSpacing:'0.08em',color:'var(--text-faint)',marginBottom:'0.5rem'}}>
                Where This Perspective Is Richest
              </div>
              {LEVELS.map(function(lvl,li){
                var tw = (RHETORIC_TAKEAWAYS[lvl.id]||{})[activePersona];
                if (!tw) return null;
                return (
                  <div key={li} style={{display:'flex',gap:'0.75rem',alignItems:'flex-start',padding:'0.5rem 0',borderBottom:'1px solid var(--border)'}}>
                    <span style={{fontSize:'1rem',flexShrink:0}}>{lvl.icon}</span>
                    <div style={{flex:1,minWidth:0}}>
                      <div style={{fontSize:'0.75rem',fontWeight:600,color:'var(--text-bright)'}}>{lvl.id}: {lvl.title}</div>
                      <div style={{fontSize:'0.75rem',color:'var(--text-muted)',lineHeight:'1.5',marginTop:'2px'}}>{tw}</div>
                    </div>
                    <button onClick={function(){setSelectedLevel(li);setActiveTab('learn');}} style={{flexShrink:0,fontSize:'0.7rem',padding:'2px 8px',borderRadius:'10px',border:'1px solid var(--border)',background:'transparent',color:'var(--text-dim)',cursor:'pointer'}}>Learn →</button>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════════════════════════
// GRAMMAR TAB COMPONENT"""

html = open(F, encoding="utf-8").read()
for label, old in [("func open", OLD_OPEN), ("chain end", OLD_CHAIN_END)]:
    assert old in html, f"{label} not found"
html = html.replace(OLD_OPEN, NEW_OPEN, 1)
html = html.replace(OLD_CHAIN_END, NEW_CHAIN_END, 1)
open(F, "w", encoding="utf-8").write(html)
print("patch_10 done — persona selector with takeaway map added to ChainTab")
