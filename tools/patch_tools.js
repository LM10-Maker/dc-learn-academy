/**
 * DC-TOOL UX Upgrade — Batch Patch Script v2
 * Applies 8 visual/UX improvements to all DC-TOOL files except 004 (already done).
 * Run from tools/ directory: node patch_tools.js
 */
const fs = require('fs');
const path = require('path');
const parser = require('@babel/parser');

const toolsDir = __dirname;
const files = fs.readdirSync(toolsDir)
  .filter(f => f.match(/^DC-TOOL-(?!004)\d{3}_v2_0_0\.html$/))
  .sort();

console.log(`Patching ${files.length} tools...\n`);

// ── CSS blocks to add before </style> ─────────────────────────────────────────
const NEW_CSS_ADDITIONS = `
/* === HERO METRIC === */
.hero-metric{background:var(--surface);border:2px solid var(--border);border-radius:12px;padding:32px;text-align:center;margin-bottom:24px}
.hero-metric-value{font-size:36px;font-weight:700;color:var(--text-bright);line-height:1.2}
.hero-metric-label{font-size:13px;color:var(--text-muted);text-transform:uppercase;letter-spacing:1.2px;font-family:var(--font-mono);margin-top:8px}
.hero-metric-sub{font-size:14px;color:var(--text-dim);margin-top:4px}
.hero-metric.red{border-color:var(--red)}
.hero-metric.amber{border-color:var(--amber)}
.hero-metric.green{border-color:var(--green)}

/* === TIER COST RANGES === */
.cost-range-t3{background:var(--amber-dim);border:1px dashed var(--amber);border-radius:6px;padding:8px 12px;margin-top:8px;font-size:13px;color:var(--text);font-family:var(--font-mono)}
.cost-range-t3::before{content:'T3 INDICATIVE ';font-weight:700;font-size:10px;color:var(--amber);letter-spacing:0.5px}
.cost-range-t1{background:var(--green-dim);border:1px solid var(--green);border-radius:6px;padding:8px 12px;margin-top:8px;font-size:13px;color:var(--text);font-family:var(--font-mono)}
.cost-range-t1::before{content:'T1 CONFIRMED ';font-weight:700;font-size:10px;color:var(--green);letter-spacing:0.5px}

/* === AUDIT SECTION HEADINGS === */
.audit-section-heading{font-size:16px;font-weight:700;color:var(--text-bright);margin:24px 0 12px;padding:12px 0;border-bottom:2px solid var(--lbe-green)}
`;

// ── Replacement print CSS ─────────────────────────────────────────────────────
const OLD_PRINT_CSS = `/* === PRINT === */
@media print{
  .no-print{display:none!important}
  body{background:#fff;color:#000}
  header{background:#1a1a1a;-webkit-print-color-adjust:exact;print-color-adjust:exact}
  .result-card,.card,.persona-lens{border:1px solid #ccc;break-inside:avoid}
  .caveat-box{background:#fff3cd;border:1px solid #d29922;-webkit-print-color-adjust:exact;print-color-adjust:exact}
  .status-pass,.status-flag,.status-fail,.tier-badge,.tl-green,.tl-amber,.tl-red{-webkit-print-color-adjust:exact;print-color-adjust:exact}
}`;

const NEW_PRINT_CSS = `/* === PRINT === */
@media print{
  .no-print{display:none!important}
  body{background:#fff;color:#000;font-size:11pt}
  header{background:#1a1a1a!important;-webkit-print-color-adjust:exact;print-color-adjust:exact;padding:12px 20px}
  .main{max-width:100%;padding:0 20px}
  .tab-row{display:none!important}

  /* Show report + audit on print */
  .result-card,.card,.persona-lens,.finding-card,.audit-step{
    border:1px solid #ccc;break-inside:avoid;page-break-inside:avoid;margin-bottom:8px
  }
  .hero-metric{border:2px solid #333;break-inside:avoid}

  /* Colour preservation */
  .caveat-box{background:#fff3cd!important;border:1px solid #d29922!important;-webkit-print-color-adjust:exact;print-color-adjust:exact}
  .status-pass,.status-flag,.status-fail,.tier-badge,.tl-green,.tl-amber,.tl-red,
  .cost-range-t1,.cost-range-t3,.finding-card.f-pass,.finding-card.f-flag,.finding-card.f-fail{
    -webkit-print-color-adjust:exact;print-color-adjust:exact
  }

  /* Page breaks */
  .signoff{page-break-before:always;margin-top:0}
  .audit-section-heading{page-break-before:always;margin-top:0}

  /* Footer on every page */
  @page{margin:15mm 15mm 20mm 15mm;@bottom-center{content:'DC-TOOL v2.1.0 | Legacy Business Engineers Ltd | legacybe.ie'}}

  /* LBE header bar */
  header::after{content:'';display:block;height:3px;background:#4a7c59;margin-top:8px;-webkit-print-color-adjust:exact;print-color-adjust:exact}
}`;

// ── Hero metric IIFE (inline JSX, 6-space indent) ─────────────────────────────
const HERO_METRIC_JSX = `      {(()=>{
        const heroStep = calcSteps.find(s=>s.id==='carbon_10yr_incremental')||calcSteps.find(s=>s.id==='C09')||
          [...calcSteps].filter(s=>s.unit==='€'&&typeof s.value==='number').sort((a,b)=>(b.value||0)-(a.value||0))[0];
        if (!heroStep||!heroStep.value||typeof heroStep.value!=='number') return null;
        const v = heroStep.value;
        const display = v >= 1e6 ? '€'+(v/1e6).toFixed(1)+'M' : '€'+Math.round(v).toLocaleString();
        const tl = (trafficLight||'AMBER').toLowerCase();
        return (
          <div className={'hero-metric '+tl}>
            <div className="hero-metric-value">{display}</div>
            <div className="hero-metric-label">10-Year Exposure</div>
            <div className="hero-metric-sub">Largest deterministic exposure — JavaScript calculation</div>
          </div>
        );
      })()}
`;

let totalPatched = 0;
let totalFailed = 0;
const results = [];

for (const file of files) {
  const filePath = path.join(toolsDir, file);
  let content = fs.readFileSync(filePath, 'utf8');
  const applied = [];

  // ─── 1. Print CSS ──────────────────────────────────────────────────────────
  if (content.includes(OLD_PRINT_CSS)) {
    content = content.replace(OLD_PRINT_CSS, NEW_PRINT_CSS);
    applied.push('print-css');
  }

  // ─── 2. Version bump ──────────────────────────────────────────────────────
  if (content.includes("const TOOL_VERSION = '2.0.0';")) {
    content = content.replace("const TOOL_VERSION = '2.0.0';", "const TOOL_VERSION = '2.1.0';");
    applied.push('version');
  }

  // ─── 3. Hero metric in CalculationsTab ────────────────────────────────────
  // Guard: 'hero-metric-value' from IIFE JSX (NOT from CSS which hasn't been added yet)
  // The CalculationsTab unique anchor: the main return starts with <div> directly
  // followed by <div className="card"> (no intervening elements like btn-row).
  // ReportTab inserts <div className="btn-row no-print"> first, so it won't match.
  const calcTabAnchor = `    <div>\n      <div className="card">\n        <div style={{display:'flex',alignItems:'center',gap:8,marginBottom:12}}>`;
  if (content.includes(calcTabAnchor) && !content.includes('hero-metric-value')) {
    content = content.replace(
      calcTabAnchor,
      `    <div>\n${HERO_METRIC_JSX}      <div className="card">\n        <div style={{display:'flex',alignItems:'center',gap:8,marginBottom:12}}>`
    );
    applied.push('hero-calc');
  }

  // ─── 5. Hero metric in ReportTab ──────────────────────────────────────────
  const reportMetricAnchor = `      {/* Metrics */}\n      <div className="metric-row">`;
  if (content.includes(reportMetricAnchor) && !content.includes('{/* Hero Metric */}')) {
    content = content.replace(
      reportMetricAnchor,
      `      {/* Hero Metric */}\n${HERO_METRIC_JSX}\n      {/* Metrics */}\n      <div className="metric-row">`
    );
    applied.push('hero-report');
  }

  // ─── 5b. New CSS classes (hero, tier ranges, audit headings) — after JSX steps ──
  const cssAnchor = `.interp-text{font-size:14px;color:var(--text);line-height:1.7;font-style:italic}\n\n</style>`;
  if (content.includes(cssAnchor) && !content.includes('.hero-metric-value{')) {
    content = content.replace(
      cssAnchor,
      `.interp-text{font-size:14px;color:var(--text);line-height:1.7;font-style:italic}\n${NEW_CSS_ADDITIONS}\n</style>`
    );
    applied.push('css-additions');
  }

  // ─── 6. Error state — professional messages ────────────────────────────────
  const ERR_PROF = `setError('Calculated results are complete — see Calculations and Audit Trail tabs. AI interpretation is temporarily unavailable but your deterministic screening results are unaffected. If this persists, contact info@legacybe.ie.');`;

  if (content.includes(`setError('Interpretation parse failed. Calculated results are still valid.');`)) {
    content = content.replace(`setError('Interpretation parse failed. Calculated results are still valid.');`, ERR_PROF);
    applied.push('err-parse');
  }
  if (content.includes(`setError('Interpretation unavailable. Calculated results are still valid.');`)) {
    content = content.replace(`setError('Interpretation unavailable. Calculated results are still valid.');`, ERR_PROF);
    applied.push('err-unavail');
  }
  content = content.replace(
    /setError\('Interpretation unavailable: ' \+ err\.message \+ '[^']*'\);/g,
    ERR_PROF
  );

  // ReportTab "Interpretation not available" inline message
  const interpOld = `: <p style={{color:'var(--text-dim)'}}>Interpretation not available. Calculated results shown below.</p>}`;
  if (content.includes(interpOld)) {
    content = content.replace(
      interpOld,
      `: <p style={{color:'var(--text-dim)'}}>Calculated results are complete — see Calculations and Audit Trail tabs. AI interpretation is temporarily unavailable but your deterministic screening results are unaffected.</p>}`
    );
    applied.push('interp-msg');
  }

  // ─── 7. JSON export metadata ──────────────────────────────────────────────
  const exportOld = `const handleExport = () => { const b=new Blob([JSON.stringify(inputs,null,2)],{type:'application/json'}); const u=URL.createObjectURL(b); const a=document.createElement('a'); a.href=u; a.download=TOOL_ID+'_inputs.json'; a.click(); URL.revokeObjectURL(u); };`;
  const exportNew = `const handleExport = () => { const exportData={_metadata:{tool_id:TOOL_ID,tool_version:TOOL_VERSION,export_date:new Date().toISOString(),canonical_data_version:'SEAI 2026 / CRU Q4 2024 / Budget 2025',schema:'dc-tool-v2'},inputs:{...inputs}}; const b=new Blob([JSON.stringify(exportData,null,2)],{type:'application/json'}); const u=URL.createObjectURL(b); const a=document.createElement('a'); a.href=u; a.download=TOOL_ID+'_inputs.json'; a.click(); URL.revokeObjectURL(u); };`;
  if (content.includes(exportOld)) {
    content = content.replace(exportOld, exportNew);
    applied.push('export-meta');
  }

  // ─── 8. Persona display — role heading, coloured dot, no emoji ────────────
  const personaOld = `<span style={{fontSize:18}}>{p.icon}</span>\n                  <span className="persona-name">{p.name}</span>\n                  <span className="persona-role">{p.role}</span>`;
  const personaNew = `<span style={{width:10,height:10,borderRadius:'50%',background:p.color,display:'inline-block',marginRight:8}}></span>\n                  <span className="persona-name">{p.role}</span>`;
  if (content.includes(personaOld)) {
    content = content.replace(personaOld, personaNew);
    applied.push('persona');
  }

  // ─── 9. Cost range T1/T3 in CalculationsTab findings ─────────────────────
  const costRangeCalcOld =
`{f.cost_range&&<p style={{fontSize:13,color:'var(--warn)',fontFamily:'var(--font-mono)',marginTop:8}}>Indicative cost: {f.cost_range}</p>}
            <p style={{fontSize:11,color:'var(--text-muted)',fontFamily:'var(--font-mono)',marginTop:4}}>Source: {f.source}</p>
          </div>
        ))}
      </div>

      <div className="caveat-box">
        All calculations above are deterministic JavaScript — same inputs always produce same outputs. Verify with any calculator. AI interpretation (next tab) does not modify any calculated value.
      </div>`;
  const costRangeCalcNew =
`{f.cost_range&&(
              <div className={f.cost_range.includes('T1')?'cost-range-t1':'cost-range-t3'}>{f.cost_range}</div>
            )}
            {f.status!=='PASS'&&f.status!=='GREEN'&&(
              <div style={{fontSize:12,color:'var(--text-muted)',marginTop:6,fontStyle:'italic'}}>This finding alone warrants a Desktop Assessment to quantify the remediation path.</div>
            )}
            <p style={{fontSize:11,color:'var(--text-muted)',fontFamily:'var(--font-mono)',marginTop:4}}>Source: {f.source}</p>
          </div>
        ))}
      </div>

      <div className="caveat-box">
        All calculations above are deterministic JavaScript — same inputs always produce same outputs. Verify with any calculator. AI interpretation (next tab) does not modify any calculated value.
      </div>`;
  if (content.includes(costRangeCalcOld)) {
    content = content.replace(costRangeCalcOld, costRangeCalcNew);
    applied.push('cost-range-calc');
  }

  // ─── 10. Cost range T1/T3 in ReportTab findings ──────────────────────────
  const costRangeRptOld =
`{f.cost_range&&<p style={{fontSize:13,color:'var(--warn)',fontFamily:'var(--font-mono)',marginTop:8}}>Indicative cost: {f.cost_range}</p>}
          <p style={{fontSize:11,color:'var(--text-muted)',fontFamily:'var(--font-mono)',marginTop:4}}>Source: {f.source}</p>
        </div>
      ))}

      {/* Personas — AI narrative */}`;
  const costRangeRptNew =
`{f.cost_range&&(
            <div className={f.cost_range.includes('T1')?'cost-range-t1':'cost-range-t3'}>{f.cost_range}</div>
          )}
          {f.status!=='PASS'&&f.status!=='GREEN'&&(
            <div style={{fontSize:12,color:'var(--text-muted)',marginTop:6,fontStyle:'italic'}}>This finding alone warrants a Desktop Assessment to quantify the remediation path.</div>
          )}
          <p style={{fontSize:11,color:'var(--text-muted)',fontFamily:'var(--font-mono)',marginTop:4}}>Source: {f.source}</p>
        </div>
      ))}

      {/* Personas — AI narrative */}`;
  if (content.includes(costRangeRptOld)) {
    content = content.replace(costRangeRptOld, costRangeRptNew);
    applied.push('cost-range-rpt');
  }

  // ─── Write & verify ───────────────────────────────────────────────────────
  if (applied.length === 0) {
    results.push({ file, status: 'SKIP', msg: 'no matching patterns found' });
    continue;
  }

  fs.writeFileSync(filePath, content);

  const scriptMatch = content.match(/<script[^>]*type="text\/babel"[^>]*>([\s\S]*?)<\/script>/);
  if (scriptMatch) {
    try {
      parser.parse(scriptMatch[1], { plugins: ['jsx'], sourceType: 'script' });
      results.push({ file, status: 'PASS', msg: applied.join(', ') });
      totalPatched++;
    } catch(e) {
      results.push({ file, status: 'FAIL', msg: e.message });
      totalFailed++;
    }
  } else {
    results.push({ file, status: 'NO-SCRIPT', msg: applied.join(', ') });
    totalPatched++;
  }
}

// Print summary
for (const r of results) {
  const icon = r.status === 'PASS' ? '✓' : r.status === 'FAIL' ? '✗' : r.status === 'SKIP' ? '-' : '?';
  console.log(`  ${icon} [${r.status}] ${r.file}\n      ${r.msg}\n`);
}
console.log(`Done. Patched: ${totalPatched}, Failed: ${totalFailed}, Skipped: ${results.filter(r=>r.status==='SKIP').length}`);
