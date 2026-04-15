"""
Patch C for DC-TOOL-010 v2.0.0
Replace INTERPRETATION_PROMPT, SECTIONS in InputTab, App.runScreening().
"""
import sys

DST = 'tools/DC-TOOL-010_v2_0_0.html'
with open(DST, encoding='utf-8') as f:
    h = f.read()

# ── Patch C1: INTERPRETATION_PROMPT ──────────────────────────────────────────
OLD_PROMPT = """/* ================================================================
   INTERPRETATION PROMPT — AI writes narrative only. Never calculates.
   Replace per tool.
   ================================================================ */
const INTERPRETATION_PROMPT = `You are interpreting pre-calculated screening results for a data centre facility in Ireland. You work for Legacy Business Engineers Ltd (LBE), an independent technical advisory firm.

CRITICAL RULES:
- DO NOT perform any arithmetic.
- DO NOT estimate any costs.
- DO NOT invent any numbers.
- Every number you reference MUST come from the CALCULATED RESULTS below.
- If you need a number that is not provided, say "not calculated in this screening."
- Use "indicative" or "screening-level" for any cost reference.
- Use "Misalignment Year" not "Stranding Year".
- Never say "compliant" — use "aligned" or "readiness".
- Never say "should" or "must" — use "consider" or "investigate".
- State: "This screening does not constitute a design deliverable or compliance determination."

Your job is INTERPRETATION ONLY — explain what the calculated numbers mean.

Respond ONLY with a JSON object. No preamble, no markdown fences.
{
  "executive_summary": "3 sentences in fund-manager language interpreting the results. Reference the actual calculated numbers.",
  "finding_interpretations": {
    "finding_id": "1-2 sentence commercial/regulatory implication for the investor"
  },
  "persona_views": {
    "ann": "Write as Fund Manager perspective — do NOT prefix with any name, start directly with the perspective. Focus on risk, cost, hold thesis, exit implications",
    "declan": "Write as Ops Manager perspective — practical operational impact, what changes day-to-day",
    "mark": "Write as MEP Engineer perspective — technical path to close gaps, standards reference",
    "sarah": "Write as ESG Analyst perspective — reporting impact, taxonomy disclosure, SFDR alignment",
    "tom": "Write as QS/Cost Manager perspective — capex phasing, payback context, benchmark comparison"
  },
  "decision_gate": "DESKTOP_ASSESSMENT or MONITORING or DISPOSAL_ANALYSIS"
}`;"""

NEW_PROMPT = """/* ================================================================
   INTERPRETATION PROMPT — AI writes narrative only. Never calculates.
   Source: DC_TOOL_010_CALC_ENGINE_v2_0.md
   ================================================================ */
const INTERPRETATION_PROMPT = `You are a data centre assessment specialist working for Legacy Business Engineers Ltd (LBE), an independent technical advisory firm. You are interpreting pre-calculated facility intake screening results for a data centre in Ireland.

RULES:
1. Every number you mention MUST come from the calculations or findings provided. Do not invent any numbers.
2. Use fund-manager language — power headroom, retrofit ROI, 10-year cost trajectory, hold thesis.
3. Refer to the facility by name. Use roles not persona names ("the fund manager" not "Ann").
4. All cost figures are screening-level estimates (T3) subject to detailed design and site survey.
5. Decision gate: if overall RED or AMBER → recommend Desktop Assessment (€10,000–€15,000).
6. LBE identifies and quantifies — never suggest LBE will design or deliver solutions.
7. EU Taxonomy PUE threshold is ≤1.3 (Delegated Act 2021/2139, T1). CRU renewable obligation is 80% (CRU/2025236, T1).
8. Carbon tax: €71/tCO₂ (Budget 2025, T1), rising to €100/tCO₂ by 2030 (Finance Act, T1).
9. Free cooling: 7,200 hrs/yr available in Dublin climate (Met Éireann 30-year, T1).
10. This screening does not constitute a design deliverable or compliance determination.

Respond ONLY with a JSON object. No preamble, no markdown fences.
{
  "executive_summary": "3 sentences in fund-manager language. MIC utilisation, retrofit ROI, 10-year cost exposure.",
  "key_findings": ["1-2 sentence interpretation for each of the 6 findings — in the same order as provided"],
  "commercial_implications": "2-3 sentences for the fund manager — power headroom, energy cost trajectory, capex requirement.",
  "recommended_next_step": "One clear recommendation with indicative cost range.",
  "caveats": "Standard screening-level caveat. State: This screening does not constitute a design deliverable or compliance determination."
}`;"""

if OLD_PROMPT not in h:
    print("ERROR: INTERPRETATION_PROMPT old block not found!")
    sys.exit(1)
h = h.replace(OLD_PROMPT, NEW_PROMPT, 1)
print("Patch C1 (INTERPRETATION_PROMPT) done.")

# ── Patch C2: SECTIONS in InputTab ───────────────────────────────────────────
OLD_SECTIONS = """  const SECTIONS = [
    { title: 'Facility Identity', ids: ['facility_name','location','build_year'] },
    { title: 'Power & IT Load', ids: ['it_load_mw','rack_count','rack_density_kw','mic_kva','voltage_kv'] },
    { title: 'Cooling & Efficiency', ids: ['pue','cooling_type'] },
    { title: 'Backup & Redundancy', ids: ['redundancy_level','generator_fuel','generator_hours'] },
    { title: 'Commercial & ESG', ids: ['ppa_pct','hall_config','total_floor_m2'] }
  ];"""

NEW_SECTIONS = """  const SECTIONS = [
    { title: 'Facility Identity',     ids: ['facility_name','location','build_year'] },
    { title: 'Power & MIC',           ids: ['it_load_mw','mic_mva','grid_feed'] },
    { title: 'IT & Rack Density',     ids: ['racks','kw_per_rack','target_kw_rack'] },
    { title: 'Cooling & Efficiency',  ids: ['pue','cooling_type','cooling_capacity_mw'] },
    { title: 'ESG & Monitoring',      ids: ['ppa_pct','bms_points'] }
  ];"""

if OLD_SECTIONS not in h:
    print("ERROR: SECTIONS old block not found!")
    sys.exit(1)
h = h.replace(OLD_SECTIONS, NEW_SECTIONS, 1)
print("Patch C2 (SECTIONS) done.")

# ── Patch C3: App.runScreening() ─────────────────────────────────────────────
OLD_RUN = """  const runScreening = async () => {
    // STEP 1: Run calcs INSTANTLY (no API)
    const { results, steps } = runCalcEngine(inputs);
    setCalcSteps(steps);

    const fResults = runFindingsEngine(inputs, results);
    setFindings(fResults);

    const tl = deriveTrafficLight(fResults);
    setTrafficLight(tl);

    // Show calculations tab immediately
    setActiveTab('calculations');

    // STEP 2: Request AI interpretation (async, non-blocking)
    setInterpreting(true);
    setInterpretation(null);
    setError(null);

    try {
      const calcSummary = steps.map(s => s.name + ': ' + s.formatted + ' ' + s.unit).join('\\n');
      const findingSummary = fResults.map(f => f.area + ': ' + f.status + ' — ' + f.detail).join('\\n');

      const userPrompt = 'FACILITY: ' + (inputs.facility_name||'Unknown') + ' | ' + (inputs.location||'') + ' | Built ' + (inputs.build_year||'?') + '\\n\\nCALCULATED RESULTS:\\n' + calcSummary + '\\n\\nFINDINGS:\\n' + findingSummary + '\\n\\nTraffic light: ' + tl + '\\n\\nInterpret these pre-calculated results. Do not perform any arithmetic.';"""

NEW_RUN = """  const runScreening = async () => {
    // STEP 1: Run calcs INSTANTLY (no API) — DC-TOOL-010 deterministic engine
    const calcs   = runCalcEngine(inputs);
    const steps   = buildAuditSteps(calcs);
    setCalcSteps(steps);

    const fResults = runFindingsEngine(calcs);
    setFindings(fResults.findings);

    const tl = deriveTrafficLight(fResults);
    setTrafficLight(tl);

    // Switch to calculations tab immediately
    setActiveTab('calculations');

    // STEP 2: Request AI narrative (async, non-blocking) — narrative only, no calculations
    setInterpreting(true);
    setInterpretation(null);
    setError(null);

    try {
      const calcSummary = Object.values(calcs).map(c => {
        const val = typeof c.result === 'object' && c.result !== null
          ? Object.entries(c.result).map(([k,v]) => k.replace(/_/g,' ') + ': ' + v).join(', ')
          : c.result;
        return c.id + ' — ' + c.label + ': ' + val + (c.unit ? ' ' + c.unit : '');
      }).join('\\n');

      const findingSummary = fResults.findings.map(f =>
        f.id + ' [' + f.status + '] ' + f.title + ': ' + f.current +
        ' | Gap: ' + f.gap + ' | Action: ' + f.action
      ).join('\\n');

      const userPrompt =
        'FACILITY: ' + (inputs.facility_name||'Unknown') + ' | ' + (inputs.location||'') +
        ' | Built ' + (inputs.build_year||'?') +
        '\\nIT Load: ' + inputs.it_load_mw + ' MW | PUE: ' + inputs.pue +
        ' | MIC: ' + inputs.mic_mva + ' MVA' +
        '\\n\\nCALCULATED RESULTS (JavaScript — do not recalculate):\\n' + calcSummary +
        '\\n\\nFINDINGS (Rule-based — do not modify):\\n' + findingSummary +
        '\\n\\nOverall risk: ' + tl +
        '\\n\\nTool: DC-TOOL-010 v2.0.0 Facility Audit Checklist' +
        '\\n\\nInterpret these pre-calculated results. Do not invent or recalculate any numbers.';"""

if OLD_RUN not in h:
    print("ERROR: App.runScreening old block not found!")
    sys.exit(1)
h = h.replace(OLD_RUN, NEW_RUN, 1)
print("Patch C3 (App.runScreening) done.")

with open(DST, 'w', encoding='utf-8') as f:
    f.write(h)
print(f"Saved. Lines: {h.count(chr(10)) + 1}")
