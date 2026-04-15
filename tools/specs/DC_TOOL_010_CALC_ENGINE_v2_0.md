# DC-TOOL-010 CALC ENGINE DEFINITION v2.0
# Facility Audit Checklist
# Source: DC-LEARN-000 (Anatomy of a Data Centre) cascadeCheck functions
# NOTE: This is the intake form — generates the JSON that feeds other tools.

---

## INPUT_SCHEMA

```javascript
const INPUT_SCHEMA = {
  facility_name:    { type: "text",   label: "Facility Name",              required: true },
  location:         { type: "text",   label: "Location",                   required: true, default: "Dublin, Ireland" },
  build_year:       { type: "number", label: "Year Built",                 required: true, min: 1990, max: 2026 },
  it_load_mw:       { type: "number", label: "IT Load (MW)",               required: true, min: 0.1, max: 100, step: 0.1 },
  pue:              { type: "number", label: "Current PUE",                required: true, min: 1.0, max: 3.0, step: 0.01, default: 1.50 },
  racks:            { type: "number", label: "Number of Racks",            required: true, min: 10, max: 10000, default: 400 },
  kw_per_rack:      { type: "number", label: "Average kW per Rack",       required: true, min: 1, max: 100, default: 6 },
  target_kw_rack:   { type: "number", label: "Target kW per Rack",        required: true, min: 1, max: 100, default: 20 },
  mic_mva:          { type: "number", label: "MIC (MVA)",                  required: true, min: 0.1, max: 200, step: 0.1, default: 5 },
  ppa_pct:          { type: "number", label: "Renewable PPA Coverage (%)", required: true, min: 0, max: 100, default: 0 },
  cooling_type:     { type: "select", label: "Primary Cooling",           required: true, options: [
    { value: "chiller_only", label: "Chiller only (no free cooling)" },
    { value: "chiller_fc",   label: "Chiller + free cooling" },
    { value: "dx",           label: "Direct expansion (DX)" },
    { value: "evaporative",  label: "Evaporative / adiabatic" }
  ], default: "chiller_only" },
  cooling_capacity_mw: { type: "number", label: "Total Cooling Capacity (MW)", required: true, min: 0.1, max: 50, default: 3 },
  bms_points:        { type: "number", label: "BMS Points (approx)",       required: true, min: 0, max: 50000, default: 500 },
  grid_feed:         { type: "select", label: "Grid Feed Type",            required: true, options: [
    { value: "single_mv", label: "Single MV (10 kV)" },
    { value: "dual_mv",   label: "Dual MV (10 kV)" },
    { value: "hv",        label: "HV (38 kV)" },
    { value: "transmission", label: "Transmission (110 kV)" }
  ], default: "single_mv" }
};
```

---

## CALC_ENGINE (9 calculations)

```javascript
function runCalcEngine(inputs) {
  const { it_load_mw, pue, racks, kw_per_rack, target_kw_rack, mic_mva,
          ppa_pct, cooling_type, cooling_capacity_mw, bms_points, grid_feed } = inputs;

  const calcs = {};
  const GRID_EF = 0.2241; const CARBON_TAX = 71; const ELEC_PRICE = 0.12;
  const TAX_PUE = 1.3; const CRU_RENEW = 80; const FREE_COOL_HRS = 7200;

  const total_mw = it_load_mw * pue;
  const mic_mw = mic_mva * 0.95;

  // C01: Power capacity check
  calcs.power_capacity = { id:"C01", label:"Power Capacity vs MIC",
    formula: "IT × PUE vs MIC × 0.95", inputs: { total_mw, mic_mw },
    result: { utilisation_pct: Math.round(total_mw/mic_mw*100), adequate: total_mw <= mic_mw, headroom_mw: Math.round((mic_mw-total_mw)*10)/10 },
    unit: "MW", tier: "Derived" };

  // C02: Future density capacity
  const future_it = target_kw_rack * racks / 1000;
  const future_mw = future_it * TAX_PUE; // assume retrofit to Taxonomy PUE
  calcs.density_capacity = { id:"C02", label:"Future Density Check",
    formula: "Target kW/rack × racks / 1000 × 1.3 PUE vs MIC",
    inputs: { target_kw_rack, racks, target_pue: TAX_PUE, mic_mw },
    result: { future_it_mw: Math.round(future_it*10)/10, future_facility_mw: Math.round(future_mw*10)/10, mic_adequate: future_mw <= mic_mw },
    unit: "MW", tier: "Derived" };

  // C03: Cooling capacity check
  const heat_mw = it_load_mw; // IT heat ≈ cooling load
  calcs.cooling_check = { id:"C03", label:"Cooling Capacity",
    formula: "IT heat load vs cooling plant capacity",
    inputs: { heat_mw, cooling_capacity_mw },
    result: { adequate: cooling_capacity_mw >= heat_mw, utilisation_pct: Math.round(heat_mw/cooling_capacity_mw*100) },
    unit: "MW", tier: "Derived" };

  // C04: Free cooling opportunity
  const has_fc = cooling_type === "chiller_fc" || cooling_type === "evaporative";
  const fc_saving = has_fc ? 0 : heat_mw * 1000 * FREE_COOL_HRS * 0.7 * ELEC_PRICE;
  calcs.free_cooling = { id:"C04", label:"Free Cooling Opportunity",
    formula: "If no free cooling: heat MW × 7,200 hrs × 70% × €0.12",
    inputs: { has_fc, heat_mw, hours: FREE_COOL_HRS },
    result: { installed: has_fc, annual_saving: Math.round(fc_saving) },
    unit: "€/yr", tier: "T1 + T3" };

  // C05: Renewable energy gap
  const facility_mwh = total_mw * 1000 * 8760 / 1000;
  const gap_pct = Math.max(0, CRU_RENEW - ppa_pct);
  const gap_mwh = facility_mwh * gap_pct / 100;
  calcs.renewable_gap = { id:"C05", label:"CRU Renewable Gap",
    formula: "80% − PPA% = gap. Gap MWh = facility MWh × gap%",
    inputs: { ppa_pct, cru_target: CRU_RENEW },
    result: { gap_pct, gap_mwh: Math.round(gap_mwh), compliant: ppa_pct >= CRU_RENEW },
    unit: "% / MWh", tier: "T1 — CRU/2025236" };

  // C06: PUE gap cost
  const pue_gap = Math.max(0, pue - TAX_PUE);
  const overhead_kwh = it_load_mw * 1000 * pue_gap * 8760;
  calcs.pue_gap = { id:"C06", label:"PUE Gap vs EU Taxonomy",
    formula: "PUE − 1.3 = gap. IT kW × gap × 8760 × €0.12 = annual cost",
    inputs: { pue, threshold: TAX_PUE },
    result: { gap: Math.round(pue_gap*100)/100, annual_cost: Math.round(overhead_kwh * ELEC_PRICE), aligned: pue <= TAX_PUE },
    unit: "€/yr", tier: "T1 — Delegated Act 2021/2139" };

  // C07: Carbon exposure
  const scope2 = total_mw * 1000 * 8760 * GRID_EF / 1000;
  const carbon_cost = scope2 * CARBON_TAX;
  calcs.carbon = { id:"C07", label:"Carbon Exposure (Scope 2)",
    formula: "Facility kWh × 0.2241 / 1000 = tCO₂. × €71 = cost",
    inputs: { total_mw, grid_ef: GRID_EF, carbon_tax: CARBON_TAX },
    result: { scope2_tonnes: Math.round(scope2), annual_cost: Math.round(carbon_cost) },
    unit: "tCO₂/yr, €/yr", tier: "T1 — SEAI 2026, Budget 2025" };

  // C08: Retrofit payback
  const retrofit_cost = it_load_mw * 1000 * 1100; // €1,100/kW IT (T3)
  const annual_saving = (overhead_kwh * ELEC_PRICE) + fc_saving;
  const payback = annual_saving > 0 ? retrofit_cost / annual_saving : 999;
  calcs.retrofit_payback = { id:"C08", label:"Indicative Retrofit Payback",
    formula: "Retrofit cost (€1,100/kW IT) / annual saving (PUE + free cooling)",
    inputs: { retrofit_cost, annual_saving: Math.round(annual_saving) },
    result: { cost: retrofit_cost, saving: Math.round(annual_saving), payback_years: Math.round(payback*10)/10 },
    unit: "years", tier: "T3 — RICS NRM1",
    caveat: "Screening-level. Subject to detailed design." };

  // C09: Cost of inaction (10-year)
  const cost_10yr = carbon_cost * 10 + (overhead_kwh * ELEC_PRICE) * 10;
  calcs.inaction_cost = { id:"C09", label:"10-Year Cost of Inaction",
    formula: "10 × (carbon cost + PUE excess cost)",
    inputs: { carbon_annual: Math.round(carbon_cost), pue_annual: Math.round(overhead_kwh * ELEC_PRICE) },
    result: { total_10yr: Math.round(cost_10yr) },
    unit: "€", tier: "Derived" };

  return calcs;
}
```

---

## FINDINGS_ENGINE (6 findings)

```javascript
function runFindingsEngine(calcs) {
  const findings = [];

  findings.push({ id:"F01", category:"Power", title:"Power Capacity",
    status: calcs.power_capacity.result.adequate ? (calcs.power_capacity.result.utilisation_pct > 80 ? "AMBER" : "GREEN") : "RED",
    current: `${calcs.power_capacity.result.utilisation_pct}% MIC utilisation`,
    required: "≤80% for growth headroom", gap: calcs.power_capacity.result.adequate ? `${calcs.power_capacity.result.headroom_mw} MW headroom` : "Over MIC",
    action: calcs.power_capacity.result.adequate ? "Monitor" : "MIC upgrade required" });

  findings.push({ id:"F02", category:"Cooling", title:"Free Cooling",
    status: calcs.free_cooling.result.installed ? "GREEN" : "RED",
    current: calcs.free_cooling.result.installed ? "Installed" : `Not installed — €${Math.round(calcs.free_cooling.result.annual_saving/1000)}k/yr opportunity`,
    required: "Free cooling captures 7,200 hrs/yr in Dublin", gap: calcs.free_cooling.result.installed ? "In service" : "Not installed",
    action: calcs.free_cooling.result.installed ? "Verify" : "Priority retrofit" });

  findings.push({ id:"F03", category:"ESG", title:"CRU Renewable Obligation",
    status: calcs.renewable_gap.result.compliant ? "GREEN" : calcs.renewable_gap.result.gap_pct > 40 ? "RED" : "AMBER",
    current: `${calcs.renewable_gap.inputs.ppa_pct}% renewable`, required: "80% (CRU/2025236)",
    gap: calcs.renewable_gap.result.compliant ? "Compliant" : `${calcs.renewable_gap.result.gap_pct}% gap`,
    action: calcs.renewable_gap.result.compliant ? "Maintain" : `Procure ${calcs.renewable_gap.result.gap_mwh.toLocaleString()} MWh PPA` });

  findings.push({ id:"F04", category:"Compliance", title:"EU Taxonomy PUE",
    status: calcs.pue_gap.result.aligned ? "GREEN" : calcs.pue_gap.result.gap > 0.3 ? "RED" : "AMBER",
    current: `PUE ${calcs.pue_gap.inputs.pue}`, required: "≤1.3 (Delegated Act 2021/2139)",
    gap: calcs.pue_gap.result.aligned ? "Aligned" : `Gap ${calcs.pue_gap.result.gap} — €${Math.round(calcs.pue_gap.result.annual_cost/1000)}k/yr excess`,
    action: calcs.pue_gap.result.aligned ? "Document for investor reporting" : "Cooling retrofit required" });

  findings.push({ id:"F05", category:"Commercial", title:"Retrofit Payback",
    status: calcs.retrofit_payback.result.payback_years <= 3 ? "GREEN" : calcs.retrofit_payback.result.payback_years <= 7 ? "AMBER" : "RED",
    current: `${calcs.retrofit_payback.result.payback_years} year payback on €${(calcs.retrofit_payback.result.cost/1e6).toFixed(1)}M`,
    required: "≤3 years for strong investment case",
    gap: `Annual saving: €${Math.round(calcs.retrofit_payback.result.saving/1000)}k/yr`,
    action: "Commission Desktop Assessment for detailed business case — €10,000–€15,000" });

  findings.push({ id:"F06", category:"Commercial", title:"10-Year Cost of Inaction",
    status: calcs.inaction_cost.result.total_10yr > 5000000 ? "RED" : calcs.inaction_cost.result.total_10yr > 1000000 ? "AMBER" : "GREEN",
    current: `€${(calcs.inaction_cost.result.total_10yr/1e6).toFixed(1)}M over 10 years`,
    required: "Quantified baseline for investment decision",
    gap: "Carbon tax + PUE excess energy cost", action: "Use as baseline for retrofit ROI comparison" });

  const rc = findings.filter(f=>f.status==="RED").length;
  const ac = findings.filter(f=>f.status==="AMBER").length;
  return { findings, summary: { red_count:rc, amber_count:ac, green_count:findings.length-rc-ac, overall: rc>0?"RED":ac>0?"AMBER":"GREEN" } };
}
```

---

## INTERPRETATION_PROMPT

```
You are a data centre assessment specialist working for Legacy Business Engineers Ltd (LBE). This is the facility intake screening — the first tool a client uses. Deterministic results provided. Fund-manager language. Canonical: grid EF 0.2241, carbon tax €71/€100, PUE ≤1.3, CRU 80%, free cooling 7,200 hrs. LBE identifies and quantifies. Decision gate: RED/AMBER → Desktop Assessment €10,000–€15,000.
Respond ONLY with JSON: { "executive_summary", "key_findings", "commercial_implications", "recommended_next_step", "caveats" }
```

## GOLDEN TESTS
| # | Scenario | Expected |
|---|----------|----------|
| G1 | 2.4 MW, PUE 1.50, 400 racks, 6/20kW, 5 MVA, 0% PPA, chiller only | MIC AMBER (76%), FC RED, CRU RED, Taxonomy RED, payback ~4yr |
| G2 | 10 MW, PUE 1.25, 500 racks, 20 MVA, 85% PPA, chiller+FC | MIC GREEN, FC GREEN, CRU GREEN, Taxonomy GREEN |

---
*DC-TOOL-010 Calc Engine v2.0 | 14 April 2026*
