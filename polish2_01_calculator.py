#!/usr/bin/env python3
"""
polish2_01_calculator.py
ITEM 1: CASCADE CALCULATOR SIDEBAR
Input:  DC-AI-001_v1_1_0.html
Output: DC-AI-001_v1_2_0.html (working copy for scripts 2-6)
"""

SRC = 'DC-AI-001_v1_1_0.html'
DST = 'DC-AI-001_v1_2_0.html'

with open(SRC, 'r', encoding='utf-8') as f:
    html = f.read()

# ─── 1. CSS ───────────────────────────────────────────────────────────────────
CSS = r"""
    /* ─── CASCADE CALCULATOR SIDEBAR ───────────────────────────────── */
    .content-with-sidebar {
      display: flex;
      flex: 1;
      align-items: flex-start;
      min-height: 0;
    }
    .calc-sidebar {
      width: 320px;
      flex-shrink: 0;
      background: var(--surface);
      border-left: 1px solid var(--border);
      overflow-y: auto;
      padding: 1.2rem;
      position: sticky;
      top: 60px;
      height: calc(100vh - 60px);
    }
    .calc-sidebar-title {
      font-size: 0.85rem;
      font-weight: 700;
      color: var(--text-bright);
      margin-bottom: 1rem;
      padding-bottom: 0.6rem;
      border-bottom: 1px solid var(--border);
    }
    .calc-input-label {
      display: block;
      font-size: 0.7rem;
      font-family: var(--font-mono);
      color: var(--text-dim);
      margin-bottom: 2px;
    }
    .calc-input {
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      color: var(--text);
      font-size: 0.82rem;
      padding: 0.35rem 0.6rem;
      width: 100%;
      outline: none;
      font-family: var(--font-sans);
      margin-bottom: 0.45rem;
    }
    .calc-input:focus { border-color: var(--lbe-green); }
    .calc-btn-primary {
      width: 100%;
      background: var(--lbe-green);
      color: #fff;
      border-radius: var(--radius-sm);
      padding: 0.55rem 0.9rem;
      font-size: 0.82rem;
      font-weight: 600;
      margin-bottom: 0.75rem;
      cursor: pointer;
      border: none;
    }
    .calc-btn-primary:hover { opacity: 0.9; }
    .calc-btn-secondary {
      width: 100%;
      background: var(--panel);
      border: 1px solid var(--border);
      color: var(--text-dim);
      border-radius: var(--radius-sm);
      padding: 0.45rem 0.9rem;
      font-size: 0.78rem;
      font-weight: 500;
      margin-bottom: 0.75rem;
      cursor: pointer;
    }
    .calc-btn-secondary:hover { background: var(--surface-3); color: var(--text); }
    .calc-result-pass {
      background: var(--green-dim);
      border: 1px solid var(--green);
      border-radius: var(--radius-sm);
      padding: 0.65rem 0.85rem;
      font-size: 0.78rem;
      line-height: 1.55;
      margin-bottom: 0.75rem;
      color: var(--text);
    }
    .calc-result-fail {
      background: var(--red-dim);
      border: 1px solid var(--red);
      border-radius: var(--radius-sm);
      padding: 0.65rem 0.85rem;
      font-size: 0.78rem;
      line-height: 1.55;
      margin-bottom: 0.75rem;
      color: var(--text);
    }
    .calc-grid-row {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      padding: 0.3rem 0.4rem;
      border-bottom: 1px solid var(--border);
      cursor: pointer;
      font-size: 0.78rem;
    }
    .calc-grid-row:hover { background: var(--panel); border-radius: 4px; }
    .calc-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }
    .calc-dot-pass { background: var(--green); }
    .calc-dot-fail { background: var(--red); }
    .calc-row-detail {
      font-size: 0.72rem;
      color: var(--text-muted);
      padding: 0.4rem 0.6rem;
      background: var(--panel);
      border-bottom: 1px solid var(--border);
      line-height: 1.5;
    }
    .calc-float-btn {
      display: none;
      position: fixed;
      bottom: 20px;
      right: 20px;
      width: 50px;
      height: 50px;
      border-radius: 50%;
      background: var(--lbe-green);
      color: #fff;
      font-size: 1.3rem;
      align-items: center;
      justify-content: center;
      box-shadow: var(--shadow-lg);
      z-index: 200;
      cursor: pointer;
      border: none;
    }
    .calc-overlay {
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(0,0,0,0.5);
      z-index: 149;
    }
    .calc-overlay.open { display: block; }
    @media (max-width: 768px) {
      .content-with-sidebar { flex-direction: column; }
      .calc-sidebar {
        display: none;
        position: fixed;
        right: 0;
        top: 0;
        height: 100vh;
        z-index: 150;
        width: 300px;
        box-shadow: var(--shadow-lg);
      }
      .calc-sidebar.open { display: block; }
      .calc-float-btn { display: flex; }
    }
    @media (min-width: 769px) {
      .main-content { max-width: 640px; }
    }
"""

html = html.replace('  </style>', CSS + '  </style>', 1)

# ─── 2. CalculatorSidebar component (insert before function App()) ─────────────
COMPONENT = r"""
// ═══════════════════════════════════════════════════════════════
// CASCADE CALCULATOR SIDEBAR COMPONENT
// ═══════════════════════════════════════════════════════════════
function CalculatorSidebar({ selectedLevel, mobileOpen, onClose }) {
  var defaults = {
    targetKW: 40, rackCount: 50, micMVA: 5, micUtilisation: 85,
    busSectionA: 1600, busUtilisation: 73, voltage: 415, pf: 0.85,
    floorRatingPSF: 150, rackWeightLbs: 3200, leaseYears: 12, electricityPrice: 0.12
  };
  var [inputs, setInputs] = React.useState(defaults);
  var [result, setResult] = React.useState(null);
  var [allResults, setAllResults] = React.useState(null);
  var [expanded, setExpanded] = React.useState(null);

  var fields = [
    ['targetKW',        'Target kW/rack',     1   ],
    ['rackCount',       'Number of racks',     1   ],
    ['micMVA',          'MIC MVA',             0.1 ],
    ['micUtilisation',  'MIC utilisation %',   1   ],
    ['busSectionA',     'Bus section amps',    100 ],
    ['busUtilisation',  'Bus utilisation %',   1   ],
    ['voltage',         'Voltage (V)',          1   ],
    ['pf',              'Power factor',        0.01],
    ['floorRatingPSF',  'Floor rating PSF',    10  ],
    ['rackWeightLbs',   'Rack weight lbs',     100 ],
    ['leaseYears',      'Lease years',          1  ],
    ['electricityPrice','Electricity \u20ac/kWh', 0.01]
  ];

  function calcInputs() {
    return {
      targetKW:         +inputs.targetKW         || 40,
      rackCount:        +inputs.rackCount         || 50,
      micMVA:           +inputs.micMVA            || 5,
      micUtilisation:   (+inputs.micUtilisation   || 85)  / 100,
      busSectionA:      +inputs.busSectionA       || 1600,
      busUtilisation:   (+inputs.busUtilisation   || 73)  / 100,
      voltage:          +inputs.voltage           || 415,
      pf:               +inputs.pf                || 0.85,
      floorRatingPSF:   +inputs.floorRatingPSF    || 150,
      rackWeightLbs:    +inputs.rackWeightLbs     || 3200,
      leaseYears:       +inputs.leaseYears        || 12,
      electricityPrice: +inputs.electricityPrice  || 0.12
    };
  }

  function runLevel(lvl) {
    try {
      var src = lvl.cascadeCheck || '';
      var body = src.replace(/^function\s*\([^)]*\)\s*\{/, '').replace(/\}\s*$/, '');
      return (new Function('inputs', body))(calcInputs());
    } catch(e) { return { pass: false, reason: 'Error: ' + e.message }; }
  }

  return (
    <aside className={'calc-sidebar' + (mobileOpen ? ' open' : '')}>
      {onClose && (
        <button onClick={onClose} style={{float:'right',background:'none',border:'none',color:'var(--text-dim)',fontSize:'1.1rem',cursor:'pointer',marginBottom:'0.5rem'}}>&#x2715;</button>
      )}
      <div className="calc-sidebar-title">&#x26A1; AI Readiness Calculator</div>
      {fields.map(function(f) {
        return (
          <div key={f[0]}>
            <label className="calc-input-label">{f[1]}</label>
            <input
              className="calc-input"
              type="number"
              step={f[2]}
              value={inputs[f[0]]}
              onChange={function(e){ var n=Object.assign({},inputs); n[f[0]]=e.target.value; setInputs(n); }}
            />
          </div>
        );
      })}
      <button className="calc-btn-primary" onClick={function(){ setResult(runLevel(LEVELS[selectedLevel])); }}>
        Find Bottlenecks &#x2192;
      </button>
      {result && (
        <div className={result.pass ? 'calc-result-pass' : 'calc-result-fail'}>
          <strong>{result.pass ? '\u2705 PASS' : '\u274C FAIL'}</strong><br/>{result.reason}
        </div>
      )}
      <button className="calc-btn-secondary" onClick={function(){ setAllResults(LEVELS.map(function(l){ return runLevel(l); })); }}>
        Test all 9 levels &#x2192;
      </button>
      {allResults && (
        <div style={{marginTop:'0.25rem'}}>
          {LEVELS.map(function(lvl, i) {
            var r = allResults[i];
            return (
              <div key={i}>
                <div className="calc-grid-row" onClick={function(){ setExpanded(expanded === i ? null : i); }}>
                  <span className={'calc-dot ' + (r.pass ? 'calc-dot-pass' : 'calc-dot-fail')} />
                  <span style={{fontWeight:700,color:'var(--text-dim)',fontSize:'0.7rem',minWidth:'20px'}}>{lvl.id}</span>
                  <span style={{flex:1,color:'var(--text)',fontSize:'0.78rem'}}>{lvl.title}</span>
                  <span style={{fontSize:'0.7rem'}}>{r.pass ? '\u2705' : '\u274C'}</span>
                </div>
                {expanded === i && <div className="calc-row-detail">{r.reason}</div>}
              </div>
            );
          })}
        </div>
      )}
      {/* FACILITY_PROFILE_SLOT */}
    </aside>
  );
}

"""

html = html.replace('function App() {', COMPONENT + 'function App() {', 1)

# ─── 3. Add calcMobileOpen state to App ───────────────────────────────────────
OLD_STATE = "  var [visitedStages, setVisitedStages] = React.useState(safeLoad('visitedStages', {}));"
NEW_STATE = OLD_STATE + "\n  var [calcMobileOpen, setCalcMobileOpen] = React.useState(false);"

html = html.replace(OLD_STATE, NEW_STATE, 1)

# ─── 4. Wrap main content with sidebar in App return ─────────────────────────
OLD_MAIN = """      {/* Main content */}
      <main className="main-content">
        {renderTab()}
      </main>"""

NEW_MAIN = """      {/* Main content + Calculator sidebar */}
      <div className="content-with-sidebar">
        <main className="main-content">
          {renderTab()}
        </main>
        <CalculatorSidebar selectedLevel={levelIdx} mobileOpen={false} />
      </div>
      <button className="calc-float-btn" onClick={() => setCalcMobileOpen(true)}>&#x26A1;</button>
      {calcMobileOpen && <div className="calc-overlay open" onClick={() => setCalcMobileOpen(false)} />}
      {calcMobileOpen && <CalculatorSidebar selectedLevel={levelIdx} mobileOpen={true} onClose={() => setCalcMobileOpen(false)} />}"""

html = html.replace(OLD_MAIN, NEW_MAIN, 1)

# ─── 5. Verify ────────────────────────────────────────────────────────────────
assert 'CalculatorSidebar' in html, "CalculatorSidebar component missing"
assert 'calc-sidebar' in html, "calc-sidebar CSS missing"
assert 'calcMobileOpen' in html, "calcMobileOpen state missing"
assert html.count('"cascadeCheck":') == 9, f"Expected 9 cascadeCheck data entries, got {html.count('cascadeCheck')}"
# Count grammar facts: each fact has a "term" key
fact_count = html.count('"plain":')
assert fact_count == 45, f"Expected 45 grammar facts, got {fact_count}"
q_count = html.count('"correct":')
assert q_count == 27, f"Expected 27 questions, got {q_count}"

with open(DST, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"[01] OK — wrote {DST}")
print(f"     cascadeCheck data entries: {html.count(chr(34)+'cascadeCheck'+chr(34)+':')}")
print(f"     grammar facts (plain)   : {fact_count}")
print(f"     assessment questions    : {q_count} (via 'correct' key)")
