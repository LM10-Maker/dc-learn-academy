# DC-TOOL-001 CALC ENGINE DEFINITION v2.0
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
