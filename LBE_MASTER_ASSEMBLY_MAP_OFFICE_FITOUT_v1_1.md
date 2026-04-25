# LBE MASTER ASSEMBLY MAP — OFFICE FIT-OUT
## Complete WC A+ MEP Package | All Systems | Feasibility through Tender
### Legacy Business Engineers Ltd | 25 April 2026

---

## REFERENCE PROJECT PROFILE

| Parameter | Value |
|-----------|-------|
| Building type | Cat A / Cat B office fit-out |
| Typical GIA | 1,500 – 10,000 m² |
| Floors | 2–8 |
| Supply | ESB Networks 400V TPN |
| HVAC strategy | VRF / ASHP / Gas boiler (varies) |
| Standards | IS 10101:2020, TGD Part L 2021, TGD Part F, CIBSE Guides A/B/C/K/G |
| Design stages | Feasibility → Scheme Design → Detailed Design → Tender |

---

## PACKAGE STRUCTURE — 14 VOLUMES

A complete MEP package for a Tier 2/3 consultancy delivering an office fit-out contains 14 volumes. Each volume lists the deliverable sections, the tool or template that produces them, and the repo location.

---

### VOLUME 1: DESIGN BASIS & BRIEFING

| # | Deliverable | Tool / Template | Repo Location | Stage |
|:-:|-------------|-----------------|---------------|:-----:|
| 1.1 | Design basis statement | Manual / Production Std §9 | — | Feas |
| 1.2 | Electrical briefing register | LBE_BRIEFING_REGISTER_ELECTRICAL | Templates/Registers/ | Feas |
| 1.3 | Mechanical briefing register | LBE_BRIEFING_REGISTER_MECHANICAL | Templates/Registers/ | Feas |
| 1.4 | Scope and exclusions | Manual / Production Std §9 | — | Feas |
| 1.5 | Information relied upon | Manual / Production Std §9 | — | Feas |
| 1.6 | Assumptions log | From briefing registers | — | Feas |

---

### VOLUME 2: ELECTRICAL LOAD ASSESSMENT

| # | Deliverable | Tool / Template | Repo Location | Stage |
|:-:|-------------|-----------------|---------------|:-----:|
| 2.1 | Connected load by category | E-LC-001 Building Load Calculator | Tools/Electrical/ | Feas |
| 2.2 | Diversity factors applied | E-LC-002 Diversity Factor Calculator | Tools/Electrical/ | Feas |
| 2.3 | ADMD calculation | E-LC-003 ADMD Calculator | Tools/Electrical/ | Feas |
| 2.4 | Maximum demand | E-LC-004 Maximum Demand Calculator | Tools/Electrical/ | Feas |
| 2.5 | Harmonics assessment | E-LC-005 Harmonics Assessment | Tools/Electrical/ | Feas |
| 2.6 | Power factor assessment | E-LC-006 Power Factor Correction | Tools/Electrical/ | Feas |
| 2.7 | K-factor transformer sizing | E-LC-007 K-Factor Transformer | Tools/Electrical/ | Feas |
| 2.8 | Day/night load profile | S2_Part1 Load Baseline engine | Engines/ | Feas |
| 2.9 | ESB supply sizing & cost | E-ESB-001 to E-ESB-004 | Tools/Electrical/ | Feas |
| 2.10 | Load assessment report (docx) | LBE docx template + engine | Engines/ | Feas |

**Skill chain:** electrical-load-calculation skill → electrical-equipment-design skill

---

### VOLUME 3: MECHANICAL LOAD ASSESSMENT

| # | Deliverable | Tool / Template | Repo Location | Stage |
|:-:|-------------|-----------------|---------------|:-----:|
| 3.1 | Heating load calculation | M-HL-001 Heating Load Calculator | Tools/Mechanical/ | Feas |
| 3.2 | Cooling load calculation | M-HL-002 Cooling Load Calculator | Tools/Mechanical/ | Feas |
| 3.3 | Ventilation rates | M-HL-003 Ventilation Rate Calculator | Tools/Mechanical/ | Feas |
| 3.4 | Air change rates | M-HL-004 Air Change Calculator | Tools/Mechanical/ | Feas |
| 3.5 | U-value verification | M-HL-005 U-Value Calculator | Tools/Mechanical/ | Feas |
| 3.6 | Heat loss (room-by-room) | M-HL-006 Heat Loss Calculator | Tools/Mechanical/ | SD |
| 3.7 | Solar gain assessment | M-HL-007 Solar Gain Calculator | Tools/Mechanical/ | Feas |

**Skill chain:** mep-base-layer → mechanical load tools

---

### VOLUME 4: PLANT SIZING & SELECTION PARAMETERS

| # | Deliverable | Tool / Template | Repo Location | Stage |
|:-:|-------------|-----------------|---------------|:-----:|
| 4.1 | Boiler / ASHP sizing | BoilerHeatPumpPlantSizer | Tools/Mechanical/ | SD |
| 4.2 | Chiller sizing parameters | SpaceHeatingCoolingLoadEstimator | Tools/InDevelopment/ | SD |
| 4.3 | AHU sizing parameters | AHU_Selection_Tool_v1 | Tools/Mechanical/ | SD |
| 4.4 | Heat pump SCOP/SEER | M-HP-002 SCOP/SEER Calculator | Tools/Mechanical/ | SD |
| 4.5 | Buffer vessel sizing | M-HP-003 Buffer Vessel Sizing | Tools/Mechanical/ | SD |
| 4.6 | Heat recovery assessment | M-AH-002 Heat Recovery Calculator | Tools/Mechanical/ | SD |
| 4.7 | Pump sizing | M-PW-002 Pump Selection Calculator | Tools/Mechanical/ | DD |
| 4.8 | Expansion vessel sizing | M-PW-003 Expansion Vessel Sizing | Tools/Mechanical/ | DD |
| 4.9 | Transformer / switchgear sizing | Electrical equipment design skill | Skills/ | SD |
| 4.10 | Generator sizing | E-GEN-001 Generator Sizing | Tools/Electrical/ | SD |
| 4.11 | UPS sizing | E-UPS-001 UPS Sizing | Tools/Electrical/ | SD |
| 4.12 | Lift specification parameters | LBE_SPEC_LIFT_TEMPLATE | Templates/Specifications/Lift/ | SD |

**Note — Mode A:** LBE calculates sizing parameters. Equipment selection (make/model) is the design team's responsibility. **Mode B:** LBE sizes and provides selection parameters including duty, capacity, dimensions, and connection sizes; final manufacturer selection subject to client approval at detailed design.

---

### VOLUME 5: PLANT ROOM & SPATIAL COORDINATION

| # | Deliverable | Tool / Template | Repo Location | Stage |
|:-:|-------------|-----------------|---------------|:-----:|
| 5.1 | Plant room sizing | PlantRoomLayoutTool_v1.7 | Tools/Mechanical/ | Feas |
| 5.2 | Electrical room / riser sizing | Electrical Riser Engineering Guide | Project Knowledge | Feas |
| 5.3 | Maintenance zone allowances | MEP Space Allocation Reference | Project Knowledge | Feas |
| 5.4 | Ceiling void depth check | ARCH-MEP-02 CeilingVoidChecker | Tools/InDevelopment/ or DC/ | Feas |
| 5.5 | Basement requirements schedule | Manual — from plant sizing outputs | — | SD |
| 5.6 | Roof plant requirements | Manual — from plant sizing outputs | — | SD |
| 5.7 | External ground requirements | Manual — from plant sizing outputs | — | SD |
| 5.8 | Architect coordination pack | Riser guide + space ref + void checker outputs | Combined | Feas |
| 5.9 | Coordination drawings list | Manual — list of drawings LBE will issue or mark up at each stage | — | SD |

**Key output:** Schedule of rooms/spaces the architect needs to accommodate, with dimensions (mm), access requirements, ventilation needs, and structural loading implications. Include list of MEP drawings to be issued or marked up (plant layouts, riser diagrams, ceiling coordination, external services).

---

### VOLUME 6: ELECTRICAL DISTRIBUTION

| # | Deliverable | Tool / Template | Repo Location | Stage |
|:-:|-------------|-----------------|---------------|:-----:|
| 6.1 | Distribution board schedules | E-DB-001 DB Schedule Generator | Tools/Electrical/ | DD |
| 6.2 | Physical board sizing | E-DB-002 Physical Board Sizing | Tools/Electrical/ | DD |
| 6.3 | Cable sizing (all circuits) | E-CS-001 Cable Sizing Calculator | Tools/Electrical/ | DD |
| 6.4 | Voltage drop verification | E-CS-002 Voltage Drop Optimiser | Tools/Electrical/ | DD |
| 6.5 | Cable derating | E-CS-003 Cable Derating | Tools/Electrical/ | DD |
| 6.6 | Busbar sizing | E-CS-004 Busbar Sizing | Tools/Electrical/ | DD |
| 6.7 | Cable tray/containment sizing | E-CS-005 Cable Tray Sizing | Tools/Electrical/ | DD |
| 6.8 | Cable grouping factors | E-CS-007 Cable Grouping | Tools/Electrical/ | DD |
| 6.9 | Form type selection | E-DB-005 Form Type Selector | Tools/Electrical/ | DD |
| 6.10 | IP rating selection | E-DB-006 IP Rating Selector | Tools/Electrical/ | DD |

**Skill chain:** electrical-distribution-design skill

---

### VOLUME 7: MECHANICAL DISTRIBUTION

| # | Deliverable | Tool / Template | Repo Location | Stage |
|:-:|-------------|-----------------|---------------|:-----:|
| 7.1 | Duct sizing | M-DW-001 Duct Sizing Calculator | Tools/Mechanical/ | DD |
| 7.2 | Duct pressure drop | M-DW-002 Duct Pressure Drop | Tools/Mechanical/ | DD |
| 7.3 | Fan selection parameters | M-DW-003 Fan Selection | Tools/Mechanical/ | DD |
| 7.4 | Grille/diffuser sizing | M-DW-004 Grille/Diffuser Sizing | Tools/Mechanical/ | DD |
| 7.5 | LTHW/CHW pipe sizing | M-PW-001 HVAC Pipe Sizing | Tools/Mechanical/ | DD |
| 7.6 | Pipework sizing (general) | lthw-chw-pipe-sizing-tool | Tools/Mechanical/ | DD |
| 7.7 | Pipework insulation specification | Mech master spec §insulation + TGD Part L Table 7 | Templates/Specifications/Mechanical/ | DD |
| 7.8 | Ductwork insulation specification | Mech master spec §insulation + CIBSE Guide B §3.6 | Templates/Specifications/Mechanical/ | DD |

---

### VOLUME 8: PROTECTION & COMPLIANCE

| # | Deliverable | Tool / Template | Repo Location | Stage |
|:-:|-------------|-----------------|---------------|:-----:|
| 8.1 | Circuit breaker selection data | E-PR-001 Circuit Breaker Selector | Tools/Electrical/ | DD |
| 8.2 | RCD selection data | E-PR-002 RCD Selector | Tools/Electrical/ | DD |
| 8.3 | Fault level calculation | E-PR-003 Fault Level Calculator | Tools/Electrical/ | DD |
| 8.4 | Discrimination study | E-PR-004 Discrimination Study | Tools/Electrical/ | DD |
| 8.5 | Arc flash assessment | E-PR-005 Arc Flash Calculator | Tools/Electrical/ | DD |
| 8.6 | SPD selection data | E-PR-007 SPD Selector | Tools/Electrical/ | DD |
| 8.7 | Earth electrode calculation | E-EA-001 Earth Electrode | Tools/Electrical/ | DD |
| 8.8 | Earth conductor sizing | E-EA-002 Earth Conductor | Tools/Electrical/ | DD |
| 8.9 | Loop impedance verification | E-EA-003 Loop Impedance | Tools/Electrical/ | DD |
| 8.10 | Part L compliance check | EC-PL-001 Part L Checker | Tools/Energy/ | SD |
| 8.11 | nZEB pathway | EC-NZ-001 NZEB Calculator | Tools/Energy/ | SD |
| 8.12 | BER pre-assessment | EC-BER-001 BER Pre-Assessment | Tools/Energy/ | Feas |
| 8.13 | Part F ventilation compliance | M-HL-003 outputs verified against TGD Part F Tables 1/2/3 | Tools/Mechanical/ + manual check | SD |
| 8.14 | BCAR 1401 Design Certificate | LBE_BCAR_1401_DESIGN_TEMPLATE | Templates/BCAR/ | DD |
| 8.15 | BCAR 1403 Inspection Plan | LBE_BCAR_1403_INSPECTION_TEMPLATE | Templates/BCAR/ | DD |

**Skill chain:** electrical-protection-compliance skill

---

### VOLUME 9: FIRE PROTECTION

| # | Deliverable | Tool / Template | Repo Location | Stage |
|:-:|-------------|-----------------|---------------|:-----:|
| 9.1 | Fire alarm system parameters | F-FA-001 Fire Alarm Calculator | Tools/Fire/ | SD |
| 9.2 | Emergency lighting calculation | F-EL-001 Emergency Lighting | Tools/Fire/ | SD |
| 9.3 | Sprinkler system parameters | F-SP-001 Sprinkler Calculator | Tools/Fire/ | SD |
| 9.4 | Smoke extract parameters | F-SM-001 Smoke Extract | Tools/Fire/ | DD |
| 9.5 | Fire damper schedule | F-DR-001 Fire Damper Schedule | Tools/Fire/ | DD |
| 9.6 | Compartmentation assessment | F-CO-001 Compartmentation | Tools/Fire/ | SD |
| 9.7 | Fire alarm cert template | LBE_CERT_FIRE_ALARM_TEMPLATE | Templates/Certificates/ | DD |
| 9.8 | Emergency lighting cert template | LBE_CERT_EMERGENCY_LIGHTING_TEMPLATE | Templates/Certificates/ | DD |

---

### VOLUME 10: PLUMBING & DRAINAGE

| # | Deliverable | Tool / Template | Repo Location | Stage |
|:-:|-------------|-----------------|---------------|:-----:|
| 10.1 | Cold water pipe sizing | P-WS-001 Cold Water Pipe Sizing | Tools/Plumbing/ | DD |
| 10.2 | Water storage calculation | P-WS-002 Water Storage | Tools/Plumbing/ | SD |
| 10.3 | DHW system calculation | P-DHW-001 DHW System Calculator | Tools/Plumbing/ | SD |
| 10.4 | Calorifier sizing | P-DHW-002 Calorifier Sizing | Tools/Plumbing/ | SD |
| 10.5 | Sanitary fixture count | P-SF-001 Sanitary Fixture | Tools/Plumbing/ | Feas |
| 10.6 | Loading units calculation | P-SF-002 Loading Units | Tools/Plumbing/ | SD |
| 10.7 | Drainage stack sizing | P-DS-001 Drainage Stack | Tools/Plumbing/ | DD |
| 10.8 | Foul drainage calculation | FoulDrainageCalculator | Tools/Plumbing/ | DD |
| 10.9 | Rainwater calculation | P-RW-001 Rainwater Calculator | Tools/Plumbing/ | SD |
| 10.10 | Attenuation sizing | P-RW-002 Attenuation Tank | Tools/Plumbing/ | SD |

---

### VOLUME 11: SPECIFICATIONS

| # | Deliverable | Tool / Template | Repo Location | Stage |
|:-:|-------------|-----------------|---------------|:-----:|
| 11.1 | Electrical intro | LBE_ELEC_INTRO_TEMPLATE | Templates/Specifications/Electrical/ | Tender |
| 11.2 | E60 Site services | LBE_SPEC_E60_TEMPLATE | Templates/Specifications/Electrical/ | Tender |
| 11.3 | E61 Distribution | LBE_SPEC_E61_TEMPLATE | Templates/Specifications/Electrical/ | Tender |
| 11.4 | E62 Power | LBE_SPEC_E62_TEMPLATE | Templates/Specifications/Electrical/ | Tender |
| 11.5 | E63 Lighting | LBE_SPEC_E63_TEMPLATE | Templates/Specifications/Electrical/ | Tender |
| 11.6 | E64 Communications | LBE_SPEC_E64_TEMPLATE | Templates/Specifications/Electrical/ | Tender |
| 11.7 | E65 Fire alarm | LBE_SPEC_E65_TEMPLATE | Templates/Specifications/Electrical/ | Tender |
| 11.8 | E66 Lightning protection | LBE_SPEC_E66_TEMPLATE | Templates/Specifications/Electrical/ | Tender |
| 11.9 | E67 Security | LBE_SPEC_E67_TEMPLATE | Templates/Specifications/Electrical/ | Tender |
| 11.10 | E68 EV / Renewables | LBE_SPEC_E68_TEMPLATE | Templates/Specifications/Electrical/ | Tender |
| 11.11 | Mechanical master spec | LBE_MECH_MASTER_SPEC_TEMPLATE | Templates/Specifications/Mechanical/ | Tender |
| 11.12 | Sprinkler spec (commercial) | LBE_SPEC_SPRINKLER_COMMERCIAL | Templates/Specifications/Sprinkler/ | Tender |
| 11.13 | Lift spec | LBE_SPEC_LIFT_TEMPLATE | Templates/Specifications/Lift/ | Tender |

---

### VOLUME 12: SCHEDULES

| # | Deliverable | Tool / Template | Repo Location | Stage |
|:-:|-------------|-----------------|---------------|:-----:|
| 12.1 | DB schedules | E-DB-001 output | Tools/Electrical/ | DD |
| 12.2 | Luminaire schedule | LBE_SCHEDULE_LUMINAIRE_TEMPLATE | Templates/Schedules/ | DD |
| 12.3 | Lighting selection schedule | LBE_SCHEDULE_LIGHTING_SELECTION | Templates/Schedules/ | DD |
| 12.4 | External lighting schedule | LBE_SCHEDULE_EXTERNAL_LIGHTING | Templates/Schedules/ | DD |
| 12.5 | Accessories schedule | LBE_SCHEDULE_ACCESSORIES_TEMPLATE | Templates/Schedules/ | Tender |
| 12.6 | BWIC schedule | LBE_BWIC_SCHEDULE_TEMPLATE | Templates/Schedules/ | Tender |
| 12.7 | Tie-in schedule | LBE_TIE_IN_SCHEDULE_TEMPLATE | Templates/Schedules/ | Tender |
| 12.8 | Mechanical equipment schedule | **GAP — template needed** | — | DD |
| 12.9 | Valve schedule | **GAP — template needed** | — | DD |
| 12.10 | Strip-out schedule | **GAP — template needed** | — | Tender |

---

### VOLUME 13: SCHEMATICS & DIAGRAMS

| # | Deliverable | Tool / Template | Repo Location | Stage |
|:-:|-------------|-----------------|---------------|:-----:|
| 13.1 | Electrical SLD | E-DB-003 SLD Generator | Tools/Electrical/ | DD |
| 13.2 | HVAC schematic | **GAP — no tool** | — | DD |
| 13.3 | Plumbing schematic | **GAP — no tool** | — | DD |
| 13.4 | Fire alarm schematic | **GAP — no tool** | — | DD |
| 13.5 | BMS schematic | **GAP — no tool** | — | DD |

---

### VOLUME 14: ADMIN, RISK & COMMERCIAL

| # | Deliverable | Tool / Template | Repo Location | Stage |
|:-:|-------------|-----------------|---------------|:-----:|
| 14.1 | Risk assessment (design) | LBE_RISK_ASSESSMENT_DESIGN_TEMPLATE | Templates/Risk/ | All |
| 14.2 | Risk assessment (operational) | LBE_RISK_ASSESSMENT_OPERATIONAL | Templates/Risk/ | Tender |
| 14.3 | Submittal register | LBE_SUBMITTAL_REGISTER_TEMPLATE | Templates/Registers/ | Tender |
| 14.4 | Transmittal register | LBE_TRANSMITTAL_REGISTER_TEMPLATE | Templates/Registers/ | Tender |
| 14.5 | Recommendation register | LBE_RECOMMENDATION_TEMPLATE | Templates/Registers/ | All |
| 14.6 | Submittal process | LBE_SUBMITTAL_PROCESS_TEMPLATE | Templates/Process/ | Tender |
| 14.7 | Site inspection guide | LBE_SITE_INSPECTION_GUIDE | Templates/Process/ | Tender |
| 14.8 | Compliance opinion cert | LBE_CERT_OPINION_COMPLIANCE_TEMPLATE | Templates/Certificates/ | DD |
| 14.9 | Tender summary | LBE_TENDER_SUMMARY_LIFT_TEMPLATE | Templates/Process/ | Tender |
| 14.10 | Fee proposal | mep-fee-calculator skill | Skills/ | Feas |
| 14.11 | Budget estimate | mep-budget-calculator skill | Skills/ | Feas |
| 14.12 | BCAR 1402 Completion cert | LBE_BCAR_1402_COMPLETION_TEMPLATE | Templates/BCAR/ | PC |

---

## GAP REGISTER — ITEMS NEEDED FOR COMPLETE PACKAGE

| # | Gap | Type | Priority | Effort |
|:-:|-----|------|:--------:|:------:|
| 1 | Mechanical equipment schedule template | Template | HIGH | 1 session |
| 2 | Valve schedule template | Template | MEDIUM | 0.5 session |
| 3 | Strip-out schedule template | Template | MEDIUM | 0.5 session |
| 4 | HVAC schematic generator | Tool | LOW | Defer — typically drawn, not calculated |
| 5 | Plumbing schematic generator | Tool | LOW | Defer — typically drawn, not calculated |
| 6 | Fire alarm schematic generator | Tool | LOW | Defer — typically drawn, not calculated |
| 7 | BMS schematic generator | Tool | LOW | Defer — typically drawn, not calculated |
| 8 | General tender summary template (beyond lift) | Template | HIGH | 1 session |

**Total gap to close:** 3 templates (HIGH priority), 1 template (MEDIUM), 4 schematics (LOW — defer).

---

## PRODUCTION SEQUENCE — STAGE BY STAGE

### FEASIBILITY (Volumes 1, 2, 3, 5 partially, 14.10, 14.11)

```
1. Briefing registers → populate from client brief
2. M-HL-001/002/003 → heating, cooling, ventilation loads
3. E-LC-001 through E-LC-007 → electrical loads, diversity, ADMD, harmonics
4. E-ESB-001 through E-ESB-004 → ESB supply sizing
5. PlantRoomLayoutTool → spatial requirements
6. Riser guide + space ref → architect coordination data
7. EC-BER-001 → BER pre-assessment
8. mep-budget-calculator → cost estimate
9. mep-fee-calculator → fee proposal
10. Assemble feasibility report
```

### SCHEME DESIGN (Volumes 4, 8.10-8.12, 9 partially)

```
1. Plant sizing tools → boiler, chiller, AHU, transformer, generator
2. E-DB-001 → preliminary DB schedules
3. EC-PL-001 + EC-NZ-001 → Part L / nZEB compliance path
4. Fire protection calculators → alarm, emergency lighting, sprinkler
5. P-WS/DHW/SF tools → water supply, DHW, fixture count
6. Update spatial coordination with sized plant
7. Assemble scheme design report
```

### DETAILED DESIGN (Volumes 6, 7, 8, 9, 10, 12, 13)

```
1. E-CS-001 through E-CS-008 → full cable schedule
2. E-DB-001 through E-DB-008 → complete DB design
3. E-PR-001 through E-PR-008 → full protection coordination
4. E-EA-001 through E-EA-003 → earthing
5. M-DW-001 through M-DW-004 → duct sizing
6. M-PW-001 through M-PW-003 → pipe sizing
7. All schedules populated
8. SLD generated (E-DB-003)
9. BCAR 1401 + 1403
10. Assemble detailed design report
```

### TENDER (Volumes 11, 12, 14)

```
1. Populate all 13 specification templates
2. Complete all schedules (luminaire, accessories, BWIC, tie-in)
3. Risk assessments
4. Submittal/transmittal registers
5. Tender summary
6. Assemble tender package
```

---

## TOOL COUNT SUMMARY

| Category | Available | Used in Package | Coverage |
|----------|:---------:|:---------------:|:--------:|
| Electrical tools | 48 | 37 | 77% |
| Mechanical tools | 10 | 10 | 100% |
| Plumbing tools | 3 | 3+ (more in repo) | ~80% |
| Fire tools | 3 | 3+ (more in repo) | ~75% |
| Energy tools | 26 | 6 | 23% |
| Templates | 37 | 33 | 89% |
| Skills | 9 | 7 | 78% |
| Engines | 10 | 4 | 40% |

**Overall coverage: ~85% of a complete office fit-out package can be produced from existing tools and templates.**

---

## DOCUMENT CONTROL

| Field | Value |
|-------|-------|
| Version | 1.0 |
| Date | 25 April 2026 |
| Author | LM / Claude |
| Status | DRAFT — for Les's review |
| Next action | Fill the 3 HIGH-priority template gaps, then run a pilot package |

---

*LBE Master Assembly Map — Office Fit-Out v1.0 | 25 April 2026 | Legacy Business Engineers Ltd*
