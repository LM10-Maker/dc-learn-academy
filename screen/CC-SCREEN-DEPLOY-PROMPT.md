# CC DEPLOY PROMPT — screen.legacybe.ie v2
# Run in Claude Code against dc-learn-academy repo
# Date: April 2026
# Commit directly to main — no branches, no PRs

---

## PRE-FLIGHT

```bash
git checkout main
git pull origin main
ls screen/
```

Expected current contents: assets/ tools/ _redirects index.html intake-form.html netlify.toml thank-you.html

---

## STEP 1 — REPLACE EXISTING FILES

Download from the ZIP and overwrite these four files in screen/:

| File | Action |
|------|--------|
| index.html | REPLACE — 6-card grid, full service ladder, updated branding |
| intake-form.html | REPLACE — minor wording updates |
| thank-you.html | REPLACE — minor wording updates |
| netlify.toml | REPLACE — adds /hz-thank-you redirect |

---

## STEP 2 — ADD NEW FILES

Copy these files from the ZIP into screen/ (all are new, none exist yet):

| File | What it is |
|------|-----------|
| hz-intake-form.html | Hybrid Zoning intake form (parked — not linked from index) |
| hz-thank-you.html | HZ confirmation page |
| LBE-SCR-Service-OnePager.html | Screening Report service description |
| LBE-AIR-Service-OnePager.html | AI Readiness service description |
| LBE-HZ-Service-OnePager.html | Hybrid Zoning service description |
| DC-RPT-HZ-001_v1_0_0.html | Hybrid Zoning sample report |
| DC-RPT-AIR-001_v1_0_0.html | AI Readiness sample report |

---

## STEP 3 — DO NOT TOUCH

Leave these untouched — no changes needed:

- screen/assets/ (entire folder)
- screen/tools/ (entire folder)
- screen/_redirects

---

## STEP 4 — COMMIT AND PUSH

```bash
git add screen/
git commit -m "screen.legacybe.ie v2 — 6 service cards, HZ + AIR reports, three one-pagers, updated service ladder, SAMPLE branding, black text sweep"
git push origin main
```

---

## STEP 5 — AFTER PUSH (manual steps, not CC)

1. Netlify auto-deploys on push to main — confirm at app.netlify.com
2. Netlify dashboard → Forms → set notification email to lmurphy@legacybe.ie for:
   - screening-intake
   - hz-intake
3. Print DC-RPT-HZ-001_v1_0_0.html to PDF in Chrome → save as sample-hz-report.pdf → upload to screen/
4. Print DC-RPT-AIR-001_v1_0_0.html to PDF in Chrome → save as sample-air-report.pdf → upload to screen/
5. Commit the two PDFs: git add screen/*.pdf && git commit -m "Add sample report PDFs" && git push origin main

---

## VERIFY LIVE

Check these URLs load correctly after deploy:
- screen.legacybe.ie (6 cards visible)
- screen.legacybe.ie/LBE-HZ-Service-OnePager.html
- screen.legacybe.ie/LBE-AIR-Service-OnePager.html
- screen.legacybe.ie/LBE-SCR-Service-OnePager.html
- screen.legacybe.ie/sample-screening-report.pdf (already live)

