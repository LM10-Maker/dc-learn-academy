# DC-TOOL-008 CALC ENGINE DEFINITION v2.0
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
