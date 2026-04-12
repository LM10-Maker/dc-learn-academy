# DC-AI FINAL POLISH — BEST OF BOTH
# What DC-LEARN does better → adopt. What DC-AI does better → keep.
# Input: DC-AI-001_v2_0_0.html
# Output: DC-AI-001_v2_1_0.html
# CC session: Sonnet, one script per fix, each under 100 lines

---

## KEEP FROM DC-AI (better than DC-LEARN)

| Feature | Why it's better |
|---------|----------------|
| Content depth | Web-verified 2026 sources, clause-level refs, position-tested Qs |
| 9-level chain (not 9-level + anatomy) | Cleaner progression for investment audience |
| Collapsed chain cards | Click to expand — DC-LEARN shows all rows flat |
| Cross-ref tags to other DC-AI modules | Investment pathway connections |
| Audience bar text | Fund-specific: "Fund Managers · Asset Owners · Colocation Executives" |
| Reference tab (not BSG) | Clearer label for fund manager audience |
| Merged Learn tab | Grammar/Logic/Rhetoric as stage buttons — single tab |

## ADOPT FROM DC-LEARN (fix in DC-AI)

### FIX 1: Grammar facts collapsed by default
**DC-LEARN:** Each grammar fact shows just the term name as a clickable row.
Click to expand → shows definition, plain English, numbers, soWhat.
**DC-AI current:** All fact content dumps at once — wall of text.
**Fix:** Make each fact a collapsible row. Default: closed. Show term name
only. Click: expand to reveal full content. Same pattern as chain cards.

### FIX 2: Card spacing — tighten to DC-LEARN density
**DC-LEARN:** 8px gap between level rows. 12px card padding. Compact.
**DC-AI current:** 16–24px gaps, generous padding. Too much whitespace.
**Fix:**
- Chain card gap: 0.5rem (8px) — already correct
- Chain card padding: 0.6rem 0.8rem (was 0.75rem 1rem)
- Grammar fact card gap: 0.4rem (was 1rem or more)
- Grammar fact card padding: 0.6rem 0.8rem
- Section gaps: 0.75rem between major sections (was 1.5rem)
- Card border-radius: 8px (not 12px)
- Remove excessive margin-top/margin-bottom on inner elements

### FIX 3: Persona relevance map — compact one-liner rows
**DC-LEARN:** Persona selector shows compact rows: "L5 · title → Rhetoric →"
**DC-AI current:** Full paragraph per level with "Learn →" buttons.
**Fix:** Each relevance row = one line:
`[L1 badge] Level title [one-sentence takeaway, max 80 chars] [Rhetoric →]`
No paragraph text. No "Learn →" button. Just the row clicks through.
Max height for the entire section: 350px with overflow scroll if needed.

### FIX 4: Cross-reference tags — small subtle pills
**DC-LEARN:** Small mono pills, muted colour, ~12px font.
**DC-AI current:** Oversized pills with full descriptions.
**Fix:** Cross-ref pills: font-size 0.65rem, --text-muted colour,
--panel background, 1px --border, max 30 chars per pill. Truncate
long descriptions. No module IDs in pill text — just the short label.

### FIX 5: Cascade results inline on chain cards
**DC-LEARN:** After "Find Bottlenecks", each chain level row shows
a PASS/FAIL badge with the reason string. Green/red left border.
**DC-AI current:** Results only in sidebar.
**Fix:** After cascade runs, add a state variable `cascadeResults`.
In each chain level row, if cascadeResults[idx] exists, show:
- Left border: 2px green (pass) or red (fail)
- Badge: "PASS" (green) or "FAIL" (red) — small pill, 0.6rem
- Reason: one line, --text-dim, 0.72rem, truncated with ellipsis

### FIX 6: Empty card-icon divs — remove or use initials
**Current:** After emoji removal, card-icon divs are empty coloured circles.
**Fix:** Either remove the card-icon div entirely (cleaner), or put a
single-letter initial inside (G for Grammar, L for Logic, R for Rhetoric,
F for Field, A for Assessment, P for Progress). Match DC-LEARN pattern.

### FIX 7: CTA copy — make it specific
**DC-LEARN:** "From learning to practice — The real-world version of what
this module teaches is a DC Performance Assessment..."
**DC-AI current:** "Need to know where your facility stands on AI readiness?"
**Fix:** Left CTA:
- Title: "From learning to practice"
- Body: "The real-world version of what this module teaches is an AI
  Readiness Assessment — an independent screening of your facility's
  power, cooling, and structural capacity for GPU-class density.
  From desktop screening (€8,500) to full programme management."
- Button: "Learn about AI Readiness Assessment →" → legacybe.ie

### FIX 8: Sidebar title icons — text not emoji
**Current:** Some sidebar card-icon divs are now empty after emoji removal.
**Fix:** Remove the card-icon div from sidebar titles entirely. Just use
the text title: "Cascade Calculator", "Facility Profile", "Methodology".
Bold, 0.9rem, --text-bright. No icon circle needed — the sidebar is
already visually distinct.

---

## CC PROMPT

Paste this into a NEW Claude Code session:

```
Read DC-AI-001_v2_0_0.html from the repo. Apply 8 targeted fixes.
Each fix is ONE Python script under 100 lines. Run them sequentially.
ZERO content changes — only CSS, layout, and component structure.

Fix 1: Collapse grammar facts by default. Each fact shows only the
term name as a clickable row. Click expands to show definition, plain
English, numbers, soWhat. Use the same expand/collapse pattern as
chain cards (state toggle, ▼/▲ chevron).

Fix 2: Tighten spacing. Chain card padding: 0.6rem 0.8rem. Grammar
fact gap: 0.4rem. Section gaps: 0.75rem. Card border-radius: 8px.
Remove excessive margins between inner elements.

Fix 3: Compact persona relevance map. Each row is ONE line:
[L badge] Title — one sentence — [Rhetoric →]. No paragraphs.
Max section height 350px with overflow-y auto.

Fix 4: Shrink cross-ref pills to 0.65rem, --text-muted, --panel bg.
Max 30 chars per pill. No module IDs — short labels only.

Fix 5: After cascade calc runs, show PASS/FAIL badge + reason inline
on each chain card row. Green/red left border. Store results in state.

Fix 6: Remove empty card-icon divs (the ones that had emojis removed).
Just delete the empty <div className="card-icon ..."></div> elements.

Fix 7: Update left CTA copy to: Title "From learning to practice",
body about AI Readiness Assessment with pricing, button to legacybe.ie.

Fix 8: Remove card-icon divs from sidebar titles. Just bold text.

Version bump to 2.1.0 in final script. Verify 27 questions, 45 facts.
Save as DC-AI-001_v2_1_0.html.
```

---

## FACTORY UPDATE — NEW STEP

The pipeline is now:

| Step | Name | What |
|------|------|------|
| 1 | SMCA | Content DNA (Opus) |
| 2 | Build | Assemble HTML from DNA (CC) |
| 3 | Technical QA | Content verification (Opus) |
| 4 | CSS Polish | Theme, tabs, layout (CC) |
| 5 | Feature Polish | Calculator, personas, CTA, progress (CC) |
| 6 | **Density Polish** | **Collapse facts, tighten spacing, inline cascade (CC)** |
| 7 | WC Review | Side-by-side vs DC-LEARN benchmark (Opus) |
| 8 | Visual Guide | SVG diagrams (Opus design + CC build) |

Step 6 is new. It's the "make it feel like DC-LEARN" pass.
Steps 4+5+6 can potentially merge into one CC session for modules 2–8
now that the template is defined.

---

## FACTORY LESSON L16

**L16: Progressive disclosure is the difference between A- and A+.**
Content quality and colour matching are necessary but not sufficient.
The user experience is determined by what's HIDDEN by default. DC-LEARN
collapses grammar facts, cross-refs, and fix solutions behind clicks.
DC-AI showed everything at once — same content, worse experience.
Every new component must default to COLLAPSED. The learner reveals
content by choosing to engage. This is the Feynman principle applied
to UI: if you can't explain it simply, maybe you're showing too much
at once.

---

*DC-AI Final Polish Spec v1.0 | April 2026*
*Supersedes: DC_AI_POLISH_PASS_2_v1_0.md*
