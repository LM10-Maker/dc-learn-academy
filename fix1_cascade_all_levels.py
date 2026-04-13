#!/usr/bin/env python3
"""Fix 1: SidebarCalculator runs ALL 9 levels when 'Find Bottlenecks' is clicked."""
import re

src = '/home/user/dc-learn-academy/DC-AI-001_v2_3_0 (3).html'
with open(src, 'r', encoding='utf-8') as f:
    html = f.read()

OLD = """function SidebarCalculator({ selectedLevel, onCascadeResult }) {
  var level = LEVELS[selectedLevel] || {};
  var fnSrc = level.cascadeCheck || '';
  var cascadeCheck = null;
  try { cascadeCheck = fnSrc ? new Function('inputs', fnSrc.replace(/^function\\s*\\(inputs\\)\\s*\\{/, '').replace(/\\}\\s*$/, '')) : null; } catch(e) {}

  var [rackCount, setRackCount] = React.useState(50);
  var [targetKW, setTargetKW] = React.useState(40);
  var [result, setResult] = React.useState(null);

  function runCheck() {
    if (!cascadeCheck) { var r={pass:false,reason:'No cascade check for this level.'}; setResult(r); if(onCascadeResult) onCascadeResult(selectedLevel,r); return; }
    try {
      var r = cascadeCheck({rackCount:Number(rackCount),targetKW:Number(targetKW)});
      setResult(r);
      if (onCascadeResult) onCascadeResult(selectedLevel, r);
    } catch(e) {
      var r = {pass:false,reason:'Calculation error: '+e.message};
      setResult(r);
      if (onCascadeResult) onCascadeResult(selectedLevel, r);
    }
  }

  return (
    <div className="sidebar-card">
      <div className="sidebar-card-title">AI Readiness Calculator</div>
      <div style={{fontSize:'0.75rem',color:'var(--text-muted)',marginBottom:'0.6rem'}}>Level {level.level||'—'}: {level.title||''}</div>
      <label style={{fontSize:'0.72rem',color:'var(--text-dim)'}}>Rack count
        <input type="number" value={rackCount} onChange={function(e){setRackCount(e.target.value);}} style={{display:'block',width:'100%',padding:'5px 8px',marginTop:'3px',background:'var(--panel)',border:'1px solid var(--border)',borderRadius:'var(--radius-sm)',color:'var(--text)',fontSize:'0.8rem',fontFamily:'var(--font-mono)'}} />
      </label>
      <label style={{fontSize:'0.72rem',color:'var(--text-dim)',marginTop:'0.5rem',display:'block'}}>Target kW/rack
        <input type="number" value={targetKW} onChange={function(e){setTargetKW(e.target.value);}} style={{display:'block',width:'100%',padding:'5px 8px',marginTop:'3px',background:'var(--panel)',border:'1px solid var(--border)',borderRadius:'var(--radius-sm)',color:'var(--text)',fontSize:'0.8rem',fontFamily:'var(--font-mono)'}} />
      </label>
      <button onClick={runCheck} style={{marginTop:'0.75rem',width:'100%',padding:'7px',background:'var(--lbe-green)',color:'#fff',border:'none',borderRadius:'var(--radius-sm)',fontWeight:600,fontSize:'0.8rem',cursor:'pointer'}}>Find Bottlenecks →</button>
      {result && (
        <div style={{marginTop:'0.6rem',padding:'0.5rem 0.7rem',borderRadius:'var(--radius-sm)',background:result.pass?'rgba(74,124,89,0.08)':'rgba(220,38,38,0.08)',border:'1px solid '+(result.pass?'var(--lbe-green)':'var(--error)'),fontSize:'0.75rem',color:'var(--text)',lineHeight:'1.5'}}>
          <strong style={{color:result.pass?'var(--lbe-green)':'var(--error)'}}>{result.pass?'✓ PASS':'✗ FAIL'}</strong> — {result.reason}
        </div>
      )}
    </div>
  );
}"""

NEW = """function SidebarCalculator({ selectedLevel, onCascadeResult }) {
  var [rackCount, setRackCount] = React.useState(50);
  var [targetKW, setTargetKW] = React.useState(40);
  var [allResults, setAllResults] = React.useState(null);

  function runCheck() {
    var results = [];
    LEVELS.forEach(function(lvl, idx) {
      var fnSrc = lvl.cascadeCheck || '';
      var fn = null;
      try { fn = fnSrc ? new Function('inputs', fnSrc.replace(/^function\\s*\\(inputs\\)\\s*\\{/, '').replace(/\\}\\s*$/, '')) : null; } catch(e) {}
      var r;
      if (!fn) { r = {pass:false,reason:'No cascade check for this level.'}; }
      else { try { r = fn({rackCount:Number(rackCount),targetKW:Number(targetKW)}); } catch(e) { r = {pass:false,reason:'Error: '+e.message}; } }
      results.push(r);
      if (onCascadeResult) onCascadeResult(idx, r);
    });
    setAllResults(results);
  }

  var failCount = allResults ? allResults.filter(function(r){return !r.pass;}).length : 0;
  var iStyle = {display:'block',width:'100%',padding:'5px 8px',marginTop:'3px',background:'var(--panel)',border:'1px solid var(--border)',borderRadius:'var(--radius-sm)',color:'var(--text)',fontSize:'0.8rem',fontFamily:'var(--font-mono)'};
  return (
    <div className="sidebar-card">
      <div className="sidebar-card-title">AI Readiness Calculator</div>
      <div style={{fontSize:'0.75rem',color:'var(--text-muted)',marginBottom:'0.6rem'}}>Runs all 9 levels simultaneously</div>
      <label style={{fontSize:'0.72rem',color:'var(--text-dim)'}}>Rack count
        <input type="number" value={rackCount} onChange={function(e){setRackCount(e.target.value);}} style={iStyle} />
      </label>
      <label style={{fontSize:'0.72rem',color:'var(--text-dim)',marginTop:'0.5rem',display:'block'}}>Target kW/rack
        <input type="number" value={targetKW} onChange={function(e){setTargetKW(e.target.value);}} style={iStyle} />
      </label>
      <button onClick={runCheck} style={{marginTop:'0.75rem',width:'100%',padding:'7px',background:'var(--lbe-green)',color:'#fff',border:'none',borderRadius:'var(--radius-sm)',fontWeight:600,fontSize:'0.8rem',cursor:'pointer'}}>Find Bottlenecks →</button>
      {allResults && (
        <div style={{marginTop:'0.6rem'}}>
          <div style={{fontSize:'0.8rem',fontWeight:700,color:failCount>0?'var(--red)':'var(--green)',marginBottom:'0.4rem',padding:'4px 8px',borderRadius:'var(--radius-sm)',background:failCount>0?'var(--red-dim)':'var(--green-dim)'}}>
            {failCount} bottleneck{failCount!==1?'s':''} found
          </div>
          {allResults.map(function(r,idx){
            var lvl=LEVELS[idx];
            return (
              <div key={idx} style={{padding:'5px 7px',marginBottom:'3px',borderRadius:'var(--radius-sm)',background:'var(--panel)',border:'1px solid var(--border)',fontSize:'0.72rem'}}>
                <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',gap:4}}>
                  <span style={{color:'var(--text-bright)',fontWeight:600}}>L{lvl.level}: {lvl.title}</span>
                  <span style={{fontWeight:700,padding:'1px 5px',borderRadius:3,background:r.pass?'var(--green-dim)':'var(--red-dim)',color:r.pass?'var(--green)':'var(--red)',whiteSpace:'nowrap'}}>{r.pass?'PASS':'FAIL'}</span>
                </div>
                <div style={{color:'var(--text-muted)',marginTop:'2px',lineHeight:1.4}}>{r.reason}</div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}"""

assert OLD in html, "Fix1: OLD text not found"
html = html.replace(OLD, NEW, 1)
with open(src, 'w', encoding='utf-8') as f:
    f.write(html)
print("Fix 1 applied: SidebarCalculator now runs all 9 levels.")
