# DC-TOOL-011 CALC ENGINE DEFINITION v2.0
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
