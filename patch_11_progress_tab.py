"""patch_11_progress_tab.py — add ProgressTab component"""
F = "DC-AI-001_v2_0_0.html"

INJECT_ANCHOR = "// ═══════════════════════════════════════════════════════════════\n// SIDEBAR COMPONENTS"

PROGRESS_COMPONENT = r"""// ═══════════════════════════════════════════════════════════════
// PROGRESS TAB
// ═══════════════════════════════════════════════════════════════
function ProgressTab({ selectedLevel, visitedStages }) {
  var totalStages = LEVELS.length * 3;
  var completed = 0;
  LEVELS.forEach(function(lvl, i) {
    var vs = (visitedStages && visitedStages[i]) || {};
    if (vs.grammar)  completed++;
    if (vs.logic)    completed++;
    if (vs.rhetoric) completed++;
  });
  var pct = Math.round((completed / totalStages) * 100);

  var storedAnswers = safeLoad('aq_answers', {});
  var assessmentDone = Object.keys(storedAnswers).length === 27;
  var assessmentScore = Object.values(storedAnswers).filter(function(a){ return a.correct; }).length;

  var META = [
    ['Module ID', 'DC-AI-001'],['Version', '2.0.0'],
    ['Series', 'DC-AI (8 modules)'],['Topic', 'Power Density'],
    ['Publisher', 'Legacy Business Engineers Ltd'],
    ['Contact', 'lmurphy@legacybe.ie']
  ];

  return (
    <div className="main-content">
      {/* Overall progress */}
      <div className="card">
        <div className="card-header">
          <div className="card-icon green">📊</div>
          <div><div className="card-title">Overall Progress</div>
            <div className="card-subtitle">{completed} of {totalStages} stages complete ({pct}%)</div>
          </div>
        </div>
        <div style={{height:'8px',background:'var(--border)',borderRadius:'4px',overflow:'hidden',marginBottom:'1rem'}}>
          <div style={{height:'100%',width:pct+'%',background:'linear-gradient(90deg,var(--lbe-green),var(--grammar))',transition:'width 0.4s ease'}}/>
        </div>

        {/* Per-level dots */}
        {LEVELS.map(function(lvl, i) {
          var vs = (visitedStages && visitedStages[i]) || {};
          return (
            <div key={i} style={{display:'flex',alignItems:'center',gap:'0.75rem',padding:'0.45rem 0',borderBottom:'1px solid var(--border)'}}>
              <span style={{fontSize:'1rem',width:'24px',textAlign:'center'}}>{lvl.icon}</span>
              <div style={{flex:1,minWidth:0}}>
                <span style={{fontSize:'0.82rem',fontWeight:500,color:'var(--text-bright)'}}>{lvl.id}: {lvl.title}</span>
              </div>
              <div style={{display:'flex',gap:'5px'}}>
                {[['G','grammar','var(--grammar)'],['L','logic','var(--logic)'],['R','rhetoric','var(--rhetoric)']].map(function(dot){
                  var done = !!vs[dot[1]];
                  return <span key={dot[0]} title={dot[1]} style={{width:'14px',height:'14px',borderRadius:'50%',background:done?dot[2]:'var(--border)',display:'flex',alignItems:'center',justifyContent:'center',fontSize:'8px',color:done?'#fff':'var(--text-faint)',fontWeight:700}}>{done?dot[0]:dot[0]}</span>;
                })}
              </div>
            </div>
          );
        })}
      </div>

      {/* Assessment results */}
      {assessmentDone && (
        <div className="card">
          <div className="card-header">
            <div className="card-icon blue">📝</div>
            <div><div className="card-title">Assessment Results</div>
              <div className="card-subtitle">Last completed run</div>
            </div>
          </div>
          <div style={{fontSize:'1.4rem',fontWeight:700,color:'var(--grammar)'}}>{assessmentScore}<span style={{fontSize:'0.9rem',color:'var(--text-muted)'}}>/27 ({Math.round(assessmentScore/27*100)}%)</span></div>
        </div>
      )}

      {/* Module info */}
      <div className="card">
        <div className="card-header">
          <div className="card-icon cyan">ℹ️</div>
          <div><div className="card-title">Module Information</div></div>
        </div>
        <table style={{width:'100%',borderCollapse:'collapse',fontSize:'0.78rem'}}>
          <tbody>
            {META.map(function(r,i){ return (
              <tr key={i} style={{borderBottom:'1px solid var(--border)',background:i%2===0?'transparent':'var(--panel)'}}>
                <td style={{padding:'5px 8px',color:'var(--text-muted)',width:'40%'}}>{r[0]}</td>
                <td style={{padding:'5px 8px',color:'var(--text)',fontFamily:'var(--font-mono)',fontSize:'0.75rem'}}>{r[1]}</td>
              </tr>
            ); })}
          </tbody>
        </table>
      </div>
    </div>
  );
}

"""

html = open(F, encoding="utf-8").read()
assert INJECT_ANCHOR in html, "Sidebar anchor not found"
html = html.replace(INJECT_ANCHOR, PROGRESS_COMPONENT + INJECT_ANCHOR, 1)
open(F, "w", encoding="utf-8").write(html)
print("patch_11 done — ProgressTab added")
