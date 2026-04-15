"""
Patch 5: Fix CalculationsTab and ReportTab counters + calc card IDs + finding fields.
"""
import sys

DST = 'tools/DC-TOOL-002_v2_0_0.html'
with open(DST, encoding='utf-8') as f:
    h = f.read()

# Fix all PASS/FLAG/FAIL counter filters — replace both instances
h = h.replace(
    "const greenCount = findings.filter(f=>f.status==='PASS').length;\n  const amberCount = findings.filter(f=>f.status==='FLAG').length;\n  const redCount = findings.filter(f=>f.status==='FAIL').length;",
    "const redCount   = findings.filter(f=>f.status==='RED').length;\n  const amberCount = findings.filter(f=>f.status==='AMBER').length;\n  const greenCount = findings.filter(f=>f.status==='GREEN').length;"
)
remaining = h.count("status==='PASS'")
print(f"After counter fix: {remaining} PASS references remain (expected 0)")

# Fix CalculationsTab summary calc card IDs
OLD_CALC_CARDS = "calcSteps.filter(s=>['carbon_cost_current','co2_tonnes','pue_gap'].includes(s.id)).map(s=>("
NEW_CALC_CARDS = "calcSteps.filter(s=>['C01','C03','C05'].includes(s.id)).map(s=>("
if OLD_CALC_CARDS in h:
    h = h.replace(OLD_CALC_CARDS, NEW_CALC_CARDS, 1)
    print("Fixed CalculationsTab summary card IDs (C01, C03, C05).")
else:
    print("WARN: calc card IDs pattern not found")

# Fix CalculationsTab finding card display
# Old: statusClass(f.status) for badge + f.area + f.tier badge + f.detail + f.cost_range + f.source
OLD_CT_FINDING = """          <div className={'finding-card'+(f.status==='GREEN'?' f-pass':f.status==='RED'?' f-fail':' f-flag')} key={f.id}>
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
              <span style={{fontSize:11,color:'var(--text-muted)',fontFamily:'var(--font-mono)'}}>{f.category||f.tier}</span>
            </div>
            <div className="finding-detail-calc">
              {f.current&&<div><strong>Current:</strong> {f.current}</div>}
              {f.required&&<div><strong>Required:</strong> {f.required}</div>}
              {f.gap&&f.gap!=='None'&&<div><strong>Gap:</strong> {f.gap}</div>}
              {f.action&&<div style={{marginTop:4,color:'var(--text-dim)'}}><strong>Action:</strong> {f.action}</div>}
              {f.detail&&!f.current&&<div>{f.detail}</div>}
            </div>
          </div>"""

if OLD_CT_FINDING in h:
    h = h.replace(OLD_CT_FINDING, NEW_CT_FINDING, 1)
    print("Fixed CalculationsTab finding card.")
else:
    print("WARN: CalculationsTab finding card pattern not found exactly")

with open(DST, 'w', encoding='utf-8') as f:
    f.write(h)
print(f"Saved. Lines: {h.count(chr(10))+1}")

# Final check
with open(DST, encoding='utf-8') as f:
    h2 = f.read()
p = h2.count("status==='PASS'"); fl = h2.count("status==='FLAG'"); fa = h2.count("status==='FAIL'")
print(f"Remaining PASS/FLAG/FAIL filter refs: {p}/{fl}/{fa}")
print(f"f.area refs: {h2.count('{f.area}')}")
print(f"f.title refs: {h2.count('f.title')}")
