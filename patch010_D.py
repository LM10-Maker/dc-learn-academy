"""
Patch D for DC-TOOL-010 v2.0.0
Fix CalculationsTab + ReportTab:
- Replace PASS/FLAG/FAIL counters with RED/AMBER/GREEN
- Update metric card calc IDs
- Fix findings card rendering (title, category, current/required/gap/action)
- Fix ReportTab findings section (GREEN/AMBER/RED, key_findings, commercial_implications, etc.)
"""
import sys

DST = 'tools/DC-TOOL-010_v2_0_0.html'
with open(DST, encoding='utf-8') as f:
    h = f.read()

# ── D1: Fix PASS/FLAG/FAIL counter variables in CalculationsTab and ReportTab ─
h = h.replace(
    "  const passCount = findings.filter(f=>f.status==='PASS').length;\n  const flagCount = findings.filter(f=>f.status==='FLAG').length;\n  const failCount = findings.filter(f=>f.status==='FAIL').length;",
    "  const redCount   = findings.filter(f=>f.status==='RED').length;\n  const amberCount = findings.filter(f=>f.status==='AMBER').length;\n  const greenCount = findings.filter(f=>f.status==='GREEN').length;"
)
# Replace all remaining references
h = h.replace('failCount', 'redCount')
h = h.replace('flagCount', 'amberCount')
h = h.replace('passCount', 'greenCount')
# Fix display text
h = h.replace('{redCount} fail, {amberCount} flag, {greenCount} pass', '{redCount} red, {amberCount} amber, {greenCount} green')
pass_refs = h.count("status==='PASS'")
print(f"D1 done. Remaining PASS refs: {pass_refs}")

# ── D2: Fix CalculationsTab summary calc card IDs ─────────────────────────────
OLD_CALC_CARDS = "calcSteps.filter(s=>['carbon_cost_current','co2_tonnes','pue_gap'].includes(s.id)).map(s=>("
NEW_CALC_CARDS = "calcSteps.filter(s=>['C06','C07','C08'].includes(s.id)).map(s=>("
if OLD_CALC_CARDS in h:
    h = h.replace(OLD_CALC_CARDS, NEW_CALC_CARDS, 1)
    print("D2 done: fixed CalculationsTab summary card IDs (C06, C07, C08).")
else:
    print("WARN D2: calc card ID pattern not found — check manually")

# ── D3: Fix ReportTab metric card ─────────────────────────────────────────────
OLD_METRIC = """{calcSteps.filter(s=>s.id==='carbon_cost_current').map(s=>(
          <div className="metric-card" key={s.id}>
            <div className="metric-label">Carbon Cost</div>
            <div className="metric-value" style={{color:'var(--warn)'}}>{s.formatted}</div>
            <div className="metric-sub">per year (T1 — deterministic)</div>
          </div>
        ))}"""
NEW_METRIC = """{calcSteps.filter(s=>s.id==='C07').map(s=>(
          <div className="metric-card" key={s.id}>
            <div className="metric-label">Carbon Cost</div>
            <div className="metric-value" style={{color:'var(--warn)'}}>
              {'€'+(s.value&&s.value.annual_cost?s.value.annual_cost:0).toLocaleString()}
            </div>
            <div className="metric-sub">per year (T1 — deterministic)</div>
          </div>
        ))}
        {calcSteps.filter(s=>s.id==='C08').map(s=>(
          <div className="metric-card" key={s.id}>
            <div className="metric-label">Retrofit Payback</div>
            <div className="metric-value" style={{color:'var(--accent)'}}>
              {s.value&&s.value.payback_years<999?s.value.payback_years+' yrs':'N/A'}
            </div>
            <div className="metric-sub">indicative (T3)</div>
          </div>
        ))}"""
if OLD_METRIC in h:
    h = h.replace(OLD_METRIC, NEW_METRIC, 1)
    print("D3 done: updated ReportTab metric cards.")
else:
    print("WARN D3: ReportTab metric card pattern not found")

# ── D4: Fix CalculationsTab finding card rendering ────────────────────────────
OLD_CT_FINDING = """          <div className={'finding-card'+(f.status==='PASS'?' f-pass':f.status==='FAIL'?' f-fail':' f-flag')} key={f.id}>
            <div style={{display:'flex',alignItems:'center',gap:10,marginBottom:8}}>
              <span className={'status-badge '+statusClass(f.status)}>{f.status}</span>
              <span style={{fontWeight:600,color:'var(--text-bright)',fontSize:15,flex:1}}>{f.area}</span>
              <span className={'tier-badge '+tierClass(f.tier)}>{f.tier}</span>
            </div>
            <div className="finding-detail-calc">{f.detail}</div>
            {f.cost_range&&<p style={{fontSize:13,color:'var(--warn)',fontFamily:'var(--font-mono)',marginTop:8}}>Indicative cost: {f.cost_range}</p>}
            <p style={{fontSize:11,color:'var(--text-muted)',fontFamily:'var(--font-mono)',marginTop:4}}>Source: {f.source}</p>
          </div>"""
NEW_CT_FINDING = """          <div className={'finding-card'+(f.status==='GREEN'?' f-pass':f.status==='RED'?' f-fail':' f-flag')} key={f.id}>
            <div style={{display:'flex',alignItems:'center',gap:10,marginBottom:8}}>
              <span className={'status-badge '+(f.status==='GREEN'?'status-pass':f.status==='RED'?'status-fail':'status-flag')}>{f.status}</span>
              <span style={{fontWeight:600,color:'var(--text-bright)',fontSize:15,flex:1}}>{f.title||f.area}</span>
              <span style={{fontSize:11,color:'var(--text-muted)',fontFamily:'var(--font-mono)'}}>{f.category||''}</span>
            </div>
            <div className="finding-detail-calc">
              {f.current&&<div><strong>Current:</strong> {f.current}</div>}
              {f.required&&<div><strong>Required:</strong> {f.required}</div>}
              {f.gap&&f.gap!=='None'&&<div><strong>Gap:</strong> {f.gap}</div>}
              {f.action&&<div style={{marginTop:4,color:'var(--text-dim)'}}><strong>Action:</strong> {f.action}</div>}
            </div>
          </div>"""
if OLD_CT_FINDING in h:
    h = h.replace(OLD_CT_FINDING, NEW_CT_FINDING, 1)
    print("D4 done: fixed CalculationsTab finding card.")
else:
    print("WARN D4: CalculationsTab finding card pattern not found")

# ── D5: Fix ReportTab findings + interpretations section ─────────────────────
OLD_RT_FINDINGS = """      {/* Findings with calcs + interpretation */}
      {findings.map(f=>(
        <div className={'finding-card'+(f.status==='PASS'?' f-pass':f.status==='FAIL'?' f-fail':' f-flag')} key={f.id}>
          <div style={{display:'flex',alignItems:'center',gap:10,marginBottom:10}}>
            <span className={'status-badge '+statusClass(f.status)}>{f.status}</span>
            <span style={{fontWeight:600,color:'var(--text-bright)',fontSize:15,flex:1}}>{f.area}</span>
            <span className={'tier-badge '+tierClass(f.tier)}>{f.tier}</span>
          </div>
          <div className="finding-detail-calc">{f.detail}</div>
          {interpretation?.finding_interpretations?.[f.id]&&(
            <div style={{marginTop:8}}>
              <div className="interp-label">Interpretation</div>
              <p className="interp-text">{interpretation.finding_interpretations[f.id]}</p>
            </div>
          )}
          {f.cost_range&&<p style={{fontSize:13,color:'var(--warn)',fontFamily:'var(--font-mono)',marginTop:8}}>Indicative cost: {f.cost_range}</p>}
          <p style={{fontSize:11,color:'var(--text-muted)',fontFamily:'var(--font-mono)',marginTop:4}}>Source: {f.source}</p>
        </div>
      ))}

      {/* Personas — AI narrative */}
      {interpretation?.persona_views&&(
        <div className="card">
          <h2>Stakeholder Perspectives</h2>
          <div className="interp-label" style={{marginBottom:12}}>AI Interpretation — qualitative context only</div>
          {Object.entries(PERSONAS).map(([key,p])=>(
            interpretation.persona_views[key]?(
              <div className="persona-lens" key={key}>
                <div style={{display:'flex',alignItems:'center',gap:8,marginBottom:6}}>
                  <span style={{fontSize:18}}>{p.icon}</span>
                  <span className="persona-name">{p.role}</span>
                </div>
                <p className="interp-text">{interpretation.persona_views[key]}</p>
              </div>
            ):null
          ))}
        </div>
      )}"""
NEW_RT_FINDINGS = """      {/* Findings with calcs + AI interpretation */}
      {findings.map((f,fi)=>(
        <div className={'finding-card'+(f.status==='GREEN'?' f-pass':f.status==='RED'?' f-fail':' f-flag')} key={f.id}>
          <div style={{display:'flex',alignItems:'center',gap:10,marginBottom:10}}>
            <span className={'status-badge '+(f.status==='GREEN'?'status-pass':f.status==='RED'?'status-fail':'status-flag')}>{f.status}</span>
            <span style={{fontWeight:600,color:'var(--text-bright)',fontSize:15,flex:1}}>{f.title||f.area}</span>
            <span style={{fontSize:11,color:'var(--text-muted)',fontFamily:'var(--font-mono)'}}>{f.category||''}</span>
          </div>
          <div className="finding-detail-calc">
            {f.current&&<div><strong>Current:</strong> {f.current}</div>}
            {f.required&&<div><strong>Required:</strong> {f.required}</div>}
            {f.gap&&f.gap!=='None'&&<div><strong>Gap:</strong> {f.gap}</div>}
            {f.action&&<div style={{marginTop:6,color:'var(--text-dim)'}}><strong>Action:</strong> {f.action}</div>}
          </div>
          {interpretation?.key_findings?.[fi]&&(
            <div style={{marginTop:8}}>
              <div className="interp-label">Interpretation</div>
              <p className="interp-text">{interpretation.key_findings[fi]}</p>
            </div>
          )}
        </div>
      ))}

      {interpretation?.commercial_implications&&(
        <div className="result-card">
          <div className="interp-label">Commercial Implications</div>
          <p className="interp-text">{interpretation.commercial_implications}</p>
        </div>
      )}
      {interpretation?.recommended_next_step&&(
        <div className="result-card" style={{borderColor:'var(--accent)'}}>
          <div className="interp-label">Recommended Next Step</div>
          <p className="interp-text">{interpretation.recommended_next_step}</p>
        </div>
      )}
      {interpretation?.caveats&&(
        <div className="caveat-box">
          <strong>Caveats:</strong> {interpretation.caveats}
        </div>
      )}"""
if OLD_RT_FINDINGS in h:
    h = h.replace(OLD_RT_FINDINGS, NEW_RT_FINDINGS, 1)
    print("D5 done: fixed ReportTab findings section.")
else:
    print("WARN D5: ReportTab findings pattern not found")
    idx = h.find("finding_interpretations")
    print(f"  'finding_interpretations' at char: {idx}")

with open(DST, 'w', encoding='utf-8') as f:
    f.write(h)
print(f"Saved. Lines: {h.count(chr(10)) + 1}")

# Final check
with open(DST, encoding='utf-8') as f:
    h2 = f.read()
p = h2.count("status==='PASS'")
fl = h2.count("status==='FLAG'")
fa = h2.count("status==='FAIL'")
print(f"Remaining PASS/FLAG/FAIL filter refs: {p}/{fl}/{fa} (expect 0/0/0)")
print(f"finding_interpretations refs: {h2.count('finding_interpretations')} (expect 0)")
print(f"f.title refs: {h2.count('f.title')} (expect >=2)")
