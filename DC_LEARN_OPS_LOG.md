# DC-LEARN Operations Log

**Repository:** dc-learn-academy
**Started:** 06 April 2026
**Rule:** Append only — never edit previous entries. Every session adds one block before SHIP/NOT SHIP verdict.

---

## Entry Format

```
## YYYY-MM-DD | Model | Module(s) | Session Type
- [TAG] Description
```

**Tags:** `[FIX]` defect resolved, `[GNEW]` new G-NEW item logged, `[SWEEP]` audit/sweep finding, `[BUILD]` new feature or component, `[DEPLOY]` pushed to Netlify, `[NOTSHIP]` blocking reason, `[BLOCKED]` dependency or external blocker, `[DECISION]` architecture or content decision recorded

**Grep cheatsheet:**
- Last deployed version per module: `grep DEPLOY DC_LEARN_OPS_LOG.md`
- Outstanding blockers: `grep NOTSHIP DC_LEARN_OPS_LOG.md`
- All G-NEW items raised: `grep GNEW DC_LEARN_OPS_LOG.md`
- Sessions per module: `grep "DC-LEARN-008" DC_LEARN_OPS_LOG.md`

---

## 2026-04-06 | Opus | ALL | Ops log creation
- [BUILD] DC_LEARN_OPS_LOG.md created — persistent append-only session log
- [DECISION] Inspired by Karpathy LLM Wiki log.md pattern, adapted for build-and-ship workflow
- [DECISION] Scope: DC-LEARN project only (16 modules). Separate LBE_OPS_LOG.md for other workstreams if needed later
- [DECISION] Karpathy Obsidian + Claude Code wiki pattern logged as post-launch candidate for regulatory monitoring (CRU, EirGrid, F-Gas, CRREM)

---
