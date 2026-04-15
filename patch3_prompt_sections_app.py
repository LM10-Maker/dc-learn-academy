"""
Patch 3: Replace INTERPRETATION_PROMPT, SECTIONS in InputTab,
         and App.runScreening() with cooling-chain versions.
"""
import sys

DST = 'tools/DC-TOOL-002_v2_0_0.html'
with open(DST, encoding='utf-8') as f:
    h = f.read()

# ── Patch C: INTERPRETATION_PROMPT ────────────────────────────────────────────
OLD_PROMPT_START = """/* ================================================================
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
   Source: DC_TOOL_002_CALC_ENGINE_v2_0.md
   ================================================================ */
const INTERPRETATION_PROMPT = `You are a data centre cooling systems specialist working for Legacy Business Engineers Ltd (LBE), an independent technical advisory firm.

You have received the results of a deterministic cooling chain screening. All numbers have been calculated by JavaScript — you MUST NOT recalculate or invent any numbers. Your job is to write a narrative interpretation of the pre-calculated results.

RULES:
1. Every number you mention MUST come from the calculations or findings provided. Do not invent.
2. Use fund-manager language — what is the risk, what does it cost, does the investment thesis work.
3. Refer to the user's facility by name. Use roles not persona names ("the fund manager" not "Ann").
4. All cost figures are screening-level estimates subject to detailed design and site survey.
5. Decision gate: if overall RED or AMBER → recommend Desktop Assessment (€10,000–€15,000).
6. LBE identifies and quantifies — never suggest LBE will design or deliver solutions.
7. This screening does not constitute a design deliverable or compliance determination.
8. Standards: EN 50600-2-3, ASHRAE TC 9.9, CIBSE Guide B2, EU F-Gas Regulation 2024/573.

Respond ONLY with a JSON object. No preamble, no markdown fences.
{
  "executive_summary": "3 sentences. Cooling efficiency risk, unrealised savings, investment thesis impact.",
  "key_findings": ["Finding narrative for each of the 6 findings provided"],
  "commercial_implications": "2-3 sentences for the fund manager — energy cost, F-Gas regulatory risk, capex.",
  "recommended_next_step": "One clear recommendation with indicative cost.",
  "caveats": "Standard screening-level caveat."
}`;"""

if OLD_PROMPT_START not in h:
    print("ERROR: INTERPRETATION_PROMPT old block not found!")
    idx = h.find('INTERPRETATION PROMPT')
    if idx != -1:
        print(repr(h[idx-5:idx+300]))
    sys.exit(1)

h = h.replace(OLD_PROMPT_START, NEW_PROMPT, 1)
print("Patch C (INTERPRETATION_PROMPT) done.")

# ── Patch D: SECTIONS in InputTab ─────────────────────────────────────────────
OLD_SECTIONS = """  const SECTIONS = [
    { title: 'Facility Identity', ids: ['facility_name','location','build_year'] },
    { title: 'Power & IT Load', ids: ['it_load_mw','rack_count','rack_density_kw','mic_kva','voltage_kv'] },
    { title: 'Cooling & Efficiency', ids: ['pue','cooling_type'] },
    { title: 'Backup & Redundancy', ids: ['redundancy_level','generator_fuel','generator_hours'] },
    { title: 'Commercial & ESG', ids: ['ppa_pct','hall_config','total_floor_m2'] }
  ];"""

NEW_SECTIONS = """  const SECTIONS = [
    { title: 'Facility Identity',         ids: ['facility_name','location','build_year'] },
    { title: 'IT Load & Efficiency',      ids: ['it_load_mw','pue'] },
    { title: 'Cooling Technology',        ids: ['cooling_type','has_free_cooling','has_containment','supply_temp_c'] },
    { title: 'Chiller Plant',             ids: ['chiller_count','chiller_kw_each','chiller_type'] },
    { title: 'Refrigerants & Water',      ids: ['refrigerant_type','refrigerant_charge_kg','has_water_meter'] },
    { title: 'Commercial & ESG',          ids: ['ppa_pct','total_floor_m2'] }
  ];"""

if OLD_SECTIONS not in h:
    print("ERROR: SECTIONS old block not found!")
    idx = h.find('const SECTIONS')
    if idx != -1:
        print(repr(h[idx:idx+300]))
    sys.exit(1)

h = h.replace(OLD_SECTIONS, NEW_SECTIONS, 1)
print("Patch D (SECTIONS) done.")

# ── Patch E: App.runScreening() ───────────────────────────────────────────────
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
    // STEP 1: Run calcs INSTANTLY (no API) — DC-TOOL-002 deterministic engine
    const calcs   = runCalcEngine(inputs);
    const steps   = buildAuditSteps(calcs);
    setCalcSteps(steps);

    const fResults = runFindingsEngine(calcs);
    setFindings(fResults.findings);

    const tl = deriveTrafficLight(fResults);
    setTrafficLight(tl);

    // Switch to calculations tab immediately (no wait for API)
    setActiveTab('calculations');

    // STEP 2: Request AI narrative (async, non-blocking) — narrative only, no calculations
    setInterpreting(true);
    setInterpretation(null);
    setError(null);

    try {
      const calcSummary = Object.values(calcs).map(c => {
        const val = typeof c.result === 'object' && c.result !== null ? JSON.stringify(c.result) : c.result;
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
        '\\n\\nCALCULATED RESULTS (JavaScript — do not recalculate):\\n' + calcSummary +
        '\\n\\nFINDINGS (Rule-based — do not modify):\\n' + findingSummary +
        '\\n\\nOverall risk: ' + tl +
        '\\n\\nTool: DC-TOOL-002 v2.0.0 Cooling Chain Screener' +
        '\\n\\nInterpret these pre-calculated results. Do not invent or recalculate any numbers.' +
        ' Refer to the facility by name. Use roles not names (e.g., "the fund manager" not "Ann").';"""

if OLD_RUN not in h:
    print("ERROR: App.runScreening old block not found!")
    idx = h.find('const runScreening')
    if idx != -1:
        print(repr(h[idx:idx+400]))
    sys.exit(1)

h = h.replace(OLD_RUN, NEW_RUN, 1)
print("Patch E (App.runScreening) done.")

# ── Patch F: Update the interpretation render to use key_findings ─────────────
# The template uses finding_interpretations + persona_views in ReportTab.
# The new format uses key_findings. We need to check the ReportTab rendering.
# For now, let's just look at what it uses.

# Check current interpretation rendering
idx = h.find('finding_interpretations')
if idx != -1:
    print(f"  NOTE: found 'finding_interpretations' at char {idx} — need to patch ReportTab")
else:
    print("  OK: no 'finding_interpretations' in template ReportTab")

idx2 = h.find('persona_views')
print(f"  'persona_views' occurrences: {h.count('persona_views')}")

with open(DST, 'w', encoding='utf-8') as f:
    f.write(h)
print(f"Saved. Lines: {h.count(chr(10))+1}")
