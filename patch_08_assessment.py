"""patch_08_assessment.py — add timer, pre-start screen, tier breakdown, immediate feedback"""
F = "DC-AI-001_v2_0_0.html"

OLD_FUNC_OPEN = "function AssessmentTab() {\n  var [shuffledQs, setShuffledQs] = React.useState(function() {\n    return shuffleArray(ASSESSMENT_QUESTIONS);\n  });"

NEW_FUNC = r"""function AssessmentTab() {
  var [started, setStarted] = React.useState(false);
  var [shuffledQs] = React.useState(function(){ return shuffleArray(ASSESSMENT_QUESTIONS); });
  var [current, setCurrent] = React.useState(0);
  var [answers, setAnswers] = React.useState({});
  var [done, setDone] = React.useState(false);
  var [seconds, setSeconds] = React.useState(0);
  var [filterTier, setFilterTier] = React.useState('all');
  var [filterLevel, setFilterLevel] = React.useState('all');

  React.useEffect(function() {
    if (!started || done) return;
    var t = setInterval(function(){ setSeconds(function(s){ return s+1; }); }, 1000);
    return function(){ clearInterval(t); };
  }, [started, done]);

  function fmt(s) { return String(Math.floor(s/60)).padStart(2,'0')+':'+String(s%60).padStart(2,'0'); }

  var total = shuffledQs.length;
  var q = shuffledQs[current] || {};
  var ansState = answers[current];
  var revealed = !!ansState;

  function handleOption(oi) {
    if (revealed) return;
    var isCorrect = oi === q.correct;
    var newA = Object.assign({}, answers);
    newA[current] = { selected: oi, correct: isCorrect };
    setAnswers(newA);
  }

  function handleNext() {
    if (current < total - 1) { setCurrent(current + 1); }
    else { setDone(true); }
  }

  function handleRestart() {
    setStarted(false); setCurrent(0); setAnswers({}); setDone(false); setSeconds(0);
  }

  var TIERS = ['knowledge','calculation','judgement'];
  var TIER_LABELS = { knowledge:'Knowledge Check', calculation:'Eng. Calculation', judgement:'Prof. Judgement' };

  /* Pre-start screen */
  if (!started) return (
    <div className="main-content">
      <div className="card">
        <div className="card-header"><div className="card-icon blue">📝</div>
          <div><div className="card-title">DC-AI-001 Assessment</div>
            <div className="card-subtitle">27 questions · three Trivium stages · 9 per stage</div></div></div>
        {TIERS.map(function(t){ return (
          <div key={t} style={{display:'flex',justifyContent:'space-between',padding:'0.6rem 0',borderBottom:'1px solid var(--border)',fontSize:'0.83rem'}}>
            <span style={{color:'var(--text)'}}>{TIER_LABELS[t]}</span>
            <span style={{color:'var(--text-muted)',fontFamily:'var(--font-mono)'}}>9 questions</span>
          </div>
        ); })}
        <button onClick={function(){setStarted(true);}} style={{marginTop:'1.25rem',padding:'10px 28px',borderRadius:'var(--radius-sm)',background:'var(--grammar)',color:'#fff',fontWeight:600,fontSize:'0.9rem',border:'none',cursor:'pointer',width:'100%'}}>
          Start Assessment →
        </button>
      </div>
    </div>
  );

  /* Score screen */
  if (done) {
    var score = Object.values(answers).filter(function(a){return a.correct;}).length;
    var pct = Math.round((score/total)*100);
    var tierScores = TIERS.map(function(t){
      var qs = shuffledQs.filter(function(q){return q.tier===t;});
      var correct = qs.filter(function(q,i){ var idx=shuffledQs.indexOf(q); return answers[idx]&&answers[idx].correct; }).length;
      return { t:t, correct:correct, total:qs.length };
    });
    var filteredReview = shuffledQs.filter(function(q,i){
      if (filterTier!=='all' && q.tier!==filterTier) return false;
      if (filterLevel!=='all' && String(q.level)!==filterLevel) return false;
      return true;
    });
    return (
      <div className="main-content">
        <div className="card">
          <div style={{textAlign:'center',padding:'1rem 0'}}>
            <div style={{fontSize:'2.5rem',fontWeight:700,color:'var(--grammar)'}}>{score}<span style={{fontSize:'1.2rem',color:'var(--text-muted)'}}>/{total}</span></div>
            <div style={{fontSize:'1rem',color:'var(--text-bright)',marginTop:'0.25rem'}}>{pct}% · {fmt(seconds)}</div>
            <div style={{height:'6px',background:'var(--border)',borderRadius:'3px',margin:'0.75rem auto',maxWidth:'300px',overflow:'hidden'}}>
              <div style={{height:'100%',width:pct+'%',background:'linear-gradient(90deg,var(--lbe-green),var(--grammar))',borderRadius:'3px'}}/>
            </div>
          </div>
          <div style={{display:'grid',gridTemplateColumns:'repeat(3,1fr)',gap:'0.5rem',marginBottom:'1rem'}}>
            {tierScores.map(function(ts){ return (
              <div key={ts.t} style={{background:'var(--panel)',border:'1px solid var(--border)',borderRadius:'var(--radius-sm)',padding:'0.6rem',textAlign:'center'}}>
                <div style={{fontSize:'0.68rem',color:'var(--text-muted)',textTransform:'uppercase',letterSpacing:'0.06em'}}>{TIER_LABELS[ts.t]}</div>
                <div style={{fontSize:'1.2rem',fontWeight:600,color:'var(--text-bright)',marginTop:'2px'}}>{ts.correct}/{ts.total}</div>
              </div>
            ); })}
          </div>
          <div style={{display:'flex',gap:'0.4rem',flexWrap:'wrap',marginBottom:'0.75rem'}}>
            {['all'].concat(TIERS).map(function(t){ return (
              <button key={t} onClick={function(){setFilterTier(t);}} style={{padding:'3px 10px',borderRadius:'12px',fontSize:'0.72rem',border:'1px solid '+(filterTier===t?'var(--grammar)':'var(--border)'),background:filterTier===t?'var(--accent-dim)':'transparent',color:filterTier===t?'var(--grammar)':'var(--text-dim)',cursor:'pointer'}}>{t==='all'?'All Tiers':TIER_LABELS[t]}</button>
            ); })}
            {[1,2,3,4,5,6,7,8,9].map(function(l){ return (
              <button key={l} onClick={function(){setFilterLevel(filterLevel===String(l)?'all':String(l));}} style={{padding:'3px 10px',borderRadius:'12px',fontSize:'0.72rem',border:'1px solid '+(filterLevel===String(l)?'var(--grammar)':'var(--border)'),background:filterLevel===String(l)?'var(--accent-dim)':'transparent',color:filterLevel===String(l)?'var(--grammar)':'var(--text-dim)',cursor:'pointer'}}>L{l}</button>
            ); })}
          </div>
          {filteredReview.map(function(qr,i){
            var idx=shuffledQs.indexOf(qr); var ar=answers[idx]||{}; var isC=ar.correct;
            return (
              <div key={i} style={{background:isC?'rgba(22,163,74,0.06)':'rgba(220,38,38,0.06)',border:'1px solid '+(isC?'var(--lbe-green)':'var(--error)'),borderRadius:'var(--radius-sm)',padding:'0.7rem',marginBottom:'0.5rem',fontSize:'0.82rem'}}>
                <div style={{display:'flex',gap:'0.4rem',marginBottom:'0.3rem'}}>
                  <span style={{fontFamily:'var(--font-mono)',fontSize:'0.7rem',background:'var(--panel)',padding:'1px 6px',borderRadius:'4px'}}>L{qr.level}</span>
                  <span style={{color:isC?'var(--lbe-green)':'var(--error)',fontWeight:600}}>{isC?'✓ Correct':'✗ Incorrect'}</span>
                </div>
                <div style={{color:'var(--text)',marginBottom:'0.3rem'}}>{qr.q}</div>
                {qr.explain && <div style={{color:'var(--text-muted)',fontSize:'0.78rem'}}>{qr.explain}</div>}
              </div>
            );
          })}
          <button onClick={handleRestart} style={{marginTop:'1rem',padding:'8px 20px',borderRadius:'var(--radius-sm)',border:'1px solid var(--border)',background:'var(--panel)',color:'var(--text)',cursor:'pointer',fontSize:'0.82rem'}}>Reset Assessment</button>
        </div>
      </div>
    );
  }

  /* Question screen */
  var optionLetters = ['A','B','C','D'];
  return (
    <div>
      <div className="assessment-header">
        <div className="assessment-progress">Question {current+1} of {total}</div>
        <div style={{fontFamily:'var(--font-mono)',fontSize:'0.9rem',color:'var(--grammar)',fontWeight:600}}>{fmt(seconds)}</div>
        <div style={{fontSize:'0.78rem',color:'var(--text-faint)'}}>Score: {Object.values(answers).filter(function(a){return a.correct;}).length}/{Object.keys(answers).length||0}</div>
      </div>
      <div className="progress-bar-wrap">
        <div className="progress-bar-fill" style={{width:((current/total)*100)+'%'}} />
      </div>
      <div className="q-card">
        <div className="q-meta">
          <span className="q-level-badge">L{q.level}</span>
          <span className={'q-tier-badge '+(q.tier||'knowledge')}>{TIER_LABELS[q.tier]||q.tier}</span>
          <span className="q-id">{q.id}</span>
        </div>
        <div className="q-text">{q.q}</div>
        <div className="q-options">
          {(q.options||[]).map(function(opt,oi){
            var cls='q-option-btn';
            if (revealed){ if(oi===q.correct) cls+=' correct'; else if(oi===ansState.selected&&oi!==q.correct) cls+=' incorrect'; }
            else if(ansState&&oi===ansState.selected) cls+=' selected';
            return (
              <button key={oi} className={cls} onClick={function(){handleOption(oi);}} disabled={revealed}>
                <span className="q-option-letter">{optionLetters[oi]}</span><span>{opt}</span>
              </button>
            );
          })}
        </div>
        {revealed && q.explain && (
          <div className={'q-explain'+(ansState.correct?'':' wrong')}>
            <div className="q-explain-label">{ansState.correct?'✓ Correct':'✗ Incorrect'}</div>
            {q.explain}
          </div>
        )}
        <div className="q-nav">
          <div/>
          {revealed
            ? <button className="q-nav-btn primary" onClick={handleNext}>{current<total-1?'Next →':'See Results'}</button>
            : (ansState ? null : <div style={{fontSize:'0.78rem',color:'var(--text-faint)'}}>Select an answer above</div>)
          }
        </div>
      </div>
    </div>
  );
}"""

# Find and replace the whole AssessmentTab up to the closing brace before BSGTab comment
ANCHOR_END = "\n\n// ═══════════════════════════════════════════════════════════════\n// BSG TAB COMPONENT"

html = open(F, encoding="utf-8").read()
assert OLD_FUNC_OPEN in html, "AssessmentTab opening not found"

start = html.index(OLD_FUNC_OPEN)
end   = html.index(ANCHOR_END, start)
html  = html[:start] + NEW_FUNC + html[end:]
open(F, "w", encoding="utf-8").write(html)
print("patch_08 done — Assessment upgraded with timer, pre-start, tier breakdown, immediate feedback")
