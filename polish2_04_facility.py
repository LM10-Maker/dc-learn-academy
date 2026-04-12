#!/usr/bin/env python3
"""
polish2_04_facility.py
ITEM 4: FACILITY PROFILE PANEL
Placed inside the CalculatorSidebar (below the calculator content).
Reads/writes DC-AI-001_v1_2_0.html
"""

WF = 'DC-AI-001_v1_2_0.html'

with open(WF, 'r', encoding='utf-8') as f:
    html = f.read()

# ─── 1. CSS ───────────────────────────────────────────────────────────────────
CSS = r"""
    /* ─── FACILITY PROFILE PANEL ───────────────────────────────────── */
    .facility-profile {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      margin-top: 1.25rem;
      overflow: hidden;
    }
    .facility-profile-header {
      padding: 0.7rem 1rem;
      border-bottom: 1px solid var(--border);
      background: var(--panel);
    }
    .facility-profile-title {
      font-size: 0.85rem;
      font-weight: 600;
      color: var(--text-bright);
      margin-bottom: 2px;
    }
    .facility-profile-subtitle {
      font-size: 0.7rem;
      color: var(--text-muted);
    }
    .facility-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0.35rem 1rem;
      font-size: 0.78rem;
      border-bottom: 1px solid var(--border);
    }
    .facility-row:last-child { border-bottom: none; }
    .facility-row:nth-child(odd)  { background: var(--surface); }
    .facility-row:nth-child(even) { background: var(--panel); }
    .facility-row-label { color: var(--text-dim); }
    .facility-row-value { color: var(--text-bright); font-weight: 600; text-align: right; }
"""

html = html.replace('  </style>', CSS + '  </style>', 1)

# ─── 2. FacilityProfile component (before function App()) ────────────────────
COMPONENT = r"""
// ═══════════════════════════════════════════════════════════════
// FACILITY PROFILE COMPONENT
// ═══════════════════════════════════════════════════════════════
function FacilityProfile() {
  var rows = [
    ['Racks',             '400'],
    ['Current density',   '8 kW/rack'],
    ['IT load',           '2.4 MW'],
    ['Current PUE',       '1.50'],
    ['Target PUE',        '1.20'],
    ['MIC',               '5 MVA (85% utilised)'],
    ['Voltage',           '10 kV ESB Networks MV'],
    ['Hall A',            '200 racks, air-cooled, 8 kW avg'],
    ['Hall B',            '200 racks, retrofit candidate'],
    ['Floor loading',     '150 psf (raised floor)'],
    ['Ceiling height',    '3.2 m'],
    ['Generator',         '3.0 MW'],
    ['UPS',               '2.8 MW'],
    ['Lease remaining',   '12 years']
  ];
  return (
    <div className="facility-profile">
      <div className="facility-profile-header">
        <div className="facility-profile-title">&#x1F3E2; Facility Profile</div>
        <div className="facility-profile-subtitle">Clonshaugh Reference DC (2012)</div>
      </div>
      {rows.map(function(r, i) {
        return (
          <div key={i} className="facility-row">
            <span className="facility-row-label">{r[0]}</span>
            <span className="facility-row-value">{r[1]}</span>
          </div>
        );
      })}
    </div>
  );
}

"""

html = html.replace('function App() {', COMPONENT + 'function App() {', 1)

# ─── 3. Inject FacilityProfile into the slot left by script 01 ───────────────
html = html.replace('      {/* FACILITY_PROFILE_SLOT */}',
                    '      <FacilityProfile />', 1)

# ─── 4. Verify ────────────────────────────────────────────────────────────────
assert 'FacilityProfile' in html, "FacilityProfile component missing"
assert 'facility-profile' in html, "facility-profile CSS missing"
assert 'Clonshaugh Reference DC' in html, "facility profile content missing"
assert '{/* FACILITY_PROFILE_SLOT */}' not in html, "slot placeholder not replaced"
assert html.count('"plain":') == 45, "grammar facts changed"
assert html.count('"correct":') == 27, "assessment questions changed"

with open(WF, 'w', encoding='utf-8') as f:
    f.write(html)

print("[04] OK — facility profile panel added inside calculator sidebar")
