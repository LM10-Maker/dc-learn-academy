# DC-TOOL-003 CALC ENGINE DEFINITION v2.0
# Redundancy Gap Tool
# Source: DC-LEARN-003 (Redundancy & Topology) cascadeCheck functions
# Architecture: LLM never calculates. Numbers are JavaScript. Narrative is AI.

---

## INPUT_SCHEMA

```javascript
const INPUT_SCHEMA = {
  // Aligned with DC-Screen field IDs
  facility_name:    { type: "text",   label: "Facility Name",           required: true },
  location:         { type: "text",   label: "Location",                required: true, default: "Dublin, Ireland" },
  build_year:       { type: "number", label: "Year Built",              required: true, min: 1990, max: 2026 },
  it_load_mw:       { type: "number", label: "IT Load (MW)",            required: true, min: 0.1, max: 100, step: 0.1 },
  pue:              { type: "number", label: "Current PUE",             required: true, min: 1.0, max: 3.0, step: 0.01, default: 1.50 },
  target_tier:      { type: "select", label: "Target Uptime Tier",      required: true, options: [
    { value: 1, label: "Tier I — Basic (99.671%)" },
    { value: 2, label: "Tier II — Redundant Components (99.741%)" },
    { value: 3, label: "Tier III — Concurrently Maintainable (99.982%)" },
    { value: 4, label: "Tier IV — Fault Tolerant (99.995%)" }
  ], default: 3 },
  // Infrastructure questions
  ups_modules:      { type: "number", label: "UPS Modules (count)",     required: true, min: 1, max: 20, default: 2 },
  ups_rating_kw:    { type: "number", label: "UPS Rating per Module (kW)", required: true, min: 100, max: 5000, default: 1350 },
  utility_feeds:    { type: "select", label: "Utility Feed Configuration", required: true, options: [
    { value: "single", label: "Single utility feed" },
    { value: "dual",   label: "Dual utility feeds" }
  ], default: "single" },
  msb_config:       { type: "select", label: "MSB Configuration",       required: true, options: [
    { value: "single_bus",   label: "Single bus" },
    { value: "bus_section",  label: "Bus section (split)" },
    { value: "dual_msb",     label: "Dual MSB" }
  ], default: "single_bus" },
  has_mops:         { type: "select", label: "Written MOPs in Place?",  required: true, options: [
    { value: true,  label: "Yes — maintenance procedures documented" },
    { value: false, label: "No — no written procedures" }
  ], default: false },
  cooling_redundancy: { type: "select", label: "Cooling Redundancy",    required: true, options: [
    { value: "N",     label: "N (no redundancy)" },
    { value: "N+1",   label: "N+1" },
    { value: "2N",    label: "2N" },
    { value: "2N+1",  label: "2N+1" }
  ], default: "N+1" },
  generator_config: { type: "select", label: "Generator Configuration", required: true, options: [
    { value: "none",  label: "No on-site generation" },
    { value: "N",     label: "N (no redundancy)" },
    { value: "N+1",   label: "N+1" },
    { value: "2N",    label: "2N" },
    { value: "2N+1",  label: "2N+1" }
  ], default: "N+1" }
};
```

---

## CALC_ENGINE (12 calculations)

All calculations are deterministic JavaScript. No API calls. Instant results.

```javascript
function runCalcEngine(inputs) {
  const { it_load_mw, pue, target_tier, ups_modules, ups_rating_kw,
          utility_feeds, msb_config, has_mops, cooling_redundancy,
          generator_config } = inputs;

  const calcs = {};
  const C = {}; // Constants with tiers

  // --- C1: Facility load ---
  C.it_load_kw = { value: it_load_mw * 1000, tier: "Input", source: "User input" };
  C.pue        = { value: pue,                tier: "Input", source: "User input" };
  calcs.facility_load_kw = {
    id: "C01",
    label: "Total Facility Load",
    formula: "IT Load (kW) × PUE",
    inputs: { it_load_kw: C.it_load_kw.value, pue: C.pue.value },
    result: C.it_load_kw.value * C.pue.value,
    unit: "kW",
    tier: "Derived"
  };

  // --- C2: UPS capacity assessment ---
  const total_ups_kw = ups_modules * ups_rating_kw;
  const n_needed = Math.ceil(C.it_load_kw.value / ups_rating_kw);
  const ups_spare = ups_modules - n_needed;
  calcs.ups_capacity = {
    id: "C02",
    label: "UPS Capacity Assessment",
    formula: "Modules × Rating vs IT Load / Rating (rounded up)",
    inputs: { ups_modules, ups_rating_kw, it_load_kw: C.it_load_kw.value },
    result: { total_kw: total_ups_kw, n_needed, spare_modules: ups_spare },
    unit: "kW / modules",
    tier: "Derived",
    detail: `${ups_modules} × ${ups_rating_kw} kW = ${total_ups_kw} kW. N=${n_needed}, spare=${ups_spare}`
  };

  // --- C3: UPS redundancy level ---
  const ups_redundancy = ups_spare >= n_needed ? "2N" :
                          ups_spare >= 1 ? "N+1" : "N+0";
  calcs.ups_redundancy = {
    id: "C03",
    label: "UPS Redundancy Level",
    formula: "If spare ≥ N → 2N; if spare ≥ 1 → N+1; else N+0",
    inputs: { n_needed, spare_modules: ups_spare },
    result: ups_redundancy,
    unit: "",
    tier: "Derived"
  };

  // --- C4: Path independence ---
  const has_dual_feed = utility_feeds === "dual";
  const has_bus_section = msb_config !== "single_bus";
  const path_count = has_dual_feed && has_bus_section ? 2 : 1;
  calcs.path_independence = {
    id: "C04",
    label: "Electrical Path Independence",
    formula: "Dual feed AND bus section → 2 paths; else 1 path",
    inputs: { utility_feeds, msb_config },
    result: { paths: path_count, dual_feed: has_dual_feed, bus_section: has_bus_section },
    unit: "paths",
    tier: "Derived"
  };

  // --- C5: Concurrent maintainability ---
  const cm_achievable = has_mops && (ups_redundancy === "N+1" || ups_redundancy === "2N") &&
                        (cooling_redundancy === "N+1" || cooling_redundancy === "2N" || cooling_redundancy === "2N+1");
  calcs.concurrent_maintainability = {
    id: "C05",
    label: "Concurrent Maintainability",
    formula: "Requires: written MOPs + UPS ≥ N+1 + Cooling ≥ N+1",
    inputs: { has_mops, ups_redundancy, cooling_redundancy },
    result: cm_achievable,
    unit: "boolean",
    tier: "Derived"
  };

  // --- C6: Fault tolerance ---
  const power_ft = ups_redundancy === "2N" && has_dual_feed;
  const cooling_ft = cooling_redundancy === "2N" || cooling_redundancy === "2N+1";
  const full_ft = power_ft && cooling_ft;
  calcs.fault_tolerance = {
    id: "C06",
    label: "Fault Tolerance Assessment",
    formula: "Power FT = 2N UPS + dual feed. Cooling FT = 2N/2N+1. Full = both",
    inputs: { ups_redundancy, utility_feeds, cooling_redundancy },
    result: { power_ft, cooling_ft, full_ft },
    unit: "boolean",
    tier: "Derived"
  };

  // --- C7: SPOF count ---
  let spof_count = 0;
  const spofs = [];
  if (!has_dual_feed) { spof_count++; spofs.push("Single utility feed"); }
  if (msb_config === "single_bus") { spof_count++; spofs.push("Single bus MSB"); }
  if (ups_redundancy === "N+0") { spof_count++; spofs.push("No UPS redundancy"); }
  if (cooling_redundancy === "N") { spof_count++; spofs.push("No cooling redundancy"); }
  if (generator_config === "none") { spof_count++; spofs.push("No on-site generation"); }
  if (generator_config === "N") { spof_count++; spofs.push("No generator redundancy"); }
  if (!has_mops) { spof_count++; spofs.push("No written MOPs"); }
  calcs.spof_count = {
    id: "C07",
    label: "Single Points of Failure (SPOF) Count",
    formula: "Count of: single feed, single bus, N+0 UPS, N cooling, no gen, N gen, no MOPs",
    inputs: { utility_feeds, msb_config, ups_redundancy, cooling_redundancy, generator_config, has_mops },
    result: { count: spof_count, items: spofs },
    unit: "SPOFs",
    tier: "Derived"
  };

  // --- C8: Actual achieved tier ---
  let actual_tier;
  if (full_ft && cm_achievable && spof_count === 0) actual_tier = 4;
  else if (cm_achievable && path_count >= 1 && spof_count <= 1) actual_tier = 3;
  else if (ups_redundancy !== "N+0" && (cooling_redundancy !== "N")) actual_tier = 2;
  else actual_tier = 1;
  calcs.actual_tier = {
    id: "C08",
    label: "Actual Achieved Tier",
    formula: "Tier IV = full FT + CM + 0 SPOFs. III = CM + ≤1 SPOF. II = redundant components. I = basic",
    inputs: { full_ft, cm_achievable, spof_count, ups_redundancy, cooling_redundancy, path_count },
    result: actual_tier,
    unit: "Tier",
    tier: "Derived"
  };

  // --- C9: Tier gap ---
  const tier_gap = target_tier - actual_tier;
  calcs.tier_gap = {
    id: "C09",
    label: "Tier Gap",
    formula: "Target Tier − Actual Tier",
    inputs: { target_tier, actual_tier },
    result: tier_gap,
    unit: "tiers",
    tier: "Derived"
  };

  // --- C10: Availability numbers ---
  const availability_map = { 1: 99.671, 2: 99.741, 3: 99.982, 4: 99.995 };
  const annual_hours = 8760;
  const current_downtime_hrs = annual_hours * (1 - availability_map[actual_tier] / 100);
  const target_downtime_hrs = annual_hours * (1 - availability_map[target_tier] / 100);
  calcs.availability = {
    id: "C10",
    label: "Availability & Downtime",
    formula: "Downtime = 8760 × (1 − availability%/100)",
    inputs: { actual_tier, target_tier },
    result: {
      current_availability: availability_map[actual_tier],
      target_availability: availability_map[target_tier],
      current_downtime_hrs: Math.round(current_downtime_hrs * 10) / 10,
      target_downtime_hrs: Math.round(target_downtime_hrs * 10) / 10,
      downtime_improvement_hrs: Math.round((current_downtime_hrs - target_downtime_hrs) * 10) / 10
    },
    unit: "% / hours",
    tier: "T1 — Uptime Institute Tier Standard"
  };

  // --- C11: Indicative upgrade cost range ---
  // T3 sourced from Uptime Institute / RICS NRM1 benchmarks
  const upgrade_cost_ranges = {
    "1_to_2": { low: 200, high: 400, source: "Uptime Institute / RICS NRM1 DC benchmarks", tier: "T3" },
    "1_to_3": { low: 800, high: 1500, source: "Uptime Institute / RICS NRM1 DC benchmarks", tier: "T3" },
    "1_to_4": { low: 1800, high: 3500, source: "Uptime Institute / RICS NRM1 DC benchmarks", tier: "T3" },
    "2_to_3": { low: 500, high: 1000, source: "Uptime Institute / RICS NRM1 DC benchmarks", tier: "T3" },
    "2_to_4": { low: 1400, high: 2800, source: "Uptime Institute / RICS NRM1 DC benchmarks", tier: "T3" },
    "3_to_4": { low: 800, high: 1600, source: "Uptime Institute / RICS NRM1 DC benchmarks", tier: "T3" }
  };
  const cost_key = `${actual_tier}_to_${target_tier}`;
  const cost_range = upgrade_cost_ranges[cost_key] || null;
  const it_load_kw_val = C.it_load_kw.value;
  calcs.upgrade_cost = {
    id: "C11",
    label: "Indicative Upgrade Cost Range",
    formula: "€/kW_IT benchmark × IT Load (kW)",
    inputs: { actual_tier, target_tier, it_load_kw: it_load_kw_val },
    result: cost_range ? {
      low: cost_range.low * it_load_kw_val,
      high: cost_range.high * it_load_kw_val,
      per_kw_low: cost_range.low,
      per_kw_high: cost_range.high,
    } : null,
    unit: "€",
    tier: cost_range ? cost_range.tier : "N/A",
    source: cost_range ? cost_range.source : "N/A — no upgrade needed",
    caveat: "Screening-level estimate. Subject to detailed design and site survey."
  };

  // --- C12: Downtime cost exposure ---
  // T3 — Uptime Institute 2023 Annual Outage Analysis
  const downtime_cost_per_hr = { low: 50000, high: 150000 }; // €/hr — varies by criticality
  const downtime_exposure = {
    current_low: current_downtime_hrs * downtime_cost_per_hr.low,
    current_high: current_downtime_hrs * downtime_cost_per_hr.high,
    target_low: target_downtime_hrs * downtime_cost_per_hr.low,
    target_high: target_downtime_hrs * downtime_cost_per_hr.high
  };
  calcs.downtime_cost = {
    id: "C12",
    label: "Annual Downtime Cost Exposure",
    formula: "Downtime (hrs) × €50K–€150K/hr (Uptime Institute 2023)",
    inputs: { current_downtime_hrs, target_downtime_hrs },
    result: downtime_exposure,
    unit: "€/yr",
    tier: "T3 — Uptime Institute 2023 Annual Outage Analysis",
    caveat: "Indicative. Actual cost depends on SLA penalties, lost revenue, and contractual obligations."
  };

  return calcs;
}
```

---

## FINDINGS_ENGINE (6 findings)

All findings are rule-based. No API calls. Traffic light derived deterministically.

```javascript
function runFindingsEngine(calcs) {
  const findings = [];

  // F1: Tier gap
  const tierGap = calcs.tier_gap.result;
  findings.push({
    id: "F01",
    category: "Redundancy",
    title: "Uptime Tier Gap",
    status: tierGap === 0 ? "GREEN" : tierGap === 1 ? "AMBER" : "RED",
    current: `Tier ${calcs.actual_tier.result}`,
    required: `Tier ${calcs.tier_gap.inputs.target_tier}`,
    gap: tierGap === 0 ? "None — target met" : `${tierGap} tier(s) below target`,
    action: tierGap === 0 ? "No upgrade required" :
            tierGap === 1 ? "Single-tier upgrade — targeted improvements to redundancy" :
            "Major infrastructure upgrade required — phased programme recommended"
  });

  // F2: SPOF exposure
  const spofCount = calcs.spof_count.result.count;
  findings.push({
    id: "F02",
    category: "Redundancy",
    title: "Single Points of Failure",
    status: spofCount === 0 ? "GREEN" : spofCount <= 2 ? "AMBER" : "RED",
    current: `${spofCount} SPOF(s) identified`,
    required: calcs.tier_gap.inputs.target_tier >= 3 ? "0 SPOFs for Tier III+" : "Minimise SPOFs",
    gap: spofCount === 0 ? "None" : calcs.spof_count.result.items.join("; "),
    action: spofCount === 0 ? "No action required" :
            `Address ${spofCount} SPOF(s): ${calcs.spof_count.result.items.join(", ")}`
  });

  // F3: Concurrent maintainability
  const cm = calcs.concurrent_maintainability.result;
  findings.push({
    id: "F03",
    category: "Operations",
    title: "Concurrent Maintainability",
    status: cm ? "GREEN" : calcs.tier_gap.inputs.target_tier >= 3 ? "RED" : "AMBER",
    current: cm ? "Achievable" : "Not achievable",
    required: calcs.tier_gap.inputs.target_tier >= 3 ? "Required for Tier III+" : "Recommended",
    gap: cm ? "None" : "Missing: " + [
      !calcs.concurrent_maintainability.inputs.has_mops ? "written MOPs" : null,
      calcs.concurrent_maintainability.inputs.ups_redundancy === "N+0" ? "UPS redundancy" : null,
      calcs.concurrent_maintainability.inputs.cooling_redundancy === "N" ? "cooling redundancy" : null
    ].filter(Boolean).join(", "),
    action: cm ? "Maintain current procedures" : "Develop MOPs and address redundancy gaps"
  });

  // F4: Path independence
  const paths = calcs.path_independence.result.paths;
  findings.push({
    id: "F04",
    category: "Electrical",
    title: "Electrical Path Independence",
    status: paths >= 2 ? "GREEN" :
            calcs.tier_gap.inputs.target_tier >= 3 ? "RED" : "AMBER",
    current: `${paths} independent path(s)`,
    required: calcs.tier_gap.inputs.target_tier >= 4 ? "2 fully independent paths (2N)" :
              calcs.tier_gap.inputs.target_tier >= 3 ? "Dual feed recommended" : "Single path acceptable",
    gap: paths >= 2 ? "None" : [
      !calcs.path_independence.result.dual_feed ? "No dual utility feed" : null,
      !calcs.path_independence.result.bus_section ? "No bus section / single MSB" : null
    ].filter(Boolean).join("; "),
    action: paths >= 2 ? "No action" : "Investigate second utility feed and MSB bus section"
  });

  // F5: Fault tolerance (Tier IV only)
  const ft = calcs.fault_tolerance.result;
  findings.push({
    id: "F05",
    category: "Redundancy",
    title: "Fault Tolerance",
    status: ft.full_ft ? "GREEN" :
            calcs.tier_gap.inputs.target_tier >= 4 ? "RED" : "AMBER",
    current: ft.full_ft ? "Full fault tolerance" :
             ft.power_ft ? "Power FT only" :
             ft.cooling_ft ? "Cooling FT only" : "No fault tolerance",
    required: calcs.tier_gap.inputs.target_tier >= 4 ? "Full FT required" : "Not required below Tier IV",
    gap: ft.full_ft ? "None" : [
      !ft.power_ft ? "Power not fault tolerant (needs 2N UPS + dual feed)" : null,
      !ft.cooling_ft ? "Cooling not fault tolerant (needs 2N/2N+1)" : null
    ].filter(Boolean).join("; "),
    action: calcs.tier_gap.inputs.target_tier < 4 ? "Not applicable for current target" :
            "Full 2N+1 infrastructure programme required"
  });

  // F6: Upgrade investment
  const cost = calcs.upgrade_cost.result;
  findings.push({
    id: "F06",
    category: "Commercial",
    title: "Indicative Upgrade Investment",
    status: cost === null ? "GREEN" : cost.high > 5000000 ? "RED" : "AMBER",
    current: cost === null ? "No upgrade needed" :
             `€${(cost.low/1e6).toFixed(1)}M–€${(cost.high/1e6).toFixed(1)}M`,
    required: "Budget allocation for tier upgrade programme",
    gap: cost === null ? "None" :
         `€${cost.per_kw_low}–€${cost.per_kw_high}/kW IT (screening-level)`,
    action: cost === null ? "No investment required" :
            "Commission Desktop Assessment for detailed costing — €10,000–€15,000"
  });

  // Traffic light summary
  const red_count = findings.filter(f => f.status === "RED").length;
  const amber_count = findings.filter(f => f.status === "AMBER").length;
  const overall = red_count > 0 ? "RED" : amber_count > 0 ? "AMBER" : "GREEN";

  return { findings, summary: { red_count, amber_count, green_count: findings.length - red_count - amber_count, overall } };
}
```

---

## INTERPRETATION_PROMPT

```
You are a data centre redundancy and resilience specialist working for Legacy Business Engineers Ltd (LBE), an independent technical advisory firm.

You have received the results of a deterministic redundancy gap screening. All numbers have been calculated by JavaScript — you MUST NOT recalculate or invent any numbers. Your job is to write a narrative interpretation of the pre-calculated results.

RULES:
1. Every number you mention MUST come from the calculations or findings provided. Do not invent.
2. Use fund-manager language — what is the risk, what does it cost, does the investment thesis work.
3. Refer to the user's facility by name. Use roles not persona names ("the fund manager" not "Ann").
4. All cost figures are screening-level estimates subject to detailed design and site survey.
5. Decision gate: if overall RED or AMBER → recommend Desktop Assessment (€10,000–€15,000).
6. LBE identifies and quantifies — never suggest LBE will design or deliver solutions.
7. CRREM DC pathway is LBE-derived (T3/T4), not published by CRREM Foundation.

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

| # | Scenario | Key Input | Expected Result |
|---|----------|-----------|-----------------|
| G1 | Clonshaugh baseline | 2.4 MW, PUE 1.50, target Tier III, 2×1350kW UPS, single feed, single bus, no MOPs, N+1 cooling, N+1 gen | Actual Tier I, gap=2, RED, 7 SPOFs |
| G2 | Well-equipped DC | 5 MW, PUE 1.25, target Tier III, 4×1500kW UPS, dual feed, bus section, MOPs yes, N+1 cooling, N+1 gen | Actual Tier III, gap=0, GREEN |
| G3 | Tier IV target, partial FT | 10 MW, PUE 1.20, target Tier IV, 8×1500kW UPS, dual feed, dual MSB, MOPs yes, 2N cooling, 2N gen | Actual Tier IV, gap=0, GREEN |
| G4 | No gen, basic | 1 MW, PUE 1.80, target Tier II, 1×1200kW UPS, single feed, single bus, no MOPs, N cooling, no gen | Actual Tier I, gap=1, RED, 6+ SPOFs |

---

*DC-TOOL-003 Calc Engine Definition v2.0 | 14 April 2026*
*Source: DC-LEARN-003 cascadeCheck functions (9 checks)*
*Architecture: deterministic JS → rule-based findings → AI narrative only*
