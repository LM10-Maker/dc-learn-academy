"""
Patch 4: Update ReportTab + CalculationsTab to match DC-TOOL-003 pattern.
- Metric cards use cooling chain calcs
- Findings: GREEN/AMBER/RED + new field names (f.title, f.category, f.current, f.required)
- Interpretation: key_findings[] array + commercial_implications + recommended_next_step
- Counters: redCount/amberCount/greenCount
"""
import sys

DST = 'tools/DC-TOOL-002_v2_0_0.html'
with open(DST, encoding='utf-8') as f:
    h = f.read()

# ── Patch F: CalculationsTab — fix status counters + finding card classes ─────
OLD_CALC_COUNTERS = """  const redCount   = findings.filter(f=>f.status==='RED').length;
  const amberCount = findings.filter(f=>f.status==='AMBER').length;
  const greenCount = findings.filter(f=>f.status==='GREEN').length;"""

# Check if template uses failCount/flagCount/passCount
if 'failCount' in h or 'passCount' in h:
    OLD_CALC_PASS = "  const failCount = findings.filter(f=>f.status==='FAIL').length;\n  const flagCount = findings.filter(f=>f.status==='FLAG').length;\n  const passCount = findings.filter(f=>f.status==='PASS').length;"
    NEW_CALC_PASS = "  const redCount   = findings.filter(f=>f.status==='RED').length;\n  const amberCount = findings.filter(f=>f.status==='AMBER').length;\n  const greenCount = findings.filter(f=>f.status==='GREEN').length;"
    count_before = h.count('failCount')
    if OLD_CALC_PASS in h:
        h = h.replace(OLD_CALC_PASS, NEW_CALC_PASS)
        print(f"Patch F1: replaced failCount/flagCount/passCount (was {count_before} occurrences)")
    else:
        print(f"WARN: failCount found ({count_before}x) but exact pattern not matched — manual check needed")
else:
    print("Patch F1: no failCount found — already using red/amber/green or not present")

# Fix counter variable references: failCount->redCount, flagCount->amberCount, passCount->greenCount
if 'failCount' in h:
    h = h.replace('failCount', 'redCount')
    h = h.replace('flagCount', 'amberCount')
    h = h.replace('passCount', 'greenCount')
    print("Patch F1b: replaced all failCount/flagCount/passCount references")

# ── Patch G: ReportTab — metric cards ─────────────────────────────────────────
# Replace the carbon_cost_current metric card with cooling chain metrics
OLD_METRIC = """{calcSteps.filter(s=>s.id==='carbon_cost_current').map(s=>(
          <div className="metric-card" key={s.id}>
            <div className="metric-label">Carbon Cost</div>
            <div className="metric-value" style={{color:'var(--warn)'}}>{s.formatted}</div>
            <div className="metric-sub">per year (T1 — deterministic)</div>
          </div>
        ))}"""

NEW_METRIC = """{calcSteps.filter(s=>s.id==='C03').map(s=>(
          <div className="metric-card" key={s.id}>
            <div className="metric-label">Annual Cooling Cost</div>
            <div className="metric-value" style={{color:'var(--warn)'}}>{'€'+(s.value||0).toLocaleString()}</div>
            <div className="metric-sub">per year (T2 — deterministic)</div>
          </div>
        ))}
        {calcSteps.filter(s=>s.id==='C05').map(s=>(
          <div className="metric-card" key={s.id}>
            <div className="metric-label">FC Saving Potential</div>
            <div className="metric-value" style={{color:'var(--green)'}}>
              {s.value&&s.value.saving_eur?'€'+(s.value.saving_eur).toLocaleString():s.formatted}
            </div>
            <div className="metric-sub">per year unrealised</div>
          </div>
        ))}"""

if OLD_METRIC not in h:
    print("WARN: carbon_cost_current metric card not found exactly — skipping patch G")
else:
    h = h.replace(OLD_METRIC, NEW_METRIC, 1)
    print("Patch G (metric cards) done.")

# ── Patch H: ReportTab — findings section ─────────────────────────────────────
OLD_FINDINGS = """      {/* Findings with calcs + interpretation */}
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

NEW_FINDINGS = """      {/* Findings with calcs + interpretation */}
      {findings.map((f,fi)=>(
        <div className={'finding-card'+(f.status==='GREEN'?' f-pass':f.status==='RED'?' f-fail':' f-flag')} key={f.id}>
          <div style={{display:'flex',alignItems:'center',gap:10,marginBottom:10}}>
            <span className={'status-badge '+(f.status==='GREEN'?'status-pass':f.status==='RED'?'status-fail':'status-flag')}>{f.status}</span>
            <span style={{fontWeight:600,color:'var(--text-bright)',fontSize:15,flex:1}}>{f.title}</span>
            <span style={{fontSize:11,color:'var(--text-muted)',fontFamily:'var(--font-mono)'}}>{f.category}</span>
          </div>
          <div className="finding-detail-calc">
            <div><strong>Current:</strong> {f.current}</div>
            <div><strong>Required:</strong> {f.required}</div>
            {f.gap&&f.gap!=='None'&&<div><strong>Gap:</strong> {f.gap}</div>}
            <div style={{marginTop:6,color:'var(--text-dim)'}}><strong>Action:</strong> {f.action}</div>
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

if OLD_FINDINGS not in h:
    print("WARN: ReportTab findings section not found exactly")
    idx = h.find('finding_interpretations')
    print(f"  finding_interpretations at char {idx}")
    idx2 = h.find('f.status===\'PASS\'')
    print(f"  f.status==='PASS' at char {idx2}")
else:
    h = h.replace(OLD_FINDINGS, NEW_FINDINGS, 1)
    print("Patch H (ReportTab findings) done.")

# ── Patch I: CalculationsTab — fix findings display ───────────────────────────
# Fix the calc tab finding cards to use new field names
OLD_CALC_FINDING = """          <div className={'finding-card'+(f.status==='GREEN'?' f-pass':f.status==='RED'?' f-fail':' f-flag')} key={f.id}>
            <div style={{display:'flex',alignItems:'center',gap:10,marginBottom:8}}>
              <span className={'status-badge '+(f.status==='GREEN'?'status-pass':f.status==='RED'?'status-fail':'status-flag')}>{f.status}</span>
              <span style={{fontWeight:600,color:'var(--text-bright)',fontSize:14,flex:1}}>{f.area}</span>"""

# Check what the calc tab has
idx_ct = h.find("f.status==='PASS'?' f-pass'")
if idx_ct != -1:
    print(f"WARN: CalculationsTab still uses f-pass/f-fail pattern at char {idx_ct}")
    # Fix calc tab
    OLD_CALC_TAB_FINDING = "f.status==='PASS'?' f-pass':f.status==='FAIL'?' f-fail':' f-flag'"
    NEW_CALC_TAB_FINDING = "f.status==='GREEN'?' f-pass':f.status==='RED'?' f-fail':' f-flag'"
    h = h.replace(OLD_CALC_TAB_FINDING, NEW_CALC_TAB_FINDING)
    print("  Fixed CalculationsTab finding card classes")

# Fix status-badge in CalculationsTab
OLD_CALC_BADGE = "(f.status==='GREEN'?'status-pass':f.status==='RED'?'status-fail':'status-flag')}>{f.status}</span>\n              <span style={{fontWeight:600,color:'var(--text-bright)',fontSize:14,flex:1}}>{f.area}<"
NEW_CALC_BADGE = "(f.status==='GREEN'?'status-pass':f.status==='RED'?'status-fail':'status-flag')}>{f.status}</span>\n              <span style={{fontWeight:600,color:'var(--text-bright)',fontSize:14,flex:1}}>{f.title||f.area}<"
if OLD_CALC_BADGE in h:
    h = h.replace(OLD_CALC_BADGE, NEW_CALC_BADGE, 1)
    print("Patch I (CalculationsTab finding title) done.")
else:
    print("WARN: CalculationsTab badge pattern not found exactly — check manually")

# Also fix f.area reference for source/tier in CalculationsTab
# These use f.source and f.tier which still exist in the findings, so should be OK

# Fix redCount/amberCount/greenCount display in ReportTab sub-metric
h = h.replace('{failCount} fail, {flagCount} flag, {passCount} pass', '{redCount} red, {amberCount} amber, {greenCount} green')
h = h.replace('{redCount} fail, {amberCount} flag, {greenCount} pass', '{redCount} red, {amberCount} amber, {greenCount} green')
print("Patch I2: fixed counter display text")

with open(DST, 'w', encoding='utf-8') as f:
    f.write(h)
print(f"Saved. Lines: {h.count(chr(10))+1}")
