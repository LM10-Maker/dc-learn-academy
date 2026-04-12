"""patch_09_sidebar_components.py — add SidebarCalculator, SidebarFacility, SidebarMethodology"""
F = "DC-AI-001_v2_0_0.html"

INJECT_ANCHOR = "function App() {"

NEW_COMPONENTS = r"""// ═══════════════════════════════════════════════════════════════
// SIDEBAR COMPONENTS
// ═══════════════════════════════════════════════════════════════
function SidebarCalculator({ selectedLevel }) {
  var level = LEVELS[selectedLevel] || {};
  var fnSrc = level.cascadeCheck || '';
  var cascadeCheck = null;
  try { cascadeCheck = fnSrc ? new Function('inputs', fnSrc.replace(/^function\s*\(inputs\)\s*\{/, '').replace(/\}\s*$/, '')) : null; } catch(e) {}

  var [rackCount, setRackCount] = React.useState(50);
  var [targetKW, setTargetKW] = React.useState(40);
  var [result, setResult] = React.useState(null);

  function runCheck() {
    if (!cascadeCheck) { setResult({pass:false,reason:'No cascade check for this level.'}); return; }
    try { setResult(cascadeCheck({rackCount:Number(rackCount),targetKW:Number(targetKW)})); }
    catch(e) { setResult({pass:false,reason:'Calculation error: '+e.message}); }
  }

  return (
    <div className="sidebar-card">
      <div className="sidebar-card-title">⚡ AI Readiness Calculator</div>
      <div style={{fontSize:'0.75rem',color:'var(--text-muted)',marginBottom:'0.6rem'}}>Level {level.level||'—'}: {level.title||''}</div>
      <label style={{fontSize:'0.72rem',color:'var(--text-dim)'}}>Rack count
        <input type="number" value={rackCount} onChange={function(e){setRackCount(e.target.value);}} style={{display:'block',width:'100%',padding:'5px 8px',marginTop:'3px',background:'var(--panel)',border:'1px solid var(--border)',borderRadius:'var(--radius-sm)',color:'var(--text)',fontSize:'0.8rem',fontFamily:'var(--font-mono)'}} />
      </label>
      <label style={{fontSize:'0.72rem',color:'var(--text-dim)',marginTop:'0.5rem',display:'block'}}>Target kW/rack
        <input type="number" value={targetKW} onChange={function(e){setTargetKW(e.target.value);}} style={{display:'block',width:'100%',padding:'5px 8px',marginTop:'3px',background:'var(--panel)',border:'1px solid var(--border)',borderRadius:'var(--radius-sm)',color:'var(--text)',fontSize:'0.8rem',fontFamily:'var(--font-mono)'}} />
      </label>
      <button onClick={runCheck} style={{marginTop:'0.75rem',width:'100%',padding:'7px',background:'var(--lbe-green)',color:'#fff',border:'none',borderRadius:'var(--radius-sm)',fontWeight:600,fontSize:'0.8rem',cursor:'pointer'}}>Find Bottlenecks →</button>
      {result && (
        <div style={{marginTop:'0.6rem',padding:'0.5rem 0.7rem',borderRadius:'var(--radius-sm)',background:result.pass?'rgba(22,163,74,0.08)':'rgba(220,38,38,0.08)',border:'1px solid '+(result.pass?'var(--lbe-green)':'var(--error)'),fontSize:'0.75rem',color:'var(--text)',lineHeight:'1.5'}}>
          <strong style={{color:result.pass?'var(--lbe-green)':'var(--error)'}}>{result.pass?'✓ PASS':'✗ FAIL'}</strong> — {result.reason}
        </div>
      )}
    </div>
  );
}

function SidebarFacility() {
  var rows = [
    ['Facility','Clonshaugh Reference DC (2012)'],
    ['Racks','200 (Hall B)'],['Avg Density','8 kW/rack'],
    ['IT Load','1.6 MW'],['PUE','1.50 (target 1.20)'],
    ['MIC','5 MVA @ 10 kV ESB Networks'],
    ['MIC Util.','~85%'],['Bus Section','1,600A @ 415V'],
    ['Bus Util.','~73%'],['PDUs','Dual 32A single-phase'],
    ['Voltage','415V 3-phase'],['PF','0.85']
  ];
  return (
    <div className="sidebar-card">
      <div className="sidebar-card-title">🏢 Facility Profile</div>
      <table style={{width:'100%',borderCollapse:'collapse',fontSize:'0.73rem'}}>
        <tbody>
          {rows.map(function(r,i){ return (
            <tr key={i} style={{borderBottom:'1px solid var(--border)',background:i%2===0?'transparent':'var(--panel)'}}>
              <td style={{padding:'3px 6px',color:'var(--text-muted)',whiteSpace:'nowrap'}}>{r[0]}</td>
              <td style={{padding:'3px 6px',color:'var(--text)',fontFamily:'var(--font-mono)',fontSize:'0.7rem'}}>{r[1]}</td>
            </tr>
          ); })}
        </tbody>
      </table>
    </div>
  );
}

function SidebarMethodology() {
  var items = [
    ['Trivium Method','Grammar → Logic → Rhetoric. Facts first, consequences second, stakeholder communication third.'],
    ['Feynman Clarify','Every fact has three layers: formal definition, plain English, and the number that makes it real.'],
    ['Weakest Link','Each level identifies the most common misconception and the exact steps to correct it.'],
    ['Five Personas','Same finding — five professional perspectives: Fund, CTO, MEP, ESG, QS.']
  ];
  return (
    <div className="sidebar-card">
      <div className="sidebar-card-title">📋 Methodology</div>
      {items.map(function(it,i){ return (
        <div key={i} style={{marginBottom:'0.6rem'}}>
          <div style={{fontSize:'0.72rem',fontWeight:600,color:'var(--text-bright)',marginBottom:'2px'}}>{it[0]}</div>
          <div style={{fontSize:'0.71rem',color:'var(--text-muted)',lineHeight:'1.5'}}>{it[1]}</div>
        </div>
      ); })}
    </div>
  );
}

"""

html = open(F, encoding="utf-8").read()
assert INJECT_ANCHOR in html, "App() anchor not found"
html = html.replace(INJECT_ANCHOR, NEW_COMPONENTS + INJECT_ANCHOR, 1)
open(F, "w", encoding="utf-8").write(html)
print("patch_09 done — SidebarCalculator, SidebarFacility, SidebarMethodology added")
