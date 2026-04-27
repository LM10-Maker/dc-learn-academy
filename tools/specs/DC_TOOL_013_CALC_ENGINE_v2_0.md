# DC-TOOL-013 CALC ENGINE DEFINITION v2.0
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
