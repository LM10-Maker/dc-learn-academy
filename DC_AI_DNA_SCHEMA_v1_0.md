# DC-AI DNA YAML SCHEMA v1.0
# Field-by-field contract between SMCA Agent (content) and Builder Agent (code)
# Every field listed here MUST appear in the SMCA output
# Every field listed here has a JSX consumer in the template
# Dead fields and orphan components are both detectable by script
#
# Legend:
#   REQUIRED = must be present, non-empty
#   OPTIONAL = may be empty string "" but key must exist
#   MIN:N    = minimum character count
#   COUNT:N  = exact count required
#   T1/T2    = source tier minimum for this field

# ═══════════════════════════════════════════════════
# TOP-LEVEL METADATA
# ═══════════════════════════════════════════════════

meta:
  module_id: string          # REQUIRED — e.g. "DC-AI-001"
  title: string              # REQUIRED — e.g. "Power Density"
  version: string            # REQUIRED — semver e.g. "1.0.0"
  chain_tab_label: string    # REQUIRED — Tab 1 label e.g. "Power Density Chain"
  hero_disclaimer: string    # REQUIRED — must contain "Fictional reference facility"
  series_position: integer   # REQUIRED — 1–8
  series_total: integer      # REQUIRED — 8
  prev_module: string|null   # null for first module
  next_module: string|null   # null for last module

# ═══════════════════════════════════════════════════
# LEVELS ARRAY — exactly 9 entries
# ═══════════════════════════════════════════════════

levels:                      # COUNT:9

  - level: integer           # REQUIRED — 1 through 9
    id: string               # REQUIRED — "L1" through "L9"
    title: string            # REQUIRED — level name
    icon: string             # REQUIRED — single emoji, decorative only (never in nav buttons)
    subtitle: string         # REQUIRED — one-line technical summary
    plainEnglish: string     # REQUIRED — MIN:80 — non-technical explanation, zero jargon
    sourceNote: string       # REQUIRED — all sources for this level, each with tier label
                             #   format: "Source Name (Year) §clause — Tier N. Source 2 — Tier N."
    retrofitRelevance: string # REQUIRED — why this matters for existing facilities
    clockQuote: string       # REQUIRED — empty string "" for DC-AI v1.0 (see clock_quotes rule in config)
    crossRefs: list[string]  # REQUIRED — MIN COUNT:2 per level (cross-platform + intra-DC-AI)
                             #   format: "DC-AI-002 L4 (CDU sizing)" or "DC-LEARN-001 L3 (Dual Bus)"

    # ─── GRAMMAR ───────────────────────────────────

    grammar:
      facts:                 # COUNT:5 per level (45 total across module)
        - term: string       # REQUIRED — vocabulary term as used in governing standard
          definition: string # REQUIRED — formal definition, cite T1/T2 source with clause
          plain: string      # REQUIRED — MIN:80 — everyday language, analogy or example, zero jargon
          number: string     # REQUIRED — quantified version with units + context + comparison
          standard: string   # REQUIRED — full standard name, edition/year, clause/table
          soWhat: string     # REQUIRED — MIN:60 — complete sentence: why this matters
                             #   rendered via SO_WHAT_MAP in the module

      whatItLooksLike: string  # REQUIRED — what you'd see on site / in a report
      siteChecklist: list[string]  # REQUIRED — 3–5 ordered items a professional would check

    # ─── LOGIC ─────────────────────────────────────

    logic:
      causeAndEffect:        # MIN COUNT:2 per level (18+ total)
        - cause: string      # REQUIRED — MIN:80 — specific action/omission, not generic
          effect: string     # REQUIRED — MIN:80 — consequence chain with figures where possible
          insight: string    # REQUIRED — MIN:80 — safe path with standard reference

      constraintLesson: string  # REQUIRED — the fundamental constraint governing this level
                                #   multi-sentence paragraph, not a label

      weakestLink:
        whatsWrong: string      # REQUIRED — plausible incorrect belief
        whatsRight: string      # REQUIRED — correct understanding with engineering reason
        howToGetThere: list[string]  # REQUIRED — 3–5 numbered steps with costs (Irish market)

    # ─── RHETORIC ──────────────────────────────────

    rhetoric:
      asset_management: string  # REQUIRED — MIN:120 — Conor's voice, concrete detail
      technology: string        # REQUIRED — MIN:120 — Helena's voice, concrete detail
      technical: string         # REQUIRED — MIN:120 — Eoin's voice, DIAGNOSTIC ONLY
                                #   ZERO instances of: should, must, recommend, install,
                                #   specify, design, prescribe. Grep-verifiable.
      compliance: string        # REQUIRED — MIN:120 — Rachel's voice, regulatory reference
      cost: string              # REQUIRED — MIN:120 — Padraig's voice, budget figure with source

    # ─── FIELD CHALLENGE ───────────────────────────

    scenario:
      title: string          # REQUIRED — descriptive, not "Challenge 1"
      situation: string      # REQUIRED — MIN:200 — 3–5 sentences, specific Clonshaugh parameters
                             #   must reference facility parameters from VERTICAL_CONFIG
      challenge: string      # REQUIRED — one clear question a 10-year professional would recognise
      fix: string            # REQUIRED — MIN:300 — step-by-step (3–5 steps)
                             #   each step: what to check, what you'd find, what it means
                             #   sourced numbers (tier-labelled) at every step
                             #   cost indication where relevant (range, "indicative, Irish market")
                             #   decision criteria explicit

    # ─── CASCADE CHECK ─────────────────────────────

    cascadeCheck: string     # REQUIRED — JavaScript function body as string
                             #   takes (inputs) object, returns {pass: boolean, reason: string}
                             #   logic must match grammar + logic section content
                             #   authored in DNA, never invented at build time

# ═══════════════════════════════════════════════════
# ASSESSMENT QUESTIONS — minimum 27 (3 per level × 9 levels)
# ═══════════════════════════════════════════════════

assessment:
  questions:                 # MIN COUNT:27
    - level: integer         # REQUIRED — 1–9
      id: string             # REQUIRED — format "Q{module_number}-{N}" e.g. "QAI001-1"
      tier: string           # REQUIRED — "knowledge" | "calculation" | "judgement"
      q: string              # REQUIRED — question text
      options: list[string]  # REQUIRED — COUNT:4 — all similarly detailed in length
                             #   longest-answer-correct ≤30% across full set (G-NEW-59)
      correct: integer       # REQUIRED — 0–3 index of correct answer
                             #   distribution: 6–8 per position across 27 questions
                             #   no more than 3 consecutive same position
      explain: string        # REQUIRED — MIN:100 — explains reasoning, not just "Correct!"
                             #   must state why each wrong answer is wrong

  # Pre-computed distribution (SMCA must report this)
  distribution:
    position_0: integer      # target 6–8
    position_1: integer      # target 6–8
    position_2: integer      # target 6–8
    position_3: integer      # target 6–8

# ═══════════════════════════════════════════════════
# COMPANION DATA MAPS
# ═══════════════════════════════════════════════════

so_what_map:                 # COUNT:45 (one per grammar fact, keyed by fact term)
  "[fact.term]": string      # REQUIRED — MIN:60 — "Why it matters: ..."
                             # CRITICAL (G-NEW-36): key order must match actual fact
                             # term order in LEVELS. Extract ordered list from facts
                             # before writing this map. Never assume logical sequence.

rhetoric_takeaways:          # COUNT:45 (9 levels × 5 personas)
  "L1":
    asset_management: string # REQUIRED — one-sentence takeaway for Conor
    technology: string       # REQUIRED — one-sentence takeaway for Helena
    technical: string        # REQUIRED — one-sentence takeaway for Eoin (diagnostic only)
    compliance: string       # REQUIRED — one-sentence takeaway for Rachel
    cost: string             # REQUIRED — one-sentence takeaway for Padraig
  # ... L2 through L9

# ═══════════════════════════════════════════════════
# DIAGRAM SPECIFICATIONS — 3 to 5 per module
# ═══════════════════════════════════════════════════

diagrams:                    # COUNT:3–5
  - level: string            # REQUIRED — "overview" or "L1"–"L9"
    title: string            # REQUIRED — what the diagram shows
    feynman_justification: string  # REQUIRED — why a picture is better than text
                                    #   if you can't write this sentence, the diagram fails
    type: string             # REQUIRED — "chain_overview" | "component" | "system_level"
    steps: integer           # REQUIRED — 2–4
    step_logic:              # REQUIRED — one entry per step
      1: string              #   what is visible / what changes at this step
      2: string
      # ...
    insight: string          # REQUIRED — teaching point revealed at final step
    key_numbers: list[string] # REQUIRED — every number must already exist in grammar facts
    layout:
      left_margin: string    # REQUIRED — engineering parameter (e.g. "kW/rack")
      right_margin: string   # REQUIRED — plain English insight
      components: list[string]  # REQUIRED — equipment/elements to draw
      flow_direction: string # REQUIRED — which way power/coolant/air/product moves
    accuracy_notes: list[string]  # OPTIONAL — physics constraints for the builder

# ═══════════════════════════════════════════════════
# GLOSSARY — 30 to 50 terms
# ═══════════════════════════════════════════════════

glossary:                    # COUNT:30–50
  - term: string             # REQUIRED — every technical term used in the module
    definition: string       # REQUIRED — concise definition

# ═══════════════════════════════════════════════════
# BIBLIOGRAPHY — 10 to 20 sources
# ═══════════════════════════════════════════════════

bibliography:                # COUNT:10–20
  - title: string            # REQUIRED — MUST be first key (verify_port.py counts {title:})
    type: string             # REQUIRED — "standard" | "regulation" | "guidance" | "manufacturer" | "market_report"
    tier: string             # REQUIRED — "T1" | "T2" | "T3" | "T4"
    year: string             # OPTIONAL — publication year
    usage: string            # OPTIONAL — where this source is used in the module

# ═══════════════════════════════════════════════════
# VALIDATION SUMMARY (SMCA must complete before RELEASE)
# ═══════════════════════════════════════════════════

validation:
  levels_count: integer           # must be 9
  facts_count: integer            # must be 45
  so_what_count: integer          # must be 45
  ce_count: integer               # must be ≥18
  persona_count: integer          # must be 45
  weakest_link_count: integer     # must be 9
  field_challenge_count: integer  # must be 9
  cascade_check_count: integer    # must be 9
  assessment_count: integer       # must be ≥27
  diagram_count: integer          # must be 3–5
  glossary_count: integer         # must be 30–50
  bibliography_count: integer     # must be 10–20

  # Depth checks
  persona_under_120: integer      # must be 0
  ce_under_80: integer            # must be 0
  plain_english_under_80: integer # must be 0
  so_what_under_60: integer       # must be 0
  explain_under_100: integer      # must be 0

  # Assessment checks
  longest_answer_correct_pct: float  # must be ≤30%
  position_distribution: list[integer]  # each 6–8
  max_consecutive_same: integer  # must be ≤3

  # Content safety
  stale_values_found: integer     # must be 0
  prescriptive_technical: integer # must be 0 (grep: should|must|recommend|install|specify|design|prescribe in Eoin context)
  banned_terms_found: integer     # must be 0

  # Verdict
  release: boolean                # true = all checks passed
  blocking_failures: list[string] # empty if release=true

# ═══════════════════════════════════════════════════
# SCHEMA CONTROL
# ═══════════════════════════════════════════════════
# Version: 1.0
# Date: 10 April 2026
# Source: Reverse-engineered from DC-LEARN Port Spec v4.2 + Series Spec v1.4
# Companions: DC_AI_VERTICAL_CONFIG_v1_3.yaml, UNIVERSAL_MODULE_BUILD_SYSTEM_v1_1.md
# Rule: Every field here has a JSX consumer in the template.
#        Every JSX consumer in the template reads from a field here.
#        Dead data and orphan components are both defects.
