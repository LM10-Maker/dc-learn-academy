# DC-TOOL-014 CALC ENGINE DEFINITION v2.0
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
