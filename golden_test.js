/**
 * Golden Test G1 — DC-TOOL-002 v2.0.0 Cooling Chain Screener
 *
 * G1: Demo inputs (Example Facility, Dublin):
 *   IT Load: 2.4 MW, PUE: 1.50
 *   has_free_cooling: 'no', has_containment: 'no'
 *   supply_temp_c: 18
 *   chiller_count: 3, chiller_kw_each: 500
 *   refrigerant_type: 'r410a', refrigerant_charge_kg: 192
 *
 * Expected:
 *   C01 cooling_load_kw = 1200 kW
 *   C02 annual_cooling_mwh = 10512 MWh/yr
 *   C03 annual_cooling_cost = €1,261,440/yr
 *   C04 free_cooling_hours = 0
 *   C05 fc_saving = 8640 MWh/yr, €1,036,800/yr
 *   C06 chiller headroom = 20% (1500 kW total, 300 kW headroom)
 *   C07 refrigerant GWP = 2088
 *   C08 F-gas = 400.9 tCO2e (192 * 2088 / 1000)
 *   C09 supply temp in_range = true (18°C in [18,27])
 *   C10 FC retrofit = €240k–€480k
 *   C11 containment = €15k–€35k
 *   F01 = RED (no FC)
 *   F02 = RED (no containment)
 *   F03 = GREEN (20% headroom exactly — check: AMBER if < 20)
 *   F04 = RED (R410A, GWP 2088)
 *   F05 = GREEN (18°C in range)
 *   F06 = AMBER (total €255k–€515k, < €1M)
 *   Overall = RED
 */

const fs = require('fs');
const src = fs.readFileSync('tools/DC-TOOL-002_v2_0_0.html', 'utf8');

// Extract script
const m = src.match(/<script[^>]+type=["']text\/babel["'][^>]*>([\s\S]*?)<\/script>/i);
if (!m) { console.error('No babel script'); process.exit(1); }

// Strip JSX and React-specific stuff so we can eval in Node
let code = m[1];
// Remove JSX / React component code (after the engines) — we only need the engine functions
// We'll manually extract just the functions we need

// Strategy: use vm with stub of CANONICAL_DATA + extract function bodies
const vm = require('vm');

const CANONICAL_DATA = {
  electricity_price: { value: 0.12, unit: '€/kWh', source: 'CRU Q4 2024', tier: 'T2' },
  free_cooling_hours: { value: 7200, unit: 'hrs/yr', source: 'Met Éireann 30yr', tier: 'T1' },
};

// Extract just the function definitions (up to the INPUT_SCHEMA line)
const engineEnd = code.indexOf('/* ================================================================\n   INPUT_SCHEMA');
if (engineEnd === -1) { console.error('Could not find INPUT_SCHEMA boundary'); process.exit(1); }
const engineCode = code.substring(0, engineEnd);

const context = vm.createContext({ CANONICAL_DATA, Math, Number, JSON, console, String, Object });
try {
  vm.runInContext(engineCode, context);
} catch(e) {
  console.error('Engine eval error:', e.message);
  process.exit(1);
}

// G1 inputs
const inp = {
  facility_name: 'Example Facility, Dublin',
  location: 'Dublin, Ireland',
  build_year: 2013,
  it_load_mw: 2.4,
  pue: 1.50,
  cooling_type: 'air_crac',
  has_free_cooling: 'no',
  has_containment: 'no',
  supply_temp_c: 18,
  chiller_count: 3,
  chiller_kw_each: 500,
  chiller_type: 'air_cooled',
  refrigerant_type: 'r410a',
  refrigerant_charge_kg: 192,
  has_water_meter: 'no',
  ppa_pct: 45,
  total_floor_m2: 1800
};

const calcs = context.runCalcEngine(inp);
const fResult = context.runFindingsEngine(calcs);

let pass = true;
function check(label, actual, expected) {
  const ok = JSON.stringify(actual) === JSON.stringify(expected);
  console.log((ok ? '✓' : '✗') + ' ' + label + ': ' + JSON.stringify(actual) + (ok ? '' : ' (expected ' + JSON.stringify(expected) + ')'));
  if (!ok) pass = false;
}
function checkApprox(label, actual, expected, tol=0.5) {
  const ok = Math.abs(actual - expected) <= tol;
  console.log((ok ? '✓' : '✗') + ' ' + label + ': ' + actual + (ok ? '' : ' (expected ~' + expected + ')'));
  if (!ok) pass = false;
}

console.log('\n=== DC-TOOL-002 v2.0.0 Golden Test G1 ===\n');

// C01
checkApprox('C01 cooling_load_kw', calcs.cooling_load_kw.result, 1200);

// C02
checkApprox('C02 annual_cooling_mwh', calcs.annual_cooling_mwh.result, 10512);

// C03
checkApprox('C03 annual_cooling_cost (€)', calcs.annual_cooling_cost.result, 1261440, 100);

// C04
check('C04 free_cooling_hours', calcs.free_cooling_hours.result, 0);

// C05
checkApprox('C05 saving_mwh', calcs.free_cooling_saving.result.saving_mwh, 8640);
checkApprox('C05 saving_eur', calcs.free_cooling_saving.result.saving_eur, 1036800, 100);

// C06
check('C06 chiller_total_kw', calcs.chiller_capacity.result.total_kw, 1500);
check('C06 headroom_pct', calcs.chiller_capacity.result.headroom_pct, 20);

// C07
check('C07 GWP r410a', calcs.refrigerant_gwp.result, 2088);

// C08
checkApprox('C08 F-gas tCO2e', calcs.fgas_exposure.result, 400.9, 0.2);

// C09
check('C09 in_range', calcs.supply_temp_assessment.result.in_range, true);
check('C09 deviation', calcs.supply_temp_assessment.result.deviation_c, 0);

// C10
check('C10 FC retrofit low', calcs.fc_retrofit_cost.result.low, 240000);
check('C10 FC retrofit high', calcs.fc_retrofit_cost.result.high, 480000);

// C11
check('C11 containment low', calcs.containment_cost.result.low, 15000);
check('C11 containment high', calcs.containment_cost.result.high, 35000);

console.log('\n--- Findings ---\n');

const findings = fResult.findings;
check('F01 status (no FC → RED)', findings[0].status, 'RED');
check('F02 status (no containment → RED)', findings[1].status, 'RED');
// C06 headroom = 20.0% exactly — threshold is >= 20 → GREEN
check('F03 status (20% headroom → GREEN)', findings[2].status, 'GREEN');
check('F04 status (R410A GWP 2088 → RED)', findings[3].status, 'RED');
check('F05 status (18°C in range → GREEN)', findings[4].status, 'GREEN');
// F06: total = 240k+15k=255k low, 480k+35k=515k high — < 1M → AMBER
check('F06 status (€515k total → AMBER)', findings[5].status, 'AMBER');

check('Overall (RED expected)', fResult.summary.overall, 'RED');
check('Red count', fResult.summary.red_count, 3);

console.log('\n' + (pass ? '=== ALL PASS ===' : '=== FAILURES DETECTED ==='));
process.exit(pass ? 0 : 1);
