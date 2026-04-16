# DC-SCREEN A+ UPGRADE — Claude Code Prompt
# Model: Sonnet | Repo: dc-learn-academy
# Date: 12 April 2026
# Scope: RPT-001 structural changes only (P3, P4, P5, P6)

## SOURCE FILES
- `DC-RPT-001_v1_0_3.html` — use the version already in the repo on main (just merged)
  - **CRITICAL:** If the repo still has v1.0.2, upload the corrected v1.0.3 from this session first.
  - v1.0.3 has P0 (banned terminology fixed) and P1 (CRREM derivation disclosure added) already applied.

## WHAT THIS PROMPT DOES
Four structural upgrades to RPT-001's calculation engine and report output. Zero content changes to CPS-001 in this session.

---

## P6 — REPORT TITLE CHANGE (do first — simplest)

Replace all instances of:
- `Carbon Position Statement` → `Asset Carbon Risk Screening`
- `Data Centre Carbon & Regulatory Screening` (subtitle) → `Investment Screening — Carbon, Regulatory & Retrofit Economics`

This changes the report header, page footers, and any reference in the HTML. Do NOT change the tool ID `DC-RPT-001` or the filename.

---

## P3 — MAKE HOLD MODEL INPUTS EDITABLE

Currently lines 1051–1056 hardcode these constants:
```javascript
var ELEC_RATE = 0.12;
var DISCOUNT_RATE = 0.08;
var TARGET_PUE = 1.3;
var RETROFIT_COST_PER_KW = 1100;
```

### Change required:
1. Add an **"Investment Assumptions"** input panel to the controls bar (or as a collapsible section above the report). Four fields:
   - **Discount Rate (%)** — default 8, range 4–15, step 0.5
   - **Target PUE** — default 1.30, range 1.10–1.50, step 0.05
   - **Retrofit Cost (€/kW IT)** — default 1,100, range 600–2,000, step 50
   - **Electricity Rate (€/kWh)** — default 0.12, range 0.08–0.20, step 0.01

2. These values feed into `reDerive()` instead of the hardcoded constants.
3. Report renders with defaults on first load. Changing any input re-renders the report immediately.
4. The exec summary and hold model section dynamically update.
5. In the printed report, show the assumptions used in a small "Assumptions" table above the hold model results.

### Style:
- Match existing `.controls-bar` styling
- Label: "Investment Assumptions" with a small "(adjust to match your fund parameters)" subtext
- Use `var(--dc-gray-pale)` background, same border-radius as existing cards

---

## P4 — ADD CRM CAPACITY MARKET REVENUE TO HOLD MODEL

The CRM T-4 clearing price is €149,960/MW/yr (SEMO PCAR2829T-4, T1 source).

### Change required:
1. Add a new constant: `var CRM_CLEARING_PRICE = 149960; // EUR/MW/yr — SEMO PCAR2829T-4`
2. Add a checkbox input to the Investment Assumptions panel: **"Include CRM capacity revenue"** — default OFF
3. When ON, calculate:
   ```
   annual_crm_revenue = inp.it_load_mw * CRM_CLEARING_PRICE
   ```
4. Add `annual_crm_revenue` to the hold model results object
5. Adjust NPV calculation:
   ```
   annual_net_benefit = annual_saving + annual_crm_revenue (if enabled)
   npv_retrofit = NPV(annual_net_benefit, 10yr, discount_rate) - retrofit_capex
   ```
6. In the exec summary, when CRM is enabled, add a line:
   ```
   "Capacity market revenue (CRM T-4): €[X]/yr included in hold model."
   ```
7. In the printed assumptions table, show: `CRM Revenue: Included / Excluded`

### Important:
- CRM revenue should be clearly labelled as **"indicative — subject to qualification and market participation"**
- Source note: `SEMO PCAR2829T-4, T1`
- This is a material number (€360K/yr for Clonshaugh) — it changes the investment thesis significantly

---

## P5 — SENSITIVITY ANALYSIS (BASE / STRESSED)

### Change required:
1. Add a **"Scenario"** toggle to the controls bar: `Base Case` | `Stressed Case`
2. **Base Case** = user-entered assumptions (from P3 inputs)
3. **Stressed Case** automatically adjusts:
   - Carbon tax: €71 → €100 (2030 legislated target)
   - Grid EF: 0.2241 → 0.18 (decarbonisation trajectory, indicative)
   - Discount rate: +2% above base case input
   - Electricity rate: +15% above base case input
4. The report shows BOTH scenarios side-by-side in the hold model section:
   - Two-column layout: Base Case | Stressed Case
   - Key metrics: Annual saving, Retrofit CAPEX (same both), NPV, Simple Payback
   - Green/red colour coding: green if NPV positive, red if negative
5. The exec summary adapts:
   - If BOTH scenarios show positive NPV: "The retrofit case is robust across scenarios."
   - If base positive but stressed negative: "The retrofit case is marginal — sensitive to carbon tax trajectory and discount rate."
   - If BOTH negative: "The retrofit does not recover cost under either scenario."
6. In print, both scenarios render in a clean comparison table.

### Style:
- Toggle buttons matching existing `.btn-secondary` style
- Active state: `var(--dc-black)` background, white text
- Comparison table: clean, minimal, no chart needed — just numbers

---

## VERSION BUMP
- Bump from v1.0.3 to **v1.1.0** (minor version — new features added)
- Update ALL version references in the file

## CONSTRAINTS
- DO NOT modify DC-CPS-001 in this session
- DO NOT change any existing calculation logic — only ADD new inputs/outputs
- DO NOT touch the CRREM pathway data or bands
- DO NOT modify the disclaimer or sign-off block (already fixed in v1.0.3)
- Vanilla JS only — no React, no framework dependencies
- All new UI must work in print (`@media print` rules)

## VERIFICATION
After all changes:
1. Open in browser with Clonshaugh demo data
2. Verify default assumptions produce same results as v1.0.3
3. Change discount rate — verify NPV updates
4. Enable CRM revenue — verify it adds to annual benefit
5. Toggle Stressed Case — verify carbon tax and EF change
6. Print to PDF — verify assumptions table and dual-scenario layout render

## SHIP CONDITION
File opens without errors, demo data renders correctly, all four features functional, print layout clean.

Commit and push directly to main. Do NOT create feature branches.
