# DC-AI-001 RUNNING FIX LOG
# Issues identified from v2.1.0 light theme screenshot review
# April 2026

---

## OPEN FIXES (from v2.1.0 review)

### FIX-A: "Currently Selected" card is too prominent
**Screenshot:** Expanded chain card shows full plainEnglish text, source note,
cross-references in a large card between the chain list and persona section.
**Problem:** This creates a wall of text that breaks the compact chain list flow.
DC-LEARN doesn't have this — clicking a level goes to the Learn tab, not an
expanded card on the Chain tab.
**Fix:** Remove the "Currently Selected" expanded detail card from the Chain tab
entirely. Clicking a chain row should navigate to Learn tab at that level
(which it already does via "Select this level →"). The expanded card is
redundant — the Learn tab already shows all that content.

### FIX-B: "Viewing As" persona section — wrong position and prominence
**Screenshot:** Sits as a separate card below the chain list with excessive
whitespace above and below. Visually disconnected from the chain.
**Problem:** In DC-LEARN, the persona selector is integrated INTO the chain
tab — compact, below the level list, same visual weight. DC-AI renders it
as a standalone padded card that looks like a separate feature.
**Fix:** 
- Remove the outer `.card` wrapper around the persona selector
- Reduce padding to match chain card rows
- Move it DIRECTLY below the last chain row (L9) with 0.5rem gap
- Remove "Viewing As" card title — just show the persona buttons directly
  with a subtle label: "View through a professional lens:"
- The relevance rows should sit flush, not in a padded card

### FIX-C: Sidebar text overflow / cut-off (light theme)
**Screenshot:** Methodology text appears truncated at the right edge.
**Problem:** Sidebar width may be too narrow or text not wrapping properly
in light theme. The sidebar panel right-edge clips content.
**Fix:** 
- Verify sidebar min-width and max-width work in both themes
- Ensure all sidebar text has `word-wrap: break-word`
- Check if Methodology description text needs smaller font (0.75rem)
- Test in both dark and light themes

---

## PREVIOUSLY FIXED (v2.0.0 → v2.1.0)

| Fix | Status |
|-----|--------|
| Grammar facts collapsed by default | ✅ Done |
| Card spacing tightened | ✅ Done |
| Persona rows compacted to one-liners | ✅ Done |
| Cross-ref pills shrunk | ✅ Done |
| Cascade PASS/FAIL inline on chain cards | ✅ Done |
| Empty card-icon divs removed | ✅ Done |
| CTA copy updated | ✅ Done |
| Sidebar titles cleaned | ✅ Done |
| Chain level names — no uppercase, proper size | ✅ Done |
| Gap standardisation | ✅ Done |
| Emoji cleanup (G-NEW-33) | ✅ Done |
| Colour match to DC-LEARN-002 | ✅ Done |
| Logo circle (border-radius 50%) | ✅ Done |
| Chain cards green (not blue) | ✅ Done |
| Persona icon emojis removed | ✅ Done |

---

## CC PROMPT FOR FIX-A + FIX-B + FIX-C

```
Read DC-AI-001_v2_1_0.html from the repo. Apply 3 targeted fixes.
Each fix is ONE Python script under 100 lines. Zero content changes.

Fix A: Remove the "Currently Selected" expanded detail card from ChainTab.
It's the card that shows plainEnglish, source note, and cross-references
for the selected level. Delete this entire section. The chain tab should
ONLY show: (1) the chain description card, (2) the 9 collapsed level rows,
(3) the persona selector. Clicking "Select this level →" already navigates
to the Learn tab — the expanded card is redundant.

Fix B: Simplify the persona selector section on the chain tab.
Remove the outer .card wrapper. Remove the "Viewing As" title.
Replace with a subtle inline label: "View through a professional lens:"
followed by the persona buttons on the same line. The relevance rows
(when a persona is selected) should render flush below with no card
padding — just rows with a bottom border. Reduce the entire persona
section's visual weight to match a sidebar panel, not a main content card.

Fix C: Fix sidebar text overflow in light theme. Add word-wrap: break-word
to .sidebar-card-title and sidebar paragraph text. Reduce Methodology
description font to 0.75rem. Verify sidebar works in both themes.

Version bump to 2.2.0. Verify 27 questions, 45 facts.
Save as DC-AI-001_v2_2_0.html.
```

---

## FACTORY LESSON L17

**L17: The Chain tab is a navigation tool, not a content display.**
DC-LEARN's chain tab shows compact level rows → click → Learn tab.
DC-AI added an expanded "Currently Selected" card and a prominent
persona card that turned the Chain tab into a second content tab.
Rule: Chain tab = compact list + calculator sidebar. All content
lives in the Learn tab. The persona selector is a navigation aid,
not a feature showcase.

---

*DC-AI Running Fix Log v1.0 | April 2026*
