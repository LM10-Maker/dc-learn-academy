DST = "/home/user/dc-learn-academy/DC-AI-001_v3_0_0.html"
with open(DST, encoding='utf-8') as f: h = f.read()

# ── 1. SidebarCalculator component ──────────────────────────────────────────
SC = r"""
function SidebarCalculator({ selectedLevel, onCascadeResult }) {
  var [rackCount, setRackCount] = React.useState(50);
  var [targetKW, setTargetKW] = React.useState(40);
  var [allResults, setAllResults] = React.useState(null);
  function runCheck() {
    var results = [];
    LEVELS.forEach(function(lvl, idx) {
      var fnSrc = lvl.cascadeCheck || '';
      var fn = null;
      try { fn = fnSrc ? new Function('inputs', fnSrc.replace(/^function\s*\(inputs\)\s*\{/, '').replace(/\}\s*$/, '')) : null; } catch(e) {}
      var r;
      if (!fn) { r = {pass:false,reason:'No cascade check for this level.'}; }
      else { try { r = fn({rackCount:Number(rackCount),targetKW:Number(targetKW)}); } catch(e) { r = {pass:false,reason:'Error: '+e.message}; } }
      results.push(r);
      if (onCascadeResult) onCascadeResult(idx, r);
    });
    setAllResults(results);
  }
  var failCount = allResults ? allResults.filter(function(r){return !r.pass;}).length : 0;
  var iStyle = {display:'block',width:'100%',padding:'5px 8px',marginTop:'3px',background:'var(--panel)',border:'1px solid var(--border)',borderRadius:'6px',color:'var(--text)',fontSize:'0.8rem',fontFamily:'var(--font-mono)'};
  return (
    <div className="sidebar-card">
      <div style={{fontWeight:700,fontSize:14,color:'var(--text-bright)',marginBottom:10}}>AI Readiness Calculator</div>
      <label style={{fontSize:'0.72rem',color:'var(--text-dim)'}}>Rack count<input type="number" value={rackCount} onChange={function(e){setRackCount(e.target.value);}} style={iStyle} /></label>
      <label style={{fontSize:'0.72rem',color:'var(--text-dim)',marginTop:'0.5rem',display:'block'}}>Target kW/rack<input type="number" value={targetKW} onChange={function(e){setTargetKW(e.target.value);}} style={iStyle} /></label>
      <button onClick={runCheck} style={{marginTop:'0.75rem',width:'100%',padding:'7px',background:'var(--lbe-green)',color:'#fff',border:'none',borderRadius:'6px',fontWeight:600,fontSize:'0.8rem',cursor:'pointer'}}>Find Bottlenecks \u2192</button>
      {allResults && (<div style={{marginTop:'0.6rem'}}>
        <div style={{fontSize:'0.8rem',fontWeight:700,color:failCount>0?'var(--red)':'var(--green)',marginBottom:'0.4rem',padding:'4px 8px',borderRadius:'6px',background:failCount>0?'var(--red-dim)':'var(--green-dim)'}}>{failCount} bottleneck{failCount!==1?'s':''} found</div>
        {allResults.map(function(r,idx){var lvl=LEVELS[idx];return (<div key={idx} style={{padding:'5px 7px',marginBottom:'3px',borderRadius:'6px',background:'var(--panel)',border:'1px solid var(--border)',fontSize:'0.72rem'}}><div style={{display:'flex',justifyContent:'space-between',alignItems:'center',gap:4}}><span style={{color:'var(--text-bright)',fontWeight:600}}>L{lvl.level}: {lvl.title}</span><span style={{fontWeight:700,padding:'1px 5px',borderRadius:3,background:r.pass?'var(--green-dim)':'var(--red-dim)',color:r.pass?'var(--green)':'var(--red)',whiteSpace:'nowrap'}}>{r.pass?'PASS':'FAIL'}</span></div><div style={{color:'var(--text-muted)',marginTop:'2px',lineHeight:1.4}}>{r.reason}</div></div>);})}
      </div>)}
    </div>
  );
}
"""

SF = r"""
function SidebarFacility() {
  var rows = [['Facility','Clonshaugh Reference DC (2012)'],['Racks','200 (Hall B)'],['Avg Density','8 kW/rack'],['IT Load','1.6 MW'],['PUE','1.50 (target 1.20)'],['MIC','5 MVA @ 10 kV ESB Networks'],['MIC Util.','~85%'],['Bus Section','1,600A @ 415V'],['Bus Util.','~73%'],['PDUs','Dual 32A single-phase'],['Voltage','415V 3-phase'],['PF','0.85']];
  return (
    <div className="sidebar-card">
      <div style={{fontWeight:700,fontSize:14,color:'var(--text-bright)',marginBottom:10}}>Facility Profile</div>
      <table style={{width:'100%',borderCollapse:'collapse',fontSize:'0.73rem'}}><tbody>{rows.map(function(r,i){return (<tr key={i} style={{borderBottom:'1px solid var(--border)',background:i%2===0?'transparent':'var(--panel)'}}><td style={{padding:'3px 6px',color:'var(--text-muted)',whiteSpace:'nowrap'}}>{r[0]}</td><td style={{padding:'3px 6px',color:'var(--text)',fontFamily:'var(--font-mono)',fontSize:'0.7rem'}}>{r[1]}</td></tr>);})}</tbody></table>
    </div>
  );
}
"""

# Insert components before `function App(){`
APP_MARKER = 'function App(){'
idx = h.index(APP_MARKER)
h = h[:idx] + SC + SF + h[idx:]
print("OK: Inserted SidebarCalculator and SidebarFacility")

# ── 2. Add cascadeResults state + handler inside App ────────────────────────
AFTER = "React.useEffect(()=>{try{safeStore.set('dc_ai_001_progress',JSON.stringify(progress));}catch(e){}},[progress]);"
CASCADE_STATE = "\n  const [cascadeResults, setCascadeResults] = React.useState(() => { try { var s = safeStore.get('dc_ai_001_cascadeResults'); return s ? JSON.parse(s) : {}; } catch(e) { return {}; } });\n  function onCascadeResult(lvlIdx, res) { setCascadeResults(function(p) { var n = Object.assign({}, p); n[lvlIdx] = res; safeStore.set('dc_ai_001_cascadeResults', JSON.stringify(n)); return n; }); }"
h = h.replace(AFTER, AFTER + CASCADE_STATE, 1)
print("OK: Added cascadeResults state and onCascadeResult to App")

# ── 3. Pass cascadeResults to ChainTab ──────────────────────────────────────
OLD_CT = '{activeTab===\'chain\' && <ChainTab setActiveTab={setActiveTab} setSelectedLevel={setSelectedLevel} progress={progress} persona={persona} onPersona={handlePersona} onPersonaLevel={handlePersonaLevel} PERSONA_MAP={PERSONA_MAP}/>'
NEW_CT = '{activeTab===\'chain\' && <ChainTab setActiveTab={setActiveTab} setSelectedLevel={setSelectedLevel} progress={progress} persona={persona} onPersona={handlePersona} onPersonaLevel={handlePersonaLevel} PERSONA_MAP={PERSONA_MAP} cascadeResults={cascadeResults}/>'
h = h.replace(OLD_CT, NEW_CT, 1)
print("OK: Passed cascadeResults to ChainTab")

# ── 4. Add sidebar tools section in App render ───────────────────────────────
SIDEBAR_ANCHOR = '<div style={{display:\'flex\',gap:12,flexWrap:\'wrap\',margin:\'0 auto\',maxWidth:1100,padding:\'0 20px\'}} className="no-print">'
SIDEBAR_INSERT = '<div style={{display:\'flex\',gap:12,flexWrap:\'wrap\',margin:\'16px auto 0\',maxWidth:1100,padding:\'0 20px\'}} className="no-print"><div style={{flex:\'0 0 320px\'}}><SidebarCalculator selectedLevel={selectedLevel} onCascadeResult={onCascadeResult} /><SidebarFacility /></div></div>\n      '
h = h.replace(SIDEBAR_ANCHOR, SIDEBAR_INSERT + SIDEBAR_ANCHOR, 1)
print("OK: Added SidebarCalculator and SidebarFacility to App render")

with open(DST, 'w', encoding='utf-8') as f: f.write(h)
print(f"\nScript 5 complete. File: {len(h)} chars, {h.count(chr(10))+1} lines")
