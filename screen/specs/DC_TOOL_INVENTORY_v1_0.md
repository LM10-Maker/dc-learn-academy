# DC-TOOL and DC-Screen Inventory
## Generated 2026-04-18 by Claude Code
## Repo: dc-learn-academy, directory: screen/

---

## DEVIATIONS

The following anomalies were observed during inventory. No action has been taken — reported only.

1. **DC-TOOL-009 is absent.** The DC-TOOL sequence runs 001–008 then jumps to 010–014. No file `DC-TOOL-009_*.html` exists in `screen/tools/`. The slot appears deliberately skipped or reserved.

2. **DC-RPT-001 is duplicated.** `screen/DC-RPT-001_v1_2_1_final.html` and `screen/tools/pipeline/DC-RPT-001_v1_2_1_final.html` are byte-for-byte identical (180,311 bytes each). One copy is redundant.

3. **Two filenames contain browser-download suffixes.** `DC-DIAG-001_v1_3_1 (4).html` (the " (4)" suffix) and `DC-R-PUE-001_PUE_Gap_Analyser_v1_0_5 (1).html` (the " (1)" suffix) follow the macOS/Windows naming pattern for repeated downloads of the same file. These may be stale artifacts rather than intentional variant files.

4. **Title/code version differs from filename version in several v1.x files.** Examples: `DC-R-FGS-001_v1_0_2.html` declares `v1.0.3` in its `<title>`; `DC-R-EED-001_EED_Compliance_Gap_Checker_v1_0_5.html` declares `v1.0.6` in a header comment; `DC-R-HTR-001_v1_0_2.html` declares `v1.0.3` in its `<title>`. Filename and in-file version are out of sync.

5. **DC-SLD-001 is at pre-release version v0.1.x.** It is the only file in the repo at a sub-v1 version. React 18 component architecture and a dark/light theme toggle suggest it was experimental work that was never promoted.

6. **Five v1.x tools have no v2.0 equivalent.** Waste heat recovery (DC-R-HTR-001), retrofit-vs-rebuild economics (DC-R-ROI-001), strategic misalignment risk (DC-R-STR-001), capex cost benchmarking (DC_Cost_Per_MW_Benchmark), and regional comparison (DC_Ireland_vs_Europe_Comparator) cover domains not present in any DC-TOOL-00x. These capabilities are absent from the v2.0 suite.

---

## Summary

| Metric | Count |
|--------|-------|
| Total HTML files under scope | 33 |
| v2.0 tools (screen/tools/) | 13 |
| Pipeline files (screen/tools/pipeline/) | 3 |
| v1.x legacy files (screen/ root) | 17 |
| — of which: ABSORBED into v2.0 | 10 |
| — of which: UNIQUE (no v2.0 equivalent) | 5 |
| — of which: PIPELINE / aggregator | 2 |
| Duplicate file (root RPT-001 = pipeline RPT-001) | 1 |

---

## v2.0 Tool Registry (screen/tools/)

All 13 v2.0 tools share the same architecture: Vanilla JS + IBM Plex fonts, traffic-light check output, AI narrative layer (INTERPRETATION_PROMPT), and JSON export. All are at version 2.0.0.

| Code | Name | Version | Size KB | Input Fields | Check IDs | AI Narrative | JSON Export | JTBD |
|------|------|---------|---------|-------------|-----------|-------------|-------------|------|
| DC-TOOL-001 | Power Chain Screener | 2.0.0 | 102.7 | facility_name, location, build_year, it_load_mw, pue, racks, kw_per_rack, mic_mva, tx_count, tx_rating_mva, ups_count, ups_rating_mva, msb_bus_rating_a, sts_rating_a | C01–C10, F01–F06 | Yes | Yes | Does this facility's power chain have sufficient capacity and redundancy to support current and target IT load? |
| DC-TOOL-002 | Cooling Chain Screener | 2.0.0 | 106.7 | facility_name, location, build_year, it_load_mw, pue, cooling_type, has_free_cooling, has_containment, supply_temp_c, chiller_count, chiller_kw_each, chiller_type, refrigerant_type | C01–C11, F01–F06 | Yes | Yes | Does this facility's cooling infrastructure support current density and can it be extended to meet target PUE and capacity? |
| DC-TOOL-003 | Redundancy Gap Tool | 2.0.0 | 105.5 | facility_name, location, build_year, it_load_mw, pue, target_tier, ups_modules, ups_rating_kw, utility_feeds, msb_config, has_mops, cooling_redundancy | C01–C12, F01–F06 | Yes | Yes | What Tier level does this facility currently achieve and what infrastructure gaps must be closed to reach the target Tier? |
| DC-TOOL-004 | Compliance Checker | 2.0.0 | 106.3 | facility_load_mw, it_load_mw, pue, annual_energy_mwh, it_energy_mwh, overhead_mwh, annual_energy_cost, electricity_price, pue_gap, taxonomy_pue, taxonomy_aligned, overhead_cost_at_target, renewable_gap_pct, ppa_pct, cru_renewable, unmatched_mwh, co2_scope2, grid_ef, carbon_cost_now, carbon_tax_current, carbon_cost_2030, carbon_tax_2030, carbon_escalation, carbon_10yr_incremental, fgas_co2eq | Multiple compliance outputs | Yes | Yes | Does this facility meet EU Taxonomy, EED, and carbon obligations, and what is the financial exposure if it does not? |
| DC-TOOL-005 | UPS Adequacy Tool | 2.0.0 | 109.2 | facility_name, location, build_year, it_load_mw, pue, racks, gen_count, gen_rating_mw, gen_redundancy, ups_rating_mva, ups_efficiency, ups_bridge_min, fuel_type, fuel_storage_l, test_hours_yr, bess_installed, bess_mw | F01–F07 | Yes | Yes | Is the UPS, generator, and BESS stack sufficient to bridge IT load through a grid outage without interruption? |
| DC-TOOL-006 | Grid Headroom Calculator | 2.0.0 | 105.6 | facility_name, location, build_year, it_load_mw, pue, racks, target_kw_rack, target_pue, mic_mva, grid_voltage, utility_feeds, tx_count, tx_rating_mva, tx_k_factor, gen_installed_mw, power_factor | Multiple grid checks | Yes | Yes | How much electrical headroom exists between the current grid connection and the target IT load, and where are the binding constraints? |
| DC-TOOL-007 | Regulatory Gap Screener | 2.0.0 | 110.7 | facility_name, location, build_year, it_load_mw, pue, ppa_pct, gen_thermal_mwth, gen_test_hrs_yr, fuel_type, refrigerant_type, refrigerant_gwp, refrigerant_charge_kg, planning_sid, eed_art26, epa_licence | C01–C15 | Yes | Yes | Which regulatory obligations (EED, F-Gas, EPA, planning) apply to this facility and which are currently unmet? |
| DC-TOOL-008 | Fire Safety Screener | 2.0.0 | 115.1 | facility_name, location, build_year, it_load_mw, rack_count, rack_density_kw, detection_type, has_subfloor_detection, suppression_type, suppression_agent_kg, last_integrity_test, has_containment, battery_type, has_bess, total_floor_m2 | C01–C08, detection, subfloor_detection, suppression, fgas, integrity, liion_bess, containment | Yes | Yes | Are fire detection, suppression, and BESS controls adequate for the current rack density and battery chemistry? |
| DC-TOOL-010 | Facility Audit Checklist | 2.0.0 | 101.4 | facility_name, location, build_year, it_load_mw, pue, racks, kw_per_rack, target_kw_rack, mic_mva, ppa_pct, cooling_type, cooling_capacity_mw, bms_points, grid_feed | C01–C09, F01–F06 | Yes | Yes | Does this facility pass a structured multi-domain audit across power, cooling, efficiency, and operational readiness? |
| DC-TOOL-011 | Security Assessment Tool | 2.0.0 | 95.1 | facility_name, location, build_year, it_load_mw, racks, perimeter_type, vehicle_access, building_entry, data_hall_access, rack_security, cctv_type, alarm_grade, zone_count, maturity_score, upgrade_cost | F01–F08 | Yes | Yes | What is the physical security maturity score and which access, surveillance, or perimeter controls are below standard? |
| DC-TOOL-012 | Commissioning Readiness Tool | 2.0.0 | 92.7 | facility_name, location, it_load_mw, cx_plan, fats_complete, sats_complete, ists_complete, load_test, pvt_complete, seasonal_cx, defects_clear, orr_passed | M1–M9, C01–C03, F01–F03 | Yes | Yes | Has this facility completed all commissioning milestones and cleared defects to a standard that supports safe operational handover? |
| DC-TOOL-013 | AI-Ready Cooling Screener | 2.0.0 | 98.8 | facility_name, location, build_year, it_load_mw, pue, racks, kw_per_rack, target_kw_rack, dlc_rack_count, floor_load_kpa, whip_circuit_a, whip_voltage, mic_mva, air_limit, dlc_split, cdu_sizing, immersion, layout, power_dist, structural, tue, mic_impact, business_case | F01–F06 | Yes | Yes | Can this facility support AI/GPU rack densities and what liquid cooling infrastructure changes are required? |
| DC-TOOL-014 | CRU Readiness Screener | 2.0.0 | 100.7 | facility_name, location, build_year, it_load_mw, pue, ppa_pct, gen_installed_mw, gen_fuel, gen_gas_fraction, has_bess, bess_mw | C01–C10, F01–F06 | Yes | Yes | Is this facility's renewable and backup power infrastructure sufficient to qualify for Carbon Removal Unit deployment? |

**Note:** DC-TOOL-009 does not exist. The sequence jumps from DC-TOOL-008 to DC-TOOL-010. See DEVIATIONS section.

---

## v1.x Legacy Tool Registry (screen/ root)

Files classified as: **ABSORBED** (functionality exists in a named v2.0 DC-TOOL), **UNIQUE** (no v2.0 equivalent), or **PIPELINE** (aggregator/renderer, not a screening tool).

| Filename | Code | Version | Size KB | Status | Absorbed Into | JTBD |
|----------|------|---------|---------|--------|--------------|------|
| DC-DIAG-001_v1_3_1 (4).html | DC-DIAG-001 | v1.3.2 (title) | 272.2 | ABSORBED | DC-TOOL-001 + DC-TOOL-002 | Is this facility a viable retrofit candidate and what are the capital and operational costs of doing nothing vs acting? |
| DC-R-CLG-001_Cooling_Retrofit_Options_v1_0_1.html | DC-R-CLG-001 | v1.0.1 | 46.4 | ABSORBED | DC-TOOL-002 | Which cooling retrofit option best matches this facility's constraints by PUE gain, payback, and disruption profile? |
| DC-R-EED-001_EED_Compliance_Gap_Checker_v1_0_5.html | DC-R-EED-001 | v1.0.5 | 74.9 | ABSORBED | DC-TOOL-007 + DC-TOOL-004 | Which EED Article obligations apply to this facility and what actions are required to close the compliance gap? |
| DC-R-FGS-001_v1_0_2.html | DC-R-FGS-001 | v1.0.3 (title) | 35.6 | ABSORBED | DC-TOOL-007 + DC-TOOL-008 | When will this facility's refrigerant stock become non-compliant under F-Gas phase-down rules and what is the replacement cost? |
| DC-R-HTR-001_v1_0_2.html | DC-R-HTR-001 | v1.0.3 (title) | 39.1 | UNIQUE | n/a | Is waste heat recovery viable for this facility under EU EED Article 12 and what is the value to a potential district heating offtaker? |
| DC-R-PUE-001_PUE_Gap_Analyser_v1_0_5 (1).html | DC-R-PUE-001 | v1.0.5 | 49.5 | ABSORBED | DC-TOOL-004 | What is the gap between current PUE and best-in-class, which interventions will close it, and what is the energy cost saving? |
| DC-R-PWR-001_Power_Densification_Check_v1_0_5.html | DC-R-PWR-001 | v1.0.5 | 52.0 | ABSORBED | DC-TOOL-001 + DC-TOOL-006 | What is the binding power chain constraint preventing this facility from reaching target rack density? |
| DC-R-ROI-001_RetrofitVsRebuild_v1_0_5.html | DC-R-ROI-001 | v1.0.5 | 54.2 | UNIQUE | n/a | Does the NPV of a phased retrofit exceed the NPV of a full rebuild or relocation over the analysis horizon? |
| DC-R-STR-001_v1_0_2.html | DC-R-STR-001 | v1.0.3 (title) | 35.4 | UNIQUE | n/a | Across regulatory, market, technical, financial, and carbon dimensions, how misaligned is this facility and when does it become a stranded asset? |
| DC-R-SUM-001_v1_0_1.html | DC-R-SUM-001 | v1.0.2 (title) | 52.8 | PIPELINE | n/a | Aggregates exported JSON from all DC-R-* screening tools into a single dashboard verdict; does not calculate new values |
| DC-RPT-001_v1_2_1_final.html | DC-RPT-001 | v1.2.3 (comment) | 176.1 | PIPELINE | n/a | Renders A4 report output from Carbon Position Statement (CPS) pipeline data; identical byte-for-byte to screen/tools/pipeline/DC-RPT-001 |
| DC-SLD-001_v0_1_0.html | DC-SLD-001 | v0.1.1 (title) | 65.1 | ABSORBED | DC-TOOL-001 + DC-TOOL-006 | Which sub-component in the power delivery chain is the binding bottleneck preventing rack density growth? (pre-release/experimental) |
| DC_Cost_Per_MW_Benchmark_v1_1_0.html | DC-F-CST-001 | v1.1.0 | 34.7 | UNIQUE | n/a | What is the expected elemental CapEx per MW for a facility of this Tier, location, and specification, benchmarked against regional norms? |
| DC_Free_Cooling_Hours_Calculator_v1_2_0.html | DC-M-FCL-001 | v1.2.0 | 29.2 | ABSORBED | DC-TOOL-002 | How many free cooling hours are available at this site location by month and what fraction of mechanical cooling can be displaced? |
| DC_Grid_Capacity_Quick_Check_v1_2_0.html | DC-F-GRD-001 | v1.2.0 | 42.6 | ABSORBED | DC-TOOL-006 | Is there sufficient grid capacity at this site to support the planned IT load growth without a new connection application? |
| DC_Ireland_vs_Europe_Comparator_v1_2_0.html | DC-F-CMP-001 | v1.2.0 | 29.7 | UNIQUE | n/a | How does this Irish facility compare to European peers on PUE, cost, renewable fraction, and carbon intensity, and where does it rank? |
| DC_Regulatory_Requirements_Checker_v1_2_0.html | DC-C-REG-001 | v1.2.0 | 29.7 | ABSORBED | DC-TOOL-007 | Which Irish planning, environmental, fire, and electrical regulatory requirements apply to this facility at its current scale? |

---

## Pipeline Files (screen/tools/pipeline/)

These are orchestration and rendering tools, not standalone screeners.

| Filename | TOOL_ID | Version | Size KB | Purpose | Inputs From | Outputs To |
|----------|---------|---------|---------|---------|-------------|-----------|
| DC-MSTR-001_v1_5_1.html | DC-MSTR-001 | v1.5.3 / v1.5.4 (title) | 82.3 | Master parameter store — project-level inputs that cascade to all screening tools in the pipeline | User (direct form entry) | All DC-R and DC-TOOL screening tools |
| DC-CPS-001_v1_0_2.html | DC-CPS-001 | v1.0.2 / v1.0.4 (title) | 285.3 | Carbon Position Statement — calculates carbon intensity, CREEM pathway alignment, and regulatory exposure | DC-MSTR-001 parameters + facility-specific inputs | DC-RPT-001 report renderer |
| DC-RPT-001_v1_2_1_final.html | (none) | v1.2.3 (comment) | 176.1 | Report renderer (CPS Mode) — produces formatted A4 HTML/PDF asset carbon risk screening report | DC-CPS-001 structured JSON | Print / PDF export |

---

## Lineage Map

For each v2.0 tool, the v1.x predecessors whose functionality it absorbed:

| v2.0 Tool | v1.x Predecessors | Key Fields Carried Forward | Fields / Scope Dropped |
|-----------|-------------------|---------------------------|----------------------|
| DC-TOOL-001 Power Chain Screener | DC-DIAG-001 (partial), DC-R-PWR-001, DC-SLD-001 | it_load_mw, pue, ups configuration, tx_rating, msb_rating | Sub-component bottleneck scoring from DC-SLD-001; multi-option ranking from DC-DIAG-001 |
| DC-TOOL-002 Cooling Chain Screener | DC-DIAG-001 (partial), DC-R-CLG-001, DC_Free_Cooling_Hours_Calculator | cooling_type, chiller config, containment, free_cooling flag, PUE | Option card comparison matrix from DC-R-CLG-001; monthly free-cooling bar chart from DC-M-FCL-001 |
| DC-TOOL-003 Redundancy Gap Tool | DC-DIAG-001 (partial) | target_tier, utility_feeds, ups_modules, msb_config, cooling_redundancy | Integrated cost/ROI comparison; no direct v1.x single-domain predecessor |
| DC-TOOL-004 Compliance Checker | DC-R-EED-001, DC-R-PUE-001 | pue, pue_gap, taxonomy_pue, annual_energy_mwh, renewable_gap_pct, co2_scope2, carbon_tax | WUE tracking; EMS and tempSetpoint fields from DC-R-EED-001; standalone PUE gauge chart |
| DC-TOOL-005 UPS Adequacy Tool | — (new in v2.0) | — | — |
| DC-TOOL-006 Grid Headroom Calculator | DC-R-PWR-001, DC-SLD-001, DC_Grid_Capacity_Quick_Check | mic_mva, tx_count, tx_rating_mva, utility_feeds, target_kw_rack, power_factor | Quick-check flag-list UI from DC-F-GRD-001; bottleneck cascade scoring from DC-SLD-001 |
| DC-TOOL-007 Regulatory Gap Screener | DC-R-EED-001, DC-R-FGS-001, DC_Regulatory_Requirements_Checker | eed_art26, refrigerant_type, refrigerant_gwp, refrigerant_charge_kg, planning_sid, epa_licence, ppa_pct | EMS, WUE, heat buyer fields from DC-R-EED-001; criticality-banded reg-item card UI |
| DC-TOOL-008 Fire Safety Screener | DC-R-FGS-001 (partial) | battery_type, has_bess, suppression_agent_kg, refrigerant charge fields | F-Gas phase-down timeline; refrigerant cost modelling from DC-R-FGS-001 |
| DC-TOOL-010 Facility Audit Checklist | — (new in v2.0) | — | — |
| DC-TOOL-011 Security Assessment Tool | — (new in v2.0) | — | — |
| DC-TOOL-012 Commissioning Readiness Tool | — (new in v2.0) | — | — |
| DC-TOOL-013 AI-Ready Cooling Screener | DC-R-CLG-001 (partial) | cooling_type, kw_per_rack, target_kw_rack, dlc_rack_count | Standard retrofit option matrix; payback / disruption scoring |
| DC-TOOL-014 CRU Readiness Screener | — (new in v2.0) | — | — |

---

## Observations

1. **DC-TOOL-009 slot is empty.** No tool with that number exists. Whether this was intentionally reserved, deleted, or never completed cannot be determined from the files alone.

2. **Five v1.x tools cover domains entirely absent from v2.0.**
   - *DC-R-HTR-001* — EU EED Article 12 waste heat recovery: no DC-TOOL equivalent.
   - *DC-R-ROI-001* — Retrofit vs rebuild NPV / IRR analysis: no DC-TOOL equivalent.
   - *DC-R-STR-001* — Multi-dimensional strategic misalignment risk radar: no DC-TOOL equivalent.
   - *DC_Cost_Per_MW_Benchmark* — CapEx elemental cost benchmarking: no DC-TOOL equivalent.
   - *DC_Ireland_vs_Europe_Comparator* — Regional peer benchmarking: no DC-TOOL equivalent.

3. **DC-R-FGS-001 is a functional outlier among v1.x files.** Despite its v1.0.x generation, it uses Tailwind CSS, has a full INTERPRETATION_PROMPT AI narrative layer, and exports JSON — capabilities only otherwise present in v2.0 tools or DC-DIAG-001. It may have been retrofitted or built after the others.

4. **DC-R-SUM-001 has no forward equivalent.** It aggregates JSON from the DC-R-* suite into a unified verdict dashboard. When (or if) the DC-R-* suite is retired, DC-R-SUM-001 becomes inoperable. No v2.0 cross-tool aggregator is visible in the file inventory.

5. **DC-SLD-001 is at v0.1.x — the only pre-release file in the repo.** It uses React 18 / Babel with a dark/light theme toggle, which matches no other file's architecture. It reads as an experiment or prototype that was later superseded by DC-TOOL-001 and DC-TOOL-006 without being promoted or removed.

6. **DC-DIAG-001 (272 KB) is the largest non-pipeline file and spans multiple domains.** Its multi-domain scope (power, cooling, cost, age, density) makes it the closest analogue to the entire DC-TOOL-001–DC-TOOL-003 cluster combined, suggesting it was the original monolithic diagnostic that the v2.0 suite decomposed into specialist tools.

7. **Four v2.0 tools (005, 010, 011, 012) have no identified v1.x predecessor.** UPS Adequacy, Facility Audit, Security Assessment, and Commissioning Readiness appear to be wholly new capabilities introduced in v2.0.

8. **Version numbers in filenames are often behind versions in code.** This pattern (filename = deploy version, code = latest edit) may indicate a deliberate release tagging practice, but creates ambiguity for tracking current versions by filename alone.

9. **DC-RPT-001 exists in two locations with identical content.** `screen/DC-RPT-001_v1_2_1_final.html` and `screen/tools/pipeline/DC-RPT-001_v1_2_1_final.html` are byte-for-byte identical. The root copy appears to be a stale duplicate of the pipeline-authoritative copy.

10. **No tool covers data centre connectivity / network infrastructure.** Power, cooling, fire, security, compliance, and commissioning are all represented in v2.0 but there is no screener for network redundancy, dark fibre diversity, or carrier-neutral connectivity — a common due-diligence dimension for colocation and hyperscale assets.
