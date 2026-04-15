# DC-TOOL-007 CALC ENGINE DEFINITION v2.0
# Regulatory Gap Screener
# Source: DC-LEARN-007 (Regulatory Framework) cascadeCheck functions
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
  ppa_pct:          { type: "number", label: "Renewable PPA Coverage (%)", required: true, min: 0, max: 100, default: 0 },
  // Generator data (for EPA and carbon calcs)
  gen_thermal_mwth: { type: "number", label: "Generator Thermal Input (MWth)", required: true, min: 0, max: 200, default: 0,
                      help: "Total generator fleet MW ÷ 0.40 efficiency" },
  gen_test_hrs_yr:  { type: "number", label: "Annual Generator Test Hours",  required: true, min: 0, max: 500, default: 200 },
  fuel_type:        { type: "select", label: "Generator Fuel",             required: true, options: [
    { value: "diesel", label: "Diesel" },
    { value: "HVO",    label: "HVO" },
    { value: "gas",    label: "Natural Gas" }
  ], default: "diesel" },
  // Refrigerant data (for F-Gas)
  refrigerant_type: { type: "select", label: "Primary Refrigerant",       required: true, options: [
    { value: "R-134a",   label: "R-134a (GWP 1,430)" },
    { value: "R-410A",   label: "R-410A (GWP 2,088)" },
    { value: "R-407C",   label: "R-407C (GWP 1,774)" },
    { value: "R-32",     label: "R-32 (GWP 675)" },
    { value: "R-1234ze", label: "R-1234ze (GWP 7)" },
    { value: "R-290",    label: "R-290 Propane (GWP 3)" },
    { value: "other",    label: "Other (specify GWP below)" }
  ], default: "R-134a" },
  refrigerant_gwp:  { type: "number", label: "Refrigerant GWP (if Other)", required: false, min: 1, max: 5000, default: 1430 },
  refrigerant_charge_kg: { type: "number", label: "Total Refrigerant Charge (kg)", required: true, min: 0, max: 50000, default: 0,
                           help: "If unknown, estimate: cooling MW × 120 kg/MW" },
  // Planning
  planning_sid:     { type: "select", label: "Above 50 MW IT?",           required: true, options: [
    { value: true,  label: "Yes — 50+ MW IT" },
    { value: false, label: "No — below 50 MW IT" }
  ], default: false }
};
```

---

## CALC_ENGINE (15 calculations)

```javascript
function runCalcEngine(inputs) {
  const { it_load_mw, pue, ppa_pct, gen_thermal_mwth, gen_test_hrs_yr,
          fuel_type, refrigerant_type, refrigerant_gwp, refrigerant_charge_kg,
          planning_sid, build_year } = inputs;

  const calcs = {};

  // === CANONICAL CONSTANTS (T1) ===
  const GRID_EF       = 0.2241;  // kgCO₂/kWh — SEAI 2026
  const CARBON_TAX    = 71;      // €/tCO₂ — Budget 2025
  const CARBON_TAX_30 = 100;     // €/tCO₂ — Finance Act 2030
  const ELEC_PRICE    = 0.12;    // €/kWh — CRU Q4 2024
  const TAX_PUE       = 1.3;     // EU Taxonomy threshold
  const CRU_RENEW     = 80;      // % — CRU/2025236
  const EED_THRESHOLD = 1;       // MW IT — EED Art 26
  const EPA_THRESHOLD = 50;      // MWth — EPA IE Licence
  const FGAS_REPORT   = 50;      // tCO₂eq — F-Gas reporting threshold
  const SID_THRESHOLD = 50;      // MW IT — Strategic Infrastructure Development
  const CRREM_BAND    = 300;     // kgCO₂/MWh_IT — LBE-derived (T3/T4, no official CRREM DC pathway)
  const FREE_COOL_HRS = 7200;    // hrs/yr <18°C — Met Éireann 30-year (T1)

  // GWP lookup
  const GWP_MAP = { "R-134a": 1430, "R-410A": 2088, "R-407C": 1774, "R-32": 675, "R-1234ze": 7, "R-290": 3 };
  const gwp = refrigerant_type === "other" ? refrigerant_gwp : (GWP_MAP[refrigerant_type] || refrigerant_gwp);

  // === CALCULATIONS ===

  // C01: EED Art 26 applicability
  calcs.eed_art26 = {
    id: "C01", label: "EED Article 26 Applicability",
    formula: "IT Load ≥ 1 MW → EED Art 26 reporting required",
    inputs: { it_load_mw, threshold: EED_THRESHOLD },
    result: { applies: it_load_mw >= EED_THRESHOLD, it_mw: it_load_mw },
    unit: "MW", tier: "T1 — EED 2023/1791 Art 26"
  };

  // C02: EPA IE Licence trigger
  calcs.epa_licence = {
    id: "C02", label: "EPA IE Licence Threshold",
    formula: "Generator thermal input ≥ 50 MWth → IE Licence required",
    inputs: { gen_thermal_mwth, threshold: EPA_THRESHOLD },
    result: { applies: gen_thermal_mwth >= EPA_THRESHOLD, thermal_mw: gen_thermal_mwth },
    unit: "MWth", tier: "T1 — EPA Industrial Emissions Directive"
  };

  // C03: EU Taxonomy PUE gap
  const pue_gap = pue - TAX_PUE;
  const overhead_kw = it_load_mw * 1000 * Math.max(0, pue_gap);
  const overhead_annual_kwh = overhead_kw * 8760;
  const overhead_cost = overhead_annual_kwh * ELEC_PRICE;
  calcs.taxonomy_pue = {
    id: "C03", label: "EU Taxonomy PUE Gap",
    formula: "PUE − 1.3 = gap. Overhead kW = IT × gap. Annual cost = kW × 8760 × €0.12",
    inputs: { pue, threshold: TAX_PUE, it_load_mw, elec_price: ELEC_PRICE },
    result: {
      gap: Math.round(pue_gap * 100) / 100,
      aligned: pue <= TAX_PUE,
      overhead_kw: Math.round(overhead_kw),
      annual_excess_kwh: Math.round(overhead_annual_kwh),
      annual_cost: Math.round(overhead_cost)
    },
    unit: "PUE / kW / €", tier: "T1 — Delegated Act 2021/2139"
  };

  // C04: Scope 2 carbon (grid electricity)
  const facility_kwh_yr = it_load_mw * 1000 * pue * 8760;
  const scope2_tonnes = facility_kwh_yr * GRID_EF / 1000;
  const it_mwh_yr = it_load_mw * 1000 * 8760 / 1000;
  calcs.scope2_carbon = {
    id: "C04", label: "Scope 2 Carbon Emissions",
    formula: "IT × PUE × 8760 × grid EF = tCO₂/yr",
    inputs: { it_load_mw, pue, grid_ef: GRID_EF },
    result: {
      facility_mwh_yr: Math.round(facility_kwh_yr / 1000),
      scope2_tonnes: Math.round(scope2_tonnes),
      it_mwh_yr: Math.round(it_mwh_yr)
    },
    unit: "tCO₂/yr", tier: "T1 — SEAI 2026"
  };

  // C05: SFDR reporting obligation
  calcs.sfdr = {
    id: "C05", label: "SFDR Reporting Obligation",
    formula: "Any DC with measurable Scope 2 → SFDR reporting applies (fund-level)",
    inputs: { scope2_tonnes: Math.round(scope2_tonnes) },
    result: { tonnes: Math.round(scope2_tonnes), reporting_required: true },
    unit: "tCO₂/yr", tier: "T1 — SFDR Regulation (EU) 2019/2088"
  };

  // C06: F-Gas CO₂ equivalent
  const charge_kg = refrigerant_charge_kg > 0 ? refrigerant_charge_kg :
                    (it_load_mw * (pue - 1) * 120); // estimate if not provided
  const co2eq_tonnes = charge_kg * gwp / 1000;
  calcs.fgas = {
    id: "C06", label: "F-Gas Refrigerant CO₂ Equivalent",
    formula: "Charge (kg) × GWP ÷ 1000 = tCO₂eq",
    inputs: { charge_kg: Math.round(charge_kg), gwp, refrigerant_type, threshold: FGAS_REPORT },
    result: {
      co2eq_tonnes: Math.round(co2eq_tonnes),
      exceeds_threshold: co2eq_tonnes >= FGAS_REPORT,
      phase_down_risk: gwp > 750 ? "HIGH" : gwp > 150 ? "MEDIUM" : "LOW"
    },
    unit: "tCO₂eq",
    tier: "T1 — Regulation (EU) 2024/573"
  };

  // C07: Planning route
  calcs.planning = {
    id: "C07", label: "Planning Route Determination",
    formula: "≥50 MW IT → SID via An Bord Pleanála. <50 MW → local authority",
    inputs: { it_load_mw, threshold: SID_THRESHOLD, planning_sid },
    result: {
      route: it_load_mw >= SID_THRESHOLD ? "SID (An Bord Pleanála)" : "Local Authority",
      sid_applies: it_load_mw >= SID_THRESHOLD
    },
    unit: "", tier: "T1 — Planning and Development Act"
  };

  // C08: CRREM carbon intensity
  const carbon_intensity = scope2_tonnes / it_mwh_yr * 1000; // kgCO₂/MWh_IT
  calcs.crrem = {
    id: "C08", label: "CRREM Carbon Intensity",
    formula: "Scope 2 (tCO₂) ÷ IT MWh × 1000 = kgCO₂/MWh_IT vs 300 pathway",
    inputs: { scope2_tonnes: Math.round(scope2_tonnes), it_mwh_yr: Math.round(it_mwh_yr), pathway: CRREM_BAND },
    result: {
      intensity: Math.round(carbon_intensity),
      pathway: CRREM_BAND,
      aligned: carbon_intensity <= CRREM_BAND,
      gap_pct: Math.round(((carbon_intensity - CRREM_BAND) / CRREM_BAND) * 100)
    },
    unit: "kgCO₂/MWh_IT",
    tier: "T3/T4 — LBE-derived CRREM DC pathway (not published by CRREM Foundation)",
    disclosure: "CRREM v2.01 does not include a published data centre pathway. The 300 kgCO₂/MWh_IT band is LBE-derived."
  };

  // C09: Carbon tax exposure
  calcs.carbon_tax = {
    id: "C09", label: "Carbon Tax Exposure (Scope 1 — generators)",
    formula: "Generator test fuel CO₂ × carbon tax rate",
    inputs: { gen_thermal_mwth, gen_test_hrs_yr, fuel_type, carbon_tax: CARBON_TAX, carbon_tax_2030: CARBON_TAX_30 },
    result: (() => {
      // Scope 1 from generator testing
      const gen_mw = gen_thermal_mwth * 0.40; // back to electrical
      const fuel_l_yr = gen_mw * 1000 * 0.27 * gen_test_hrs_yr;
      const co2_t = fuel_type === "HVO" ? fuel_l_yr * 2.68 / 1000 * 0.10 :
                    fuel_type === "gas" ? gen_mw * 1000 * 0.205 * gen_test_hrs_yr / 1000 :
                    fuel_l_yr * 2.68 / 1000;
      return {
        scope1_tonnes: Math.round(co2_t),
        tax_current: Math.round(co2_t * CARBON_TAX),
        tax_2030: Math.round(co2_t * CARBON_TAX_30),
        fuel_litres_yr: Math.round(fuel_l_yr)
      };
    })(),
    unit: "tCO₂/yr, €/yr",
    tier: "T1 — Budget 2025, Finance Act, SEAI"
  };

  // C10: CRU renewable gap
  const renewable_gap = CRU_RENEW - ppa_pct;
  const gap_mwh = renewable_gap > 0 ? (facility_kwh_yr / 1000) * (renewable_gap / 100) : 0;
  calcs.cru_renewable = {
    id: "C10", label: "CRU Renewable Energy Gap",
    formula: "80% CRU requirement − current PPA% = gap. Gap MWh = facility MWh × gap%",
    inputs: { ppa_pct, cru_target: CRU_RENEW, facility_mwh: Math.round(facility_kwh_yr / 1000) },
    result: {
      gap_pct: Math.max(0, renewable_gap),
      compliant: ppa_pct >= CRU_RENEW,
      gap_mwh: Math.round(gap_mwh),
      indicative_ppa_cost: Math.round(gap_mwh * 0.08) // €0.08/kWh premium estimate (T3)
    },
    unit: "% / MWh",
    tier: "T1 — CRU/2025236"
  };

  // C11: Estimated PUE improvement cost
  const pue_retrofit_cost_per_kw = { low: 800, high: 1200 }; // €/kW IT — RICS NRM1 DC benchmark (T3)
  const pue_retrofit = pue_gap > 0 ? {
    low: pue_retrofit_cost_per_kw.low * it_load_mw * 1000,
    high: pue_retrofit_cost_per_kw.high * it_load_mw * 1000
  } : null;
  calcs.pue_retrofit_cost = {
    id: "C11", label: "Indicative PUE Retrofit Cost",
    formula: "€800–1,200/kW IT (cooling retrofit to achieve PUE ≤1.3)",
    inputs: { pue_gap: Math.round(pue_gap * 100) / 100, it_load_kw: it_load_mw * 1000 },
    result: pue_retrofit,
    unit: "€",
    tier: "T3 — RICS NRM1 DC benchmarks",
    caveat: "Screening-level estimate. Subject to detailed design."
  };

  // C12: Regulatory compliance score
  let compliant_count = 0;
  let total_regs = 9;
  if (it_load_mw >= EED_THRESHOLD) compliant_count++; // EED — just need to report (awareness)
  if (gen_thermal_mwth < EPA_THRESHOLD) compliant_count++;
  if (pue <= TAX_PUE) compliant_count++;
  compliant_count++; // SFDR — reporting obligation only
  if (co2eq_tonnes < FGAS_REPORT) compliant_count++;
  if (!planning_sid || it_load_mw < SID_THRESHOLD) compliant_count++;
  if (carbon_intensity <= CRREM_BAND) compliant_count++;
  if (scope2_tonnes * CARBON_TAX < 100000) compliant_count++; // carbon tax manageable
  if (ppa_pct >= CRU_RENEW) compliant_count++;
  calcs.compliance_score = {
    id: "C12", label: "Regulatory Compliance Score",
    formula: "Count of regulations where facility meets threshold or gap is minimal",
    inputs: { total_regs },
    result: { score: compliant_count, total: total_regs, pct: Math.round(compliant_count / total_regs * 100) },
    unit: "/ 9", tier: "Derived"
  };

  // C13: Free cooling opportunity
  calcs.free_cooling = {
    id: "C13", label: "Dublin Free Cooling Opportunity",
    formula: "7,200 hrs/yr <18°C × cooling load MW × electricity saved",
    inputs: { free_cool_hrs: FREE_COOL_HRS, cooling_mw: it_load_mw * (pue - 1), elec_price: ELEC_PRICE },
    result: {
      hours_available: FREE_COOL_HRS,
      potential_saving_kwh: Math.round(it_load_mw * (pue - 1) * 1000 * FREE_COOL_HRS * 0.7), // 70% capture rate
      potential_saving_eur: Math.round(it_load_mw * (pue - 1) * 1000 * FREE_COOL_HRS * 0.7 * ELEC_PRICE)
    },
    unit: "kWh/yr, €/yr",
    tier: "T1 (Met Éireann), T3 (capture rate)"
  };

  // C14: 10-year carbon tax trajectory
  const tax_trajectory = [];
  for (let yr = 2026; yr <= 2035; yr++) {
    const rate = 71 + (yr - 2025) * ((100 - 71) / (2030 - 2025)); // linear interpolation
    const capped_rate = Math.min(rate, 100); // cap at €100 target
    tax_trajectory.push({
      year: yr,
      rate: Math.round(capped_rate),
      scope2_cost: Math.round(scope2_tonnes * capped_rate),
      scope1_cost: Math.round(calcs.carbon_tax.result.scope1_tonnes * capped_rate)
    });
  }
  calcs.carbon_trajectory = {
    id: "C14", label: "10-Year Carbon Tax Trajectory",
    formula: "Linear interpolation €71 (2025) → €100 (2030), flat thereafter",
    inputs: { scope2_tonnes: Math.round(scope2_tonnes), scope1_tonnes: calcs.carbon_tax.result.scope1_tonnes },
    result: { trajectory: tax_trajectory },
    unit: "€/yr",
    tier: "T1 — Finance Act"
  };

  // C15: Total annual regulatory cost exposure
  const total_reg_cost = calcs.taxonomy_pue.result.annual_cost +
                         calcs.carbon_tax.result.tax_current +
                         calcs.cru_renewable.result.indicative_ppa_cost;
  calcs.total_reg_exposure = {
    id: "C15", label: "Total Annual Regulatory Cost Exposure",
    formula: "PUE excess cost + carbon tax + PPA premium",
    inputs: { pue_cost: calcs.taxonomy_pue.result.annual_cost,
              carbon_tax: calcs.carbon_tax.result.tax_current,
              ppa_premium: calcs.cru_renewable.result.indicative_ppa_cost },
    result: total_reg_cost,
    unit: "€/yr", tier: "Derived",
    caveat: "Screening-level aggregation. Individual items subject to detailed assessment."
  };

  return calcs;
}
```

---

## FINDINGS_ENGINE (9 findings)

```javascript
function runFindingsEngine(calcs) {
  const findings = [];

  // F1: EED Art 26
  const eed = calcs.eed_art26.result;
  findings.push({
    id: "F01", category: "Reporting", title: "EED Article 26 Reporting",
    status: eed.applies ? "AMBER" : "GREEN",
    current: `${eed.it_mw} MW IT load`,
    required: "≥1 MW → energy efficiency reporting required by June 2025",
    gap: eed.applies ? "Reporting obligation — verify submission status" : "Below threshold",
    action: eed.applies ? "Confirm EED Art 26 reporting submitted or in preparation" : "No action"
  });

  // F2: EPA IE Licence
  const epa = calcs.epa_licence.result;
  findings.push({
    id: "F02", category: "Regulatory", title: "EPA IE Licence",
    status: epa.applies ? "RED" : epa.thermal_mw > 40 ? "AMBER" : "GREEN",
    current: `${epa.thermal_mw} MWth generator thermal input`,
    required: "<50 MWth (EPA Industrial Emissions threshold)",
    gap: epa.applies ? `${(epa.thermal_mw - 50).toFixed(1)} MWth above threshold` : "Below",
    action: epa.applies ? "EPA IE Licence application required — 12+ month process" :
            epa.thermal_mw > 40 ? "Approaching threshold — monitor with fleet expansion" : "No action"
  });

  // F3: EU Taxonomy PUE
  const tax = calcs.taxonomy_pue.result;
  findings.push({
    id: "F03", category: "Compliance", title: "EU Taxonomy PUE Alignment",
    status: tax.aligned ? "GREEN" : tax.gap > 0.3 ? "RED" : "AMBER",
    current: `PUE ${calcs.taxonomy_pue.inputs.pue}`,
    required: "PUE ≤1.3 (Delegated Act 2021/2139)",
    gap: tax.aligned ? "Aligned" : `PUE gap ${tax.gap}. Excess overhead: ${tax.overhead_kw} kW costing €${Math.round(tax.annual_cost/1000)}k/yr`,
    action: tax.aligned ? "Taxonomy-aligned — document for investor reporting" :
            "Cooling system retrofit required to achieve PUE ≤1.3"
  });

  // F4: F-Gas risk
  const fgas = calcs.fgas.result;
  findings.push({
    id: "F04", category: "Regulatory", title: "F-Gas Phase-Down Risk",
    status: fgas.phase_down_risk === "HIGH" ? "RED" : fgas.phase_down_risk === "MEDIUM" ? "AMBER" : "GREEN",
    current: `${fgas.co2eq_tonnes} tCO₂eq (${calcs.fgas.inputs.refrigerant_type}, GWP ${calcs.fgas.inputs.gwp})`,
    required: fgas.exceeds_threshold ? "Above 50 tCO₂eq reporting threshold" : "Below reporting threshold",
    gap: fgas.phase_down_risk === "HIGH" ? "High-GWP refrigerant — EU 2024/573 phase-down applies" :
         fgas.phase_down_risk === "MEDIUM" ? "Medium-GWP — monitor phase-down schedule" : "Low-GWP — compliant",
    action: fgas.phase_down_risk === "HIGH" ? "Plan refrigerant transition — 3–5 year replacement cycle" :
            fgas.phase_down_risk === "MEDIUM" ? "Monitor EU F-Gas phase-down schedule" : "No action"
  });

  // F5: CRREM misalignment
  const crrem = calcs.crrem.result;
  findings.push({
    id: "F05", category: "ESG", title: "CRREM Misalignment Risk",
    status: crrem.aligned ? "GREEN" : crrem.gap_pct > 30 ? "RED" : "AMBER",
    current: `${crrem.intensity} kgCO₂/MWh_IT`,
    required: `≤${crrem.pathway} kgCO₂/MWh_IT (LBE-derived pathway)`,
    gap: crrem.aligned ? "Aligned" : `${crrem.gap_pct}% above pathway — Misalignment Year risk`,
    action: crrem.aligned ? "Document alignment for SFDR/fund reporting" :
            "PUE improvement + renewable PPA required to close CRREM gap",
    disclosure: "CRREM v2.01 does not include a published DC pathway. Band is LBE-derived (T3/T4)."
  });

  // F6: CRU renewable obligation
  const cru = calcs.cru_renewable.result;
  findings.push({
    id: "F06", category: "Regulatory", title: "CRU Renewable Energy Obligation",
    status: cru.compliant ? "GREEN" : cru.gap_pct > 40 ? "RED" : "AMBER",
    current: `${calcs.cru_renewable.inputs.ppa_pct}% renewable`,
    required: "80% (CRU/2025236)",
    gap: cru.compliant ? "Compliant" : `${cru.gap_pct}% gap = ${cru.gap_mwh.toLocaleString()} MWh uncovered`,
    action: cru.compliant ? "Maintain PPA coverage" :
            `Procure ${cru.gap_mwh.toLocaleString()} MWh PPA — indicative premium €${Math.round(cru.indicative_ppa_cost/1000)}k/yr`
  });

  // F7: Carbon tax trajectory
  const ctax = calcs.carbon_tax.result;
  findings.push({
    id: "F07", category: "Commercial", title: "Carbon Tax Exposure",
    status: ctax.tax_2030 > 100000 ? "RED" : ctax.tax_2030 > 25000 ? "AMBER" : "GREEN",
    current: `€${ctax.tax_current.toLocaleString()}/yr at €71/tCO₂`,
    required: `€${ctax.tax_2030.toLocaleString()}/yr at €100/tCO₂ (2030)`,
    gap: `${ctax.scope1_tonnes} tCO₂/yr Scope 1`,
    action: ctax.scope1_tonnes > 50 ? "Evaluate HVO/gas transition for Scope 1 reduction" : "Monitor"
  });

  // F8: Planning route
  const plan = calcs.planning.result;
  findings.push({
    id: "F08", category: "Regulatory", title: "Planning Route",
    status: plan.sid_applies ? "AMBER" : "GREEN",
    current: plan.route,
    required: plan.sid_applies ? "SID process — longer timeline, additional consultation" : "Standard LA process",
    gap: plan.sid_applies ? "SID route required for ≥50 MW IT" : "Below SID threshold",
    action: plan.sid_applies ? "Engage planning consultants early — SID process 18–24 months" : "Standard planning applies"
  });

  // F9: Overall compliance position
  const score = calcs.compliance_score.result;
  findings.push({
    id: "F09", category: "Summary", title: "Regulatory Compliance Score",
    status: score.pct >= 80 ? "GREEN" : score.pct >= 50 ? "AMBER" : "RED",
    current: `${score.score}/${score.total} (${score.pct}%)`,
    required: "Full compliance across all 9 regulatory domains",
    gap: score.score === score.total ? "Fully compliant" : `${score.total - score.score} area(s) require attention`,
    action: score.pct < 80 ? "Commission comprehensive regulatory gap assessment" :
            "Maintain compliance — annual review recommended"
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
You are a data centre regulatory compliance specialist working for Legacy Business Engineers Ltd (LBE), an independent technical advisory firm.

You have received the results of a deterministic regulatory gap screening covering 9 regulatory domains: EED Art 26, EPA IE Licence, EU Taxonomy, SFDR, F-Gas, Irish Planning, CRREM, Carbon Tax, and CRU Renewable Obligation. All numbers have been calculated by JavaScript — you MUST NOT recalculate or invent any numbers.

RULES:
1. Every number you mention MUST come from the calculations or findings provided. Do not invent.
2. Use fund-manager language — what is the risk, what does it cost, does the 10-year hold thesis work.
3. CRREM DC pathway is LBE-derived (T3/T4). CRREM v2.01 does NOT include a published DC pathway. Always disclose this.
4. Use "Misalignment Year" — NEVER "Stranding Year".
5. CRU renewable obligation: 80% (CRU/2025236). State explicitly whether this is grid or qualifying renewable.
6. All cost figures are screening-level estimates.
7. Decision gate: if overall RED or AMBER → recommend Desktop Assessment (€10,000–€15,000).
8. LBE identifies and quantifies — never suggest LBE will design or deliver solutions.

Respond ONLY with a JSON object:
{
  "executive_summary": "3 sentences. How many regulations fail, total cost exposure, hold thesis impact.",
  "regulatory_matrix": [{"domain": "EED Art 26", "status": "GREEN/AMBER/RED", "summary": "..."}],
  "commercial_implications": "2-3 sentences for the fund manager. Emphasise 2030 trajectory.",
  "recommended_next_step": "One clear recommendation with indicative cost.",
  "caveats": "Standard screening-level caveat plus CRREM disclosure."
}
```

---

## GOLDEN TESTS

| # | Scenario | Key Inputs | Expected Results |
|---|----------|-----------|-----------------|
| G1 | Clonshaugh baseline | 2.4 MW IT, PUE 1.50, 0% PPA, 25 MWth gen, diesel, R-134a 600kg, <50MW | EED AMBER, EPA GREEN, Taxonomy RED (gap 0.20), F-Gas RED (858 tCO₂eq), CRREM ~336 RED, CRU RED (0%), Score ~3/9 |
| G2 | Modern compliant DC | 10 MW IT, PUE 1.25, 85% PPA, 40 MWth gen, HVO, R-1234ze 500kg, <50MW | EED AMBER (report), EPA GREEN, Taxonomy GREEN, F-Gas GREEN, CRREM ~280 GREEN, CRU GREEN, Score ~8/9 |
| G3 | Hyperscale non-compliant | 50 MW IT, PUE 1.60, 20% PPA, 100 MWth gen, diesel, R-410A 5000kg, ≥50MW | EED AMBER, EPA RED, Taxonomy RED, F-Gas RED (10,440t), CRREM RED, CRU RED, Planning SID, Score ~1/9 |

---

*DC-TOOL-007 Calc Engine Definition v2.0 | 14 April 2026*
*Source: DC-LEARN-007 cascadeCheck functions (9 checks)*
*Architecture: deterministic JS → rule-based findings → AI narrative only*
