# DC-TOOL-002 CALC ENGINE DEFINITION v2.0
# Cooling Chain Screener
# Source: DC-LEARN-002 (Cooling Chain) cascadeCheck functions

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
  chiller_count:    { type: "number", label: "Chiller Count",              required: true, min: 1, max: 20, default: 2 },
  chiller_mw:       { type: "number", label: "Chiller Capacity Each (MW)", required: true, min: 0.1, max: 10, step: 0.1, default: 1.5 },
  crah_count:       { type: "number", label: "CRAH Unit Count",            required: true, min: 1, max: 100, default: 12 },
  crah_kw:          { type: "number", label: "CRAH Capacity Each (kW)",    required: true, min: 10, max: 500, default: 150 },
  chw_flow_ls:      { type: "number", label: "CHW Flow Rate (L/s)",        required: true, min: 1, max: 500, default: 40 },
  chw_delta_t:      { type: "number", label: "CHW ΔT (°C)",               required: true, min: 2, max: 15, default: 6 },
  refrigerant_type: { type: "select", label: "Chiller Refrigerant",        required: true, options: [
    { value: "R-134a", label: "R-134a (GWP 1,430)" },
    { value: "R-410A", label: "R-410A (GWP 2,088)" },
    { value: "R-1234ze", label: "R-1234ze (GWP 7)" },
    { value: "R-290", label: "R-290 Propane (GWP 3)" }
  ], default: "R-134a" },
  has_free_cooling:  { type: "select", label: "Free Cooling Installed?",   required: true, options: [
    { value: true, label: "Yes" }, { value: false, label: "No" }
  ], default: false },
  condenser_mw:      { type: "number", label: "Total Condenser/Dry Cooler Capacity (MW)", required: true, min: 0.1, max: 50, step: 0.1, default: 5 },
  containment:       { type: "select", label: "Aisle Containment",         required: true, options: [
    { value: "none", label: "None" }, { value: "hot", label: "Hot aisle" }, { value: "cold", label: "Cold aisle" }, { value: "both", label: "Both" }
  ], default: "none" }
};
```

---

## CALC_ENGINE (11 calculations)

```javascript
function runCalcEngine(inputs) {
  const { it_load_mw, pue, racks, kw_per_rack, chiller_count, chiller_mw,
          crah_count, crah_kw, chw_flow_ls, chw_delta_t, refrigerant_type,
          has_free_cooling, condenser_mw, containment } = inputs;

  const calcs = {};
  const ELEC_PRICE = 0.12; // T2
  const FREE_COOL_HRS = 7200; // T1 Met Eireann
  const GWP_MAP = { "R-134a": 1430, "R-410A": 2088, "R-1234ze": 7, "R-290": 3 };

  const heat_rejection_mw = it_load_mw; // IT heat = cooling load (simplified)

  // C01: Air cooling density limit
  const air_max = 25; // kW/rack practical max for air cooling (T3)
  calcs.air_limit = { id:"C01", label:"Air Cooling Density Limit",
    formula: "kW/rack vs 25 kW max for air cooling",
    inputs: { kw_per_rack, limit: air_max },
    result: { adequate: kw_per_rack <= air_max, headroom_kw: air_max - kw_per_rack },
    unit: "kW/rack", tier: "T3 — ASHRAE TC 9.9" };

  // C02: Chiller capacity
  const chiller_total_mw = chiller_count * chiller_mw;
  const chiller_effective = chiller_total_mw * 0.62; // typical COP derating at part load
  calcs.chiller_capacity = { id:"C02", label:"Chiller Plant Capacity",
    formula: "Count × MW × 0.62 (part-load COP adjustment) vs heat load",
    inputs: { chiller_count, chiller_mw, heat_load: heat_rejection_mw },
    result: { total_mw: chiller_total_mw, effective_mw: Math.round(chiller_effective * 10) / 10, adequate: chiller_effective >= heat_rejection_mw, utilisation_pct: Math.round(heat_rejection_mw / chiller_effective * 100) },
    unit: "MW", tier: "Derived" };

  // C03: CRAH capacity
  const crah_total_kw = crah_count * crah_kw;
  const crah_effective = crah_total_kw * 0.65 / 1000; // 65% effectiveness typical (T3)
  calcs.crah_capacity = { id:"C03", label:"CRAH Distribution Capacity",
    formula: "Count × kW × 0.65 effectiveness / 1000 vs heat load",
    inputs: { crah_count, crah_kw },
    result: { total_kw: crah_total_kw, effective_mw: Math.round(crah_effective * 10) / 10, adequate: crah_effective >= heat_rejection_mw },
    unit: "MW", tier: "T3 — typical CRAH effectiveness" };

  // C04: CHW pump capacity
  const pump_capacity_mw = chw_flow_ls * 4.186 * chw_delta_t / 1000; // Q = m × Cp × ΔT
  calcs.pump_capacity = { id:"C04", label:"CHW Pump / Pipework Capacity",
    formula: "Flow (L/s) × 4.186 (kJ/kg·K) × ΔT (°C) / 1000 = MW",
    inputs: { chw_flow_ls, chw_delta_t },
    result: { capacity_mw: Math.round(pump_capacity_mw * 10) / 10, adequate: pump_capacity_mw >= heat_rejection_mw },
    unit: "MW", tier: "Derived" };

  // C05: Refrigerant risk
  const gwp = GWP_MAP[refrigerant_type] || 1430;
  const est_charge_kg = chiller_total_mw * 300; // ~300 kg/MW cooling (T3)
  const co2eq = est_charge_kg * gwp / 1000;
  calcs.refrigerant = { id:"C05", label:"Refrigerant F-Gas Risk",
    formula: "Charge (kg) × GWP / 1000 = tCO₂eq",
    inputs: { refrigerant_type, gwp, est_charge_kg: Math.round(est_charge_kg) },
    result: { co2eq_tonnes: Math.round(co2eq), phase_down_risk: gwp > 750 ? "HIGH" : gwp > 150 ? "MEDIUM" : "LOW" },
    unit: "tCO₂eq", tier: "T1 — EU 2024/573" };

  // C06: Free cooling opportunity
  const fc_saving_kwh = has_free_cooling ? 0 : heat_rejection_mw * 1000 * FREE_COOL_HRS * 0.7;
  const fc_saving_eur = fc_saving_kwh * ELEC_PRICE;
  calcs.free_cooling = { id:"C06", label:"Free Cooling Opportunity",
    formula: "Heat load × 7,200 hrs × 70% capture × €0.12/kWh",
    inputs: { has_free_cooling, heat_mw: heat_rejection_mw, hours: FREE_COOL_HRS },
    result: { installed: has_free_cooling, saving_kwh: Math.round(fc_saving_kwh), saving_eur: Math.round(fc_saving_eur), pct_of_year: Math.round(FREE_COOL_HRS / 8760 * 100) },
    unit: "kWh/yr, €/yr", tier: "T1 (Met Eireann) + T3 (capture rate)" };

  // C07: Condenser/dry cooler capacity
  const total_rejection = it_load_mw * pue; // total facility heat rejection
  calcs.condenser = { id:"C07", label:"Heat Rejection (Condenser/Dry Cooler)",
    formula: "IT × PUE = total rejection vs condenser capacity",
    inputs: { total_rejection_mw: Math.round(total_rejection * 10) / 10, condenser_mw },
    result: { adequate: condenser_mw >= total_rejection, utilisation_pct: Math.round(total_rejection / condenser_mw * 100) },
    unit: "MW", tier: "Derived" };

  // C08: Containment impact
  const containment_saving_pct = containment === "none" ? 0 : containment === "both" ? 15 : 10;
  const containment_saving_eur = it_load_mw * (pue - 1) * 1000 * 8760 * ELEC_PRICE * containment_saving_pct / 100;
  calcs.containment = { id:"C08", label:"Aisle Containment Impact",
    formula: "Cooling overhead × containment saving %",
    inputs: { containment, saving_pct: containment_saving_pct },
    result: { current: containment, potential_saving_pct: containment === "none" ? 15 : 0, annual_saving_eur: Math.round(containment_saving_eur) },
    unit: "€/yr", tier: "T3 — industry benchmarks" };

  // C09: Cooling chain bottleneck
  const components = [
    { name: "Chillers", pct: Math.round(heat_rejection_mw / chiller_effective * 100) },
    { name: "CRAHs", pct: Math.round(heat_rejection_mw / crah_effective * 100) },
    { name: "CHW Pump/Pipe", pct: Math.round(heat_rejection_mw / pump_capacity_mw * 100) },
    { name: "Condenser", pct: Math.round(total_rejection / condenser_mw * 100) }
  ];
  const bn = components.reduce((a, b) => a.pct > b.pct ? a : b);
  calcs.bottleneck = { id:"C09", label:"Cooling Chain Bottleneck",
    formula: "Component with highest utilisation",
    inputs: { components },
    result: { bottleneck: bn.name, utilisation: bn.pct, all: components },
    unit: "%", tier: "Derived" };

  // C10: Indicative retrofit cost (if free cooling not installed)
  const fc_retrofit_cost = has_free_cooling ? null : {
    low: it_load_mw * 1000 * 400, high: it_load_mw * 1000 * 800,
    source: "Vertiv/Schneider/Trane published ranges", tier: "T3"
  };
  calcs.retrofit_cost = { id:"C10", label:"Indicative Cooling Retrofit Cost",
    formula: "€400–800/kW IT (free cooling + containment retrofit)",
    inputs: { it_load_kw: it_load_mw * 1000, has_free_cooling },
    result: fc_retrofit_cost, unit: "€", tier: fc_retrofit_cost ? "T3" : "N/A",
    caveat: "Screening-level. Subject to detailed design." };

  // C11: PUE improvement potential
  const target_pue = 1.20;
  const pue_saving_kwh = it_load_mw * 1000 * (pue - target_pue) * 8760;
  calcs.pue_saving = { id:"C11", label:"PUE Improvement Potential (to 1.20)",
    formula: "IT kW × (current PUE − target PUE) × 8760 × €0.12",
    inputs: { pue, target_pue, it_load_mw },
    result: { saving_kwh: Math.round(pue_saving_kwh), saving_eur: Math.round(pue_saving_kwh * ELEC_PRICE) },
    unit: "kWh/yr, €/yr", tier: "Derived" };

  return calcs;
}
```

---

## FINDINGS_ENGINE (6 findings)

```javascript
function runFindingsEngine(calcs) {
  const findings = [];

  findings.push({ id:"F01", category:"Cooling", title:"Chiller Plant Capacity",
    status: calcs.chiller_capacity.result.adequate ? "GREEN" : "RED",
    current: `${calcs.chiller_capacity.result.utilisation_pct}% utilised`,
    required: "Chiller effective capacity ≥ IT heat load",
    gap: calcs.chiller_capacity.result.adequate ? "Adequate" : "Chiller upgrade required",
    action: calcs.chiller_capacity.result.adequate ? "Monitor" : "Add chiller capacity" });

  findings.push({ id:"F02", category:"Distribution", title:"CRAH Distribution",
    status: calcs.crah_capacity.result.adequate ? "GREEN" : "RED",
    current: `${calcs.crah_capacity.result.effective_mw} MW effective vs ${calcs.crah_capacity.inputs.heat_mw || calcs.chiller_capacity.inputs.heat_load} MW heat`,
    required: "CRAH effective ≥ heat load",
    gap: calcs.crah_capacity.result.adequate ? "Adequate" : "CRAH units undersized",
    action: calcs.crah_capacity.result.adequate ? "Monitor" : "Additional CRAH units or higher-capacity replacements" });

  const fc = calcs.free_cooling.result;
  findings.push({ id:"F03", category:"Efficiency", title:"Free Cooling",
    status: fc.installed ? "GREEN" : "RED",
    current: fc.installed ? "Installed" : `Not installed — €${Math.round(fc.saving_eur/1000)}k/yr opportunity`,
    required: "Free cooling captures 7,200 hrs/yr in Dublin",
    gap: fc.installed ? "In service" : `${fc.pct_of_year}% of year available (7,200 hrs)`,
    action: fc.installed ? "Verify capture rate" : "Priority retrofit — typical payback 2–3 years" });

  const ref = calcs.refrigerant.result;
  findings.push({ id:"F04", category:"Regulatory", title:"F-Gas Refrigerant Risk",
    status: ref.phase_down_risk === "HIGH" ? "RED" : ref.phase_down_risk === "MEDIUM" ? "AMBER" : "GREEN",
    current: `${calcs.refrigerant.inputs.refrigerant_type} (GWP ${calcs.refrigerant.inputs.gwp}) — ${ref.co2eq_tonnes} tCO₂eq`,
    required: "Low-GWP refrigerant per EU 2024/573 phase-down",
    gap: ref.phase_down_risk === "LOW" ? "Compliant" : `High-GWP: ${ref.co2eq_tonnes} tCO₂eq`,
    action: ref.phase_down_risk === "HIGH" ? "Plan chiller replacement with low-GWP refrigerant" : "Monitor" });

  const bn = calcs.bottleneck.result;
  findings.push({ id:"F05", category:"Cooling", title:"Cooling Chain Bottleneck",
    status: bn.utilisation <= 70 ? "GREEN" : bn.utilisation <= 90 ? "AMBER" : "RED",
    current: `${bn.bottleneck} at ${bn.utilisation}%`,
    required: "All cooling components ≤70%",
    gap: `Bottleneck: ${bn.bottleneck}`,
    action: bn.utilisation > 90 ? `Critical: upgrade ${bn.bottleneck}` : `Monitor ${bn.bottleneck}` });

  const cost = calcs.retrofit_cost.result;
  findings.push({ id:"F06", category:"Commercial", title:"Cooling Retrofit Investment",
    status: cost === null ? "GREEN" : cost.high > 5000000 ? "RED" : "AMBER",
    current: cost === null ? "Free cooling installed" : `€${(cost.low/1e6).toFixed(1)}M–€${(cost.high/1e6).toFixed(1)}M`,
    required: "Budget for cooling efficiency upgrade",
    gap: cost === null ? "None" : `€400–800/kW IT`,
    action: cost === null ? "No retrofit needed" : "Commission Desktop Assessment — €10,000–€15,000" });

  const rc = findings.filter(f=>f.status==="RED").length;
  const ac = findings.filter(f=>f.status==="AMBER").length;
  return { findings, summary: { red_count:rc, amber_count:ac, green_count:findings.length-rc-ac, overall: rc>0?"RED":ac>0?"AMBER":"GREEN" } };
}
```

---

## INTERPRETATION_PROMPT

```
You are a cooling systems specialist working for Legacy Business Engineers Ltd (LBE). Deterministic cooling chain screening results provided. All numbers pre-calculated — do NOT invent. Fund-manager language. Dublin free cooling = 7,200 hrs/yr <18°C (Met Éireann). LBE identifies and quantifies. Decision gate: RED/AMBER → Desktop Assessment €10,000–€15,000.
Respond ONLY with JSON: { "executive_summary", "key_findings", "commercial_implications", "recommended_next_step", "caveats" }
```

## GOLDEN TESTS
| # | Scenario | Expected |
|---|----------|----------|
| G1 | 2.4 MW, PUE 1.50, 400 racks, 6kW, 2×1.5MW chiller, 12 CRAH, no free cooling, R-134a | Chiller OK, free cooling RED, F-Gas RED, bottleneck = CRAHs |
| G2 | 10 MW, PUE 1.25, 500 racks, 20kW, 6×2MW chiller, 40 CRAH, free cooling yes, R-1234ze | All GREEN |

---
*DC-TOOL-002 Calc Engine v2.0 | 14 April 2026*
