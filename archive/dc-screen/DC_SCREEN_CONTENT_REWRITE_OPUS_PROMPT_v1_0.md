# DC-SCREEN CONTENT REWRITE — Opus Prompt
# Model: Opus | Repo: dc-learn-academy
# Date: 12 April 2026
# Dependency: Run AFTER DC_SCREEN_A_PLUS_CC_PROMPT_v1_0.md ships
# Scope: RPT-001 content rewrite — Ann's language throughout

## PREREQUISITE
DC-RPT-001 must be at v1.1.0 with P3 (editable hold model), P4 (CRM revenue),
P5 (sensitivity analysis), and P6 (title change) already applied.
If any of those are missing, STOP and report.

## CONTEXT
The report's exec summary already speaks Ann's language — three questions answered
in fund-manager terms. But the rest of the report reverts to engineering organising
principles. This session extends Ann's language through every section.

## WHO IS ANN
- Infrastructure fund manager, 20 years experience
- She commissions asset risk assessments, not carbon audits
- She presents to an investment committee that wants: risk, cost, return
- She doesn't read kgCO₂/MWh — she reads €, years, and % return
- She doesn't care HOW the engineering works — she cares WHAT IT MEANS for her hold thesis

## P2 — SECTION HEADER REFRAMING

Replace engineering-organised headers with investment-organised headers:

| Current Header | New Header | Rationale |
|----------------|------------|-----------|
| Carbon Intensity | Asset Carbon Position | Ann thinks in positions, not intensities |
| Key Metrics | Facility Performance Summary | Metrics is engineer language |
| CRREM Position | Regulatory Alignment Status | Ann cares about regulatory exposure, not CRREM methodology |
| Regulatory Exposure | Compliance Risk Register | She manages risk registers |
| Recommended Actions | Remediation Options & Economics | She needs economics attached to every action |
| Decision Gate (next step box heading) | Recommended Next Step | Cleaner |

### Important:
- The section CONTENT stays the same — only headers change
- The exec summary is already correct — do not touch it
- Do NOT change any variable names, function names, or IDs
- This is purely rendered text visible to the reader

## P7 — DECISION GATE CTA ALIGNMENT

The decision gate currently offers:
- Desktop Assessment: €10,000–€15,000 + VAT
- Disposal Analysis: €8,000–€12,000 + VAT
- Compliance Monitoring: from €5,000/yr + VAT

### Rewrite the CTA copy to:
1. **Desktop Assessment** — Position as the entry point to DC-S01:
   "A Desktop Assessment is the first step toward a full facility evaluation.
   It validates these screening figures with site-specific data, produces a
   phased remediation programme, and confirms whether the hold thesis is
   defensible. Delivered in 2–4 weeks."
   Price stays: €10,000–€15,000 + VAT
   Add: "(This is the entry point to our DC-S01 service.)"

2. **Disposal Analysis** — Position clearly:
   "Before committing capital, a Disposal Analysis benchmarks current market
   value against retrofit-then-sell economics. It identifies the optimal exit
   window and quantifies the cost of delay."
   Price stays: €8,000–€12,000 + VAT

3. **Compliance Monitoring** — Add context:
   "Annual monitoring tracks regulatory changes across CRU, EED, F-Gas, EU
   Taxonomy, and CRREM. Provides early warning if your facility's risk
   position changes."
   Price stays: from €5,000/yr + VAT

### Contact line:
Replace any "contact" text with:
"Contact: info@legacybe.ie | legacybe.ie"
Do NOT use personal email or phone number.

## CONSTRAINTS
- DO NOT change any JavaScript logic, calculations, or variable names
- DO NOT modify the disclaimer, sign-off, or CRREM derivation disclosure
- DO NOT change the exec summary (already correct)
- Changes are to rendered HTML text content only
- All changes must work in both screen and print layouts

## VERSION BUMP
- v1.1.0 → v1.1.1

## VERIFICATION
1. Open in browser with Clonshaugh demo data
2. Read page 1 header-to-footer as Ann — every header makes sense in investment language
3. Read page 2 — compliance risk register, remediation options with economics, decision gate
4. Print to PDF — clean, professional, investment-committee ready
5. The question: can Ann hand this to her IC without a cover note explaining it?

Commit and push directly to main. Do NOT create feature branches.
