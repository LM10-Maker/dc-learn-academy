# DC-TOOL-012 CALC ENGINE DEFINITION v2.0
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
