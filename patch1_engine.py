"""
Patch 1: Replace CALC_ENGINE[] + FINDINGS_ENGINE[] arrays
         AND the CALC ENGINE RUNNER section
         with cooling-chain-specific function-based engine.
"""
import sys

DST = 'tools/DC-TOOL-002_v2_0_0.html'
with open(DST, encoding='utf-8') as f:
    h = f.read()

# ── Patch A: CALC_ENGINE[] + FINDINGS_ENGINE[] arrays ────────────────────────
OLD_A = """/* ================================================================
   CALC_ENGINE — Deterministic JavaScript. No AI. No network.
   Replace per tool. Every formula visible and auditable.
   ================================================================ */
const CALC_ENGINE = ["""

# Find start of INPUT_SCHEMA comment that follows FINDINGS_ENGINE
OLD_A_END = """];

/* ================================================================
   INPUT_SCHEMA — Same as v1.0 (DC-Screen aligned)
   ================================================================ */"""

NEW_A_START = """/* ================================================================
   CALC ENGINE — 11 deterministic calculations (C01–C11)
   Source: DC_TOOL_002_CALC_ENGINE_v2_0.md
   RULE: LLM never calculates. Numbers are JavaScript. Narrative is AI.
   ================================================================ */
function runCalcEngine(inp) {
  const calcs = {};

  // C01: Cooling Load
  const it_load_kw = inp.it_load_mw * 1000;
  const cooling_load_kw = it_load_kw * (inp.pue - 1);
  calcs.cooling_load_kw = {
    id: 'C01', label: 'Cooling Load',
    formula: 'IT Load (kW) × (PUE − 1)',
    inputs: { it_load_kw, pue: inp.pue },
    result: Math.round(cooling_load_kw),
    unit: 'kW', tier: 'Derived'
  };

  // C02: Annual Cooling Energy
  const annual_cooling_mwh = cooling_load_kw * 8760 / 1000;
  calcs.annual_cooling_mwh = {
    id: 'C02', label: 'Annual Cooling Energy',
    formula: 'Cooling Load (kW) × 8,760 hrs ÷ 1,000',
    inputs: { cooling_load_kw: Math.round(cooling_load_kw) },
    result: Math.round(annual_cooling_mwh),
    unit: 'MWh/yr', tier: 'Derived'
  };

  // C03: Annual Cooling Energy Cost
  // T2 — CRU Q4 2024 (€0.12/kWh)
  const elec_price_mwh = CANONICAL_DATA.electricity_price.value * 1000;
  const annual_cooling_cost = annual_cooling_mwh * elec_price_mwh;
  calcs.annual_cooling_cost = {
    id: 'C03', label: 'Annual Cooling Energy Cost',
    formula: 'Annual Cooling Energy (MWh) × €120/MWh',
    inputs: { annual_cooling_mwh: Math.round(annual_cooling_mwh), elec_price_per_mwh: elec_price_mwh },
    result: Math.round(annual_cooling_cost),
    unit: '€/yr', tier: 'T2',
    source: CANONICAL_DATA.electricity_price.source
  };

  // C04: Free Cooling Hours Utilised
  // T1 — Met Éireann 30-year average: 7,200 hrs/yr below 18°C in Dublin
  const fc_potential = CANONICAL_DATA.free_cooling_hours.value;
  const fc_hours = inp.has_free_cooling === 'yes' ? 7200 :
                   inp.has_free_cooling === 'partial' ? 3600 : 0;
  calcs.free_cooling_hours = {
    id: 'C04', label: 'Free Cooling Hours Utilised',
    formula: 'Yes → 7,200 hrs/yr | Partial → 3,600 hrs/yr | No → 0 hrs/yr',
    inputs: { has_free_cooling: inp.has_free_cooling, dublin_potential_hrs: fc_potential },
    result: fc_hours,
    unit: 'hrs/yr', tier: 'T1',
    source: CANONICAL_DATA.free_cooling_hours.source
  };

  // C05: Unrealised Free Cooling Saving
  const fc_unrealised_hrs = fc_potential - fc_hours;
  const fc_saving_mwh = fc_unrealised_hrs * cooling_load_kw / 1000;
  const fc_saving_eur = fc_saving_mwh * elec_price_mwh;
  calcs.free_cooling_saving = {
    id: 'C05', label: 'Unrealised Free Cooling Saving',
    formula: '(7,200 − Utilised hrs) × Cooling Load (kW) ÷ 1,000',
    inputs: { unrealised_hrs: fc_unrealised_hrs, cooling_load_kw: Math.round(cooling_load_kw) },
    result: { saving_mwh: Math.round(fc_saving_mwh), saving_eur: Math.round(fc_saving_eur) },
    unit: 'MWh/yr | €/yr', tier: 'Derived'
  };

  // C06: Chiller Capacity & Headroom
  const has_chiller_data = inp.chiller_count > 0 && inp.chiller_kw_each > 0;
  const chiller_total_kw = has_chiller_data ? inp.chiller_count * inp.chiller_kw_each : null;
  const chiller_headroom_pct = chiller_total_kw !== null ?
    Math.round((chiller_total_kw - cooling_load_kw) / chiller_total_kw * 100 * 10) / 10 : null;
  calcs.chiller_capacity = {
    id: 'C06', label: 'Chiller Capacity & Headroom',
    formula: 'Count × kW each = Total; Headroom = (Total − Cooling Load) ÷ Total × 100',
    inputs: has_chiller_data
      ? { chiller_count: inp.chiller_count, chiller_kw_each: inp.chiller_kw_each, cooling_load_kw: Math.round(cooling_load_kw) }
      : { note: 'Chiller data not provided' },
    result: chiller_total_kw !== null
      ? { total_kw: chiller_total_kw, headroom_pct: chiller_headroom_pct }
      : null,
    unit: 'kW / %', tier: 'Derived'
  };

  // C07: Refrigerant GWP Lookup
  // T1 — EU F-Gas Regulation 2024/573 GWP values
  const gwp_map = { r410a: 2088, r407c: 1774, r134a: 1430, r32: 675, r1234ze: 7, none: 0 };
  const gwp = inp.refrigerant_type && gwp_map[inp.refrigerant_type] !== undefined
    ? gwp_map[inp.refrigerant_type] : null;
  calcs.refrigerant_gwp = {
    id: 'C07', label: 'Refrigerant GWP',
    formula: 'Lookup: R410A=2,088 | R407C=1,774 | R134a=1,430 | R32=675 | R1234ze=7 | None=0',
    inputs: { refrigerant_type: inp.refrigerant_type || 'not provided' },
    result: gwp,
    unit: 'GWP (tCO₂e/tonne)', tier: 'T1',
    source: 'EU F-Gas Regulation 2024/573'
  };

  // C08: F-Gas Exposure
  // T1 — EU F-Gas Regulation 2024/573
  const fgas_tco2e = (gwp !== null && inp.refrigerant_charge_kg > 0)
    ? Math.round(inp.refrigerant_charge_kg * gwp / 1000 * 10) / 10 : null;
  calcs.fgas_exposure = {
    id: 'C08', label: 'F-Gas Exposure',
    formula: 'Charge (kg) × GWP ÷ 1,000',
    inputs: { charge_kg: inp.refrigerant_charge_kg || 'not provided', gwp: gwp !== null ? gwp : 'unknown' },
    result: fgas_tco2e,
    unit: 'tCO₂e', tier: 'T1',
    source: 'EU F-Gas Regulation 2024/573'
  };

  // C09: Supply Temperature Assessment
  // T1 — ASHRAE TC 9.9 Class A1 range: 18–27°C
  const supply_temp = Number(inp.supply_temp_c) || null;
  const ashrae_min = 18;
  const ashrae_max = 27;
  const in_ashrae = supply_temp !== null && supply_temp >= ashrae_min && supply_temp <= ashrae_max;
  const temp_deviation = supply_temp !== null
    ? (supply_temp < ashrae_min ? supply_temp - ashrae_min : supply_temp > ashrae_max ? supply_temp - ashrae_max : 0)
    : null;
  calcs.supply_temp_assessment = {
    id: 'C09', label: 'Supply Temperature Assessment',
    formula: 'ASHRAE TC 9.9 Class A1 range: 18°C – 27°C',
    inputs: { supply_temp_c: supply_temp !== null ? supply_temp : 'not provided', ashrae_range: '18–27°C' },
    result: supply_temp !== null ? { in_range: in_ashrae, deviation_c: temp_deviation } : null,
    unit: '°C', tier: 'T1',
    source: 'ASHRAE TC 9.9 Thermal Guidelines for Data Centres'
  };

  // C10: Indicative Free Cooling Retrofit Cost
  // T3 — CIBSE KS16 / BSRIA BG29: €100–€200 per kW IT
  const fc_retrofit_low  = inp.has_free_cooling !== 'yes' ? Math.round(it_load_kw * 100) : 0;
  const fc_retrofit_high = inp.has_free_cooling !== 'yes' ? Math.round(it_load_kw * 200) : 0;
  calcs.fc_retrofit_cost = {
    id: 'C10', label: 'Indicative Free Cooling Retrofit Cost',
    formula: 'IT Load (kW) × €100–€200/kW IT',
    inputs: { it_load_kw, has_free_cooling: inp.has_free_cooling },
    result: inp.has_free_cooling !== 'yes' ? { low: fc_retrofit_low, high: fc_retrofit_high } : null,
    unit: '€', tier: 'T3',
    source: 'CIBSE KS16 / BSRIA BG29 Data Centre Cooling Guidelines',
    caveat: 'Screening-level estimate. Subject to detailed design and site survey.'
  };

  // C11: Indicative Aisle Containment Cost
  // T3 — BSRIA BG29: €15,000–€35,000 per hall (flat rate)
  const containment_low  = inp.has_containment !== 'yes' ? 15000 : 0;
  const containment_high = inp.has_containment !== 'yes' ? 35000 : 0;
  calcs.containment_cost = {
    id: 'C11', label: 'Indicative Containment Cost',
    formula: '€15,000–€35,000 per hall (BSRIA BG29 flat rate)',
    inputs: { has_containment: inp.has_containment },
    result: inp.has_containment !== 'yes' ? { low: containment_low, high: containment_high } : null,
    unit: '€', tier: 'T3',
    source: 'BSRIA BG29 Data Centre Cooling Guidelines',
    caveat: 'Per-hall flat rate — screening-level estimate only.'
  };

  return calcs;
}

/* ================================================================
   FINDINGS ENGINE — 6 rule-based findings (F01–F06)
   Source: DC_TOOL_002_CALC_ENGINE_v2_0.md
   ================================================================ */
function runFindingsEngine(calcs) {
  const findings = [];

  // F01: Free Cooling Utilisation
  const fcHrs    = calcs.free_cooling_hours.result;
  const fcSaving = calcs.free_cooling_saving.result;
  findings.push({
    id: 'F01',
    category: 'Energy Efficiency',
    title: 'Free Cooling Utilisation',
    status: fcHrs >= 7200 ? 'GREEN' : fcHrs >= 3600 ? 'AMBER' : 'RED',
    current: fcHrs >= 7200 ? 'Full free cooling installed (7,200 hrs/yr)' :
             fcHrs >= 3600 ? 'Partial free cooling (3,600 hrs/yr)' :
             'No free cooling installed (0 hrs/yr)',
    required: '7,200 hrs/yr available in Dublin climate (Met Éireann T1)',
    gap: fcHrs >= 7200 ? 'None — fully utilised' :
         (7200 - fcHrs).toLocaleString() + ' hrs/yr unrealised' +
         (fcSaving ? ' — €' + Math.round(fcSaving.saving_eur / 1000).toLocaleString() + 'k/yr savings foregone' : ''),
    action: fcHrs >= 7200 ? 'Maintain and verify economiser operation' :
            fcHrs >= 3600 ? 'Commission full economiser upgrade — investigate Part 2 capacity' :
            'Install air-side or fluid economiser — significant energy savings available'
  });

  // F02: Aisle Containment
  const containment  = calcs.containment_cost.inputs.has_containment;
  const containCost  = calcs.containment_cost.result;
  findings.push({
    id: 'F02',
    category: 'Airflow Management',
    title: 'Aisle Containment',
    status: containment === 'yes' ? 'GREEN' : containment === 'partial' ? 'AMBER' : 'RED',
    current: containment === 'yes' ? 'Full hot/cold aisle containment in place' :
             containment === 'partial' ? 'Partial containment — some aisles uncontained' :
             'No aisle containment — uncontrolled airflow mixing',
    required: 'Hot-aisle or cold-aisle containment (ASHRAE TC 9.9)',
    gap: containment === 'yes' ? 'None' :
         containment === 'partial' ? 'Partial containment — bypass losses reducing cooling efficiency' :
         'Full containment absent — bypass and recirculation causing PUE uplift',
    action: containment === 'yes' ? 'No action required' :
            containCost
              ? 'Containment retrofit — indicative €' + containCost.low.toLocaleString() + '–€' + containCost.high.toLocaleString() + ' (T3 screening)'
              : 'Assess containment options — BSRIA BG29 guidance'
  });

  // F03: Chiller Capacity Headroom
  const chillerResult = calcs.chiller_capacity.result;
  const headroom      = chillerResult ? chillerResult.headroom_pct : null;
  findings.push({
    id: 'F03',
    category: 'Plant Capacity',
    title: 'Chiller Capacity Headroom',
    status: headroom === null ? 'AMBER' : headroom >= 20 ? 'GREEN' : headroom >= 5 ? 'AMBER' : 'RED',
    current: headroom !== null
      ? chillerResult.total_kw.toLocaleString() + ' kW total capacity — ' + headroom + '% headroom'
      : 'Chiller data not provided',
    required: '≥20% headroom to accommodate density growth (EN 50600-2-3)',
    gap: headroom === null ? 'Insufficient data — chiller count/capacity not provided' :
         headroom >= 20 ? 'None — adequate headroom' :
         Math.max(0, 20 - headroom).toFixed(1) + ' percentage points below 20% threshold',
    action: headroom === null ? 'Provide chiller plant data for full capacity assessment' :
            headroom >= 20 ? 'No action required' :
            headroom >= 5 ? 'Plan chiller capacity expansion within 12–18 months' :
            'Urgent: near-capacity — density growth constrained'
  });

  // F04: F-Gas & Refrigerant Risk
  const gwp    = calcs.refrigerant_gwp.result;
  const fgas   = calcs.fgas_exposure.result;
  const refType = calcs.refrigerant_gwp.inputs.refrigerant_type;
  findings.push({
    id: 'F04',
    category: 'Regulatory',
    title: 'F-Gas & Refrigerant Risk',
    status: gwp === null ? 'AMBER' : gwp <= 7 ? 'GREEN' : gwp <= 675 ? 'AMBER' : 'RED',
    current: gwp !== null
      ? refType.toUpperCase() + ' — GWP ' + gwp.toLocaleString() +
        (fgas !== null ? ' | ' + fgas + ' tCO₂e exposure' : '')
      : 'Refrigerant type not provided',
    required: 'EU F-Gas Regulation 2024/573 — progressive phase-out of high-GWP refrigerants',
    gap: gwp === null ? 'Insufficient data — refrigerant type not identified' :
         gwp <= 7 ? 'None — low-GWP refrigerant in use' :
         gwp <= 675 ? 'Moderate GWP — monitor EU F-Gas phase-out schedule' :
         'High GWP (' + gwp.toLocaleString() + ') — subject to EU F-Gas phase-out restrictions',
    action: gwp === null ? 'Identify refrigerant types across all cooling units' :
            gwp <= 7 ? 'No action — aligned with F-Gas direction of travel' :
            gwp <= 675 ? 'Plan refrigerant transition as equipment reaches end-of-life' :
            'Assess replacement schedule — high-GWP refrigerants face progressive restriction under EU 2024/573'
  });

  // F05: Supply Temperature (ASHRAE A1 Alignment)
  const tempResult = calcs.supply_temp_assessment.result;
  const supplyTempInput = calcs.supply_temp_assessment.inputs.supply_temp_c;
  findings.push({
    id: 'F05',
    category: 'Thermal Management',
    title: 'Supply Temperature (ASHRAE A1)',
    status: tempResult === null ? 'AMBER' :
            tempResult.in_range ? 'GREEN' :
            tempResult.deviation_c !== null && tempResult.deviation_c < -5 ? 'RED' : 'AMBER',
    current: supplyTempInput && supplyTempInput !== 'not provided'
      ? 'Supply air at ' + supplyTempInput + '°C'
      : 'Supply temperature not provided',
    required: '18–27°C (ASHRAE TC 9.9 Class A1)',
    gap: tempResult === null ? 'Temperature setpoint not provided' :
         tempResult.in_range ? 'None — within ASHRAE A1 range' :
         tempResult.deviation_c < 0
           ? Math.abs(tempResult.deviation_c) + '°C below lower limit — overcooling, excess energy use'
           : tempResult.deviation_c + '°C above upper limit — thermal risk to IT equipment',
    action: tempResult === null ? 'Log supply temperature setpoints from BMS/DCIM' :
            tempResult.in_range ? 'Maintain current setpoint — verify with BMS trend data' :
            tempResult.deviation_c < 0 ? 'Raise supply temperature setpoint — directly reduces cooling energy cost' :
            'Review thermal margins — investigate IT equipment thermal thresholds'
  });

  // F06: Indicative Cooling Upgrade Investment
  const fcCost    = calcs.fc_retrofit_cost.result;
  const ctCost    = calcs.containment_cost.result;
  const totalLow  = (fcCost ? fcCost.low  : 0) + (ctCost ? ctCost.low  : 0);
  const totalHigh = (fcCost ? fcCost.high : 0) + (ctCost ? ctCost.high : 0);
  findings.push({
    id: 'F06',
    category: 'Commercial',
    title: 'Indicative Cooling Upgrade Investment',
    status: totalHigh === 0 ? 'GREEN' : totalHigh > 1000000 ? 'RED' : 'AMBER',
    current: totalHigh === 0 ? 'No cooling upgrades identified' :
             '€' + Math.round(totalLow / 1000).toLocaleString() + 'k–€' + Math.round(totalHigh / 1000).toLocaleString() + 'k indicative upgrade cost',
    required: 'Budget provision for cooling efficiency programme',
    gap: totalHigh === 0 ? 'None — cooling chain adequate' :
         '€' + Math.round(totalLow / 1000).toLocaleString() + 'k–€' + Math.round(totalHigh / 1000).toLocaleString() + 'k (T3 screening-level)',
    action: totalHigh === 0 ? 'No investment required at this time' :
            'Commission Desktop Assessment for detailed scope and costing — €10,000–€15,000'
  });

  const red_count   = findings.filter(f => f.status === 'RED').length;
  const amber_count = findings.filter(f => f.status === 'AMBER').length;
  const overall     = red_count > 0 ? 'RED' : amber_count > 0 ? 'AMBER' : 'GREEN';
  return { findings, summary: { red_count, amber_count, green_count: findings.length - red_count - amber_count, overall } };
}"""

NEW_A_END = """

/* ================================================================
   INPUT_SCHEMA — Same as v1.0 (DC-Screen aligned)
   ================================================================ */"""

# Build the full old and new strings
old_a = OLD_A
# Find the end: everything from OLD_A start to OLD_A_END
idx_start = h.find(OLD_A)
if idx_start == -1:
    print("ERROR: CALC_ENGINE start not found!")
    sys.exit(1)
idx_end = h.find(OLD_A_END, idx_start)
if idx_end == -1:
    print("ERROR: INPUT_SCHEMA separator not found!")
    sys.exit(1)

old_block_a = h[idx_start : idx_end + len(OLD_A_END)]
new_block_a = NEW_A_START + NEW_A_END

h = h[:idx_start] + new_block_a + h[idx_start + len(old_block_a):]
print(f"Patch A done: replaced {len(old_block_a)} chars with {len(new_block_a)} chars")

# ── Patch B: CALC ENGINE RUNNER section ──────────────────────────────────────
OLD_B_START = """/* ================================================================
   CALC ENGINE RUNNER — Deterministic. No AI.
   ================================================================ */
function runCalcEngine(inputs) {"""

OLD_B_END = """function deriveTrafficLight(findings) {
  if (findings.some(f => f.status === 'FAIL')) return 'RED';
  if (findings.some(f => f.status === 'FLAG')) return 'AMBER';
  return 'GREEN';
}"""

NEW_B = """/* ================================================================
   CALC ENGINE RUNNER — delegates to runCalcEngine / runFindingsEngine above
   ================================================================ */
// runCalcEngine, runFindingsEngine, buildAuditSteps, deriveTrafficLight
// are defined in the CALC ENGINE and FINDINGS ENGINE sections above.

/* ================================================================
   AUDIT TRAIL HELPERS
   ================================================================ */
function formatCalcResult(result) {
  if (result === null || result === undefined) return 'N/A';
  if (typeof result === 'boolean') return result ? 'Yes' : 'No';
  if (typeof result === 'object') {
    return Object.entries(result).map(([k, v]) => {
      const lbl = k.replace(/_/g, ' ');
      if (Array.isArray(v))      return lbl + ': ' + (v.length ? v.join(', ') : 'none');
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

idx_b_start = h.find(OLD_B_START)
if idx_b_start == -1:
    print("ERROR: CALC ENGINE RUNNER start not found!")
    sys.exit(1)
idx_b_end_start = h.find(OLD_B_END, idx_b_start)
if idx_b_end_start == -1:
    print("ERROR: old deriveTrafficLight not found!")
    sys.exit(1)
idx_b_end = idx_b_end_start + len(OLD_B_END)

old_block_b = h[idx_b_start : idx_b_end]
h = h[:idx_b_start] + NEW_B + h[idx_b_end:]
print(f"Patch B done: replaced {len(old_block_b)} chars with {len(NEW_B)} chars")

with open(DST, 'w', encoding='utf-8') as f:
    f.write(h)
print(f"Saved. Lines: {h.count(chr(10))+1}")
