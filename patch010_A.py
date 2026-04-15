"""
Patch A for DC-TOOL-010 v2.0.0
Replace CALC_ENGINE[] + FINDINGS_ENGINE[] arrays and CALC ENGINE RUNNER
with function-based deterministic engine from DC_TOOL_010_CALC_ENGINE_v2_0.md
"""
import sys

DST = 'tools/DC-TOOL-010_v2_0_0.html'
with open(DST, encoding='utf-8') as f:
    h = f.read()

# ── Patch A: Replace CALC_ENGINE[] + FINDINGS_ENGINE[] arrays ─────────────────
OLD_A_START = """/* ================================================================
   CALC_ENGINE — Deterministic JavaScript. No AI. No network.
   Replace per tool. Every formula visible and auditable.
   ================================================================ */
const CALC_ENGINE = ["""

OLD_A_END = """/* ================================================================
   INPUT_SCHEMA — Same as v1.0 (DC-Screen aligned)
   ================================================================ */"""

NEW_A = """/* ================================================================
   CALC ENGINE — 9 deterministic calculations (C01–C09)
   Source: DC_TOOL_010_CALC_ENGINE_v2_0.md
   RULE: LLM never calculates. Numbers are JavaScript. Narrative is AI.
   ================================================================ */
function runCalcEngine(inputs) {
  const { it_load_mw, pue, racks, kw_per_rack, target_kw_rack, mic_mva,
          ppa_pct, cooling_type, cooling_capacity_mw, bms_points, grid_feed } = inputs;

  const calcs = {};
  const GRID_EF       = 0.2241;   // kgCO2/kWh — SEAI 2026 (T1)
  const CARBON_TAX    = 71;       // €/tCO2 — Budget 2025 (T1)
  const ELEC_PRICE    = 0.12;     // €/kWh — CRU Q4 2024 (T2)
  const TAX_PUE       = 1.3;      // EU Taxonomy threshold (T1)
  const CRU_RENEW     = 80;       // % — CRU/2025236 (T1)
  const FREE_COOL_HRS = 7200;     // hrs/yr <18°C Dublin — Met Éireann 30yr (T1)
  const RETROFIT_KW   = 1100;     // €/kW IT cooling retrofit — RICS NRM1 (T3)

  const total_mw = (it_load_mw || 0) * (pue || 1);
  const mic_mw   = (mic_mva || 0) * 0.95;

  // C01: Power Capacity vs MIC
  calcs.power_capacity = {
    id: 'C01', label: 'Power Capacity vs MIC',
    formula: 'IT × PUE = facility MW; MIC × 0.95 = available MW',
    inputs: { total_mw: Math.round(total_mw * 100) / 100, mic_mw: Math.round(mic_mw * 100) / 100 },
    result: {
      utilisation_pct: mic_mw > 0 ? Math.round(total_mw / mic_mw * 100) : 0,
      adequate: total_mw <= mic_mw,
      headroom_mw: Math.round((mic_mw - total_mw) * 10) / 10
    },
    unit: 'MW', tier: 'Derived'
  };

  // C02: Future Density Check
  const future_it_mw  = ((target_kw_rack || 0) * (racks || 0)) / 1000;
  const future_fac_mw = future_it_mw * TAX_PUE;
  calcs.density_capacity = {
    id: 'C02', label: 'Future Density Check',
    formula: 'Target kW/rack × racks / 1,000 × 1.3 PUE vs MIC',
    inputs: { target_kw_rack, racks, target_pue: TAX_PUE, mic_mw: Math.round(mic_mw * 10) / 10 },
    result: {
      future_it_mw:      Math.round(future_it_mw * 10) / 10,
      future_facility_mw: Math.round(future_fac_mw * 10) / 10,
      mic_adequate: future_fac_mw <= mic_mw
    },
    unit: 'MW', tier: 'Derived'
  };

  // C03: Cooling Capacity Check
  const heat_mw = it_load_mw || 0; // IT heat load ≈ cooling load
  calcs.cooling_check = {
    id: 'C03', label: 'Cooling Capacity Check',
    formula: 'IT heat load vs cooling plant capacity',
    inputs: { heat_mw: Math.round(heat_mw * 10) / 10, cooling_capacity_mw: cooling_capacity_mw || 0 },
    result: {
      adequate: (cooling_capacity_mw || 0) >= heat_mw,
      utilisation_pct: cooling_capacity_mw > 0 ? Math.round(heat_mw / cooling_capacity_mw * 100) : 0
    },
    unit: 'MW', tier: 'Derived'
  };

  // C04: Free Cooling Opportunity
  const has_fc = cooling_type === 'chiller_fc' || cooling_type === 'evaporative';
  const fc_saving_eur = has_fc ? 0 : heat_mw * 1000 * FREE_COOL_HRS * 0.7 * ELEC_PRICE;
  calcs.free_cooling = {
    id: 'C04', label: 'Free Cooling Opportunity',
    formula: 'If no free cooling: heat MW × 7,200 hrs × 70% capture × €0.12/kWh',
    inputs: { has_fc, heat_mw: Math.round(heat_mw * 10) / 10, free_cool_hrs: FREE_COOL_HRS, elec_price: ELEC_PRICE },
    result: { installed: has_fc, annual_saving: Math.round(fc_saving_eur) },
    unit: '€/yr', tier: 'T1 (Met Éireann) + T3 (capture rate)'
  };

  // C05: CRU Renewable Gap
  const facility_mwh = total_mw * 8760;
  const gap_pct      = Math.max(0, CRU_RENEW - (ppa_pct || 0));
  const gap_mwh      = facility_mwh * gap_pct / 100;
  calcs.renewable_gap = {
    id: 'C05', label: 'CRU Renewable Gap',
    formula: '80% − PPA% = gap. Gap MWh = facility MWh × gap%',
    inputs: { ppa_pct: ppa_pct || 0, cru_target: CRU_RENEW, facility_mwh: Math.round(facility_mwh) },
    result: { gap_pct, gap_mwh: Math.round(gap_mwh), compliant: (ppa_pct || 0) >= CRU_RENEW },
    unit: '% / MWh', tier: 'T1 — CRU/2025236'
  };

  // C06: PUE Gap Cost (EU Taxonomy)
  const pue_gap       = Math.max(0, (pue || 1) - TAX_PUE);
  const overhead_kwh  = (it_load_mw || 0) * 1000 * pue_gap * 8760;
  calcs.pue_gap = {
    id: 'C06', label: 'PUE Gap vs EU Taxonomy',
    formula: 'PUE − 1.3 = gap. IT kW × gap × 8,760 hrs × €0.12/kWh = annual cost',
    inputs: { pue: pue || 0, threshold: TAX_PUE, it_load_kw: (it_load_mw || 0) * 1000 },
    result: {
      gap: Math.round(pue_gap * 100) / 100,
      annual_cost: Math.round(overhead_kwh * ELEC_PRICE),
      aligned: (pue || 1) <= TAX_PUE
    },
    unit: '€/yr', tier: 'T1 — Delegated Act 2021/2139'
  };

  // C07: Carbon Exposure (Scope 2)
  const scope2_t   = total_mw * 1000 * 8760 * GRID_EF / 1000;
  const carbon_cost = scope2_t * CARBON_TAX;
  calcs.carbon = {
    id: 'C07', label: 'Carbon Exposure (Scope 2)',
    formula: 'Facility kWh × 0.2241 / 1,000 = tCO₂/yr. × €71 = cost',
    inputs: { total_mw: Math.round(total_mw * 100) / 100, grid_ef: GRID_EF, carbon_tax: CARBON_TAX },
    result: { scope2_tonnes: Math.round(scope2_t), annual_cost: Math.round(carbon_cost) },
    unit: 'tCO₂/yr, €/yr', tier: 'T1 — SEAI 2026, Budget 2025'
  };

  // C08: Indicative Retrofit Payback
  const retrofit_cost  = (it_load_mw || 0) * 1000 * RETROFIT_KW;
  const annual_saving  = (overhead_kwh * ELEC_PRICE) + fc_saving_eur;
  const payback_years  = annual_saving > 0 ? Math.round(retrofit_cost / annual_saving * 10) / 10 : 999;
  calcs.retrofit_payback = {
    id: 'C08', label: 'Indicative Retrofit Payback',
    formula: 'Retrofit cost (€1,100/kW IT) ÷ annual saving (PUE gap + free cooling)',
    inputs: { retrofit_cost, annual_saving: Math.round(annual_saving) },
    result: { cost: retrofit_cost, saving: Math.round(annual_saving), payback_years },
    unit: 'years', tier: 'T3 — RICS NRM1',
    caveat: 'Screening-level estimate. Subject to detailed design and site survey.'
  };

  // C09: 10-Year Cost of Inaction
  const cost_10yr = carbon_cost * 10 + (overhead_kwh * ELEC_PRICE) * 10;
  calcs.inaction_cost = {
    id: 'C09', label: '10-Year Cost of Inaction',
    formula: '10 × (carbon cost + PUE excess energy cost)',
    inputs: { carbon_annual: Math.round(carbon_cost), pue_annual: Math.round(overhead_kwh * ELEC_PRICE) },
    result: { total_10yr: Math.round(cost_10yr) },
    unit: '€', tier: 'Derived'
  };

  return calcs;
}

/* ================================================================
   FINDINGS ENGINE — 6 rule-based findings (F01–F06)
   Source: DC_TOOL_010_CALC_ENGINE_v2_0.md
   ================================================================ */
function runFindingsEngine(calcs) {
  const findings = [];

  // F01: Power Capacity
  const pc = calcs.power_capacity.result;
  findings.push({
    id: 'F01', category: 'Power', title: 'Power Capacity vs MIC',
    status: !pc.adequate ? 'RED' : pc.utilisation_pct > 80 ? 'AMBER' : 'GREEN',
    current: pc.utilisation_pct + '% MIC utilisation (' + Math.round(calcs.power_capacity.inputs.total_mw * 100) / 100 + ' MW of ' + Math.round(calcs.power_capacity.inputs.mic_mw * 100) / 100 + ' MW)',
    required: '≤80% MIC utilisation for growth headroom',
    gap: pc.adequate ? pc.headroom_mw + ' MW headroom available' : 'Facility load exceeds MIC — ' + Math.abs(pc.headroom_mw) + ' MW overload',
    action: pc.adequate
      ? (pc.utilisation_pct > 80 ? 'MIC approaching capacity — plan augmentation' : 'Monitor utilisation trend')
      : 'MIC upgrade required — engage ESB Networks'
  });

  // F02: Free Cooling
  const fc = calcs.free_cooling.result;
  findings.push({
    id: 'F02', category: 'Cooling', title: 'Free Cooling Installation',
    status: fc.installed ? 'GREEN' : 'RED',
    current: fc.installed ? 'Free cooling installed and in service' : 'No free cooling — €' + Math.round(fc.annual_saving / 1000).toLocaleString() + 'k/yr saving foregone',
    required: 'Air-side or fluid economiser to capture 7,200 hrs/yr in Dublin (Met Éireann T1)',
    gap: fc.installed ? 'In service — verify economiser operation' : 'Free cooling absent — full 7,200 hrs/yr opportunity unrealised',
    action: fc.installed
      ? 'Confirm economiser control strategy and winter operation'
      : 'Priority retrofit — indicative annual saving €' + Math.round(fc.annual_saving / 1000).toLocaleString() + 'k/yr'
  });

  // F03: CRU Renewable Obligation
  const rg = calcs.renewable_gap.result;
  findings.push({
    id: 'F03', category: 'ESG', title: 'CRU Renewable Obligation',
    status: rg.compliant ? 'GREEN' : rg.gap_pct > 40 ? 'RED' : 'AMBER',
    current: (calcs.renewable_gap.inputs.ppa_pct || 0) + '% renewable (PPA/GO coverage)',
    required: '80% renewable energy obligation (CRU/2025236)',
    gap: rg.compliant ? 'Compliant with CRU obligation' : rg.gap_pct + '% gap = ' + rg.gap_mwh.toLocaleString() + ' MWh uncovered',
    action: rg.compliant
      ? 'Maintain PPA coverage — document for investor reporting'
      : 'Procure ' + rg.gap_mwh.toLocaleString() + ' MWh PPA/GOs to close gap'
  });

  // F04: EU Taxonomy PUE
  const pg = calcs.pue_gap.result;
  findings.push({
    id: 'F04', category: 'Compliance', title: 'EU Taxonomy PUE Alignment',
    status: pg.aligned ? 'GREEN' : pg.gap > 0.3 ? 'RED' : 'AMBER',
    current: 'PUE ' + (calcs.pue_gap.inputs.pue || 0),
    required: 'PUE ≤1.3 (EU Taxonomy Delegated Act 2021/2139)',
    gap: pg.aligned
      ? 'Taxonomy-aligned — document for investor reporting'
      : 'Gap ' + pg.gap + ' PUE points — excess energy cost €' + Math.round(pg.annual_cost / 1000).toLocaleString() + 'k/yr',
    action: pg.aligned
      ? 'Maintain PUE monitoring — evidence for SFDR/taxonomy disclosure'
      : 'Cooling system retrofit required to achieve PUE ≤1.3'
  });

  // F05: Retrofit Payback
  const rp = calcs.retrofit_payback.result;
  findings.push({
    id: 'F05', category: 'Commercial', title: 'Retrofit Investment Payback',
    status: rp.payback_years <= 3 ? 'GREEN' : rp.payback_years <= 7 ? 'AMBER' : 'RED',
    current: rp.payback_years < 999
      ? rp.payback_years + ' year payback on €' + (rp.cost / 1e6).toFixed(1) + 'M indicative retrofit'
      : 'No retrofit saving identified',
    required: '≤3 years for strong investment case',
    gap: rp.saving > 0
      ? 'Annual saving: €' + Math.round(rp.saving / 1000).toLocaleString() + 'k/yr (PUE + free cooling)'
      : 'No current gap — no retrofit saving',
    action: 'Commission Desktop Assessment for detailed business case — €10,000–€15,000'
  });

  // F06: 10-Year Cost of Inaction
  const ic = calcs.inaction_cost.result;
  findings.push({
    id: 'F06', category: 'Commercial', title: '10-Year Cost of Inaction',
    status: ic.total_10yr > 5000000 ? 'RED' : ic.total_10yr > 1000000 ? 'AMBER' : 'GREEN',
    current: '€' + (ic.total_10yr / 1e6).toFixed(1) + 'M over 10 years (carbon + PUE excess)',
    required: 'Quantified baseline for retrofit ROI comparison',
    gap: 'Carbon cost: €' + Math.round(calcs.inaction_cost.inputs.carbon_annual / 1000).toLocaleString() + 'k/yr | PUE excess: €' + Math.round(calcs.inaction_cost.inputs.pue_annual / 1000).toLocaleString() + 'k/yr',
    action: 'Use as baseline for Desktop Assessment ROI comparison'
  });

  const rc = findings.filter(f => f.status === 'RED').length;
  const ac = findings.filter(f => f.status === 'AMBER').length;
  return {
    findings,
    summary: { red_count: rc, amber_count: ac, green_count: findings.length - rc - ac, overall: rc > 0 ? 'RED' : ac > 0 ? 'AMBER' : 'GREEN' }
  };
}

/* ================================================================
   INPUT_SCHEMA — Same as v1.0 (DC-Screen aligned)
   ================================================================ */"""

# Find boundaries
idx_start = h.find(OLD_A_START)
if idx_start == -1:
    print("ERROR: CALC_ENGINE start not found!")
    sys.exit(1)
idx_end = h.find(OLD_A_END, idx_start)
if idx_end == -1:
    print("ERROR: INPUT_SCHEMA separator not found!")
    sys.exit(1)

old_block = h[idx_start : idx_end + len(OLD_A_END)]
h = h[:idx_start] + NEW_A + h[idx_start + len(old_block):]
print(f"Patch A done: replaced {len(old_block)} chars with {len(NEW_A)} chars")

# ── Patch B: Replace CALC ENGINE RUNNER ──────────────────────────────────────
OLD_RUNNER_START = """/* ================================================================
   CALC ENGINE RUNNER — Deterministic. No AI.
   ================================================================ */
function runCalcEngine(inputs) {"""

OLD_RUNNER_END = """function deriveTrafficLight(findings) {
  if (findings.some(f => f.status === 'FAIL')) return 'RED';
  if (findings.some(f => f.status === 'FLAG')) return 'AMBER';
  return 'GREEN';
}"""

NEW_RUNNER = """/* ================================================================
   CALC ENGINE RUNNER — delegates to runCalcEngine / runFindingsEngine above
   ================================================================ */

/* ================================================================
   AUDIT TRAIL HELPERS
   ================================================================ */
function formatCalcResult(result) {
  if (result === null || result === undefined) return 'N/A';
  if (typeof result === 'boolean') return result ? 'Yes' : 'No';
  if (typeof result === 'object') {
    return Object.entries(result).map(([k, v]) => {
      const lbl = k.replace(/_/g, ' ');
      if (typeof v === 'boolean') return lbl + ': ' + (v ? 'Yes' : 'No');
      if (typeof v === 'number') return lbl + ': ' + (Number.isInteger(v) ? v.toLocaleString() : v.toFixed(1));
      return lbl + ': ' + v;
    }).join(' | ');
  }
  return String(result);
}

function buildAuditSteps(calcs) {
  if (!calcs) return [];
  return Object.values(calcs).map(c => ({
    id:        c.id,
    name:      c.label,
    formula:   c.formula,
    value:     c.result,
    formatted: formatCalcResult(c.result),
    unit:      c.unit || '',
    tier:      c.tier || 'Derived',
    source:    c.source || c.tier || 'Derived',
    caveat:    c.caveat || null,
    inputs_used: c.inputs ? Object.entries(c.inputs).map(([k, v]) => ({
      label:  k.replace(/_/g, ' '),
      value:  typeof v === 'boolean' ? (v ? 'Yes' : 'No') : v,
      tier:   'Input',
      source: 'User input or derived'
    })) : []
  }));
}

function deriveTrafficLight(findingsResult) {
  return findingsResult.summary.overall;
}"""

idx_runner_start = h.find(OLD_RUNNER_START)
if idx_runner_start == -1:
    print("ERROR: CALC ENGINE RUNNER start not found!")
    sys.exit(1)
idx_runner_end_start = h.find(OLD_RUNNER_END, idx_runner_start)
if idx_runner_end_start == -1:
    print("ERROR: old deriveTrafficLight not found!")
    sys.exit(1)
idx_runner_end = idx_runner_end_start + len(OLD_RUNNER_END)

old_runner = h[idx_runner_start : idx_runner_end]
h = h[:idx_runner_start] + NEW_RUNNER + h[idx_runner_end:]
print(f"Patch B (runner) done: replaced {len(old_runner)} chars with {len(NEW_RUNNER)} chars")

with open(DST, 'w', encoding='utf-8') as f:
    f.write(h)
print(f"Saved. Lines: {h.count(chr(10)) + 1}")
