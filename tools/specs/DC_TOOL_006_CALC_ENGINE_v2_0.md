# DC-TOOL-006 CALC ENGINE DEFINITION v2.0
# Grid Headroom Calculator
# Source: DC-LEARN-006 (Grid Connection) cascadeCheck functions
# Architecture: LLM never calculates. Numbers are JavaScript. Narrative is AI.

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
  target_kw_rack:   { type: "number", label: "Target kW/Rack",            required: true, min: 1, max: 100, default: 20 },
  target_pue:       { type: "number", label: "Target PUE (post-retrofit)", required: true, min: 1.0, max: 2.0, step: 0.01, default: 1.20 },
  // Grid connection
  mic_mva:          { type: "number", label: "MIC (MVA)",                  required: true, min: 0.1, max: 200, step: 0.1, default: 5 },
  grid_voltage:     { type: "select", label: "Grid Voltage",              required: true, options: [
    { value: "10kV",  label: "10 kV (ESB Networks MV)" },
    { value: "20kV",  label: "20 kV (ESB Networks MV)" },
    { value: "38kV",  label: "38 kV (ESB Networks HV)" },
    { value: "110kV", label: "110 kV (EirGrid Transmission)" }
  ], default: "10kV" },
  utility_feeds:    { type: "select", label: "Utility Feed Configuration", required: true, options: [
    { value: "single", label: "Single feed" },
    { value: "dual",   label: "Dual feed" }
  ], default: "single" },
  // Transformer
  tx_count:         { type: "number", label: "Transformer Count",          required: true, min: 1, max: 10, default: 2 },
  tx_rating_mva:    { type: "number", label: "Transformer Rating Each (MVA)", required: true, min: 0.5, max: 50, step: 0.1, default: 2.5 },
  tx_k_factor:      { type: "number", label: "K-Factor Derating",         required: true, min: 0.5, max: 1.0, step: 0.05, default: 0.80 },
  // Generation
  gen_installed_mw: { type: "number", label: "Installed Generation (MW)",  required: true, min: 0, max: 200, default: 0 },
  power_factor:     { type: "number", label: "Site Power Factor",          required: true, min: 0.80, max: 1.0, step: 0.01, default: 0.95 }
};
```

---

## CALC_ENGINE (13 calculations)

```javascript
function runCalcEngine(inputs) {
  const { it_load_mw, pue, racks, target_kw_rack, target_pue,
          mic_mva, grid_voltage, utility_feeds, tx_count, tx_rating_mva,
          tx_k_factor, gen_installed_mw, power_factor } = inputs;

  const calcs = {};

  // Constants (T1 sourced)
  const CRM_PRICE = 149960;        // €/MW/yr — SEMO PCAR2829T-4
  const GEN_LICENCE_MW = 10;       // MW — generation licence threshold

  // --- C01: Current facility demand ---
  const current_mw = it_load_mw * pue;
  calcs.current_demand = {
    id: "C01", label: "Current Facility Demand",
    formula: "IT Load × PUE",
    inputs: { it_load_mw, pue },
    result: current_mw, unit: "MW", tier: "Derived"
  };

  // --- C02: Current demand in MVA ---
  const current_mva = current_mw / power_factor;
  calcs.current_demand_mva = {
    id: "C02", label: "Current Apparent Power Demand",
    formula: "Facility MW ÷ Power Factor",
    inputs: { current_mw, power_factor },
    result: Math.round(current_mva * 10) / 10, unit: "MVA", tier: "Derived"
  };

  // --- C03: Connection tier determination ---
  let connection_tier, timeline, operator;
  if (current_mw <= 5) {
    connection_tier = "MV (10 kV)"; timeline = "6–18 months"; operator = "ESB Networks";
  } else if (current_mw <= 20) {
    connection_tier = "HV (38 kV)"; timeline = "12–36 months"; operator = "ESB Networks";
  } else {
    connection_tier = "Transmission (110 kV)"; timeline = "4–8 years"; operator = "EirGrid";
  }
  calcs.connection_tier = {
    id: "C03", label: "Grid Connection Tier",
    formula: "≤5 MW → MV 10kV; ≤20 MW → HV 38kV; >20 MW → 110kV Transmission",
    inputs: { current_mw },
    result: { tier: connection_tier, timeline, operator },
    unit: "", tier: "T1 — ESB Networks / EirGrid connection policy"
  };

  // --- C04: MIC utilisation ---
  const mic_mw = mic_mva * 0.9; // derated to MW at typical PF
  const mic_utilisation = (current_mw / mic_mw) * 100;
  calcs.mic_utilisation = {
    id: "C04", label: "MIC Utilisation",
    formula: "Demand MW ÷ (MIC MVA × 0.9 PF) × 100",
    inputs: { current_mw, mic_mva, pf: 0.9 },
    result: { utilisation_pct: Math.round(mic_utilisation), available_mw: mic_mw, headroom_mw: Math.round((mic_mw - current_mw) * 10) / 10 },
    unit: "%", tier: "Derived"
  };

  // --- C05: Transformer capacity per path ---
  const tx_per_path_mw = tx_rating_mva * tx_k_factor * power_factor;
  const demand_per_path = current_mw / tx_count;
  const tx_adequate = demand_per_path <= tx_per_path_mw;
  calcs.tx_capacity = {
    id: "C05", label: "Transformer Loading (per path)",
    formula: "TX MVA × K-factor × PF = MW capacity. Demand / TX count = per-path demand",
    inputs: { tx_rating_mva, tx_k_factor, power_factor, tx_count, current_mw },
    result: {
      capacity_mw: Math.round(tx_per_path_mw * 10) / 10,
      demand_per_path_mw: Math.round(demand_per_path * 10) / 10,
      adequate: tx_adequate,
      utilisation_pct: Math.round((demand_per_path / tx_per_path_mw) * 100)
    },
    unit: "MW/path", tier: "Derived"
  };

  // --- C06: N-1 resilience check ---
  // Can the facility survive loss of one feed/transformer?
  const n_minus_1_capacity = (tx_count - 1) * tx_per_path_mw;
  const n_minus_1_ok = current_mw <= n_minus_1_capacity;
  calcs.n_minus_1 = {
    id: "C06", label: "N-1 Transformer Resilience",
    formula: "(TX count − 1) × capacity ≥ Facility demand",
    inputs: { tx_count, tx_per_path_mw, current_mw },
    result: {
      surviving_capacity_mw: Math.round(n_minus_1_capacity * 10) / 10,
      adequate: n_minus_1_ok,
      shortfall_mw: n_minus_1_ok ? 0 : Math.round((current_mw - n_minus_1_capacity) * 10) / 10
    },
    unit: "MW", tier: "Derived"
  };

  // --- C07: Power factor compliance ---
  const pf_compliant = power_factor >= 0.95;
  calcs.power_factor_check = {
    id: "C07", label: "Power Factor Grid Code Compliance",
    formula: "PF ≥ 0.95 (ESB Grid Code / EU Demand Connection Code)",
    inputs: { power_factor, threshold: 0.95 },
    result: { compliant: pf_compliant, current: power_factor },
    unit: "PF", tier: "T1 — ESB Grid Code"
  };

  // --- C08: DCC applicability ---
  const dcc_threshold = 0.25; // MW
  const dcc_applies = current_mw > dcc_threshold;
  calcs.dcc_check = {
    id: "C08", label: "EU Demand Connection Code Applicability",
    formula: "Demand > 0.25 MW → DCC applies",
    inputs: { current_mw, threshold: dcc_threshold },
    result: dcc_applies,
    unit: "boolean", tier: "T1 — EU DCC Regulation"
  };

  // --- C09: Generation licence check ---
  const gen_licence_needed = gen_installed_mw > GEN_LICENCE_MW;
  const crm_revenue = gen_licence_needed ? gen_installed_mw * CRM_PRICE : 0;
  calcs.gen_licence = {
    id: "C09", label: "Generation Licence & CRM Revenue",
    formula: "If installed gen > 10 MW → licence required. Revenue = MW × €149,960/yr",
    inputs: { gen_installed_mw, threshold: GEN_LICENCE_MW, crm_price: CRM_PRICE },
    result: { licence_needed: gen_licence_needed, crm_annual: crm_revenue },
    unit: "€/yr", tier: "T1 — SEMO PCAR2829T-4"
  };

  // --- C10: Future capacity at target density ---
  const future_it_mw = (racks * target_kw_rack) / 1000;
  const future_facility_mw = future_it_mw * target_pue;
  const future_mic_ok = future_facility_mw <= mic_mw;
  calcs.future_capacity = {
    id: "C10", label: "Future Capacity at Target Density",
    formula: "Racks × target_kW/rack ÷ 1000 × target_PUE = future demand",
    inputs: { racks, target_kw_rack, target_pue, mic_mw },
    result: {
      future_it_mw: Math.round(future_it_mw * 10) / 10,
      future_facility_mw: Math.round(future_facility_mw * 10) / 10,
      mic_adequate: future_mic_ok,
      mic_gap_mw: future_mic_ok ? 0 : Math.round((future_facility_mw - mic_mw) * 10) / 10
    },
    unit: "MW", tier: "Derived"
  };

  // --- C11: Future connection tier ---
  let future_tier, future_timeline, future_operator;
  if (future_facility_mw <= 5) {
    future_tier = "MV (10 kV)"; future_timeline = "N/A — current tier"; future_operator = "ESB Networks";
  } else if (future_facility_mw <= 20) {
    future_tier = "HV (38 kV)"; future_timeline = "12–36 months"; future_operator = "ESB Networks";
  } else {
    future_tier = "Transmission (110 kV)"; future_timeline = "4–8 years"; future_operator = "EirGrid";
  }
  calcs.future_connection = {
    id: "C11", label: "Future Grid Connection Requirement",
    formula: "Same thresholds as C03, applied to future demand",
    inputs: { future_facility_mw },
    result: { tier: future_tier, timeline: future_timeline, operator: future_operator,
              tier_change: connection_tier !== future_tier },
    unit: "", tier: "T1 — ESB/EirGrid"
  };

  // --- C12: Indicative MIC upgrade cost ---
  // T3 — ESB Networks published connection costs
  const mic_upgrade_needed = !future_mic_ok;
  const mic_upgrade_cost = mic_upgrade_needed ? {
    low: future_facility_mw <= 20 ? 1500000 : 4000000,
    high: future_facility_mw <= 20 ? 4000000 : 15000000,
    source: "ESB Networks indicative connection charges",
    tier: "T3"
  } : null;
  calcs.mic_upgrade_cost = {
    id: "C12", label: "Indicative MIC Upgrade Cost",
    formula: "Based on connection tier: MV €1.5–4M, HV €4–15M",
    inputs: { mic_upgrade_needed, future_facility_mw },
    result: mic_upgrade_cost,
    unit: "€", tier: mic_upgrade_cost ? mic_upgrade_cost.tier : "N/A",
    caveat: "Subject to ESB Networks/EirGrid connection offer. 52-week+ lead time typical."
  };

  // --- C13: Headroom summary ---
  calcs.headroom_summary = {
    id: "C13", label: "Grid Headroom Summary",
    formula: "MIC headroom now and at target density",
    inputs: { current_mw, future_facility_mw, mic_mw },
    result: {
      current_headroom_mw: Math.round((mic_mw - current_mw) * 10) / 10,
      current_headroom_pct: Math.round(((mic_mw - current_mw) / mic_mw) * 100),
      future_headroom_mw: Math.round((mic_mw - future_facility_mw) * 10) / 10,
      future_headroom_pct: Math.round(((mic_mw - future_facility_mw) / mic_mw) * 100)
    },
    unit: "MW / %", tier: "Derived"
  };

  return calcs;
}
```

---

## FINDINGS_ENGINE (7 findings)

```javascript
function runFindingsEngine(calcs) {
  const findings = [];

  // F1: MIC headroom (current)
  const mic = calcs.mic_utilisation.result;
  findings.push({
    id: "F01", category: "Grid", title: "Current MIC Headroom",
    status: mic.utilisation_pct <= 70 ? "GREEN" : mic.utilisation_pct <= 90 ? "AMBER" : "RED",
    current: `${mic.utilisation_pct}% MIC utilisation (${mic.headroom_mw} MW headroom)`,
    required: "≤70% utilisation recommended for growth",
    gap: mic.utilisation_pct <= 70 ? "Adequate headroom" :
         `${mic.utilisation_pct}% — ${mic.utilisation_pct > 90 ? "critically" : ""} constrained`,
    action: mic.utilisation_pct <= 70 ? "No action" : "Plan MIC upgrade for density growth"
  });

  // F2: Transformer capacity
  const tx = calcs.tx_capacity.result;
  findings.push({
    id: "F02", category: "Electrical", title: "Transformer Loading",
    status: tx.utilisation_pct <= 70 ? "GREEN" : tx.adequate ? "AMBER" : "RED",
    current: `${tx.utilisation_pct}% loaded (${tx.demand_per_path_mw} MW per path)`,
    required: `${tx.capacity_mw} MW per path capacity`,
    gap: tx.adequate ? "Within limits" : `${(tx.demand_per_path_mw - tx.capacity_mw).toFixed(1)} MW overload per path`,
    action: tx.adequate ? "Monitor loading" : "Transformer upgrade required"
  });

  // F3: N-1 resilience
  const n1 = calcs.n_minus_1.result;
  findings.push({
    id: "F03", category: "Electrical", title: "N-1 Transformer Resilience",
    status: n1.adequate ? "GREEN" : "RED",
    current: n1.adequate ? "Facility survives loss of one transformer" : `${n1.shortfall_mw} MW shortfall on loss of one transformer`,
    required: "Full load maintained with one transformer offline",
    gap: n1.adequate ? "None" : `${n1.shortfall_mw} MW gap`,
    action: n1.adequate ? "N-1 resilience confirmed" : "Add transformer capacity or reduce load"
  });

  // F4: Future MIC adequacy
  const fc = calcs.future_capacity.result;
  findings.push({
    id: "F04", category: "Grid", title: "Future Capacity at Target Density",
    status: fc.mic_adequate ? "GREEN" : "RED",
    current: `Target: ${fc.future_facility_mw} MW (${fc.future_it_mw} MW IT at PUE ${calcs.future_capacity.inputs.target_pue})`,
    required: `MIC capacity: ${calcs.mic_utilisation.result.available_mw} MW`,
    gap: fc.mic_adequate ? "MIC adequate for target" : `${fc.mic_gap_mw} MW beyond current MIC`,
    action: fc.mic_adequate ? "MIC adequate — no upgrade needed" :
            "MIC upgrade required — engage ESB Networks early (52-week+ lead time)"
  });

  // F5: Connection tier change
  const ftc = calcs.future_connection.result;
  findings.push({
    id: "F05", category: "Grid", title: "Grid Tier Migration Risk",
    status: ftc.tier_change ? "RED" : "GREEN",
    current: `Current: ${calcs.connection_tier.result.tier}`,
    required: ftc.tier_change ? `Future: ${ftc.tier} (${ftc.operator})` : "No tier change",
    gap: ftc.tier_change ? `Tier change: ${calcs.connection_tier.result.tier} → ${ftc.tier}. Timeline: ${ftc.timeline}` : "None",
    action: ftc.tier_change ? `Critical path item — ${ftc.timeline} timeline for ${ftc.tier} connection` : "No action"
  });

  // F6: Power factor
  const pf = calcs.power_factor_check.result;
  findings.push({
    id: "F06", category: "Grid", title: "Power Factor Compliance",
    status: pf.compliant ? "GREEN" : "AMBER",
    current: `PF ${pf.current}`,
    required: "≥0.95 (ESB Grid Code)",
    gap: pf.compliant ? "Compliant" : `PF ${pf.current} below 0.95 minimum`,
    action: pf.compliant ? "Compliant" : "Install power factor correction equipment"
  });

  // F7: Generation licence / CRM
  const gen = calcs.gen_licence.result;
  findings.push({
    id: "F07", category: "Commercial", title: "Generation Licence & CRM Revenue",
    status: gen.licence_needed ? "AMBER" : "GREEN",
    current: gen.licence_needed ?
      `${calcs.gen_licence.inputs.gen_installed_mw} MW installed — licence required` :
      `${calcs.gen_licence.inputs.gen_installed_mw} MW installed — below threshold`,
    required: ">10 MW installed generation triggers licence requirement",
    gap: gen.licence_needed ? "Licence application needed" : "Below threshold",
    action: gen.licence_needed ?
      `Apply for generation licence. CRM revenue potential: €${(gen.crm_annual/1000).toFixed(0)}k/yr` :
      "No licence needed. Monitor if generation fleet expands."
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
You are a grid connection and electrical distribution specialist working for Legacy Business Engineers Ltd (LBE), an independent technical advisory firm.

You have received the results of a deterministic grid headroom screening. All numbers have been calculated by JavaScript — you MUST NOT recalculate or invent any numbers. Your job is to write a narrative interpretation of the pre-calculated results.

RULES:
1. Every number you mention MUST come from the calculations or findings provided. Do not invent.
2. Use fund-manager language — what is the risk, what does it cost, does the investment thesis work.
3. ESB Networks connection timelines are critical path items — always flag the 52-week+ lead time.
4. All cost figures are screening-level estimates subject to ESB Networks/EirGrid connection offer.
5. Decision gate: if overall RED or AMBER → recommend Desktop Assessment (€10,000–€15,000).
6. LBE identifies and quantifies — never suggest LBE will design or deliver solutions.
7. Voltage levels: ≤5MW → 10kV ESB Networks MV. ≤20MW → 38kV ESB Networks HV. >20MW → 110kV EirGrid.
8. CRM T-4: €149,960/MW/yr (SEMO PCAR2829T-4).

Respond ONLY with a JSON object:
{
  "executive_summary": "3 sentences. Headroom position, growth constraint, investment impact.",
  "key_findings": ["Finding narrative for each finding"],
  "commercial_implications": "2-3 sentences for the fund manager. Emphasise timeline risk.",
  "recommended_next_step": "One clear recommendation with indicative cost.",
  "caveats": "Standard screening-level caveat."
}
```

---

## GOLDEN TESTS

| # | Scenario | Key Inputs | Expected Results |
|---|----------|-----------|-----------------|
| G1 | Clonshaugh baseline | 2.4 MW IT, PUE 1.50, 400 racks, 5 MVA MIC, 10kV, single, 2×2.5 MVA TX, K=0.8, PF 0.95 | 3.6 MW demand, MIC 80% used, 1.9 MW headroom, future 9.6 MW → MIC RED |
| G2 | Well-provisioned | 5 MW IT, PUE 1.25, 200 racks, 20 MVA MIC, 38kV, dual, 4×5 MVA TX, K=0.85 | 6.25 MW, MIC 35%, headroom GREEN, N-1 OK |
| G3 | Growth constrained | 8 MW IT, PUE 1.40, 600 racks, 10 MVA MIC, 10kV, single, 2×5 MVA TX, K=0.80 | 11.2 MW demand > 9 MW MIC → RED, tier change 10kV→38kV |

---

*DC-TOOL-006 Calc Engine Definition v2.0 | 14 April 2026*
*Source: DC-LEARN-006 cascadeCheck functions (9 checks)*
*Architecture: deterministic JS → rule-based findings → AI narrative only*
