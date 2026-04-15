#!/usr/bin/env python3
"""Fix 4: Assessment layout — match DC-LEARN benchmark."""

src = '/home/user/dc-learn-academy/DC-AI-001_v2_3_0 (3).html'
with open(src, 'r', encoding='utf-8') as f:
    html = f.read()

# 4a: Update pre-start description box — add tier time allocations
OLD4a = """      <div style={{marginBottom:16,padding:'12px 16px',border:'1px solid var(--green)',borderLeft:'3px solid var(--green)',borderRadius:8,background:'transparent'}}>
        <div style={{fontSize:12,color:'var(--text-dim)',lineHeight:1.7}}>
          27 questions across three Trivium stages — 9 per stage, one per chain level.<br/>
          A 15-minute timer starts on your first answer. Score is shown after each question.
        </div>
      </div>
      <div className="card">
        <div style={{display:'flex',alignItems:'center',gap:12,marginBottom:16}}>
          <div style={{width:44,height:44,borderRadius:'50%',border:'2px solid var(--grammar)',display:'flex',alignItems:'center',justifyContent:'center',fontSize:20}}>⏱</div>
          <div>
            <div style={{fontSize:22,fontWeight:700,color:'var(--grammar)'}}>15:00</div>
            <div style={{fontSize:11,color:'var(--text-muted)'}}>starts on first answer</div>
          </div>
        </div>
        <div style={{marginBottom:16}}>
          {TIERS.map(function(t){ return (
            <div key={t} style={{display:'flex',justifyContent:'space-between',padding:'0.6rem 0',borderBottom:'1px solid var(--border)',fontSize:'0.83rem'}}>
              <span style={{color:'var(--text)'}}>{TIER_LABELS[t]}</span>
              <span style={{color:'var(--text-muted)',fontFamily:'var(--font-mono)'}}>9 questions</span>
            </div>
          ); })}
        </div>
        <button onClick={function(){setStarted(true);}} style={{marginTop:'0.5rem',padding:'10px 28px',borderRadius:'var(--radius-sm)',background:'var(--grammar)',color:'#fff',fontWeight:600,fontSize:'0.9rem',border:'none',cursor:'pointer',width:'100%'}}>
          Start Assessment →
        </button>
      </div>"""
NEW4a = """      <div className="card" style={{marginBottom:16,padding:12,borderLeft:'3px solid var(--green)'}}>
        <div style={{fontSize:12,color:'var(--text-dim)',lineHeight:1.8}}>
          27 questions across three Trivium stages — 9 per stage, one per chain level.<br/>
          <strong>Knowledge Check</strong> (Grammar): can you recall the key facts? <span style={{fontFamily:'var(--font-mono)',fontSize:11,color:'var(--green)'}}>60s</span><br/>
          <strong>Eng. Calculation</strong> (Logic): can you work through the consequences? <span style={{fontFamily:'var(--font-mono)',fontSize:11,color:'var(--green)'}}>120s</span><br/>
          <strong>Prof. Judgement</strong> (Rhetoric): can you explain it to each stakeholder? <span style={{fontFamily:'var(--font-mono)',fontSize:11,color:'var(--green)'}}>90s</span>
        </div>
      </div>
      <div className="card">
        <div style={{display:'flex',alignItems:'center',gap:12,marginBottom:16}}>
          <div style={{width:44,height:44,borderRadius:'50%',border:'2px solid var(--grammar)',display:'flex',alignItems:'center',justifyContent:'center',fontSize:20}}>⏱</div>
          <div>
            <div style={{fontFamily:'var(--font-mono)',fontSize:22,fontWeight:700,color:'var(--grammar)',letterSpacing:2}}>15:00</div>
            <div style={{fontSize:11,color:'var(--text-muted)'}}>starts on first answer</div>
          </div>
        </div>
        <div style={{marginBottom:16}}>
          {TIERS.map(function(t){ return (
            <div key={t} style={{display:'flex',justifyContent:'space-between',padding:'0.6rem 0',borderBottom:'1px solid var(--border)',fontSize:'0.83rem'}}>
              <span style={{color:'var(--text)'}}>{TIER_LABELS[t]}</span>
              <span style={{color:'var(--text-muted)',fontFamily:'var(--font-mono)'}}>9 questions</span>
            </div>
          ); })}
        </div>
        <button onClick={function(){setStarted(true);}} style={{marginTop:'0.5rem',padding:'12px 28px',borderRadius:'var(--radius-sm)',background:'var(--lbe-green)',color:'#fff',fontWeight:600,fontSize:'0.9rem',border:'none',cursor:'pointer',width:'100%'}}>
          Start Assessment →
        </button>
      </div>"""
assert OLD4a in html, "Fix4a: pre-start screen not found"
html = html.replace(OLD4a, NEW4a, 1)

# 4b: Add tier-coloured borderLeft to q-card on question screen
OLD4b = """      <div className="q-card">
        <div className="q-meta">
          <span className="q-level-badge">L{q.level}</span>
          <span className={'q-tier-badge '+(q.tier||'knowledge')}>{TIER_LABELS[q.tier]||q.tier}</span>
          <span className="q-id">{q.id}</span>
        </div>"""
NEW4b = """      <div className="q-card" style={{borderLeft:'3px solid '+({knowledge:'var(--grammar)',calculation:'var(--logic)',judgement:'var(--rhetoric)'}[q.tier||'knowledge']||'var(--grammar)'),borderRadius:'0 var(--radius-lg) var(--radius-lg) 0'}}>
        <div className="q-meta">
          <span className="q-level-badge">L{q.level}</span>
          <span className={'q-tier-badge '+(q.tier||'knowledge')}>{TIER_LABELS[q.tier]||q.tier}</span>
          <span className="q-id">{q.id}</span>
        </div>"""
assert OLD4b in html, "Fix4b: q-card not found"
html = html.replace(OLD4b, NEW4b, 1)

# 4c: Score screen — add tier-coloured borders to review items (tier colour instead of pass/fail)
OLD4c = """              <div key={i} style={{background:isC?'rgba(74,124,89,0.06)':'rgba(220,38,38,0.06)',border:'1px solid '+(isC?'var(--lbe-green)':'var(--error)'),borderRadius:'var(--radius-sm)',padding:'0.7rem',marginBottom:'0.5rem',fontSize:'0.82rem'}}>
                <div style={{display:'flex',gap:'0.4rem',marginBottom:'0.3rem'}}>
                  <span style={{fontFamily:'var(--font-mono)',fontSize:'0.7rem',background:'var(--panel)',padding:'1px 6px',borderRadius:'4px'}}>L{qr.level}</span>
                  <span style={{color:isC?'var(--lbe-green)':'var(--error)',fontWeight:600}}>{isC?'✓ Correct':'✗ Incorrect'}</span>
                </div>"""
NEW4c = """              <div key={i} style={{background:isC?'rgba(74,124,89,0.06)':'rgba(220,38,38,0.06)',borderLeft:'3px solid '+({knowledge:'var(--grammar)',calculation:'var(--logic)',judgement:'var(--rhetoric)'}[qr.tier]||'var(--grammar)'),border:'1px solid '+(isC?'var(--lbe-green)':'var(--error)'),borderRadius:'0 var(--radius-sm) var(--radius-sm) 0',padding:'0.7rem',marginBottom:'0.5rem',fontSize:'0.82rem'}}>
                <div style={{display:'flex',gap:'0.4rem',alignItems:'center',marginBottom:'0.3rem'}}>
                  <span style={{fontFamily:'var(--font-mono)',fontSize:'0.7rem',background:'var(--panel)',padding:'1px 6px',borderRadius:'4px'}}>L{qr.level}</span>
                  <span className={'q-tier-badge '+(qr.tier||'knowledge')} style={{fontSize:'0.65rem',padding:'1px 6px'}}>{TIER_LABELS[qr.tier]||qr.tier}</span>
                  <span style={{color:isC?'var(--lbe-green)':'var(--error)',fontWeight:600}}>{isC?'✓ Correct':'✗ Incorrect'}</span>
                </div>"""
assert OLD4c in html, "Fix4c: score review items not found"
html = html.replace(OLD4c, NEW4c, 1)

with open(src, 'w', encoding='utf-8') as f:
    f.write(html)
print("Fix 4 applied: Assessment layout updated to match DC-LEARN benchmark.")
