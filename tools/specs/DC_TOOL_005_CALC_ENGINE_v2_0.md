# DC-TOOL-005 CALC ENGINE DEFINITION v2.0
# UPS Adequacy Tool
# Source: DC-LEARN-005 (Backup Power) cascadeCheck functions
# Architecture: LLM never calculates. Numbers are JavaScript. Narrative is AI.

---

## INPUT_SCHEMA

```javascript
const INPUT_SCHEMA = {
  facility_name:    { type: "text",   label: "Facility Name",             required: true },
  location:         { type: "text",   label: "Location",                  required: true, default: "Dublin, Ireland" },
  build_year:       { type: "number", label: "Year Built",                required: true, min: 1990, max: 2026 },
  it_load_mw:       { type: "number", label: "IT Load (MW)",              required: true, min: 0.1, max: 100, step: 0.1 },
  pue:              { type: "number", label: "Current PUE",               required: true, min: 1.0, max: 3.0, step: 0.01, default: 1.50 },
  racks:            { type: "number", label: "Number of Racks",           required: true, min: 10, max: 10000, default: 400 },
  // Generator fleet
  gen_count:        { type: "number", label: "Generator Count",           required: true, min: 0, max: 50, default: 4 },
  gen_rating_mw:    { type: "number", label: "Generator Rating Each (MW)", required: true, min: 0.5, max: 5, step: 0.1, default: 2.5 },
  gen_redundancy:   { type: "select", label: "Generator Redundancy",      required: true, options: [
    { value: "N",     label: "N" },
    { value: "N+1",   label: "N+1" },
    { value: "2N+1",  label: "2(N+1)" }
  ], default: "N+1" },
  // UPS
  ups_rating_mva:   { type: "number", label: "Total UPS Rating (MVA)",    required: true, min: 0.1, max: 50, step: 0.1, default: 3.6 },
  ups_efficiency:   { type: "number", label: "UPS Efficiency (%)",        required: true, min: 85, max: 99, default: 96 },
  ups_bridge_min:   { type: "number", label: "UPS Bridge Time (minutes)", required: true, min: 1, max: 30, default: 10 },
  // Fuel
  fuel_type:        { type: "select", label: "Fuel Type",                 required: true, options: [
    { value: "diesel", label: "Diesel" },
    { value: "HVO",    label: "HVO (Hydrotreated Vegetable Oil)" },
    { value: "gas",    label: "Natural Gas" }
  ], default: "diesel" },
  fuel_storage_l:   { type: "number", label: "Fuel Storage (litres)",     required: true, min: 0, max: 1000000, default: 175000 },
  test_hours_yr:    { type: "number", label: "Annual Generator Test Hours", required: true, min: 0, max: 500, default: 200 },
  // BESS
  bess_installed:   { type: "select", label: "BESS Installed?",          required: true, options: [
    { value: true,  label: "Yes" },
    { value: false, label: "No" }
  ], default: false },
  bess_mw:          { type: "number", label: "BESS Capacity (MW)",       required: false, min: 0, max: 100, default: 0 }
};
```

---

## CALC_ENGINE (14 calculations)

```javascript
function runCalcEngine(inputs) {
  const { it_load_mw, pue, racks, gen_count, gen_rating_mw, gen_redundancy,
          ups_rating_mva, ups_efficiency, ups_bridge_min, fuel_type,
          fuel_storage_l, test_hours_yr, bess_installed, bess_mw } = inputs;

  const calcs = {};

  // Constants (T1/T2 sourced)
  const CARBON_TAX = 71;        // €/tCO₂ — Budget 2025 (T1)
  const CARBON_TAX_2030 = 100;  // €/tCO₂ — Finance Act (T1)
  const ELEC_PRICE = 0.12;      // €/kWh — CRU Q4 2024 (T2)
  const EPA_THRESHOLD = 50;     // MWth — EPA IE Licence (T1)
  const DIESEL_CO2_KG_L = 2.68; // kgCO₂/L — SEAI (T1)
  const DIESEL_BURN_KWH = 0.27; // L/kWh output — typical gen set (T3)
  const GEN_EFFICIENCY = 0.40;  // 40% electrical efficiency (T3)
  const CRM_PRICE = 149960;     // €/MW/yr — SEMO PCAR2829T-4 (T1)
  const GEN_SYNC_TIME = 25;     // seconds — typical (T3)

  // --- C01: Facility load ---
  const total_mw = it_load_mw * pue;
  calcs.facility_load = {
    id: "C01", label: "Total Facility Load",
    formula: "IT Load × PUE",
    inputs: { it_load_mw, pue },
    result: total_mw, unit: "MW", tier: "Derived"
  };

  // --- C02: Generator fleet capacity ---
  const gen_fleet_mw = gen_count * gen_rating_mw;
  const gen_utilisation = total_mw / gen_fleet_mw * 100;
  calcs.gen_capacity = {
    id: "C02", label: "Generator Fleet Capacity",
    formula: "Count × Rating. Utilisation = Facility Load / Fleet",
    inputs: { gen_count, gen_rating_mw, total_mw },
    result: { fleet_mw: gen_fleet_mw, utilisation_pct: Math.round(gen_utilisation) },
    unit: "MW / %", tier: "Derived"
  };

  // --- C03: Generator adequacy (80% loading limit) ---
  const gen_adequate = total_mw <= gen_fleet_mw * 0.8;
  calcs.gen_adequacy = {
    id: "C03", label: "Generator Adequacy (80% Loading Limit)",
    formula: "Facility Load ≤ Fleet × 0.8",
    inputs: { total_mw, gen_fleet_mw, limit: gen_fleet_mw * 0.8 },
    result: gen_adequate, unit: "boolean", tier: "Derived",
    detail: `${total_mw.toFixed(1)} MW vs ${(gen_fleet_mw * 0.8).toFixed(1)} MW (80% of ${gen_fleet_mw} MW)`
  };

  // --- C04: EPA thermal threshold ---
  const thermal_mw = gen_fleet_mw / GEN_EFFICIENCY;
  calcs.epa_thermal = {
    id: "C04", label: "EPA Thermal Input",
    formula: "Generator Fleet / Efficiency = Thermal Input",
    inputs: { gen_fleet_mw, efficiency: GEN_EFFICIENCY },
    result: { thermal_mw, threshold: EPA_THRESHOLD, exceeds: thermal_mw > EPA_THRESHOLD },
    unit: "MWth", tier: "Derived",
    detail: `${gen_fleet_mw} MW ÷ ${GEN_EFFICIENCY} = ${thermal_mw.toFixed(1)} MWth vs ${EPA_THRESHOLD} MWth EPA`
  };

  // --- C05: Annual diesel consumption & CO₂ ---
  const fuel_litres_yr = it_load_mw * pue * 1000 * DIESEL_BURN_KWH * test_hours_yr;
  const co2_tonnes_yr = fuel_litres_yr * DIESEL_CO2_KG_L / 1000;
  const carbon_tax_current = co2_tonnes_yr * CARBON_TAX;
  const carbon_tax_2030 = co2_tonnes_yr * CARBON_TAX_2030;
  calcs.diesel_emissions = {
    id: "C05", label: "Annual Generator Emissions (Testing)",
    formula: "IT×PUE×1000×0.27 L/kWh×test_hrs = litres. ×2.68 kgCO₂/L = tonnes",
    inputs: { it_load_mw, pue, test_hours_yr, burn_rate: DIESEL_BURN_KWH, co2_factor: DIESEL_CO2_KG_L },
    result: {
      litres_yr: Math.round(fuel_litres_yr),
      co2_tonnes: Math.round(co2_tonnes_yr),
      tax_current: Math.round(carbon_tax_current),
      tax_2030: Math.round(carbon_tax_2030)
    },
    unit: "L/yr, tCO₂/yr, €/yr",
    tier: "T1 (SEAI, Budget 2025) + T3 (burn rate)"
  };

  // --- C06: UPS loss ---
  const ups_loss_pct = (100 - ups_efficiency) / 100;
  const ups_loss_kw = it_load_mw * 1000 * ups_loss_pct;
  const ups_loss_cost = ups_loss_kw * 8760 * ELEC_PRICE;
  calcs.ups_loss = {
    id: "C06", label: "UPS Conversion Loss",
    formula: "IT Load × (1 − efficiency) = loss. ×8760×€0.12 = cost",
    inputs: { it_load_mw, ups_efficiency, elec_price: ELEC_PRICE },
    result: { loss_kw: Math.round(ups_loss_kw), annual_cost: Math.round(ups_loss_cost) },
    unit: "kW / €/yr", tier: "Derived"
  };

  // --- C07: UPS capacity adequacy ---
  const ups_mw = ups_rating_mva * 0.9; // PF 0.9
  const ups_adequate = total_mw <= ups_mw;
  calcs.ups_capacity = {
    id: "C07", label: "UPS Capacity vs Facility Load",
    formula: "UPS MVA × 0.9 PF vs Facility Load",
    inputs: { ups_rating_mva, pf: 0.9, total_mw },
    result: { ups_mw: ups_mw.toFixed(1), gap_mw: (total_mw - ups_mw).toFixed(1), adequate: ups_adequate },
    unit: "MW", tier: "Derived"
  };

  // --- C08: Transfer time margin ---
  const bridge_seconds = ups_bridge_min * 60;
  const margin_seconds = bridge_seconds - GEN_SYNC_TIME;
  calcs.transfer_margin = {
    id: "C08", label: "Generator Transfer Time Margin",
    formula: "UPS bridge (seconds) − Generator sync time",
    inputs: { ups_bridge_min, gen_sync_seconds: GEN_SYNC_TIME },
    result: { bridge_s: bridge_seconds, sync_s: GEN_SYNC_TIME, margin_s: margin_seconds },
    unit: "seconds", tier: "T3 (typical sync time)"
  };

  // --- C09: Fuel endurance ---
  const burn_rate_full = total_mw * 1000 * DIESEL_BURN_KWH; // L/hr at full facility load
  const endurance_hrs = fuel_storage_l / burn_rate_full;
  calcs.fuel_endurance = {
    id: "C09", label: "Fuel Endurance at Full Load",
    formula: "Storage (L) ÷ burn rate (L/hr)",
    inputs: { fuel_storage_l, burn_rate_l_hr: Math.round(burn_rate_full), total_mw },
    result: { endurance_hrs: Math.round(endurance_hrs * 10) / 10 },
    unit: "hours", tier: "T3 (burn rate)"
  };

  // --- C10: 2(N+1) generator fleet sizing ---
  const n_gens = Math.ceil(total_mw / gen_rating_mw);
  const fleet_2n1 = 2 * (n_gens + 1);
  const fleet_cost = fleet_2n1 * gen_rating_mw * 400000; // €400K/MW — Caterpillar/Cummins (T3)
  calcs.gen_fleet_2n1 = {
    id: "C10", label: "2(N+1) Generator Fleet Sizing",
    formula: "N = ceil(Facility/Rating). 2(N+1) count. Cost = count × MW × €400K/MW",
    inputs: { total_mw, gen_rating_mw, cost_per_mw: 400000 },
    result: { n_required: n_gens, fleet_2n1: fleet_2n1, cost: fleet_cost },
    unit: "generators / €",
    tier: "T3 — Caterpillar/Cummins/MTU published ranges"
  };

  // --- C11: BESS sizing (if not installed) ---
  const bess_target = Math.max(2, Math.round(it_load_mw * 0.5));
  const ds3_revenue = bess_target * 0.7 * 20 * 8760; // conservative DS3 estimate
  calcs.bess_opportunity = {
    id: "C11", label: "BESS Opportunity Assessment",
    formula: "Target = max(2, IT×0.5). DS3 revenue = MW × 0.7 utilisation × €20/MWh × 8760",
    inputs: { it_load_mw, bess_installed, bess_mw },
    result: {
      recommended_mw: bess_target,
      current_mw: bess_installed ? bess_mw : 0,
      gap_mw: bess_target - (bess_installed ? bess_mw : 0),
      ds3_revenue_yr: Math.round(ds3_revenue)
    },
    unit: "MW / €/yr",
    tier: "T3 — BNEF H2 2025, EirGrid DS3 rate estimate"
  };

  // --- C12: CRM revenue potential ---
  const gen_licence_threshold = 10; // MW
  const crm_eligible = gen_fleet_mw > gen_licence_threshold;
  const crm_revenue = crm_eligible ? gen_fleet_mw * CRM_PRICE : 0;
  calcs.crm_revenue = {
    id: "C12", label: "CRM Revenue Potential",
    formula: "If fleet > 10 MW → fleet × €149,960/MW/yr",
    inputs: { gen_fleet_mw, threshold: gen_licence_threshold, crm_price: CRM_PRICE },
    result: { eligible: crm_eligible, annual_revenue: crm_revenue },
    unit: "€/yr",
    tier: "T1 — SEMO PCAR2829T-4"
  };

  // --- C13: Total backup infrastructure cost ---
  const ups_cost = total_mw * 1000 * 120; // €120/kW — Schneider/ABB/Eaton (T3)
  const batt_cost = total_mw * 1000 * ups_bridge_min / 60 / 0.8 * 250; // €250/kWh battery (T3)
  const total_backup = fleet_cost + ups_cost + batt_cost;
  calcs.total_backup_cost = {
    id: "C13", label: "Total Backup Infrastructure Cost (2(N+1))",
    formula: "Generators + UPS + Battery",
    inputs: { gen_cost: fleet_cost, ups_cost, batt_cost },
    result: { gen: fleet_cost, ups: ups_cost, battery: batt_cost, total: total_backup },
    unit: "€",
    tier: "T3 — Schneider/ABB/Eaton/Caterpillar published ranges",
    caveat: "Screening-level. Subject to detailed design and tender."
  };

  // --- C14: HVO transition savings ---
  const hvo_co2_reduction = 0.90; // 90% reduction vs diesel — ISCC-certified (T2)
  const hvo_saved_tonnes = co2_tonnes_yr * hvo_co2_reduction;
  const hvo_saved_tax = hvo_saved_tonnes * CARBON_TAX;
  calcs.hvo_transition = {
    id: "C14", label: "HVO Fuel Transition Impact",
    formula: "Diesel CO₂ × 90% reduction × carbon tax",
    inputs: { diesel_co2: Math.round(co2_tonnes_yr), reduction: hvo_co2_reduction, carbon_tax: CARBON_TAX },
    result: { saved_tonnes: Math.round(hvo_saved_tonnes), saved_tax: Math.round(hvo_saved_tax) },
    unit: "tCO₂/yr, €/yr",
    tier: "T2 — ISCC-certified HVO lifecycle"
  };

  return calcs;
}
```

---

## FINDINGS_ENGINE (7 findings)

```javascript
function runFindingsEngine(calcs) {
  const findings = [];

  // F1: Generator adequacy
  findings.push({
    id: "F01", category: "Power", title: "Generator Fleet Adequacy",
    status: calcs.gen_adequacy.result ? "GREEN" : "RED",
    current: `${calcs.gen_capacity.result.fleet_mw} MW fleet (${calcs.gen_capacity.result.utilisation_pct}% loaded)`,
    required: `≤80% loading (${(calcs.gen_capacity.result.fleet_mw * 0.8).toFixed(1)} MW usable)`,
    gap: calcs.gen_adequacy.result ? "None" : `${calcs.gen_adequacy.inputs.total_mw.toFixed(1)} MW exceeds 80% limit`,
    action: calcs.gen_adequacy.result ? "Adequate — no action" : "Generator fleet upgrade required"
  });

  // F2: EPA licence trigger
  const epa = calcs.epa_thermal.result;
  findings.push({
    id: "F02", category: "Regulatory", title: "EPA IE Licence Threshold",
    status: epa.exceeds ? "RED" : epa.thermal_mw > 40 ? "AMBER" : "GREEN",
    current: `${epa.thermal_mw.toFixed(1)} MWth total thermal input`,
    required: "≤50 MWth (EPA Industrial Emissions threshold)",
    gap: epa.exceeds ? `${(epa.thermal_mw - 50).toFixed(1)} MWth above threshold` : "Below threshold",
    action: epa.exceeds ? "EPA IE Licence application required" :
            epa.thermal_mw > 40 ? "Approaching threshold — monitor with any fleet expansion" : "No action"
  });

  // F3: UPS capacity
  const ups = calcs.ups_capacity.result;
  findings.push({
    id: "F03", category: "Power", title: "UPS Capacity",
    status: ups.adequate ? "GREEN" : "RED",
    current: `${ups.ups_mw} MW UPS capacity (at 0.9 PF)`,
    required: `${calcs.facility_load.result.toFixed(1)} MW facility load`,
    gap: ups.adequate ? "None" : `${ups.gap_mw} MW shortfall`,
    action: ups.adequate ? "Adequate" : "UPS upgrade or additional modules required"
  });

  // F4: Transfer time margin
  const tm = calcs.transfer_margin.result;
  findings.push({
    id: "F04", category: "Power", title: "Generator Transfer Margin",
    status: tm.margin_s > 300 ? "GREEN" : tm.margin_s > 60 ? "AMBER" : "RED",
    current: `${tm.bridge_s}s bridge vs ${tm.sync_s}s sync = ${tm.margin_s}s margin`,
    required: ">300s margin recommended for operational comfort",
    gap: tm.margin_s > 300 ? "Adequate" : `${300 - tm.margin_s}s below recommended margin`,
    action: tm.margin_s > 300 ? "Adequate" : "Review UPS battery health and generator start reliability"
  });

  // F5: Fuel endurance
  const fe = calcs.fuel_endurance.result;
  findings.push({
    id: "F05", category: "Operations", title: "Fuel Endurance",
    status: fe.endurance_hrs >= 72 ? "GREEN" : fe.endurance_hrs >= 24 ? "AMBER" : "RED",
    current: `${fe.endurance_hrs} hours at full load`,
    required: "≥72 hours recommended (extended grid outage — Storm Éowyn precedent)",
    gap: fe.endurance_hrs >= 72 ? "Adequate" : `${(72 - fe.endurance_hrs).toFixed(0)} hours below 72-hour target`,
    action: fe.endurance_hrs >= 72 ? "Adequate" : "Increase fuel storage or establish priority refuelling contract"
  });

  // F6: Carbon tax exposure
  const emissions = calcs.diesel_emissions.result;
  findings.push({
    id: "F06", category: "Commercial", title: "Generator Carbon Tax Exposure",
    status: emissions.tax_2030 > 100000 ? "RED" : emissions.tax_2030 > 25000 ? "AMBER" : "GREEN",
    current: `€${emissions.tax_current.toLocaleString()}/yr at €71/tCO₂`,
    required: `€${emissions.tax_2030.toLocaleString()}/yr at €100/tCO₂ (2030)`,
    gap: `${emissions.co2_tonnes} tCO₂/yr from generator testing`,
    action: emissions.co2_tonnes > 50 ? "Evaluate HVO transition to reduce Scope 1 by ~90%" :
            "Moderate exposure — monitor carbon tax trajectory"
  });

  // F7: BESS opportunity
  const bess = calcs.bess_opportunity.result;
  findings.push({
    id: "F07", category: "Commercial", title: "BESS Revenue Opportunity",
    status: bess.gap_mw > 0 ? "AMBER" : "GREEN",
    current: `${bess.current_mw} MW installed`,
    required: `${bess.recommended_mw} MW recommended (DS3 eligible)`,
    gap: bess.gap_mw > 0 ? `${bess.gap_mw} MW BESS gap` : "Adequate",
    action: bess.gap_mw > 0 ? `Install ${bess.gap_mw} MW BESS — indicative DS3 revenue €${Math.round(bess.ds3_revenue_yr/1000)}k/yr` :
            "BESS adequate — verify DS3 contract terms"
  });

  const red_count = findings.filter(f => f.status === "RED").length;
  const amber_count = findings.filter(f => f.status === "AMBER").length;
  const overall = red_count > 0 ? "RED" : amber_count > 0 ? "AMBER" : "GREEN";

  return { findings, summary: { red_count, amber_count, green_count: findings.length - red_count - amber_count, overall } };
}
```

---

## INTERPRETATION_PROMPT

```
You are a backup power and UPS specialist working for Legacy Business Engineers Ltd (LBE), an independent technical advisory firm.

You have received the results of a deterministic UPS and backup power screening. All numbers have been calculated by JavaScript — you MUST NOT recalculate or invent any numbers. Your job is to write a narrative interpretation of the pre-calculated results.

RULES:
1. Every number you mention MUST come from the calculations or findings provided. Do not invent.
2. Use fund-manager language — what is the risk, what does it cost, does the investment thesis work.
3. Reference Storm Éowyn (72-hour grid outage) as the benchmark for fuel endurance.
4. All cost figures are screening-level estimates subject to detailed design and tender.
5. Decision gate: if overall RED or AMBER → recommend Desktop Assessment (€10,000–€15,000).
6. LBE identifies and quantifies — never suggest LBE will design or deliver solutions.
7. Carbon tax: €71/tCO₂ current (Budget 2025), €100/tCO₂ by 2030 (Finance Act).
8. CRM T-4: €149,960/MW/yr (SEMO PCAR2829T-4).

Respond ONLY with a JSON object:
{
  "executive_summary": "3 sentences. Risk, cost, investment thesis impact.",
  "key_findings": ["Finding narrative for each finding"],
  "commercial_implications": "2-3 sentences for the fund manager.",
  "recommended_next_step": "One clear recommendation with indicative cost.",
  "caveats": "Standard screening-level caveat."
}
```

---

## GOLDEN TESTS

| # | Scenario | Key Inputs | Expected Results |
|---|----------|-----------|-----------------|
| G1 | Clonshaugh baseline | 2.4 MW IT, PUE 1.50, 4×2.5MW gen, 3.6 MVA UPS, 96%, 10min bridge, diesel, 175kL, 200 test hrs, no BESS | Gen adequate (3.6<8.0), UPS adequate (3.24>3.6), endurance ~180hrs, EPA 25 MWth OK |
| G2 | Overloaded small DC | 5 MW IT, PUE 1.60, 2×2.5MW gen, 3.0 MVA UPS, 94%, 5min bridge, diesel, 10kL | Gen RED (8.0>4.0), UPS RED (2.7<8.0), endurance RED (~5hrs) |
| G3 | Large hyperscale | 20 MW IT, PUE 1.25, 12×2.5MW gen, 30 MVA UPS, 97%, 15min bridge, HVO, 500kL, 200 test hrs, 10MW BESS | Gen adequate, UPS adequate, EPA 75 MWth RED, CRM €4.5M/yr |

---

*DC-TOOL-005 Calc Engine Definition v2.0 | 14 April 2026*
*Source: DC-LEARN-005 cascadeCheck functions (9 checks)*
*Architecture: deterministic JS → rule-based findings → AI narrative only*
