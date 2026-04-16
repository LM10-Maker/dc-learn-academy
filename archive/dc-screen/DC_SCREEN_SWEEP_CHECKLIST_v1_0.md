# DC-SCREEN SWEEP CHECKLIST v1.0
# Legacy Business Engineers Ltd | 12 April 2026
# Run this checklist before every delivery. No exceptions.

---

## AUTOMATED CHECKS (run verify_screen.py)

| ID | Check | FAIL Condition | Blocking? |
|----|-------|---------------|-----------|
| S01 | Stale Canonical Values | Any stale value present (€83,050, 0.295, 0.185, €56, €63.50, Les McGuinness) | YES — instant block |
| S02 | Banned Terminology | Any banned term present (stranding, CRU Compliance, exact, quiz, Electrical Engineer, Hall 1/2, Aoife/Marcus/Síle, Ballycoolin) | YES |
| S03 | CRREM Derivation Disclosure | File references CRREM but contains no derivation disclosure | YES — PI exposure |
| S04 | Disclaimer Present | No screening disclaimer found in tool | YES — PI exposure |
| S05 | PI Statement Present | No Professional Indemnity reference | WARN |
| S06 | Version Consistency | Mixed version strings within same file | YES |
| S07 | Contact Email | Wrong email (les@legacybe.ie) or personal phone number | YES |
| S08 | Unicode Escapes | Literal \uXXXX sequences present | WARN (with count) |
| S09 | Clonshaugh Params | Clonshaugh mentioned but key params inconsistent | WARN |
| S10 | Source Tier Coverage | File has calculations but zero tier markers | WARN |
| S11 | Intelligence Layer Language | Prescriptive delivery language in CTA/marketing text | WARN |
| S12 | Canonical Values Present | Correct canonical values missing from calculation files | WARN |

**Ship condition:** Zero FAIL across all scanned tools. WARNs acceptable if acknowledged.

---

## MANUAL CHECKS (human review — not automatable)

| ID | Check | What to Look For |
|----|-------|-----------------|
| M01 | Ann readability | Can Ann hand this to her investment committee without explanation? |
| M02 | Section headers | Investment language, not engineering language? |
| M03 | Hold model assumptions | Visible, labelled, adjustable? Not hardcoded? |
| M04 | Sensitivity analysis | Base case + stressed case shown? |
| M05 | CRM revenue option | Available as optional input where investment returns are calculated? |
| M06 | Decision gate alignment | CTA prices consistent with service ladder? |
| M07 | Print layout | A4 clean, professional, no cut-off content, no browser chrome? |
| M08 | Demo data | Clonshaugh renders correctly with all canonical parameters? |
| M09 | Mark's voice | Diagnostic only? Zero prescriptive language (should/must/recommend/install/specify/design)? |
| M10 | Data chain | Does MSTR → CPS → RPT flow work end-to-end? |

---

## SWEEP PROCESS

1. Run `python3 verify_screen.py` — resolve all FAILs
2. Open each modified tool in browser with Clonshaugh demo data
3. Read RPT-001 output as Ann (M01–M02)
4. Check hold model (M03–M05)
5. Check decision gate (M06)
6. Print to PDF (M07)
7. Mark's voice spot-check on any diagnostic text (M09)
8. Append to `DC_SCREEN_OPS_LOG.md`
9. Verdict: SHIP or NOT SHIP

---

## DOCUMENT CONTROL

| Field | Value |
|-------|-------|
| Version | 1.0 |
| Date | 12 April 2026 |
| Author | LM + Claude |
| Status | ACTIVE |
| Origin | DC-LEARN governance adapted for screening tools |
| Companion | verify_screen.py, DC_SCREEN_OPS_LOG.md |
