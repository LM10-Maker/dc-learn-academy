#!/usr/bin/env python3
"""Create Batch 2 calc engine definitions in tools/ directory."""
import os

with open("tools/DC_TOOL_001_CALC_ENGINE_v2_0.md", "w") as f:
    f.write("""# DC-TOOL-001 CALC ENGINE DEFINITION v2.0
# Power Chain Screener
# Source: DC-LEARN-001 (Power Distribution) cascadeCheck functions

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
  mic_mva:          { type: "number", label: "MIC (MVA)",                  required: true, min: 0.1, max: 200, step: 0.1, default: 5 },
  tx_count:         { type: "number", label: "Transformer Count",          required: true, min: 1, max: 10, default: 2 },
  tx_rating_mva:    { type: "number", label: "TX Rating Each (MVA)",       required: true, min: 0.5, max: 50, step: 0.1, default: 2 },
  ups_count:        { type: "number", label: "UPS Module Count",           required: true, min: 1, max: 20, default: 2 },
  ups_rating_mva:   { type: "number", label: "UPS Rating Each (MVA)",      required: true, min: 0.1, max: 5, step: 0.1, default: 1.5 },
  msb_bus_rating_a: { type: "number", label: "MSB Bus Rating (A)",         required: true, min: 100, max: 10000, default: 3200 },
  sts_rating_a:     { type: "number", label: "STS Rating per Feed (A)",    required: true, min: 0, max: 5000, default: 250 },
  pdu_per_row:      { type: "number", label: "PDUs per Row (count)",       required: true, min: 1, max: 50, default: 1 },
  pdu_rating_kw:    { type: "number", label: "PDU Rating (kW)",            required: true, min: 10, max: 500, default: 277 },
  whip_circuit_a:   { type: "number", label: "Rack Whip Circuit Rating (A)", required: true, min: 16, max: 63, default: 32 },
  whip_voltage:     { type: "number", label: "Rack Whip Voltage (V)",      required: true, min: 200, max: 415, default: 230 }
};
```

---

## CALC_ENGINE (10 calculations)

```javascript
function runCalcEngine(inputs) {
  const { it_load_mw, pue, racks, kw_per_rack, mic_mva, tx_count, tx_rating_mva,
          ups_count, ups_rating_mva, msb_bus_rating_a, sts_rating_a,
          pdu_per_row, pdu_rating_kw, whip_circuit_a, whip_voltage } = inputs;

  const calcs = {};
  const total_mw = it_load_mw * pue;

  // C01: MIC utilisation
  const mic_mw = mic_mva * 0.9;
  calcs.mic_utilisation = {
    id: "C01", label: "MIC Utilisation",
    formula: "Facility MW / (MIC MVA × 0.9 PF)",
    inputs: { total_mw, mic_mva },
    result: { utilisation_pct: Math.round(total_mw / mic_mw * 100), headroom_mw: Math.round((mic_mw - total_mw) * 10) / 10 },
    unit: "% / MW", tier: "Derived"
  };

  // C02: Transformer capacity per path
  const tx_derated = tx_rating_mva * 0.8 * 0.9; // K-factor × PF
  const demand_per_tx = total_mw / tx_count;
  calcs.tx_loading = {
    id: "C02", label: "Transformer Loading",
    formula: "TX MVA × 0.8 (K-derate) × 0.9 (PF) = capacity. Demand / count = per-TX",
    inputs: { tx_rating_mva, tx_count, total_mw },
    result: { capacity_mw: Math.round(tx_derated * 10) / 10, demand_per_tx: Math.round(demand_per_tx * 10) / 10, adequate: demand_per_tx <= tx_derated },
    unit: "MW/path", tier: "Derived"
  };

  // C03: MSB fault level check
  const bus_mva = msb_bus_rating_a * 400 * 1.732 / 1e6; // 3-phase at 400V
  calcs.msb_capacity = {
    id: "C03", label: "MSB Bus Capacity",
    formula: "Bus A × 400V × √3 / 1e6 = MVA. Check vs half facility demand (A/B split)",
    inputs: { msb_bus_rating_a, total_mw },
    result: { bus_mva: Math.round(bus_mva * 10) / 10, demand_per_bus: Math.round(total_mw / 2 * 10) / 10, adequate: total_mw / 2 <= bus_mva },
    unit: "MVA", tier: "Derived"
  };

  // C04: UPS capacity
  const ups_kw_total = ups_count * ups_rating_mva * 0.9 * 1000; // PF 0.9, to kW
  const ups_string_kw = ups_rating_mva * 0.9 * 1000;
  calcs.ups_capacity = {
    id: "C04", label: "UPS Capacity vs IT Load",
    formula: "UPS count × MVA × 0.9 PF × 1000 = kW total vs IT kW",
    inputs: { ups_count, ups_rating_mva, it_load_kw: it_load_mw * 1000 },
    result: { total_kw: Math.round(ups_kw_total), string_kw: Math.round(ups_string_kw), adequate: ups_kw_total >= it_load_mw * 1000 },
    unit: "kW", tier: "Derived"
  };

  // C05: STS transfer capacity
  const amps_per_rack = (kw_per_rack * 1000) / (whip_voltage * 3); // simplified 3-phase
  const total_amps = amps_per_rack * racks;
  calcs.sts_capacity = {
    id: "C05", label: "STS Transfer Capacity",
    formula: "IT amps vs STS rating. Amps = kW × 1000 / (V × phases)",
    inputs: { kw_per_rack, racks, sts_rating_a, whip_voltage },
    result: { total_amps: Math.round(total_amps), sts_amps: sts_rating_a, adequate: total_amps <= sts_rating_a },
    unit: "A", tier: "Derived"
  };

  // C06: PDU capacity
  const pdu_count = Math.ceil(racks / 50); // typical 1 PDU per 50 racks
  const pdu_total_kw = pdu_count * pdu_rating_kw;
  calcs.pdu_capacity = {
    id: "C06", label: "PDU Distribution Capacity",
    formula: "PDU count × rating vs IT load",
    inputs: { pdu_count, pdu_rating_kw, it_load_kw: it_load_mw * 1000 },
    result: { count: pdu_count, total_kw: pdu_total_kw, adequate: pdu_total_kw >= it_load_mw * 1000, utilisation_pct: Math.round(it_load_mw * 1000 / pdu_total_kw * 100) },
    unit: "kW", tier: "Derived"
  };

  // C07: Rack whip capacity
  const whip_kw = whip_circuit_a * 0.8 * whip_voltage / 1000; // 80% derating
  calcs.whip_capacity = {
    id: "C07", label: "Rack Whip Circuit Capacity",
    formula: "Circuit A × 0.8 (derating) × voltage / 1000 = kW available per rack",
    inputs: { whip_circuit_a, whip_voltage },
    result: { available_kw: Math.round(whip_kw * 10) / 10, required_kw: kw_per_rack, adequate: whip_kw >= kw_per_rack },
    unit: "kW/rack", tier: "Derived"
  };

  // C08: Diversity and growth headroom
  const diversity_factor = kw_per_rack <= 6 ? 0.7 : kw_per_rack <= 15 ? 0.8 : 0.9;
  const diversified_kw = kw_per_rack * racks * diversity_factor;
  const headroom_pct = ((ups_kw_total - diversified_kw) / ups_kw_total) * 100;
  calcs.diversity = {
    id: "C08", label: "Diversity & Growth Headroom",
    formula: "Diversified demand = kW × racks × diversity. Headroom = (UPS − diversified) / UPS",
    inputs: { kw_per_rack, racks, diversity_factor },
    result: { diversified_kw: Math.round(diversified_kw), headroom_pct: Math.round(headroom_pct), growth_kw: Math.round(ups_kw_total - diversified_kw) },
    unit: "kW / %", tier: "T3 — industry diversity factors"
  };

  // C09: Power chain bottleneck identification
  const components = [
    { name: "MIC", capacity_kw: mic_mw * 1000, utilisation: total_mw / mic_mw * 100 },
    { name: "Transformers", capacity_kw: tx_derated * tx_count * 1000, utilisation: total_mw / (tx_derated * tx_count) * 100 },
    { name: "UPS", capacity_kw: ups_kw_total, utilisation: it_load_mw * 1000 / ups_kw_total * 100 },
    { name: "PDU", capacity_kw: pdu_total_kw, utilisation: it_load_mw * 1000 / pdu_total_kw * 100 },
    { name: "Rack Whip", capacity_kw: whip_kw * racks, utilisation: kw_per_rack / whip_kw * 100 }
  ];
  const bottleneck = components.reduce((a, b) => a.utilisation > b.utilisation ? a : b);
  calcs.bottleneck = {
    id: "C09", label: "Power Chain Bottleneck",
    formula: "Component with highest utilisation = weakest link",
    inputs: { components: components.map(c => ({ name: c.name, utilisation: Math.round(c.utilisation) })) },
    result: { bottleneck: bottleneck.name, utilisation: Math.round(bottleneck.utilisation), all: components.map(c => ({ name: c.name, pct: Math.round(c.utilisation) })) },
    unit: "%", tier: "Derived"
  };

  // C10: Indicative upgrade cost
  const upgrade_needed = total_mw > mic_mw || !calcs.tx_loading.result.adequate || !calcs.ups_capacity.result.adequate;
  const cost_per_kw = { low: 300, high: 600 }; // T3 — RICS NRM1 / Schneider/ABB
  calcs.upgrade_cost = {
    id: "C10", label: "Indicative Power Chain Upgrade Cost",
    formula: "IT kW × €300–600/kW (screener-level, electrical infrastructure only)",
    inputs: { it_load_kw: it_load_mw * 1000, upgrade_needed },
    result: upgrade_needed ? { low: cost_per_kw.low * it_load_mw * 1000, high: cost_per_kw.high * it_load_mw * 1000 } : null,
    unit: "€", tier: "T3 — RICS NRM1 / Schneider/ABB published ranges",
    caveat: "Screening-level. Subject to detailed design and site survey."
  };

  return calcs;
}
```

---

## FINDINGS_ENGINE (6 findings)

```javascript
function runFindingsEngine(calcs) {
  const findings = [];
  const mic = calcs.mic_utilisation.result;
  findings.push({ id:"F01", category:"Grid", title:"MIC Headroom",
    status: mic.utilisation_pct <= 70 ? "GREEN" : mic.utilisation_pct <= 90 ? "AMBER" : "RED",
    current: `${mic.utilisation_pct}% utilised (${mic.headroom_mw} MW headroom)`,
    required: "≤70% recommended for density growth", gap: mic.utilisation_pct <= 70 ? "Adequate" : "Constrained",
    action: mic.utilisation_pct <= 70 ? "No action" : "Plan MIC upgrade — 52-week+ ESB lead time" });

  const tx = calcs.tx_loading.result;
  findings.push({ id:"F02", category:"Electrical", title:"Transformer Capacity",
    status: tx.adequate ? "GREEN" : "RED",
    current: `${tx.demand_per_tx} MW per TX vs ${tx.capacity_mw} MW capacity`,
    required: "Demand per TX ≤ derated capacity", gap: tx.adequate ? "Within limits" : "Overloaded",
    action: tx.adequate ? "Monitor" : "Transformer upgrade or additional unit required" });

  const ups = calcs.ups_capacity.result;
  findings.push({ id:"F03", category:"Power", title:"UPS Capacity",
    status: ups.adequate ? "GREEN" : "RED",
    current: `${ups.total_kw} kW UPS vs ${calcs.ups_capacity.inputs.it_load_kw} kW IT`,
    required: "UPS ≥ IT load (kW)", gap: ups.adequate ? "Adequate" : "Shortfall",
    action: ups.adequate ? "Adequate" : "UPS upgrade required" });

  const bn = calcs.bottleneck.result;
  findings.push({ id:"F04", category:"Power", title:"Power Chain Bottleneck",
    status: bn.utilisation <= 70 ? "GREEN" : bn.utilisation <= 90 ? "AMBER" : "RED",
    current: `${bn.bottleneck} at ${bn.utilisation}% — weakest link`,
    required: "All components ≤70% for growth headroom", gap: `Bottleneck: ${bn.bottleneck}`,
    action: bn.utilisation > 90 ? `Critical: upgrade ${bn.bottleneck} before density increase` : `Monitor ${bn.bottleneck}` });

  const whip = calcs.whip_capacity.result;
  findings.push({ id:"F05", category:"Distribution", title:"Rack Whip Capacity",
    status: whip.adequate ? "GREEN" : "RED",
    current: `${whip.available_kw} kW available vs ${whip.required_kw} kW required`,
    required: "Whip ≥ target kW/rack", gap: whip.adequate ? "Adequate" : "Whip upgrade needed for target density",
    action: whip.adequate ? "Adequate for current density" : "Re-cable to 3-phase or higher-rated whips" });

  const cost = calcs.upgrade_cost.result;
  findings.push({ id:"F06", category:"Commercial", title:"Indicative Upgrade Investment",
    status: cost === null ? "GREEN" : cost.high > 5000000 ? "RED" : "AMBER",
    current: cost === null ? "No upgrade needed" : `€${(cost.low/1e6).toFixed(1)}M–€${(cost.high/1e6).toFixed(1)}M`,
    required: "Budget for power chain upgrade", gap: cost === null ? "None" : `€${300}–€${600}/kW IT`,
    action: cost === null ? "No investment required" : "Commission Desktop Assessment — €10,000–€15,000" });

  const red_count = findings.filter(f => f.status === "RED").length;
  const amber_count = findings.filter(f => f.status === "AMBER").length;
  const overall = red_count > 0 ? "RED" : amber_count > 0 ? "AMBER" : "GREEN";
  return { findings, summary: { red_count, amber_count, green_count: findings.length - red_count - amber_count, overall } };
}
```

---

## INTERPRETATION_PROMPT

```
You are a power distribution specialist working for Legacy Business Engineers Ltd (LBE). You have received deterministic power chain screening results. All numbers are pre-calculated — do NOT invent numbers. Write fund-manager language: risk, cost, investment thesis. LBE identifies and quantifies — never designs or delivers. Decision gate: RED/AMBER → Desktop Assessment €10,000–€15,000.

Respond ONLY with JSON: { "executive_summary", "key_findings", "commercial_implications", "recommended_next_step", "caveats" }
```

## GOLDEN TESTS

| # | Scenario | Expected |
|---|----------|----------|
| G1 | 2.4 MW IT, PUE 1.50, 400 racks, 6kW, 5 MVA MIC, 2×2MVA TX | MIC 80%, TX overloaded, bottleneck = TX |
| G2 | 5 MW IT, PUE 1.25, 200 racks, 25kW, 20 MVA MIC, 4×5MVA TX | All GREEN, headroom adequate |

---
*DC-TOOL-001 Calc Engine v2.0 | 14 April 2026*
""")

with open("tools/DC_TOOL_002_CALC_ENGINE_v2_0.md", "w") as f:
    f.write("""# DC-TOOL-002 CALC ENGINE DEFINITION v2.0
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
""")

with open("tools/DC_TOOL_008_CALC_ENGINE_v2_0.md", "w") as f:
    f.write("""# DC-TOOL-008 CALC ENGINE DEFINITION v2.0
# Fire Safety Screener
# Source: DC-LEARN-008 (Fire Safety) cascadeCheck functions
# NOTE: This tool is primarily checklist-based — fewer numerical calcs, more rule-based findings.

---

## INPUT_SCHEMA

```javascript
const INPUT_SCHEMA = {
  facility_name:       { type: "text",   label: "Facility Name",              required: true },
  location:            { type: "text",   label: "Location",                   required: true, default: "Dublin, Ireland" },
  build_year:          { type: "number", label: "Year Built",                 required: true, min: 1990, max: 2026 },
  it_load_mw:          { type: "number", label: "IT Load (MW)",               required: true, min: 0.1, max: 100, step: 0.1 },
  racks:               { type: "number", label: "Number of Racks",            required: true, min: 10, max: 10000, default: 400 },
  detection_type:      { type: "select", label: "Detection System",           required: true, options: [
    { value: "vesda_all",     label: "VESDA — all zones (ceiling + sub-floor)" },
    { value: "vesda_ceiling", label: "VESDA — ceiling only" },
    { value: "point",         label: "Point detectors only" }
  ], default: "vesda_ceiling" },
  suppression_agent:   { type: "select", label: "Suppression Agent",          required: true, options: [
    { value: "novec",    label: "Novec 1230 (FK-5-1-12, GWP 1)" },
    { value: "fm200",    label: "FM-200 (HFC-227ea, GWP 3,220)" },
    { value: "inergen",  label: "Inergen (IG-541, GWP 0)" },
    { value: "sprinkler", label: "Sprinkler only (no gaseous)" },
    { value: "none",     label: "None" }
  ], default: "fm200" },
  battery_type:        { type: "select", label: "UPS Battery Chemistry",      required: true, options: [
    { value: "vrla",   label: "VRLA (lead-acid)" },
    { value: "li_ion", label: "Li-ion" },
    { value: "nic_zn", label: "Nickel-Zinc" }
  ], default: "vrla" },
  has_li_ion_suppress: { type: "select", label: "Li-ion Specific Suppression?", required: true, options: [
    { value: true,  label: "Yes — CO/H₂ detection + HPWM installed" },
    { value: false, label: "No" }
  ], default: false },
  sprinkler_head_temp: { type: "number", label: "Sprinkler Head Rating (°C)", required: true, min: 57, max: 141, default: 57 },
  hot_aisle_temp:      { type: "number", label: "Measured Hot Aisle Temp (°C)", required: true, min: 25, max: 55, default: 43 },
  unsealed_penetrations: { type: "number", label: "Known Unsealed Penetrations", required: true, min: 0, max: 500, default: 0 },
  hold_time_known:     { type: "select", label: "Suppression Hold Time Verified?", required: true, options: [
    { value: true, label: "Yes — hold time >10 min confirmed" },
    { value: false, label: "No — hold time unknown or untested" }
  ], default: false },
  fas_bms_tested:      { type: "select", label: "FAS-BMS Integration Tested?", required: true, options: [
    { value: true, label: "Yes — cause & effect tested" },
    { value: false, label: "No — untested" }
  ], default: false },
  fra_date:            { type: "number", label: "Last FRA Year",              required: true, min: 2010, max: 2026, default: 2019 },
  has_bess:            { type: "select", label: "BESS Installed?",            required: true, options: [
    { value: true, label: "Yes" }, { value: false, label: "No" }
  ], default: false }
};
```

---

## CALC_ENGINE (8 calculations)

```javascript
function runCalcEngine(inputs) {
  const { detection_type, suppression_agent, battery_type, has_li_ion_suppress,
          sprinkler_head_temp, hot_aisle_temp, unsealed_penetrations,
          hold_time_known, fas_bms_tested, fra_date, has_bess, it_load_mw, racks } = inputs;

  const calcs = {};
  const CURRENT_YEAR = 2026;

  // C01: Detection coverage assessment
  calcs.detection = { id:"C01", label:"Detection Coverage",
    formula: "VESDA all zones = full. Ceiling only = sub-floor gap. Point = insufficient for DC",
    inputs: { detection_type },
    result: { full_coverage: detection_type === "vesda_all", sub_floor_gap: detection_type !== "vesda_all", grade: detection_type === "vesda_all" ? "Full" : detection_type === "vesda_ceiling" ? "Partial — sub-floor unmonitored" : "Insufficient" },
    unit: "", tier: "T1 — IS 3218 / EN 54" };

  // C02: Suppression agent GWP assessment
  const GWP_MAP = { novec: 1, fm200: 3220, inergen: 0, sprinkler: 0, none: 0 };
  const agent_gwp = GWP_MAP[suppression_agent] || 0;
  calcs.suppression = { id:"C02", label:"Suppression Agent Assessment",
    formula: "Agent GWP check vs F-Gas phase-down (EU 2024/573)",
    inputs: { suppression_agent, gwp: agent_gwp },
    result: { gwp: agent_gwp, f_gas_risk: agent_gwp > 750 ? "HIGH" : "LOW", has_gaseous: !["sprinkler","none"].includes(suppression_agent) },
    unit: "GWP", tier: "T1 — ISO 14520 / EU 2024/573" };

  // C03: Li-ion battery fire risk
  calcs.li_ion_risk = { id:"C03", label:"Li-ion Battery Fire Protection",
    formula: "Li-ion requires CO/H₂ detection + HPWM. VRLA requires standard suppression.",
    inputs: { battery_type, has_li_ion_suppress },
    result: { at_risk: battery_type === "li_ion" && !has_li_ion_suppress, adequate: battery_type !== "li_ion" || has_li_ion_suppress },
    unit: "", tier: "T1 — NFPA 855 / UL 9540A" };

  // C04: Sprinkler head temperature margin
  const margin = sprinkler_head_temp - hot_aisle_temp;
  const required_margin = 30; // EN 12845
  calcs.sprinkler_margin = { id:"C04", label:"Sprinkler Head Temperature Margin",
    formula: "Head rating − hot aisle temp ≥ 30°C (EN 12845)",
    inputs: { sprinkler_head_temp, hot_aisle_temp, required: required_margin },
    result: { margin_c: margin, adequate: margin >= required_margin, recommended_head: hot_aisle_temp + required_margin },
    unit: "°C", tier: "T1 — EN 12845" };

  // C05: Compartmentation integrity
  calcs.compartmentation = { id:"C05", label:"Fire Compartmentation Integrity",
    formula: "Unsealed penetrations count — EN 1366-3 requires all sealed",
    inputs: { unsealed_penetrations },
    result: { count: unsealed_penetrations, compliant: unsealed_penetrations === 0 },
    unit: "penetrations", tier: "T1 — EN 1366-3 / IS 3218" };

  // C06: Suppression hold time + FAS-BMS
  calcs.hold_time = { id:"C06", label:"Suppression Hold Time & FAS Integration",
    formula: "Hold time >10 min confirmed AND FAS-BMS cause & effect tested",
    inputs: { hold_time_known, fas_bms_tested },
    result: { hold_ok: hold_time_known, fas_ok: fas_bms_tested, both_ok: hold_time_known && fas_bms_tested },
    unit: "", tier: "T1 — IS 3218" };

  // C07: FRA currency
  const fra_age = CURRENT_YEAR - fra_date;
  calcs.fra_currency = { id:"C07", label:"Fire Risk Assessment Currency",
    formula: "FRA should be reviewed annually. >3 years = overdue.",
    inputs: { fra_date, current_year: CURRENT_YEAR },
    result: { age_years: fra_age, current: fra_age <= 1, overdue: fra_age > 3 },
    unit: "years", tier: "T1 — Regulatory Reform (Fire Safety) Order / IS 3218" };

  // C08: BESS fire risk
  calcs.bess_risk = { id:"C08", label:"BESS Fire Risk Assessment",
    formula: "BESS installed → requires dedicated fire strategy per NFPA 855",
    inputs: { has_bess },
    result: { at_risk: has_bess, requires_strategy: has_bess },
    unit: "", tier: "T1 — NFPA 855 / UL 9540A" };

  return calcs;
}
```

---

## FINDINGS_ENGINE (8 findings)

```javascript
function runFindingsEngine(calcs) {
  const findings = [];

  findings.push({ id:"F01", category:"Detection", title:"Detection Coverage",
    status: calcs.detection.result.full_coverage ? "GREEN" : calcs.detection.result.sub_floor_gap ? "RED" : "RED",
    current: calcs.detection.result.grade, required: "VESDA all zones (IS 3218)",
    gap: calcs.detection.result.full_coverage ? "Full coverage" : "Sub-floor unmonitored — cable fire risk",
    action: calcs.detection.result.full_coverage ? "Adequate" : "Install sub-floor VESDA aspirating detection" });

  findings.push({ id:"F02", category:"Suppression", title:"Suppression Agent F-Gas Risk",
    status: calcs.suppression.result.f_gas_risk === "HIGH" ? "RED" : calcs.suppression.result.has_gaseous ? "GREEN" : "RED",
    current: `${calcs.suppression.inputs.suppression_agent} (GWP ${calcs.suppression.result.gwp})`,
    required: "Low-GWP agent (Novec 1230 or Inergen)", gap: calcs.suppression.result.f_gas_risk === "HIGH" ? "High-GWP agent — EU phase-down applies" : "Compliant",
    action: calcs.suppression.result.f_gas_risk === "HIGH" ? "Plan agent replacement — Novec 1230 transition" : "No action" });

  findings.push({ id:"F03", category:"Battery", title:"Li-ion Battery Protection",
    status: calcs.li_ion_risk.result.adequate ? "GREEN" : "RED",
    current: calcs.li_ion_risk.result.at_risk ? "Li-ion without dedicated suppression" : "Adequate",
    required: "CO/H₂ detection + HPWM for Li-ion (NFPA 855)", gap: calcs.li_ion_risk.result.adequate ? "None" : "No Li-ion specific protection",
    action: calcs.li_ion_risk.result.adequate ? "Adequate" : "Install CO/H₂ detection and high-pressure water mist" });

  const sp = calcs.sprinkler_margin.result;
  findings.push({ id:"F04", category:"Suppression", title:"Sprinkler Head Temperature",
    status: sp.adequate ? "GREEN" : "RED",
    current: `${sp.margin_c}°C margin (need ≥30°C per EN 12845)`,
    required: `≥${calcs.sprinkler_margin.inputs.required}°C margin. Recommend ${sp.recommended_head}°C heads in hot aisles`,
    gap: sp.adequate ? "Adequate" : `${30 - sp.margin_c}°C below EN 12845 minimum — spurious discharge risk`,
    action: sp.adequate ? "No action" : `Replace hot aisle heads with ${sp.recommended_head}°C rated (79°C or 93°C)` });

  findings.push({ id:"F05", category:"Passive", title:"Fire Compartmentation",
    status: calcs.compartmentation.result.compliant ? "GREEN" : "RED",
    current: `${calcs.compartmentation.result.count} unsealed penetrations`,
    required: "Zero unsealed penetrations (EN 1366-3)",
    gap: calcs.compartmentation.result.compliant ? "Compliant" : `${calcs.compartmentation.result.count} penetrations unsealed`,
    action: calcs.compartmentation.result.compliant ? "Maintain" : "Seal all penetrations — fire-rated intumescent required" });

  findings.push({ id:"F06", category:"Systems", title:"Hold Time & FAS-BMS Integration",
    status: calcs.hold_time.result.both_ok ? "GREEN" : "RED",
    current: `Hold time: ${calcs.hold_time.result.hold_ok?"Verified":"Unknown"}. FAS-BMS: ${calcs.hold_time.result.fas_ok?"Tested":"Untested"}`,
    required: "Both verified per IS 3218", gap: calcs.hold_time.result.both_ok ? "None" : "Incomplete verification",
    action: calcs.hold_time.result.both_ok ? "Maintain" : "Commission integrity test + FAS-BMS cause & effect test" });

  findings.push({ id:"F07", category:"Compliance", title:"Fire Risk Assessment",
    status: calcs.fra_currency.result.current ? "GREEN" : calcs.fra_currency.result.overdue ? "RED" : "AMBER",
    current: `FRA dated ${calcs.fra_currency.inputs.fra_date} (${calcs.fra_currency.result.age_years} years old)`,
    required: "Annual review recommended. >3 years = overdue.", gap: calcs.fra_currency.result.overdue ? "Overdue" : "Due for review",
    action: calcs.fra_currency.result.overdue ? "Commission updated FRA immediately" : "Schedule annual review" });

  if (calcs.bess_risk.result.requires_strategy) {
    findings.push({ id:"F08", category:"BESS", title:"BESS Fire Strategy",
      status: "AMBER", current: "BESS installed — fire strategy status unknown",
      required: "Dedicated BESS fire strategy per NFPA 855", gap: "Verify BESS fire protection strategy exists",
      action: "Review BESS fire risk assessment and suppression adequacy" });
  }

  const rc = findings.filter(f=>f.status==="RED").length;
  const ac = findings.filter(f=>f.status==="AMBER").length;
  return { findings, summary: { red_count:rc, amber_count:ac, green_count:findings.length-rc-ac, overall: rc>0?"RED":ac>0?"AMBER":"GREEN" } };
}
```

---

## INTERPRETATION_PROMPT

```
You are a fire safety specialist working for Legacy Business Engineers Ltd (LBE). Deterministic fire safety screening results provided. All numbers pre-calculated — do NOT invent. Fund-manager language. Key standards: IS 3218, EN 12845, EN 1366-3, NFPA 855 (BESS), ISO 14520 (gaseous), EU 2024/573 (F-Gas). LBE identifies and quantifies. Decision gate: RED/AMBER → Desktop Assessment €10,000–€15,000.
Respond ONLY with JSON: { "executive_summary", "key_findings", "commercial_implications", "recommended_next_step", "caveats" }
```

## GOLDEN TESTS
| # | Scenario | Expected |
|---|----------|----------|
| G1 | VESDA ceiling only, FM-200, Li-ion no suppress, 57°C heads, 43°C hot aisle, 47 penetrations, no hold time, FRA 2019 | Detection RED, FM-200 RED, Li-ion RED, sprinkler RED (14°C margin), compartment RED, hold time RED, FRA RED |
| G2 | VESDA all, Novec, VRLA, 79°C heads, 35°C hot aisle, 0 penetrations, hold verified, FAS tested, FRA 2025 | All GREEN |

---
*DC-TOOL-008 Calc Engine v2.0 | 14 April 2026*
""")

with open("tools/DC_TOOL_010_CALC_ENGINE_v2_0.md", "w") as f:
    f.write("""# DC-TOOL-010 CALC ENGINE DEFINITION v2.0
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
""")

with open("tools/DC_TOOL_011_CALC_ENGINE_v2_0.md", "w") as f:
    f.write("""# DC-TOOL-011 CALC ENGINE DEFINITION v2.0
# Security Assessment Tool
# Source: DC-LEARN-011 (Physical Security) — primarily checklist-based

---

## INPUT_SCHEMA

```javascript
const INPUT_SCHEMA = {
  facility_name: { type:"text", label:"Facility Name", required:true },
  location:      { type:"text", label:"Location", required:true, default:"Dublin, Ireland" },
  build_year:    { type:"number", label:"Year Built", required:true, min:1990, max:2026 },
  it_load_mw:    { type:"number", label:"IT Load (MW)", required:true, min:0.1, max:100, step:0.1 },
  racks:         { type:"number", label:"Number of Racks", required:true, min:10, max:10000, default:400 },
  // Security zone questions (8 domains from DC-LEARN-011 L1-L8)
  perimeter_type:  { type:"select", label:"Perimeter Security", required:true, options:[
    {value:"pids_hvm", label:"PIDS + HVM + clear zone"}, {value:"fence_detect", label:"Fence + detection"},
    {value:"fence_only", label:"Fence only"}, {value:"none", label:"No perimeter security"}
  ], default:"fence_only" },
  vehicle_access:  { type:"select", label:"Vehicle Access Control", required:true, options:[
    {value:"dual_gate_uvss", label:"Dual-gate airlock + UVSS"}, {value:"barrier_anpr", label:"Rising barrier + ANPR"},
    {value:"barrier_only", label:"Single barrier"}, {value:"open", label:"Open access"}
  ], default:"barrier_only" },
  building_entry:  { type:"select", label:"Building Entry Control", required:true, options:[
    {value:"mantrap_apb", label:"Mantrap + anti-passback"}, {value:"card_pin", label:"Card + PIN"},
    {value:"card_only", label:"Single card reader"}, {value:"key", label:"Key access"}
  ], default:"card_only" },
  data_hall_access: { type:"select", label:"Data Hall Access", required:true, options:[
    {value:"biometric_card", label:"2FA (biometric + card)"}, {value:"card_pin", label:"Card + PIN"},
    {value:"card_only", label:"Single-factor card"}, {value:"shared_key", label:"Shared key"}
  ], default:"card_only" },
  rack_security:   { type:"select", label:"Rack/Cabinet Security", required:true, options:[
    {value:"electronic_audit", label:"Electronic locks + audit trail"}, {value:"electronic", label:"Electronic locks (no audit)"},
    {value:"barrel_key", label:"Barrel key locks"}, {value:"none", label:"No rack locks"}
  ], default:"barrel_key" },
  cctv_type:       { type:"select", label:"CCTV System", required:true, options:[
    {value:"ip_90day", label:"IP cameras + 90-day retention"}, {value:"ip_30day", label:"IP cameras + 30-day retention"},
    {value:"analogue", label:"Analogue cameras"}, {value:"none", label:"No CCTV"}
  ], default:"analogue" },
  alarm_grade:     { type:"select", label:"Intruder Alarm Grade", required:true, options:[
    {value:"grade3_dual_arc", label:"Grade 3 + dual-path + ARC"}, {value:"grade3_single", label:"Grade 3 + single-path"},
    {value:"grade2", label:"Grade 2"}, {value:"none", label:"No alarm system"}
  ], default:"grade2" }
};
```

---

## CALC_ENGINE (3 calculations)

```javascript
function runCalcEngine(inputs) {
  const calcs = {};

  // C01: Security zone count
  const zones_present = [
    inputs.perimeter_type !== "none",
    inputs.vehicle_access !== "open",
    inputs.building_entry !== "key",
    inputs.data_hall_access !== "shared_key"
  ].filter(Boolean).length;
  calcs.zone_count = { id:"C01", label:"Security Zone Assessment",
    formula: "Count distinct security zones (perimeter, vehicle, building, data hall)",
    inputs: { zones_present }, result: { count: zones_present, required: 4, adequate: zones_present >= 4 },
    unit: "zones", tier: "T1 — EN 50600-1 / Uptime Institute" };

  // C02: Security maturity score
  const score_map = {
    perimeter: { pids_hvm:4, fence_detect:3, fence_only:1, none:0 },
    vehicle: { dual_gate_uvss:4, barrier_anpr:3, barrier_only:1, open:0 },
    entry: { mantrap_apb:4, card_pin:3, card_only:1, key:0 },
    hall: { biometric_card:4, card_pin:3, card_only:1, shared_key:0 },
    rack: { electronic_audit:4, electronic:3, barrel_key:1, none:0 },
    cctv: { ip_90day:4, ip_30day:3, analogue:1, none:0 },
    alarm: { grade3_dual_arc:4, grade3_single:3, grade2:1, none:0 }
  };
  const scores = {
    perimeter: score_map.perimeter[inputs.perimeter_type]||0,
    vehicle: score_map.vehicle[inputs.vehicle_access]||0,
    entry: score_map.entry[inputs.building_entry]||0,
    hall: score_map.hall[inputs.data_hall_access]||0,
    rack: score_map.rack[inputs.rack_security]||0,
    cctv: score_map.cctv[inputs.cctv_type]||0,
    alarm: score_map.alarm[inputs.alarm_grade]||0
  };
  const total = Object.values(scores).reduce((a,b)=>a+b, 0);
  const max_score = 28;
  calcs.maturity_score = { id:"C02", label:"Security Maturity Score",
    formula: "7 domains × 0-4 scale. Max 28.", inputs: scores,
    result: { score: total, max: max_score, pct: Math.round(total/max_score*100), domains: scores },
    unit: "/ 28", tier: "Derived" };

  // C03: Indicative upgrade cost
  const gaps = Object.entries(scores).filter(([k,v]) => v < 3).length;
  const cost_per_domain = { low: 50000, high: 200000 }; // T3 — Axis/Genetec/Gallagher
  calcs.upgrade_cost = { id:"C03", label:"Indicative Security Upgrade Cost",
    formula: "Domains scoring <3 × €50K–€200K per domain",
    inputs: { domains_below_3: gaps },
    result: gaps > 0 ? { low: gaps * cost_per_domain.low, high: gaps * cost_per_domain.high, domains: gaps } : null,
    unit: "€", tier: "T3 — Axis/Genetec/Gallagher published ranges",
    caveat: "Screening-level. Subject to site security survey." };

  return calcs;
}
```

---

## FINDINGS_ENGINE (8 findings — one per domain + overall)

```javascript
function runFindingsEngine(calcs) {
  const findings = [];
  const domains = calcs.maturity_score.result.domains;
  const labels = { perimeter:"Perimeter Security", vehicle:"Vehicle Access", entry:"Building Entry",
    hall:"Data Hall Access", rack:"Rack Security", cctv:"CCTV & Surveillance", alarm:"Intruder Alarm" };

  for (const [key, score] of Object.entries(domains)) {
    findings.push({ id:`F0${findings.length+1}`, category:"Security", title:labels[key],
      status: score >= 4 ? "GREEN" : score >= 3 ? "AMBER" : "RED",
      current: `Score ${score}/4`, required: "≥3 for adequate security",
      gap: score >= 3 ? "Adequate" : "Below minimum standard",
      action: score >= 3 ? "Maintain" : `Upgrade ${labels[key]} — see calc engine for specifics` });
  }

  // F08: Overall
  const total = calcs.maturity_score.result;
  findings.push({ id:"F08", category:"Summary", title:"Overall Security Maturity",
    status: total.pct >= 75 ? "GREEN" : total.pct >= 50 ? "AMBER" : "RED",
    current: `${total.score}/${total.max} (${total.pct}%)`, required: "≥75% for institutional-grade security",
    gap: total.pct >= 75 ? "Adequate" : `${total.max - total.score} points below target`,
    action: total.pct < 75 ? "Commission security assessment — €10,000–€15,000" : "Annual review recommended" });

  const rc = findings.filter(f=>f.status==="RED").length;
  const ac = findings.filter(f=>f.status==="AMBER").length;
  return { findings, summary: { red_count:rc, amber_count:ac, green_count:findings.length-rc-ac, overall: rc>0?"RED":ac>0?"AMBER":"GREEN" } };
}
```

---

## INTERPRETATION_PROMPT

```
You are a physical security specialist working for Legacy Business Engineers Ltd (LBE). Deterministic security screening results provided — 7 security domains scored 0-4. Fund-manager language. Key standards: EN 50600-1 (DC security), EN 62676 (CCTV), EN 50131 (intruder alarm). LBE identifies and quantifies. Decision gate: RED/AMBER → Desktop Assessment €10,000–€15,000.
Respond ONLY with JSON: { "executive_summary", "key_findings", "commercial_implications", "recommended_next_step", "caveats" }
```

## GOLDEN TESTS
| # | Scenario | Expected |
|---|----------|----------|
| G1 | All minimum (fence/barrier/card/card/barrel/analogue/grade2) | Score 7/28 (25%), all RED except none |
| G2 | All maximum | Score 28/28 (100%), all GREEN |

---
*DC-TOOL-011 Calc Engine v2.0 | 14 April 2026*
""")

with open("tools/DC_TOOL_012_CALC_ENGINE_v2_0.md", "w") as f:
    f.write("""# DC-TOOL-012 CALC ENGINE DEFINITION v2.0
# Commissioning Readiness Tool
# Source: DC-LEARN-013 (Commissioning) — staged milestone checklist

---

## INPUT_SCHEMA

```javascript
const INPUT_SCHEMA = {
  facility_name: { type:"text", label:"Facility Name", required:true },
  location:      { type:"text", label:"Location", required:true, default:"Dublin, Ireland" },
  it_load_mw:    { type:"number", label:"Design IT Load (MW)", required:true, min:0.1, max:100, step:0.1 },
  // 9 commissioning milestones (pass/fail)
  cx_plan:       { type:"select", label:"1. Cx Plan Approved?", required:true, options:[{value:true,label:"Yes"},{value:false,label:"No"}], default:false },
  fats_complete:  { type:"select", label:"2. All FATs Complete?", required:true, options:[{value:true,label:"Yes"},{value:false,label:"No"}], default:false },
  sats_complete:  { type:"select", label:"3. All SATs Complete?", required:true, options:[{value:true,label:"Yes"},{value:false,label:"No"}], default:false },
  ists_complete:  { type:"select", label:"4. All ISTs Complete?", required:true, options:[{value:true,label:"Yes"},{value:false,label:"No"}], default:false },
  load_test:     { type:"select", label:"5. Full-Chain Load Test Done?", required:true, options:[{value:true,label:"Yes"},{value:false,label:"No"}], default:false },
  pvt_complete:  { type:"select", label:"6. PVT Complete (72-hr)?", required:true, options:[{value:true,label:"Yes"},{value:false,label:"No"}], default:false },
  seasonal_cx:   { type:"select", label:"7. Seasonal Cx Done (both)?", required:true, options:[{value:true,label:"Yes — both seasons"},{value:false,label:"No"}], default:false },
  defects_clear: { type:"select", label:"8. All Cat A/B Defects Cleared?", required:true, options:[{value:true,label:"Yes"},{value:false,label:"No"}], default:false },
  orr_passed:    { type:"select", label:"9. Operational Readiness Review Passed?", required:true, options:[{value:true,label:"Yes"},{value:false,label:"No"}], default:false }
};
```

---

## CALC_ENGINE (3 calculations)

```javascript
function runCalcEngine(inputs) {
  const calcs = {};
  const milestones = [
    { id:"M1", name:"Cx Plan", done: inputs.cx_plan },
    { id:"M2", name:"FATs", done: inputs.fats_complete },
    { id:"M3", name:"SATs", done: inputs.sats_complete },
    { id:"M4", name:"ISTs", done: inputs.ists_complete },
    { id:"M5", name:"Full-Chain Load Test", done: inputs.load_test },
    { id:"M6", name:"PVT (72-hour)", done: inputs.pvt_complete },
    { id:"M7", name:"Seasonal Cx", done: inputs.seasonal_cx },
    { id:"M8", name:"Defect Clearance", done: inputs.defects_clear },
    { id:"M9", name:"ORR", done: inputs.orr_passed }
  ];

  // C01: Completion count
  const done_count = milestones.filter(m=>m.done).length;
  calcs.completion = { id:"C01", label:"Commissioning Completion",
    formula: "Count completed milestones / 9",
    inputs: { milestones: milestones.map(m=>({name:m.name, done:m.done})) },
    result: { done: done_count, total: 9, pct: Math.round(done_count/9*100), next: milestones.find(m=>!m.done)?.name || "All complete" },
    unit: "/ 9", tier: "Derived" };

  // C02: Readiness gate
  const sequential_ok = milestones.every((m, i) => i === 0 || !m.done || milestones[i-1].done);
  calcs.readiness = { id:"C02", label:"Commissioning Readiness Gate",
    formula: "All milestones must be sequential — no skipping stages",
    inputs: { sequential_ok },
    result: { ready: done_count === 9, sequential: sequential_ok, gate: done_count === 9 ? "PASS" : sequential_ok ? "IN PROGRESS" : "OUT OF SEQUENCE" },
    unit: "", tier: "T1 — ASHRAE Guideline 0 / CIBSE Commissioning Code" };

  // C03: Indicative Cx cost
  const cx_cost_per_kw = { low: 80, high: 150 }; // T3 — RICS NRM1
  calcs.cx_cost = { id:"C03", label:"Indicative Commissioning Cost",
    formula: "€80–150/kW IT (RICS NRM1 Cx benchmarks)",
    inputs: { it_load_kw: inputs.it_load_mw * 1000 },
    result: { low: cx_cost_per_kw.low * inputs.it_load_mw * 1000, high: cx_cost_per_kw.high * inputs.it_load_mw * 1000 },
    unit: "€", tier: "T3 — RICS NRM1",
    caveat: "Screening-level estimate. CxA fee, equipment vendor Cx costs, and defect rectification costs are additional." };

  return calcs;
}
```

---

## FINDINGS_ENGINE (3 findings)

```javascript
function runFindingsEngine(calcs) {
  const findings = [];
  const comp = calcs.completion.result;
  findings.push({ id:"F01", category:"Commissioning", title:"Overall Completion",
    status: comp.pct === 100 ? "GREEN" : comp.pct >= 60 ? "AMBER" : "RED",
    current: `${comp.done}/${comp.total} milestones (${comp.pct}%)`,
    required: "9/9 for operational readiness", gap: comp.pct === 100 ? "Complete" : `Next: ${comp.next}`,
    action: comp.pct === 100 ? "Proceed to operations" : `Complete ${comp.next} before proceeding` });

  const ready = calcs.readiness.result;
  findings.push({ id:"F02", category:"Commissioning", title:"Sequence Integrity",
    status: ready.gate === "PASS" ? "GREEN" : ready.sequential ? "AMBER" : "RED",
    current: ready.gate, required: "Sequential completion — no skipping stages",
    gap: ready.sequential ? "In sequence" : "OUT OF SEQUENCE — stages skipped",
    action: ready.sequential ? "Continue in order" : "Return to earliest incomplete milestone" });

  const cost = calcs.cx_cost.result;
  findings.push({ id:"F03", category:"Commercial", title:"Commissioning Budget",
    status: "AMBER", current: `€${(cost.low/1e6).toFixed(1)}M–€${(cost.high/1e6).toFixed(1)}M`,
    required: "Budget allocation for remaining Cx activities",
    gap: `€80–150/kW IT (screening-level)`, action: "Verify Cx budget against remaining scope" });

  const rc = findings.filter(f=>f.status==="RED").length;
  const ac = findings.filter(f=>f.status==="AMBER").length;
  return { findings, summary: { red_count:rc, amber_count:ac, green_count:findings.length-rc-ac, overall: rc>0?"RED":ac>0?"AMBER":"GREEN" } };
}
```

---

## INTERPRETATION_PROMPT

```
You are a commissioning specialist working for Legacy Business Engineers Ltd (LBE). Deterministic commissioning readiness results provided. 9 sequential milestones: Cx Plan → FATs → SATs → ISTs → Load Test → PVT → Seasonal Cx → Defect Clearance → ORR. Fund-manager language. Standards: ASHRAE Guideline 0, CIBSE Cx Code. LBE identifies and quantifies. Decision gate: incomplete → Desktop Assessment €10,000–€15,000.
Respond ONLY with JSON: { "executive_summary", "key_findings", "commercial_implications", "recommended_next_step", "caveats" }
```

## GOLDEN TESTS
| # | Scenario | Expected |
|---|----------|----------|
| G1 | All false (nothing done) | 0/9 RED, next = Cx Plan |
| G2 | First 5 true, rest false | 5/9 AMBER, next = PVT |
| G3 | All true | 9/9 GREEN, gate PASS |

---
*DC-TOOL-012 Calc Engine v2.0 | 14 April 2026*
""")

with open("tools/DC_TOOL_013_CALC_ENGINE_v2_0.md", "w") as f:
    f.write("""# DC-TOOL-013 CALC ENGINE DEFINITION v2.0
# AI-Ready Cooling Screener
# Source: DC-LEARN-014 (High-Density/Liquid Cooling)

---

## INPUT_SCHEMA

```javascript
const INPUT_SCHEMA = {
  facility_name: { type:"text", label:"Facility Name", required:true },
  location:      { type:"text", label:"Location", required:true, default:"Dublin, Ireland" },
  build_year:    { type:"number", label:"Year Built", required:true, min:1990, max:2026 },
  it_load_mw:    { type:"number", label:"Current IT Load (MW)", required:true, min:0.1, max:100, step:0.1 },
  pue:           { type:"number", label:"Current PUE", required:true, min:1.0, max:3.0, step:0.01, default:1.50 },
  racks:         { type:"number", label:"Number of Racks", required:true, min:10, max:10000, default:400 },
  kw_per_rack:   { type:"number", label:"Current kW per Rack", required:true, min:1, max:100, default:6 },
  target_kw_rack:{ type:"number", label:"Target kW per Rack (AI pods)", required:true, min:20, max:200, default:30 },
  dlc_rack_count:{ type:"number", label:"Planned DLC Rack Count", required:true, min:0, max:5000, default:40 },
  floor_load_kpa:{ type:"number", label:"Current Floor Load Rating (kN/m²)", required:true, min:1, max:20, default:5 },
  whip_circuit_a:{ type:"number", label:"Rack Whip Circuit (A)", required:true, min:16, max:63, default:32 },
  whip_voltage:  { type:"number", label:"Whip Voltage (V)", required:true, min:200, max:415, default:230 },
  mic_mva:       { type:"number", label:"MIC (MVA)", required:true, min:0.1, max:200, default:5 }
};
```

---

## CALC_ENGINE (10 calculations)

```javascript
function runCalcEngine(inputs) {
  const { it_load_mw, pue, racks, kw_per_rack, target_kw_rack, dlc_rack_count,
          floor_load_kpa, whip_circuit_a, whip_voltage, mic_mva } = inputs;

  const calcs = {};
  const ELEC_PRICE = 0.12; const AIR_MAX = 25; const DLC_CAPTURE = 0.75;
  const IMMERSION_THRESHOLD = 80; const DLC_FLOOR_LOAD = 10; // kN/m² for DLC racks

  // C01: Air cooling limit check
  calcs.air_limit = { id:"C01", label:"Air Cooling Density Limit",
    formula: "Target kW/rack vs 25 kW air cooling max (ASHRAE TC 9.9)",
    inputs: { target_kw_rack, limit: AIR_MAX },
    result: { exceeds_air: target_kw_rack > AIR_MAX, requires_dlc: target_kw_rack > AIR_MAX },
    unit: "kW/rack", tier: "T3 — ASHRAE TC 9.9" };

  // C02: DLC heat split
  const dlc_kw = target_kw_rack * DLC_CAPTURE;
  const air_kw = target_kw_rack * (1 - DLC_CAPTURE);
  calcs.dlc_split = { id:"C02", label:"DLC/Air Heat Split",
    formula: "DLC captures 75% of rack heat. Air handles 25%.",
    inputs: { target_kw_rack, dlc_capture: DLC_CAPTURE },
    result: { dlc_kw: Math.round(dlc_kw * 10) / 10, air_kw: Math.round(air_kw * 10) / 10 },
    unit: "kW/rack", tier: "T3 — manufacturer spec (Vertiv/CoolIT)" };

  // C03: CDU sizing
  const cdu_cap_kw = 200; // typical CDU capacity (T3)
  const total_dlc_kw = dlc_rack_count * dlc_kw;
  const cdus_needed = Math.ceil(total_dlc_kw / cdu_cap_kw);
  calcs.cdu_sizing = { id:"C03", label:"CDU Sizing",
    formula: "DLC racks × DLC kW / CDU capacity = CDUs needed",
    inputs: { dlc_rack_count, dlc_kw_per_rack: Math.round(dlc_kw), cdu_cap_kw },
    result: { cdus_needed, total_dlc_kw: Math.round(total_dlc_kw), cdu_count_n1: cdus_needed + 1 },
    unit: "CDUs", tier: "T3 — CoolIT/Vertiv published" };

  // C04: Immersion threshold
  calcs.immersion = { id:"C04", label:"Immersion vs DLC Decision",
    formula: "≥80 kW/rack → consider immersion. <80 → DLC (cold plate) preferred.",
    inputs: { target_kw_rack, threshold: IMMERSION_THRESHOLD },
    result: { technology: target_kw_rack >= IMMERSION_THRESHOLD ? "Immersion cooling recommended" : "DLC (cold plate) suitable" },
    unit: "kW/rack", tier: "T3 — industry guidance" };

  // C05: Hybrid hall layout
  const air_racks = racks - dlc_rack_count;
  calcs.layout = { id:"C05", label:"Hybrid Hall Layout",
    formula: "Total racks − DLC racks = air-cooled racks",
    inputs: { racks, dlc_rack_count },
    result: { air_racks, dlc_racks: dlc_rack_count, dlc_pct: Math.round(dlc_rack_count / racks * 100) },
    unit: "racks", tier: "Derived" };

  // C06: Power distribution check
  const current_whip_kw = whip_circuit_a * 0.8 * whip_voltage / 1000;
  const three_phase_kw = 32 * 0.8 * 400 * 1.732 / 1000; // 3-phase upgrade path
  calcs.power_dist = { id:"C06", label:"Rack Power Distribution",
    formula: "Current whip capacity vs target kW/rack. 3-phase upgrade path.",
    inputs: { current_whip_kw: Math.round(current_whip_kw * 10) / 10, target_kw_rack },
    result: { adequate: current_whip_kw >= target_kw_rack, three_phase_kw: Math.round(three_phase_kw * 10) / 10, needs_upgrade: current_whip_kw < target_kw_rack },
    unit: "kW/rack", tier: "Derived" };

  // C07: Structural assessment
  calcs.structural = { id:"C07", label:"Floor Load Assessment",
    formula: "DLC rack load vs current floor rating",
    inputs: { current_kpa: floor_load_kpa, required_kpa: DLC_FLOOR_LOAD },
    result: { adequate: floor_load_kpa >= DLC_FLOOR_LOAD, gap_kpa: Math.max(0, DLC_FLOOR_LOAD - floor_load_kpa) },
    unit: "kN/m²", tier: "T3 — structural engineering guidance" };

  // C08: TUE vs PUE comparison
  const dlc_pue = 1.15; // T3 — achievable with DLC
  const tue_factor = 0.85; // T3 — IT equipment effectiveness
  const tue = dlc_pue * tue_factor;
  calcs.tue = { id:"C08", label:"TUE vs PUE Analysis",
    formula: "TUE = PUE × IT effectiveness factor. Reveals what PUE hides.",
    inputs: { current_pue: pue, dlc_pue, tue_factor },
    result: { current_pue: pue, target_pue: dlc_pue, tue, pue_saving: Math.round((pue - dlc_pue) * 100) / 100 },
    unit: "PUE / TUE", tier: "T3 — The Green Grid TUE metric" };

  // C09: MIC impact of DLC pods
  const new_it_mw = (air_racks * kw_per_rack + dlc_rack_count * target_kw_rack) / 1000;
  const new_facility_mw = new_it_mw * dlc_pue;
  const mic_mw = mic_mva * 0.9;
  calcs.mic_impact = { id:"C09", label:"MIC Impact of DLC Deployment",
    formula: "(Air racks × current kW + DLC racks × target kW) × DLC PUE vs MIC",
    inputs: { new_it_mw: Math.round(new_it_mw * 10) / 10, new_facility_mw: Math.round(new_facility_mw * 10) / 10, mic_mw },
    result: { adequate: new_facility_mw <= mic_mw, utilisation_pct: Math.round(new_facility_mw / mic_mw * 100) },
    unit: "MW", tier: "Derived" };

  // C10: Retrofit business case
  const current_annual = it_load_mw * pue * 1000 * 8760 * ELEC_PRICE;
  const future_annual = new_it_mw * dlc_pue * 1000 * 8760 * ELEC_PRICE;
  const energy_saving = current_annual - future_annual;
  const dlc_capex = dlc_rack_count * target_kw_rack * 200; // €200/kW DLC hardware (T3)
  calcs.business_case = { id:"C10", label:"DLC Retrofit Business Case",
    formula: "Energy saving = (current − future) annual cost. Payback = CAPEX / saving",
    inputs: { current_annual: Math.round(current_annual), future_annual: Math.round(future_annual), dlc_capex },
    result: { saving_eur: Math.round(energy_saving), capex: dlc_capex, payback_years: energy_saving > 0 ? Math.round(dlc_capex / energy_saving * 10) / 10 : 999 },
    unit: "€/yr", tier: "T3 — CoolIT/Vertiv published",
    caveat: "Screening-level. Revenue from increased density not included." };

  return calcs;
}
```

---

## FINDINGS_ENGINE (6 findings)

```javascript
function runFindingsEngine(calcs) {
  const findings = [];

  findings.push({ id:"F01", category:"Cooling", title:"Air Cooling Limit",
    status: calcs.air_limit.result.requires_dlc ? "RED" : "GREEN",
    current: `Target ${calcs.air_limit.inputs.target_kw_rack} kW/rack`,
    required: `≤${calcs.air_limit.inputs.limit} kW for air cooling`,
    gap: calcs.air_limit.result.requires_dlc ? "Exceeds air cooling — DLC required" : "Air cooling sufficient",
    action: calcs.air_limit.result.requires_dlc ? "Direct liquid cooling (DLC) deployment required" : "Air cooling adequate" });

  findings.push({ id:"F02", category:"Distribution", title:"Rack Power Distribution",
    status: calcs.power_dist.result.adequate ? "GREEN" : "RED",
    current: `${calcs.power_dist.inputs.current_whip_kw} kW/rack available`,
    required: `${calcs.power_dist.inputs.target_kw_rack} kW/rack target`,
    gap: calcs.power_dist.result.adequate ? "Adequate" : "Re-cabling required",
    action: calcs.power_dist.result.adequate ? "No action" : `Upgrade to 3-phase (${calcs.power_dist.result.three_phase_kw} kW available)` });

  findings.push({ id:"F03", category:"Structural", title:"Floor Load Capacity",
    status: calcs.structural.result.adequate ? "GREEN" : "RED",
    current: `${calcs.structural.inputs.current_kpa} kN/m²`,
    required: `${calcs.structural.inputs.required_kpa} kN/m² for DLC racks`,
    gap: calcs.structural.result.adequate ? "Adequate" : `${calcs.structural.result.gap_kpa} kN/m² shortfall`,
    action: calcs.structural.result.adequate ? "No structural work" : "Structural reinforcement required — commission survey" });

  findings.push({ id:"F04", category:"Grid", title:"MIC Impact",
    status: calcs.mic_impact.result.adequate ? (calcs.mic_impact.result.utilisation_pct > 80 ? "AMBER" : "GREEN") : "RED",
    current: `${calcs.mic_impact.result.utilisation_pct}% MIC after DLC deployment`,
    required: "Within MIC capacity", gap: calcs.mic_impact.result.adequate ? "Within limits" : "MIC upgrade required",
    action: calcs.mic_impact.result.adequate ? "Monitor" : "MIC upgrade needed — 52-week+ ESB lead time" });

  const bc = calcs.business_case.result;
  findings.push({ id:"F05", category:"Commercial", title:"DLC Retrofit Payback",
    status: bc.payback_years <= 3 ? "GREEN" : bc.payback_years <= 7 ? "AMBER" : "RED",
    current: `${bc.payback_years} year payback on €${(bc.capex/1e6).toFixed(1)}M`,
    required: "≤3 years for strong case (energy only — excludes density revenue)",
    gap: `Annual energy saving: €${Math.round(bc.saving_eur/1000)}k/yr`,
    action: "Commission Desktop Assessment for full business case including density revenue — €10,000–€15,000" });

  findings.push({ id:"F06", category:"Technology", title:"Cooling Technology Selection",
    status: "AMBER", current: calcs.immersion.result.technology,
    required: "Technology selection based on target density and workload",
    gap: `CDU requirement: ${calcs.cdu_sizing.result.cdus_needed}+1 units`,
    action: "Engage cooling specialist for technology selection and detailed design" });

  const rc = findings.filter(f=>f.status==="RED").length;
  const ac = findings.filter(f=>f.status==="AMBER").length;
  return { findings, summary: { red_count:rc, amber_count:ac, green_count:findings.length-rc-ac, overall: rc>0?"RED":ac>0?"AMBER":"GREEN" } };
}
```

---

## INTERPRETATION_PROMPT

```
You are a high-density cooling specialist working for Legacy Business Engineers Ltd (LBE). Deterministic AI-ready cooling screening results provided. Key concepts: DLC (direct liquid cooling) captures 75% of rack heat, air handles 25%. TUE reveals what PUE hides. ASHRAE TC 9.9 air limit ~25 kW/rack. ≥80 kW/rack → immersion. Fund-manager language. LBE identifies and quantifies. Decision gate: RED/AMBER → Desktop Assessment €10,000–€15,000.
Respond ONLY with JSON: { "executive_summary", "key_findings", "commercial_implications", "recommended_next_step", "caveats" }
```

## GOLDEN TESTS
| # | Scenario | Expected |
|---|----------|----------|
| G1 | 2.4 MW, PUE 1.50, 400 racks, 6kW current, 30kW target, 40 DLC, 5kN/m² floor, 32A/230V, 5 MVA MIC | Air limit RED, power RED, structural RED (5<10), MIC AMBER |
| G2 | 10 MW, PUE 1.25, 500 racks, 20kW, 60kW target, 100 DLC, 15kN/m², 63A/415V, 20 MVA | Air RED (>25), power OK, structural OK, MIC OK |

---
*DC-TOOL-013 Calc Engine v2.0 | 14 April 2026*
""")

with open("tools/DC_TOOL_014_CALC_ENGINE_v2_0.md", "w") as f:
    f.write("""# DC-TOOL-014 CALC ENGINE DEFINITION v2.0
# CRU Readiness Screener
# Source: DC-LEARN-015 (CRU Readiness)

---

## INPUT_SCHEMA

```javascript
const INPUT_SCHEMA = {
  facility_name: { type:"text", label:"Facility Name", required:true },
  location:      { type:"text", label:"Location", required:true, default:"Dublin, Ireland" },
  build_year:    { type:"number", label:"Year Built", required:true, min:1990, max:2026 },
  it_load_mw:    { type:"number", label:"IT Load (MW)", required:true, min:0.1, max:100, step:0.1 },
  pue:           { type:"number", label:"Current PUE", required:true, min:1.0, max:3.0, step:0.01, default:1.50 },
  ppa_pct:       { type:"number", label:"Renewable PPA Coverage (%)", required:true, min:0, max:100, default:0 },
  gen_installed_mw: { type:"number", label:"Installed Generation (MW)", required:true, min:0, max:200, default:0 },
  gen_fuel:      { type:"select", label:"Generation Fuel", required:true, options:[
    {value:"diesel",label:"Diesel"},{value:"gas",label:"Natural Gas"},{value:"hvo",label:"HVO"},{value:"none",label:"No on-site generation"}
  ], default:"none" },
  gen_gas_fraction: { type:"number", label:"Gas Fraction of Generation (%)", required:false, min:0, max:100, default:0 },
  has_bess:      { type:"select", label:"BESS Installed?", required:true, options:[{value:true,label:"Yes"},{value:false,label:"No"}], default:false },
  bess_mw:       { type:"number", label:"BESS Capacity (MW)", required:false, min:0, max:100, default:0 }
};
```

---

## CALC_ENGINE (10 calculations)

```javascript
function runCalcEngine(inputs) {
  const { it_load_mw, pue, ppa_pct, gen_installed_mw, gen_fuel,
          gen_gas_fraction, has_bess, bess_mw } = inputs;

  const calcs = {};
  const CRU_RENEW = 80; const GRID_EF = 0.2241; const GAS_EF = 0.205;
  const CARBON_TAX = 71; const CARBON_TAX_30 = 100; const ELEC_PRICE = 0.12;
  const CRM_PRICE = 149960; const TAX_PUE = 1.3; const EPA_THRESHOLD = 50;

  const facility_mw = it_load_mw * pue;
  const facility_mwh = facility_mw * 8760;
  const it_mwh = it_load_mw * 8760;

  // C01: CRU generation tier
  const tier = facility_mw < 1 ? "Exempt" : facility_mw < 10 ? "Autoproducer (1-10 MVA)" : "Full Generation Licence";
  calcs.cru_tier = { id:"C01", label:"CRU Generation Tier",
    formula: "Facility MVA: <1 exempt, 1-10 autoproducer, >10 full licence",
    inputs: { facility_mw }, result: { tier, requires_licence: facility_mw >= 10 },
    unit: "MVA", tier: "T1 — CRU" };

  // C02: Renewable PPA gap
  const gap_pct = Math.max(0, CRU_RENEW - ppa_pct);
  const gap_mwh = facility_mwh * gap_pct / 100;
  const ppa_cost_low = gap_mwh * 75 / 1e6;
  const ppa_cost_high = gap_mwh * 95 / 1e6;
  calcs.renewable_gap = { id:"C02", label:"CRU Renewable Energy Gap",
    formula: "80% − PPA%. Gap MWh = facility × gap%. Cost = MWh × €75–95/MWh",
    inputs: { ppa_pct, cru_target: CRU_RENEW, facility_mwh: Math.round(facility_mwh) },
    result: { gap_pct, gap_mwh: Math.round(gap_mwh), compliant: ppa_pct >= CRU_RENEW, cost_low: Math.round(ppa_cost_low * 1e6), cost_high: Math.round(ppa_cost_high * 1e6) },
    unit: "% / MWh / €", tier: "T1 — CRU/2025236, T3 — PPA pricing" };

  // C03: SEM revenue potential
  const gen_mw = gen_installed_mw > 0 ? gen_installed_mw : facility_mw * 0.95;
  const crm_low = gen_mw * 30000; const crm_high = gen_mw * 70000;
  const ds3_low = gen_mw * 0.5 * 15000; const ds3_high = gen_mw * 0.5 * 25000;
  calcs.sem_revenue = { id:"C03", label:"SEM Revenue Potential",
    formula: "CRM: gen MW × €30K–70K. DS3: gen MW × 0.5 × €15K–25K",
    inputs: { gen_mw: Math.round(gen_mw * 10) / 10, crm_price: CRM_PRICE },
    result: { crm_low, crm_high, ds3_low, ds3_high, total_low: crm_low + ds3_low, total_high: crm_high + ds3_high },
    unit: "€/yr", tier: "T1 — SEMO PCAR2829T-4, T3 — DS3 estimate" };

  // C04: Carbon trajectory (Scope 2 + Scope 1)
  const scope2 = facility_mwh * 1000 * GRID_EF / 1e6; // MWh × kgCO2/kWh / 1000
  const gas_fraction = gen_gas_fraction / 100;
  const gas_mwh = gen_fuel === "gas" ? facility_mwh * gas_fraction : 0;
  const scope1_gas = gas_mwh * GAS_EF; // tCO2 (approximation)
  calcs.carbon = { id:"C04", label:"Carbon Trajectory",
    formula: "Scope 2 = facility MWh × grid EF. Scope 1 = gas MWh × gas EF.",
    inputs: { facility_mwh: Math.round(facility_mwh), grid_ef: GRID_EF, gas_ef: GAS_EF },
    result: { scope2_tonnes: Math.round(scope2), scope1_tonnes: Math.round(scope1_gas), total: Math.round(scope2 + scope1_gas), tax_current: Math.round((scope2 + scope1_gas) * CARBON_TAX), tax_2030: Math.round((scope2 + scope1_gas) * CARBON_TAX_30) },
    unit: "tCO₂/yr", tier: "T1 — SEAI 2026" };

  // C05: EPA check
  const gen_thermal = gen_installed_mw / 0.40;
  calcs.epa = { id:"C05", label:"EPA IE Licence Check",
    formula: "Gen MW / 0.40 efficiency = MWth. ≥50 MWth → IE Licence",
    inputs: { gen_installed_mw, efficiency: 0.40 },
    result: { thermal_mw: Math.round(gen_thermal * 10) / 10, exceeds: gen_thermal >= EPA_THRESHOLD },
    unit: "MWth", tier: "T1 — EPA" };

  // C06: EU Taxonomy PUE check
  calcs.taxonomy = { id:"C06", label:"EU Taxonomy PUE",
    formula: "PUE ≤ 1.3", inputs: { pue, threshold: TAX_PUE },
    result: { aligned: pue <= TAX_PUE, gap: Math.round((pue - TAX_PUE) * 100) / 100 },
    unit: "PUE", tier: "T1 — Delegated Act 2021/2139" };

  // C07: BESS opportunity
  const bess_target = Math.max(2, Math.round(facility_mw * 0.3));
  const bess_gap = bess_target - (has_bess ? bess_mw : 0);
  calcs.bess = { id:"C07", label:"BESS Opportunity",
    formula: "Target = max(2, facility MW × 0.3). Gap = target − installed.",
    inputs: { facility_mw, has_bess, bess_mw },
    result: { target: bess_target, installed: has_bess ? bess_mw : 0, gap: Math.max(0, bess_gap) },
    unit: "MW", tier: "T3 — BNEF" };

  // C08: Generation technology comparison
  const gen_options = [
    { name: "Gas CHP", capex_per_mw: 800000, efficiency: 0.85, co2_per_mwh: 0.205 * 1000 / 0.85 },
    { name: "Gas Turbine", capex_per_mw: 600000, efficiency: 0.35, co2_per_mwh: 0.205 * 1000 / 0.35 },
    { name: "BESS", capex_per_mw: 500000, efficiency: 0.90, co2_per_mwh: 0 },
    { name: "Diesel Gen", capex_per_mw: 400000, efficiency: 0.40, co2_per_mwh: 2.68 * 0.27 * 1000 }
  ];
  calcs.gen_comparison = { id:"C08", label:"Generation Technology Comparison",
    formula: "4-way comparison: Gas CHP, Gas Turbine, BESS, Diesel Gen",
    inputs: { gen_mw: Math.round(gen_mw * 10) / 10 },
    result: gen_options.map(o => ({ ...o, capex: Math.round(o.capex_per_mw * gen_mw), annual_co2: Math.round(o.co2_per_mwh * gen_mw * 200 / 1000) })),
    unit: "€ / tCO₂/yr", tier: "T3 — Jenbacher/Wartsila/BNEF/Caterpillar" };

  // C09: Full compliance programme cost
  const pue_cost = pue > TAX_PUE ? it_load_mw * 1000 * 1100 : 0;
  const ppa_cost = gap_mwh > 0 ? (ppa_cost_low + ppa_cost_high) / 2 * 1e6 : 0;
  const total_programme = pue_cost + ppa_cost;
  calcs.programme_cost = { id:"C09", label:"Full CRU Compliance Programme Cost",
    formula: "PUE retrofit + PPA procurement (annual) + generation",
    inputs: { pue_retrofit: pue_cost, ppa_annual: Math.round(ppa_cost) },
    result: { total_capex: pue_cost, annual_ppa: Math.round(ppa_cost), payback_context: "Offset by SEM revenue + energy savings" },
    unit: "€", tier: "T3", caveat: "Screening-level." };

  // C10: CRU readiness score
  let score = 0;
  if (ppa_pct >= CRU_RENEW) score++;
  if (pue <= TAX_PUE) score++;
  if (gen_thermal < EPA_THRESHOLD) score++;
  if (gen_fuel !== "diesel") score++;
  if (has_bess) score++;
  calcs.readiness_score = { id:"C10", label:"CRU Readiness Score",
    formula: "5 criteria: PPA ≥80%, PUE ≤1.3, EPA clear, non-diesel gen, BESS installed",
    inputs: { criteria: 5 },
    result: { score, total: 5, pct: Math.round(score / 5 * 100) },
    unit: "/ 5", tier: "Derived" };

  return calcs;
}
```

---

## FINDINGS_ENGINE (6 findings)

```javascript
function runFindingsEngine(calcs) {
  const findings = [];

  findings.push({ id:"F01", category:"CRU", title:"Renewable PPA Coverage",
    status: calcs.renewable_gap.result.compliant ? "GREEN" : calcs.renewable_gap.result.gap_pct > 40 ? "RED" : "AMBER",
    current: `${calcs.renewable_gap.inputs.ppa_pct}% renewable`,
    required: "80% (CRU/2025236)", gap: calcs.renewable_gap.result.compliant ? "Compliant" : `${calcs.renewable_gap.result.gap_pct}% gap`,
    action: calcs.renewable_gap.result.compliant ? "Maintain" : `Procure PPA: €${Math.round(calcs.renewable_gap.result.cost_low/1000)}k–€${Math.round(calcs.renewable_gap.result.cost_high/1000)}k/yr` });

  findings.push({ id:"F02", category:"Compliance", title:"EU Taxonomy PUE",
    status: calcs.taxonomy.result.aligned ? "GREEN" : "RED",
    current: `PUE ${calcs.taxonomy.inputs.pue}`, required: "≤1.3",
    gap: calcs.taxonomy.result.aligned ? "Aligned" : `Gap ${calcs.taxonomy.result.gap}`,
    action: calcs.taxonomy.result.aligned ? "Document" : "Cooling retrofit required" });

  findings.push({ id:"F03", category:"Regulatory", title:"EPA IE Licence",
    status: calcs.epa.result.exceeds ? "RED" : calcs.epa.result.thermal_mw > 40 ? "AMBER" : "GREEN",
    current: `${calcs.epa.result.thermal_mw} MWth`, required: "<50 MWth",
    gap: calcs.epa.result.exceeds ? "Above threshold" : "Below",
    action: calcs.epa.result.exceeds ? "EPA IE Licence application required" : "Monitor" });

  findings.push({ id:"F04", category:"Commercial", title:"SEM Revenue Opportunity",
    status: calcs.sem_revenue.result.total_high > 500000 ? "GREEN" : "AMBER",
    current: `€${Math.round(calcs.sem_revenue.result.total_low/1000)}k–€${Math.round(calcs.sem_revenue.result.total_high/1000)}k/yr potential`,
    required: "CRM + DS3 revenue stream", gap: "Revenue opportunity — requires generation licence + dispatch capability",
    action: "Evaluate SEM participation — commission energy trading assessment" });

  findings.push({ id:"F05", category:"Carbon", title:"Carbon Tax Trajectory",
    status: calcs.carbon.result.tax_2030 > 500000 ? "RED" : calcs.carbon.result.tax_2030 > 100000 ? "AMBER" : "GREEN",
    current: `€${calcs.carbon.result.tax_current.toLocaleString()}/yr (2025)`,
    required: `€${calcs.carbon.result.tax_2030.toLocaleString()}/yr (2030)`,
    gap: `${calcs.carbon.result.total} tCO₂/yr total`, action: "PPA + PUE retrofit reduces Scope 2. Fuel switch reduces Scope 1." });

  const score = calcs.readiness_score.result;
  findings.push({ id:"F06", category:"Summary", title:"CRU Readiness Score",
    status: score.pct >= 80 ? "GREEN" : score.pct >= 40 ? "AMBER" : "RED",
    current: `${score.score}/${score.total} (${score.pct}%)`, required: "5/5 for full CRU readiness",
    gap: score.score === score.total ? "Fully ready" : `${score.total - score.score} areas need attention`,
    action: score.pct < 80 ? "Commission CRU readiness assessment — €10,000–€15,000" : "Annual compliance review" });

  const rc = findings.filter(f=>f.status==="RED").length;
  const ac = findings.filter(f=>f.status==="AMBER").length;
  return { findings, summary: { red_count:rc, amber_count:ac, green_count:findings.length-rc-ac, overall: rc>0?"RED":ac>0?"AMBER":"GREEN" } };
}
```

---

## INTERPRETATION_PROMPT

```
You are a CRU data centre policy specialist working for Legacy Business Engineers Ltd (LBE). Deterministic CRU readiness screening results provided. Key: CRU renewable obligation 80% (CRU/2025236), EU Taxonomy PUE ≤1.3, EPA 50 MWth, carbon tax €71/€100, CRM €149,960/MW/yr. Use "CRU Readiness" not "CRU Compliance." Fund-manager language. LBE identifies and quantifies. Decision gate: RED/AMBER → Desktop Assessment €10,000–€15,000.
Respond ONLY with JSON: { "executive_summary", "key_findings", "commercial_implications", "recommended_next_step", "caveats" }
```

## GOLDEN TESTS
| # | Scenario | Expected |
|---|----------|----------|
| G1 | 2.4 MW, PUE 1.50, 0% PPA, 0 MW gen, diesel, no BESS | CRU RED (0%), Taxonomy RED, Score 1/5 |
| G2 | 10 MW, PUE 1.25, 85% PPA, 5 MW gas gen, BESS 4 MW | CRU GREEN, Taxonomy GREEN, EPA GREEN, Score 4/5 |

---
*DC-TOOL-014 Calc Engine v2.0 | 14 April 2026*
""")

print("Created 8 Batch 2 calc engine definitions in tools/")
for f in sorted(os.listdir("tools")):
    if "CALC_ENGINE" in f: print(f"  {f}")