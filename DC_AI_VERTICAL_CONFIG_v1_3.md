# DC-AI VERTICAL CONFIG v1.3
# AI-Ready Data Centre Investment Intelligence
# Legacy Business Engineers Ltd | April 2026
#
# This file is the single input to the SMCA mega-prompt.
# Paste it into the prompt. The agent does the rest.

vertical:
  name: "DC-AI"
  full_name: "AI-Ready Data Centre Investment Intelligence"
  industry: "Data Centre Retrofit for AI/GPU Workloads"
  module_count: 8
  id_prefix: "DC-AI"
  deploy_domain: "ai.legacybe.ie"
  relationship_to_dc_learn: "DC-LEARN teaches DC fundamentals. DC-AI assumes fundamentals and asks: can this facility handle 30–100+ kW/rack AI workloads, and what does it cost to get there?"
  dc_learn_prerequisite: "Recommended but not required. DC-AI modules are self-contained. Learners without DC fundamentals will be signposted to DC-LEARN where prerequisite knowledge is assumed."
  audience: "Fund managers, asset owners, colocation executives, CTO/CTOs, and their technical advisors making €10M–100M+ retrofit investment decisions"
  tone: "Investment-grade. Every fact defensible in a board paper. Every number sourced. No hype."

reference_facility:
  name: "Clonshaugh DC"
  description: "Fictional small data centre. Same facility as DC-LEARN, but now asking the AI readiness question."
  parameters:
    racks: 400
    it_load_mw: 2.4
    pue_current: 1.50
    pue_target: 1.20
    mic_mva: 5
    voltage_kv: 10
    grid_connection: "ESB Networks MV (NOT 110 kV, NOT EirGrid)"
    current_rack_density_kw: 8  # legacy air-cooled average
    halls:
      - name: "Hall A"
        status: "Legacy air-cooled, 200 racks, 8 kW/rack average, containment installed"
        role: "Continues to serve existing tenants at current density"
      - name: "Hall B"
        status: "Retrofit candidate for AI zone"
        target_density_kw: "40–100 kW/rack"
        role: "AI/GPU zone — direct-to-chip liquid cooling, upgraded power distribution"
    building_year: 2012
    floor_loading_psf: 150  # raised floor, legacy spec
    ceiling_height_m: 3.2
    chilled_water: true
    free_cooling_capable: true
    generator_capacity_mw: 3.0
    ups_capacity_mw: 2.8
    remaining_lease_years: 12
  constraints:
    - "MIC at 85% utilisation — limited headroom for AI density without utility upgrade"
    - "Floor loading insufficient for liquid-cooled GPU racks (need 250+ psf for 3,000 lb racks)"
    - "Ceiling height marginal for hot aisle containment on taller GPU cabinets (800mm × 1200mm)"
    - "No liquid piping infrastructure in Hall B"
    - "10 kV ESB Networks — upgrade to higher capacity takes 12–24 months"

personas:
  asset_management:
    name: "Conor"
    role: "Asset Manager (Fund)"
    lens: "Investment returns, asset valuation, tenant demand, fund reporting"
    voice_sample: >
      We're seeing 40% of our DC portfolio tenants ask about AI-ready capacity
      in the last 6 months. Two have served notice because we can't offer above
      10 kW/rack. That's €2.4M in annual revenue walking out the door. The
      retrofit capex is €6–8M for Hall B, but if we don't spend it, the asset
      devalues anyway because no AI-capable tenant will sign a new lease. The
      question isn't whether to retrofit — it's whether 18 months is fast enough
      to retain the tenants we've got.
  technology:
    name: "Helena"
    role: "Chief Technology Officer (Colocation)"
    lens: "Technical feasibility, minimum viable AI zone, speed to market, competitive positioning"
    voice_sample: >
      I need to offer 40 kW racks to a hyperscaler prospect by Q3. That means
      direct-to-chip cooling in Hall B, new busbars rated for the density, and
      a CDU plant room somewhere I haven't figured out yet. The building was
      designed for 8 kW/rack air-cooled — every system downstream of the
      transformer needs re-evaluating. I don't need a full rebuild. I need the
      minimum viable AI zone that I can expand later. What's the fastest path
      to 50 racks at 40 kW?
  technical:
    name: "Eoin"
    role: "MEP Retrofit Engineer"
    lens: "Measurements, calculations, constraints. DIAGNOSTIC ONLY — identifies, measures, quantifies. Never prescribes solutions."
    voice_sample: >
      The existing power distribution is rated for 1.2 MW across Hall B — that's
      200 racks at 6 kW average with 20% headroom. To serve 50 racks at 40 kW,
      we need 2 MW to the hall floor. The main switchboard has spare ways but
      the bus section is rated at 1,600A — that supports approximately 1.1 MW
      at 0.85 power factor on 415V. The measurement shows we're at 73% of bus
      capacity today. The gap between 1.1 MW available and 2 MW required is the
      binding constraint. The transformer has 15% spare capacity on the LV side.
      That gives us maybe 375 kVA additional — roughly 320 kW usable. Not enough.
  compliance:
    name: "Rachel"
    role: "ESG & Regulatory Director"
    lens: "EU Taxonomy alignment, CRU/2025236, CSRD reporting, CRREM misalignment risk, SFDR"
    voice_sample: >
      If we double our power draw for AI, our Taxonomy PUE must stay below 1.3
      — that's achievable with liquid cooling but only if the CDU waste heat is
      recovered or the free cooling offset compensates. The bigger issue is
      CRU/2025236: we need 80% renewable sourcing, and our current CPPA covers
      2.4 MW. If Hall B adds 2 MW of AI load, we need a new CPPA or additional
      REGOs for that increment. Without it, our SFDR Article 8 fund can't report
      the facility as Taxonomy-aligned, and institutional investors won't touch
      the next fund raise.
  cost:
    name: "Padraig"
    role: "Project QS / Cost Manager"
    lens: "Budgets, phasing, capex classification, Irish market rates, payback analysis"
    voice_sample: >
      Retrofit cost benchmarks are running €2–3M per MW of IT capacity for
      DLC integration — that's indicative, 2025 market, and it varies by site
      condition. For Clonshaugh Hall B at 2 MW target, we're looking at €4–6M
      all-in including power distribution upgrades, CDU plant, piping, structural
      reinforcement, and commissioning. Phased: €1.5–2M in Phase 1 for
      infrastructure prep, then €100–150K per rack for the DLC fit-out. The AI
      tenant premium on lease rates is €150–200/kW/month above standard — at
      50 racks × 40 kW, that's €300K–400K/yr additional revenue. Payback on
      the retrofit is 10–15 years at that rate, or 4–6 years if you fill
      Hall B to 100 racks.

canonical_data:
  # DC-LEARN inherited (Irish context)
  - parameter: "Grid emission factor"
    value: "0.2241 kgCO₂/kWh"
    source: "SEAI 2026"
    tier: "T1"
  - parameter: "Carbon tax (current)"
    value: "€71/tCO₂"
    source: "Budget 2025"
    tier: "T1"
  - parameter: "Carbon tax (2030 target)"
    value: "€100/tCO₂"
    source: "Finance Act"
    tier: "T1"
  - parameter: "Electricity price"
    value: "€0.12/kWh"
    source: "CRU Q4 2024"
    tier: "T2"
  - parameter: "Dublin free cooling"
    value: "7,200 hrs/yr <18°C"
    source: "Met Éireann 30-year normals"
    tier: "T1"
  - parameter: "EU Taxonomy PUE"
    value: "≤1.3"
    source: "Delegated Act 2021/2139"
    tier: "T1"
  - parameter: "CRU renewable obligation"
    value: "80%"
    source: "CRU/2025236"
    tier: "T1"
  - parameter: "CRM T-4 clearing price"
    value: "€149,960/MW/yr"
    source: "SEMO PCAR2829T-4"
    tier: "T1"
  - parameter: "Clonshaugh PUE"
    value: "1.50 current / 1.20 target"
    source: "DC-LEARN Series Spec v1.4 §2"
    tier: "T1"
  # AI/GPU-specific
  - parameter: "Air cooling physical limit"
    value: "~41 kW/rack (with optimised containment)"
    source: "Industry consensus, physics-derived — no single published standard"
    tier: "T3"
  - parameter: "NVIDIA Blackwell GB300 rack power"
    value: "163 kW/rack"
    source: "NVIDIA published specs 2025"
    tier: "T3"
  - parameter: "NVIDIA GPU power trajectory"
    value: "Doubling every ~2 years; 1,500W/chip projected 2026"
    source: "NVIDIA roadmap"
    tier: "T3"
  - parameter: "DLC market size 2025"
    value: "$5.52B"
    source: "Grand View Research / industry reports"
    tier: "T2"
  - parameter: "DLC market CAGR to 2030"
    value: "23.31%"
    source: "Industry forecast consensus"
    tier: "T2"
  - parameter: "Direct-to-chip market share"
    value: "47% of liquid cooling market"
    source: "Industry reports 2025"
    tier: "T2"
  - parameter: "DC liquid cooling adoption rate"
    value: "22% of data centres now implementing"
    source: "Industry survey 2025"
    tier: "T2"
  - parameter: "Retrofit cost per MW (DLC integration)"
    value: "€2–3M (indicative, varies by site condition)"
    source: "Industry benchmarks 2025, converted to EUR"
    tier: "T3"
  - parameter: "Legacy raised floor loading"
    value: "150 psf typical"
    source: "Structural engineering standards"
    tier: "T2"
  - parameter: "Liquid-cooled GPU rack weight"
    value: "3,000+ lbs"
    source: "Manufacturer specifications (NVIDIA, Supermicro)"
    tier: "T3"
  - parameter: "Utility upgrade lead time (major markets)"
    value: "12–24 months"
    source: "Industry observation; ESB Networks typical timelines"
    tier: "T2"
  - parameter: "Utility upgrade cost"
    value: ">€2M per MW"
    source: "Industry benchmarks, converted to EUR"
    tier: "T3"
  - parameter: "Pre-2015 DC AI-readiness gap"
    value: "68% lack power density/cooling capacity for AI workloads"
    source: "Industry survey 2025"
    tier: "T2"
  - parameter: "Cooling as % of total DC energy (traditional)"
    value: "~40%"
    source: "Industry consensus; Uptime Institute"
    tier: "T2"
  - parameter: "Global DC energy consumption"
    value: "460 TWh annually"
    source: "IEA"
    tier: "T1"
  - parameter: "Global DC infrastructure spend 2024"
    value: "$290B"
    source: "IoT Analytics 2025"
    tier: "T2"
  - parameter: "Projected DC infrastructure spend 2030"
    value: "$1 trillion"
    source: "IoT Analytics / industry consensus"
    tier: "T2"
  - parameter: "Hyperscaler combined capex 2025"
    value: "$380B+ (Microsoft, Google, Amazon, Meta)"
    source: "Company earnings reports / guidance"
    tier: "T1"
  - parameter: "15-year-old HVAC efficiency degradation"
    value: "~70% of nameplate capacity"
    source: "Industry observation; ASHRAE data"
    tier: "T2"
  - parameter: "GPU cabinet dimensions (AI)"
    value: "800mm × 1200mm (vs legacy 600mm × 1000mm)"
    source: "NVIDIA / OEM specifications"
    tier: "T3"

stale_values:
  - stale: "Air cooling works up to 20 kW/rack"
    correct: "~41 kW with optimised containment"
    reason: "Old rule of thumb; modern hot/cold aisle containment extends the range significantly"
  - stale: "Liquid cooling is niche or experimental"
    correct: "22% adoption, $5.52B market, 47% D2C market share"
    reason: "Tipped from bleeding-edge to baseline in 2025"
  - stale: "5–15 kW average rack density"
    correct: "Still true for legacy general compute; stale for AI context (40–163+ kW)"
    reason: "Must always specify context — legacy vs AI"
  - stale: "CRM €83,050"
    correct: "€149,960/MW/yr"
    reason: "SEMO PCAR2829T-4; old value from previous auction"
  - stale: "Grid EF 0.295"
    correct: "0.2241 kgCO₂/kWh"
    reason: "SEAI 2026 update"
  - stale: "Carbon tax €56 or €63.50"
    correct: "€71/tCO₂"
    reason: "Budget 2025"
  - stale: "Clonshaugh PUE 1.80/1.30"
    correct: "1.50 current / 1.20 target"
    reason: "Updated in Series Spec v1.2"

terminology:
  use:
    - "Misalignment Year (not Stranding Year)"
    - "CRU Readiness (not CRU Compliance — overclaim)"
    - "indicative / screening-level / estimated (not exact / guaranteed)"
    - "Direct-to-chip (DLC) (not 'direct liquid cooling' — ambiguous)"
    - "AI workload density (not 'AI power density' — conflates power with workload)"
    - "Assessment (not Quiz)"
    - "Hall A / Hall B (not Hall 1 / Hall 2)"
    - "MEP Engineer (not Electrical Engineer — covers M+E+P+cooling+fire)"
    - "Les Murphy CEng (not Les McGuinness)"
    - "NEAP (commercial buildings) (not DEAP — residential only)"
    - "Retrofit (not refurbishment — implies functional upgrade, not cosmetic)"
    - "Coolant Distribution Unit / CDU (not 'cooling unit' — too vague)"
  never:
    - "Stranding Year"
    - "CRU Compliance"
    - "exact / guaranteed / fully compliant"
    - "direct liquid cooling (use DLC or direct-to-chip)"
    - "AI power density"
    - "Quiz"
    - "Hall 1 / Hall 2"
    - "Electrical Engineer (for Eoin)"
    - "Les McGuinness"
    - "LBE professional experience (as a source)"
    - "Ballycoolin (retired facility name)"

positioning:
  intelligence_layer: >
    DC-AI identifies and quantifies. It does not design or deliver solutions.
    Engineering firms are learners, referral sources, and delivery partners —
    not competitors.
  technical_persona_rule: >
    Eoin diagnoses only — measures, calculates, identifies constraints.
    Never specifies, designs, prescribes, recommends, or selects products.
  cta_language: "Need to know where your facility stands on AI readiness?"
  service_ladder:
    - code: "DC-AI-S01"
      name: "AI Readiness Screening"
      price: "€8,500"
      scope: "Desktop assessment of facility AI readiness potential"
    - code: "DC-AI-S02"
      name: "AI Readiness Assessment"
      price: "€25,000"
      scope: "On-site 2-week assessment with board-ready report"
    - code: "DC-AI-S03"
      name: "Retrofit Feasibility Study"
      price: "€75,000"
      scope: "Detailed engineering scope, phased cost plan, planning pathway"
    - code: "DC-AI-S04"
      name: "Retrofit Programme Management"
      price: "€150,000–360,000"
      scope: "Full programme management from design through commissioning"
  pi_safe: true
  anonymisation: true

module_map:
  - id: "DC-AI-001"
    title: "Power Density"
    chain_tab_label: "Power Density Chain"
    prev: null
    next: "DC-AI-002"
    levels:
      L1:
        title: "Legacy Density"
        subtitle: "Why most existing facilities are stuck at 5–8 kW/rack"
        scope: "Historical design assumptions, 480V/415V distribution sized for general compute, typical PDU and whip capacity. What Clonshaugh Hall B was built for."
        stage_focus: "Grammar — vocabulary of power density, kW/rack, nameplate vs actual"
      L2:
        title: "Optimised Air-Cooled Density"
        subtitle: "Pushing air cooling from 8 to 15 kW/rack with containment"
        scope: "Hot/cold aisle containment, blanking panels, optimised airflow. The cheap wins before liquid. What Hall A achieved."
        stage_focus: "Grammar — containment vocabulary, CFD basics, delta-T"
      L3:
        title: "The Air Ceiling"
        subtitle: "Why physics stops air cooling at ~41 kW/rack"
        scope: "Thermodynamics of air as a cooling medium, volumetric flow limits, acoustic limits, fan energy penalty. The hard wall."
        stage_focus: "Logic — cause-and-effect of pushing air beyond its physics"
      L4:
        title: "The DLC Threshold"
        subtitle: "When and why the transition to liquid becomes mandatory"
        scope: "Decision framework: at what density does DLC become necessary vs optional? Total cost of ownership crossover point. The hybrid zone (20–40 kW) where both work."
        stage_focus: "Logic — cost and physics trade-offs that drive the decision"
      L5:
        title: "Direct-to-Chip at Scale"
        subtitle: "100 kW/rack — the current AI production sweet spot"
        scope: "DLC architecture: cold plates, manifolds, CDU, secondary loop. How 100 kW racks actually work. What the piping looks like. Coolant selection."
        stage_focus: "Grammar + Logic — new vocabulary plus how the system functions"
      L6:
        title: "GB300 Class Density"
        subtitle: "163 kW/rack and beyond — NVIDIA's current ceiling"
        scope: "Blackwell GB300 NVL72 rack requirements. Power, cooling, weight, cable count. What changes between 100 kW and 163 kW. Why it's not just 'more of the same.'"
        stage_focus: "Logic — cascading constraints when density doubles"
      L7:
        title: "Power Distribution Redesign"
        subtitle: "Why existing switchboards, busbars, and PDUs can't serve AI racks"
        scope: "Bus section ratings, PDU capacity, whip sizing, protection coordination. The gap between what's installed and what's needed. Eoin's binding constraint analysis."
        stage_focus: "Logic — measurement and gap analysis methodology"
      L8:
        title: "Voltage Optimisation"
        subtitle: "415V vs 480V vs medium voltage to the rack — the efficiency argument"
        scope: "Voltage drop at high current, I²R losses in distribution, 415V European vs 480V US convention, emerging MV-to-rack architectures. Why voltage choice affects opex for the life of the facility."
        stage_focus: "Rhetoric — professional judgement on voltage strategy for retrofit"
      L9:
        title: "The Retrofit Investment Decision"
        subtitle: "Should Clonshaugh Hall B go to 40 kW, 100 kW, or not bother?"
        scope: "Integrating all 8 levels: physics limits, cost, grid capacity, structural constraints, regulatory, tenant demand, fund returns. The board-level decision that divides experienced professionals."
        stage_focus: "Rhetoric — Conor, Helena, Eoin, Rachel, and Padraig each give their verdict"

  - id: "DC-AI-002"
    title: "Cooling Transformation"
    chain_tab_label: "Cooling Chain"
    prev: "DC-AI-001"
    next: "DC-AI-003"
    levels:
      L1:
        title: "Air Cooling Physics"
        subtitle: "What air can and cannot do as a heat transfer medium"
        scope: "Specific heat capacity of air vs water vs dielectric fluid. Mass flow rate requirements per kW. Why air is 3,500× worse than water at moving heat."
      L2:
        title: "Containment Optimisation"
        subtitle: "Extracting every last kW from the existing air infrastructure"
        scope: "Hot aisle containment, cold aisle containment, chimney cabinets. Clonshaugh Hall A as the worked example. ROI on containment retrofit."
      L3:
        title: "Rear-Door Heat Exchangers"
        subtitle: "The bridge technology between air and full liquid"
        scope: "Passive and active RDHx, chilled water connection, neutral air discharge. When RDHx extends the air envelope to 25–30 kW/rack without full DLC."
      L4:
        title: "Direct-to-Chip Cooling"
        subtitle: "Cold plates on GPUs — how the dominant AI cooling technology works"
        scope: "D2C architecture, cold plate design, manifold routing, secondary loop, CDU function. 47% market share. The new baseline."
      L5:
        title: "CDU Sizing & Placement"
        subtitle: "The plant room problem nobody plans for early enough"
        scope: "CDU capacity per MW of IT, floor space, piping routes, heat rejection to existing chilled water or dry coolers. Where does the CDU go in a building not designed for it?"
      L6:
        title: "Immersion Cooling"
        subtitle: "Submerging servers in fluid — niche or future standard?"
        scope: "Single-phase vs two-phase immersion. Tank design. Maintenance access. Current adoption (~3%). Use cases where immersion beats D2C."
      L7:
        title: "Hybrid Architectures"
        subtitle: "Running air-cooled and liquid-cooled zones in the same facility"
        scope: "Hall A air + Hall B liquid. Shared chilled water plant. BMS integration. The practical reality of most retrofits — you don't convert everything at once."
      L8:
        title: "Piping Infrastructure"
        subtitle: "The hidden retrofit cost — getting liquid from CDU to rack"
        scope: "Pipe routing in raised floor vs overhead. Leak detection. Redundancy (N+1 CDU). Isolation valves. Commissioning and pressure testing. What breaks when you run water through a building designed for air."
      L9:
        title: "Waste Heat Recovery"
        subtitle: "Turning cooling cost into revenue — district heating, absorption chillers"
        scope: "DLC return water at 45–60°C — usable for heating. District heating connection feasibility. EU Energy Efficiency Directive waste heat requirements. The business case that changes the cooling equation."

  - id: "DC-AI-003"
    title: "Structural Readiness"
    chain_tab_label: "Structural Chain"
    prev: "DC-AI-002"
    next: "DC-AI-004"
    levels:
      L1:
        title: "Floor Loading Assessment"
        subtitle: "Legacy 150 psf vs 3,000 lb liquid-cooled GPU racks"
        scope: "Raised floor vs slab-on-grade. Point loading vs distributed loading. How to assess existing capacity. When floor reinforcement is needed."
      L2:
        title: "Ceiling Height & Clearance"
        subtitle: "Why 3.0m clear height kills containment options for tall GPU racks"
        scope: "800mm × 1200mm GPU cabinets vs 600mm × 1000mm legacy. Hot aisle containment clearance requirements. When ceiling height is the binding constraint."
      L3:
        title: "Column Spacing & Layout"
        subtitle: "Structural columns that prevent efficient GPU rack placement"
        scope: "Legacy column grids optimised for 600mm racks. Layout efficiency loss with 1200mm deep cabinets. When you can't get the rack count you need."
      L4:
        title: "Cable Pathway Capacity"
        subtitle: "AI racks need 10× the cabling — can the pathways handle it?"
        scope: "Power cable count per rack at 40 kW vs 8 kW. Fibre count for GPU interconnects. Overhead vs underfloor routing. Pathway fill ratios."
      L5:
        title: "Liquid Piping Routes"
        subtitle: "Getting coolant from CDU to every rack without destroying the floor"
        scope: "Main distribution headers, branch piping, flexible connections. Floor penetrations. Overhead vs underfloor. Leak containment zones."
      L6:
        title: "Weight Distribution"
        subtitle: "GPU racks don't just weigh more — they weigh differently"
        scope: "Centre of gravity shift with liquid. Uneven loading on raised floor tiles. Seismic bracing for heavy racks. Weight mapping per row."
      L7:
        title: "Seismic & Vibration"
        subtitle: "Heavy racks, liquid piping, and pumps change the vibration profile"
        scope: "CDU pump vibration transmission. Anti-vibration mounts. Seismic restraint for liquid-cooled racks. Irish seismic zone (low but non-zero)."
      L8:
        title: "Structural Remediation"
        subtitle: "What it costs to fix the building vs what it costs to build new"
        scope: "Floor reinforcement methods and costs. Steel supplementary framing. Slab thickening. When remediation costs exceed 40% of new-build — the walk-away threshold."
      L9:
        title: "Structural Go/No-Go"
        subtitle: "Some buildings simply cannot retrofit — how to make the call"
        scope: "The structural assessment framework. Red flags that kill a retrofit. The honest conversation with the fund manager when the building says no."

  - id: "DC-AI-004"
    title: "Grid & Utility"
    chain_tab_label: "Grid Chain"
    prev: "DC-AI-003"
    next: "DC-AI-005"
    levels:
      L1:
        title: "Current MIC Utilisation"
        subtitle: "How much power headroom does the facility actually have?"
        scope: "Maximum Import Capacity (MIC) vs actual peak demand. Measurement methodology. Clonshaugh: 5 MVA MIC at 85% — 750 kVA headroom."
      L2:
        title: "Demand Growth Modelling"
        subtitle: "Projecting power demand with AI density on top of existing load"
        scope: "Hall B at 2 MW AI load + Hall A at 1.2 MW existing. Total 3.2 MW IT × PUE. Does it fit within 5 MVA MIC? (Spoiler: barely, with DLC PUE.)"
      L3:
        title: "ESB Networks Upgrade Process"
        subtitle: "What happens when you need more than your MIC allows"
        scope: "Application process, technical assessment, cost allocation, build timeline. 12–24 month lead time. The capacity you need vs the capacity available on the local network."
      L4:
        title: "CRU/2025236 Obligations"
        subtitle: "The regulatory instrument that governs every new DC power connection in Ireland"
        scope: "Large Energy User (LEU) Connection Policy. 80% renewable obligation. Demand-side flexibility requirements. What this means for a retrofit that increases power draw."
      L5:
        title: "Behind-the-Meter Generation"
        subtitle: "On-site power to reduce grid dependency and improve resilience"
        scope: "Gas generation, CHP, solar PV. EPA IE licence thresholds. CRM eligibility. When BTM generation makes the retrofit financially viable."
      L6:
        title: "BESS for Peak Shaving"
        subtitle: "Battery storage to manage demand peaks without MIC upgrade"
        scope: "BESS sizing for DC peak shaving. Charge/discharge cycles. Grid services revenue. Can BESS defer a €2M+ MIC upgrade?"
      L7:
        title: "Renewable Sourcing at Scale"
        subtitle: "Doubling power draw means doubling renewable procurement"
        scope: "CPPA structures. REGO certificates. Additionality. The gap between 'matched' and 'genuine' renewable sourcing. Cost per MWh."
      L8:
        title: "Grid Stability & Curtailment"
        subtitle: "What happens to your AI workloads when the grid says no"
        scope: "DS3 system services. Curtailment risk. Demand response obligations. The tension between 'always-on AI' and 'flexible grid citizen.'"
      L9:
        title: "Grid Strategy for AI"
        subtitle: "The integrated power strategy that makes the retrofit investable"
        scope: "Combining MIC optimisation + BTM generation + BESS + renewable sourcing + demand flexibility into a coherent grid strategy. The board paper that unlocks the capex."

  - id: "DC-AI-005"
    title: "Financial Modelling"
    chain_tab_label: "Investment Chain"
    prev: "DC-AI-004"
    next: "DC-AI-006"
    levels:
      L1:
        title: "Retrofit Cost per MW"
        subtitle: "€2–3M per MW — what's included and what drives the variance"
        scope: "Cost breakdown: power distribution, cooling (CDU + piping), structural, commissioning, professional fees. Site condition as the primary variance driver."
      L2:
        title: "Phased Deployment Economics"
        subtitle: "Why you don't retrofit 200 racks on day one"
        scope: "Phase 1 infrastructure (€1.5–2M, zero downtime). Phase 2 pilot (50 racks, €100–150K/rack). Phase 3 production rollout. Cash flow profile."
      L3:
        title: "Capex vs Opex Classification"
        subtitle: "How the accountant sees the retrofit — and why it matters for fund reporting"
        scope: "IFRS 16 lease treatment. IAS 16 capitalisation rules. What's capex (structural, switchboard) vs opex (CDU maintenance, coolant). Impact on fund NAV reporting."
      L4:
        title: "AI Tenant Pricing Premium"
        subtitle: "What the market pays for AI-ready capacity — and how long the premium lasts"
        scope: "€150–200/kW/month AI premium vs €80–120/kW/month standard. Lease structures. Committed vs uncommitted capacity. How long before AI-ready is table stakes."
      L5:
        title: "Payback Period Calculation"
        subtitle: "The number Conor needs before he signs the capex approval"
        scope: "Worked example: €6M retrofit, €400K/yr additional revenue at 50 racks, payback 15 years. At 100 racks filled: payback 6 years. The sensitivity that matters most."
      L6:
        title: "CRREM Misalignment Impact"
        subtitle: "What stranding risk does to asset valuation — and how AI retrofit changes the trajectory"
        scope: "CRREM pathway with current PUE vs post-retrofit PUE. Misalignment Year shift. Valuation discount for stranded assets. How DLC PUE improvement changes the CRREM picture."
      L7:
        title: "Fund Return Modelling"
        subtitle: "IRR, cash-on-cash, and the 7-year fund horizon"
        scope: "Fund lifecycle: deploy capex in year 2, fill AI zone by year 4, exit in year 7. What return does the retrofit generate vs holding without retrofit (declining value)?"
      L8:
        title: "Lease Restructuring"
        subtitle: "How to renegotiate leases to fund the retrofit through tenant commitment"
        scope: "Pre-let agreements for AI capacity. Tenant contribution to retrofit capex. Lease extension in exchange for AI-ready build-out. Risk sharing."
      L9:
        title: "The Investment Case"
        subtitle: "Retrofit, sell, or do nothing — the fund-level decision"
        scope: "Three scenarios modelled: (A) retrofit Hall B, (B) sell the asset as-is, (C) hold and accept tenant attrition. NPV comparison. The board presentation that 5 personas would each write differently."

  - id: "DC-AI-006"
    title: "Regulatory & ESG"
    chain_tab_label: "Compliance Chain"
    prev: "DC-AI-005"
    next: "DC-AI-007"
    levels:
      L1:
        title: "EU Taxonomy PUE ≤1.3"
        subtitle: "The efficiency threshold that determines Taxonomy alignment"
        scope: "Delegated Act 2021/2139 criteria. How DLC changes PUE arithmetic (cooling energy drops, IT load rises). Can Clonshaugh hit 1.2 with liquid cooling?"
      L2:
        title: "CRU/2025236 — Renewable 80%"
        subtitle: "Ireland's renewable sourcing obligation for large energy users"
        scope: "LEU Connection Policy. What counts as renewable. CPPA requirements. Timeline for compliance. What happens if you increase load without increasing renewables."
      L3:
        title: "CSRD Reporting"
        subtitle: "What the Corporate Sustainability Reporting Directive means for DC owners"
        scope: "ESRS E1 (climate), ESRS E3 (water). Double materiality for data centres. What metrics must be reported. How AI retrofit affects the numbers."
      L4:
        title: "SFDR Fund Classification"
        subtitle: "Why ESG fund classification depends on facility-level compliance"
        scope: "Article 6 / 8 / 9 classification. Taxonomy alignment as the gate. If the DC isn't Taxonomy-aligned, the fund can't report it as Article 8. Investor consequence."
      L5:
        title: "CRREM Misalignment Year"
        subtitle: "When the facility's carbon pathway crosses the market threshold"
        scope: "CRREM methodology applied to DC (LBE-derived bands — T3/T4 disclosure mandatory). Misalignment Year before and after retrofit. The number Rachel puts in the ESG report."
      L6:
        title: "Water Usage (WUE)"
        subtitle: "Liquid cooling uses less water than evaporative towers — but not zero"
        scope: "WUE metric. DLC closed-loop vs open cooling tower. Water consumption comparison. Water stress maps for Dublin. Reporting requirements."
      L7:
        title: "Carbon Accounting for AI"
        subtitle: "Scope 1, 2, 3 implications of doubling facility power for AI workloads"
        scope: "Scope 2: grid electricity doubles. Scope 3: embodied carbon in GPU hardware. Scope 1: backup generation. How to account for AI's carbon footprint honestly."
      L8:
        title: "Planning Permission"
        subtitle: "Does the retrofit trigger a new planning application?"
        scope: "Material change of use. Noise assessment for outdoor CDU/dry coolers. Generator emissions. Environmental impact. ABP process if required."
      L9:
        title: "Regulatory Strategy"
        subtitle: "The integrated compliance framework that makes the retrofit defensible"
        scope: "Taxonomy + CRU + CSRD + SFDR + CRREM + planning — all in one coherent strategy. What Rachel presents to the board alongside Conor's financial case."

  - id: "DC-AI-007"
    title: "Deployment Strategy"
    chain_tab_label: "Deployment Chain"
    prev: "DC-AI-006"
    next: "DC-AI-008"
    levels:
      L1:
        title: "AI Readiness Assessment"
        subtitle: "The structured methodology for evaluating retrofit potential"
        scope: "LBE's assessment framework: power, cooling, structural, grid, regulatory — scored per dimension. The output that tells you go/no-go before you spend capex."
      L2:
        title: "Pilot Zone Selection"
        subtitle: "Choosing the right 50 racks to prove the concept"
        scope: "Criteria: proximity to power, floor loading adequacy, piping route feasibility, tenant commitment. Why Hall B row 1–5 is the right pilot zone for Clonshaugh."
      L3:
        title: "Phased Migration Planning"
        subtitle: "How to sequence the retrofit without losing existing tenants"
        scope: "Phase gates. Dependencies (power before cooling before racks). Parallel workstreams. Critical path. The programme Padraig prices and Helena sequences."
      L4:
        title: "Zero-Downtime Retrofit"
        subtitle: "The engineering of keeping the lights on while rebuilding around them"
        scope: "Concurrent maintainability. Temporary cooling during changeover. Power switching sequences. What can be done live vs what requires an outage window."
      L5:
        title: "DLC Commissioning Protocol"
        subtitle: "Pressure testing, leak detection, flow balancing — before the first GPU powers on"
        scope: "Pre-commissioning checks. Hydrostatic pressure test. Coolant fill and bleed. Flow balancing per rack. Thermal performance verification. The Cx checklist."
      L6:
        title: "Performance Verification"
        subtitle: "Proving the retrofit delivers what was promised"
        scope: "Acceptance criteria: PUE, rack density achieved, cooling capacity delivered, power quality. 30/60/90 day monitoring. Performance guarantee mechanisms."
      L7:
        title: "Tenant Onboarding"
        subtitle: "From empty rack to live AI workload — the handover process"
        scope: "SLA definition for AI-density service. Tenant fit-out coordination. Power and cooling commissioning per cabinet. Monitoring handover."
      L8:
        title: "Monitoring & Optimisation"
        subtitle: "Continuous performance management after go-live"
        scope: "DCIM integration for liquid cooling metrics. CDU performance trending. Coolant quality monitoring. PUE tracking at rack level. Alarm management."
      L9:
        title: "Phase 2 Planning"
        subtitle: "Lessons from the pilot that shape the full rollout"
        scope: "Post-implementation review. What worked, what didn't, what cost more than expected. The updated business case for Phase 2 expansion. When to stop."

  - id: "DC-AI-008"
    title: "Market Intelligence"
    chain_tab_label: "Market Chain"
    prev: "DC-AI-007"
    next: null
    levels:
      L1:
        title: "AI Workload Taxonomy"
        subtitle: "Training vs inference vs RAG — different workloads, different infrastructure"
        scope: "What each workload type demands from the DC. Training: sustained high density, long runs. Inference: variable, latency-sensitive. RAG: storage + compute hybrid."
      L2:
        title: "Tenant Requirement Profiles"
        subtitle: "What hyperscalers, enterprises, and AI startups actually ask for"
        scope: "Tier 1 hyperscaler requirements vs Tier 2 enterprise AI vs Tier 3 AI startup. Power, cooling, connectivity, security, compliance — by tenant type."
      L3:
        title: "Colocation Pricing Trends"
        subtitle: "The AI premium and how long it lasts"
        scope: "Price per kW trends 2023–2026. AI-ready vs standard pricing gap. Geographic variation. Market data from CBRE, JLL, DC Byte."
      L4:
        title: "Competitor Positioning"
        subtitle: "Who in Ireland and Europe is already AI-ready — and who's bluffing"
        scope: "Major operators' AI-ready capacity claims. Genuine DLC deployment vs marketing. How to assess competitor facilities objectively."
      L5:
        title: "Geographic Demand Patterns"
        subtitle: "Dublin, London, Frankfurt, Amsterdam, Marseille — where AI tenants are going"
        scope: "Data centre cluster analysis. Power availability by market. Latency requirements. Ireland's position: cheap wind, constrained grid, strong connectivity."
      L6:
        title: "Supply Chain Constraints"
        subtitle: "Transformers, CDUs, switchgear — 12–18 month lead times for critical equipment"
        scope: "The supply chain bottleneck that determines retrofit timeline. What to order first. Manufacturer capacity. The risk of waiting."
      L7:
        title: "Technology Roadmap"
        subtitle: "GPU, networking, cooling — what's coming in the next 3 years"
        scope: "NVIDIA roadmap (Blackwell → Rubin → Vera). Networking (800G → 1.6T). Cooling (D2C → microfluidics → on-chip). What today's retrofit must accommodate for tomorrow's hardware."
      L8:
        title: "3-Year Market Outlook"
        subtitle: "Where the AI DC market is heading — and what it means for asset owners"
        scope: "Demand projections. Supply pipeline. Pricing forecasts. Regulatory trajectory. The macro view that frames every investment decision in this platform."
      L9:
        title: "Investment Decision Framework"
        subtitle: "The structured methodology for deciding: retrofit, sell, build new, or partner"
        scope: "Decision tree integrating all 8 modules. Scoring framework. Sensitivity analysis. The one-page summary that goes to the investment committee."

branding:
  font_display: "IBM Plex Sans"
  font_mono: "IBM Plex Mono"
  colours:
    grammar: "#2563EB"
    logic: "#d97706"
    rhetoric: "#7c3aed"
    accent_green: "#16a34a"
    error: "#dc2626"
    surface_dark: "#181C20"
    surface_light: "#F5F5F5"
  logo: "Use LBE_LOGO_CONST.txt from project knowledge"
  copyright: "© 2026 Legacy Business Engineers Ltd"
  website: "legacybe.ie"
  contact: "lmurphy@legacybe.ie"

build_config:
  template_source: "DC-LEARN-002 (canonical template)"
  cdn: "cdnjs.cloudflare.com ONLY (never unpkg)"
  react_version: "18"
  babel: "standalone"
  persistence: "safeStore (localStorage wrapper)"
  themes: ["dark", "light"]
  file_size_ceiling: "800 KB comfortable, 1 MB hard limit"
  build_method: "Python r''' raw strings for JSX — never f-strings"
  verification: "verify_port.py + depth_audit.py"
  deploy: "Netlify (GitHub auto-deploy)"
  series_nav: "Module N of 8 · DC-AI v1.0"
  dna_schema: "DC_AI_DNA_SCHEMA_v1_0.yaml — must be attached to every SMCA session"

crrem_disclosure:
  rule: >
    CRREM v2.01 does NOT include a published data centre pathway. Any DC-specific
    CRREM bands (e.g. 200/300/400 kgCO₂/MWh_IT) are LBE-derived (T3/T4).
    Every module, report, or tool referencing CRREM DC bands MUST disclose the
    derivation method. Use "Misalignment Year" not "Stranding Year."

crm_context:
  note: >
    CRM T-4 clearing price of €149,960/MW/yr matters for AI retrofit because it
    sets the capacity market revenue floor that changes payback calculations on
    power infrastructure upgrades. Any module touching financial modelling or grid
    capacity must reference this as the current auction benchmark.

assessment_quality:
  inherited_from: "DC-LEARN G-NEW-54, G-NEW-59"
  rules:
    - "All 4 options must be similarly detailed — a learner who always picks the longest answer should score ≤30%"
    - "Run depth_audit.py on every delivery — benchmark against DC-LEARN module 013 profile"
    - "Zero FC (financial case) answers in any module is a shipping blocker"
    - "Fisher-Yates shuffle on assessment questions — render path only, never mutate source array"

clock_quotes:
  status: "empty for v1.0 — no companion narrative written yet"
  rule: >
    All clockQuote fields must be set to empty string "". The SMCA agent
    must NOT invent, fabricate, or generate placeholder quotes. Clock quotes
    will be backfilled only if a DC-AI companion narrative is written.
    Lesson from DC-LEARN: 002 had 9 keyed clockQuotes tied to chapter
    content. 013 had 1 inline quote. Inconsistency caused a fleet sweep.
    DC-AI starts clean — all empty, all consistent, backfill as a batch
    when the narrative exists.

cross_platform_refs:
  purpose: >
    DC-AI learners who completed DC-LEARN should see the connection.
    These refs appear in the crossRefs array alongside intra-DC-AI refs.
    Format in module: "DC-LEARN-001 L3 (Dual Bus Topology)" — same
    pattern as DC-LEARN internal cross-refs.
  mapping:
    DC-AI-001:
      - "DC-LEARN-001 (Power Chain) — foundational power distribution"
      - "DC-LEARN-006 (Grid Connection) — ESB Networks MV, MIC, transformer sizing"
      - "DC-LEARN-005 (Backup Power) — UPS and generator capacity constraints"
    DC-AI-002:
      - "DC-LEARN-002 (Cooling Chain) — CRAH/CRAC, chilled water, free cooling fundamentals"
      - "DC-LEARN-014 (Liquid Cooling) — DLC principles, CDU, immersion basics"
      - "DC-LEARN-004 (Efficiency) — PUE measurement and improvement"
    DC-AI-003: []  # No direct DC-LEARN structural equivalent
    DC-AI-004:
      - "DC-LEARN-006 (Grid Connection) — MIC, ESB Networks process, capacity"
      - "DC-LEARN-015 (CRU Readiness) — CRU/2025236, renewable obligation, LEU policy"
      - "DC-LEARN-012 (Energy Centres) — behind-the-meter generation, BESS, CHP"
    DC-AI-005:
      - "DC-LEARN-004 (Efficiency) — PUE-based business case, energy cost modelling"
      - "DC-LEARN-012 (Energy Centres) — SEM revenue stacking, CRM valuation"
      - "DC-LEARN-007 (Regulatory) — CRREM, carbon tax, EU Taxonomy financial impact"
    DC-AI-006:
      - "DC-LEARN-007 (Regulatory) — EED, EU Taxonomy, SFDR, F-Gas, CRREM"
      - "DC-LEARN-010 (Net Zero) — carbon accounting, SBTi, renewable procurement"
      - "DC-LEARN-015 (CRU Readiness) — CRU/2025236 full compliance chain"
    DC-AI-007:
      - "DC-LEARN-013 (Commissioning) — Cx protocols, SAT, witness testing"
      - "DC-LEARN-003 (Redundancy) — concurrent maintainability, maintenance bypass"
    DC-AI-008: []  # Market intelligence — no DC-LEARN equivalent
  rule: >
    Every DC-AI module must include at least 2 cross-platform refs to
    DC-LEARN where a mapping exists. The SMCA agent writes these into
    the crossRefs array at Level 1 (foundational connection) and the
    most relevant deeper level. DC-AI-003 and DC-AI-008 have no DC-LEARN
    equivalent — intra-DC-AI refs only for those modules.

# END OF CONFIG
# v1.3 — added 9-level breakdowns for all 8 modules + DNA schema reference
# Next step: paste SMCA mega-prompt into Opus with this file + DC_AI_DNA_SCHEMA_v1_0.yaml attached
