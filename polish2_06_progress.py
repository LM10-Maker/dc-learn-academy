#!/usr/bin/env python3
"""
polish2_06_progress.py
ITEM 6: PROGRESS TAB
- Adds Progress tab (after Assessment, before Reference)
- 4 sections: overall progress, assessment results, per-level grid, module info
- Bumps version to 1.2.0 in all 4 reference points
Reads/writes DC-AI-001_v1_2_0.html
"""

WF = 'DC-AI-001_v1_2_0.html'

with open(WF, 'r', encoding='utf-8') as f:
    html = f.read()

# ─── 1. CSS ───────────────────────────────────────────────────────────────────
CSS = r"""
    /* ─── PROGRESS TAB ─────────────────────────────────────────────── */
    .tab-btn.active[data-tab='progress'] { border-bottom-color: var(--lbe-green); color: var(--lbe-green); }
    .progress-section-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      padding: 1.4rem;
      margin-bottom: 1.25rem;
      box-shadow: var(--shadow);
    }
    .progress-tier-row {
      flex: 1;
      min-width: 110px;
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      padding: 0.6rem 0.8rem;
    }
    .progress-level-row {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      padding: 0.55rem 0.75rem;
      font-size: 0.82rem;
      border-radius: 4px;
    }
    .progress-level-row:nth-child(odd)  { background: var(--surface); }
    .progress-level-row:nth-child(even) { background: var(--panel); }
    .progress-dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      flex-shrink: 0;
    }
    .progress-info-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0.45rem 0;
      border-bottom: 1px solid var(--border);
      font-size: 0.82rem;
    }
    .progress-info-row:last-child { border-bottom: none; }
"""

html = html.replace('  </style>', CSS + '  </style>', 1)

# ─── 2. Add 'progress' tab to TABS array (before 'bsg') ─────────────────────
OLD_TABS = "  { id: 'assessment', label: 'Assessment' },\n  { id: 'bsg',        label: 'Reference' }"
NEW_TABS = "  { id: 'assessment', label: 'Assessment' },\n  { id: 'progress',   label: 'Progress'   },\n  { id: 'bsg',        label: 'Reference' }"

assert OLD_TABS in html, "TABS array pattern not found"
html = html.replace(OLD_TABS, NEW_TABS, 1)

# ─── 3. ProgressTab component (insert before function App()) ─────────────────
COMPONENT = r"""
// ═══════════════════════════════════════════════════════════════
// PROGRESS TAB COMPONENT
// ═══════════════════════════════════════════════════════════════
function ProgressTab({ visitedStages }) {
  var visited = visitedStages || {};

  // Section 1: overall completion
  var totalStages = 27; // 9 levels x 3 stages
  var completedStages = 0;
  for (var li = 0; li < 9; li++) {
    var vs = visited[li] || {};
    if (vs.grammar)  completedStages++;
    if (vs.logic)    completedStages++;
    if (vs.rhetoric) completedStages++;
  }
  var overallPct = Math.round((completedStages / totalStages) * 100);

  // Section 2: assessment results from localStorage
  var storedAnswers = safeLoad('aq_answers', {});
  var answeredCount = Object.keys(storedAnswers).length;
  var assessDone = answeredCount >= ASSESSMENT_QUESTIONS.length;
  var score = 0;
  var tierScores  = { knowledge: 0, calculation: 0, judgement: 0 };
  var tierTotals  = { knowledge: 0, calculation: 0, judgement: 0 };
  if (assessDone) {
    ASSESSMENT_QUESTIONS.forEach(function(q, i) {
      var ans = storedAnswers[i];
      if (ans) {
        tierTotals[q.tier] = (tierTotals[q.tier] || 0) + 1;
        if (ans.correct) {
          score++;
          tierScores[q.tier] = (tierScores[q.tier] || 0) + 1;
        }
      }
    });
  }
  var assessPct = assessDone ? Math.round((score / ASSESSMENT_QUESTIONS.length) * 100) : 0;

  var tierDefs = [
    ['knowledge',   'Knowledge',   'var(--grammar)'],
    ['calculation', 'Calculation', 'var(--logic)'  ],
    ['judgement',   'Judgement',   'var(--rhetoric)']
  ];

  var moduleRows = [
    ['Module',    'DC-AI-001 Power Density'     ],
    ['Version',   '1.2.0'                       ],
    ['Series',    'DC-AI \u00b7 Module 1 of 8'  ],
    ['Publisher', 'Legacy Business Engineers Ltd'],
    ['Contact',   'lmurphy@legacybe.ie'         ]
  ];

  return (
    <div>

      {/* Section 1: Overall Progress */}
      <div className="progress-section-card">
        <div className="card-header">
          <div className="card-icon green">&#x1F4CA;</div>
          <div>
            <div className="card-title">Overall Progress</div>
            <div className="card-subtitle">{completedStages}/{totalStages} stages complete ({overallPct}%)</div>
          </div>
        </div>
        <div className="progress-bar-wrap">
          <div className="progress-bar-fill" style={{width: overallPct + '%'}} />
        </div>
        <div style={{fontSize:'0.78rem',color:'var(--text-muted)',marginTop:'0.4rem'}}>
          {completedStages} of 27 stages visited &mdash; Grammar, Logic, Rhetoric across all 9 levels
        </div>
      </div>

      {/* Section 2: Assessment Results */}
      {assessDone ? (
        <div className="progress-section-card">
          <div className="card-header">
            <div className="card-icon blue">&#x1F3AF;</div>
            <div>
              <div className="card-title">Assessment Results</div>
              <div className="card-subtitle">Completed &mdash; {score}/{ASSESSMENT_QUESTIONS.length} correct</div>
            </div>
          </div>
          <div style={{textAlign:'center',padding:'0.75rem 0'}}>
            <span style={{fontSize:'2rem',fontWeight:700,color:'var(--grammar)'}}>{score}</span>
            <span style={{fontSize:'1rem',color:'var(--text-muted)'}}>/{ASSESSMENT_QUESTIONS.length}</span>
            <span style={{marginLeft:'0.5rem',fontSize:'1rem',color:'var(--text-muted)'}}>({assessPct}%)</span>
          </div>
          <div className="progress-bar-wrap">
            <div className="progress-bar-fill" style={{width: assessPct + '%'}} />
          </div>
          <div style={{display:'flex',gap:'0.75rem',marginTop:'0.75rem',flexWrap:'wrap'}}>
            {tierDefs.map(function(t) {
              return (
                <div key={t[0]} className="progress-tier-row">
                  <div style={{fontSize:'0.65rem',fontWeight:700,textTransform:'uppercase',letterSpacing:'0.07em',color:t[2],marginBottom:'0.3rem'}}>{t[1]}</div>
                  <div style={{fontSize:'1.1rem',fontWeight:700,color:'var(--text-bright)'}}>
                    {tierScores[t[0]] || 0}<span style={{fontSize:'0.8rem',color:'var(--text-muted)'}}>/{tierTotals[t[0]] || 9}</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      ) : (
        <div className="progress-section-card">
          <div className="card-header">
            <div className="card-icon blue">&#x1F3AF;</div>
            <div>
              <div className="card-title">Assessment Results</div>
              <div className="card-subtitle">Not yet completed</div>
            </div>
          </div>
          <p style={{fontSize:'0.82rem',color:'var(--text-muted)',lineHeight:'1.65'}}>
            Complete the Assessment tab to see your score breakdown here.
          </p>
        </div>
      )}

      {/* Section 3: Per-Level Completion Grid */}
      <div className="progress-section-card">
        <div className="card-header">
          <div className="card-icon amber">&#x1F4CB;</div>
          <div>
            <div className="card-title">Per-Level Completion</div>
            <div className="card-subtitle">
              <span style={{color:'var(--grammar)',fontWeight:600}}>&#x25CF; Grammar</span>
              {' \u00b7 '}
              <span style={{color:'var(--logic)',fontWeight:600}}>&#x25CF; Logic</span>
              {' \u00b7 '}
              <span style={{color:'var(--rhetoric)',fontWeight:600}}>&#x25CF; Rhetoric</span>
            </div>
          </div>
        </div>
        <div>
          {LEVELS.map(function(lvl, li) {
            var vs = visited[li] || {};
            return (
              <div key={li} className="progress-level-row">
                <span style={{fontSize:'1rem'}}>{lvl.icon}</span>
                <span style={{flex:1,fontWeight:600,color:'var(--text)'}}>{lvl.id}: {lvl.title}</span>
                <span className="progress-dot" style={{background: vs.grammar  ? 'var(--grammar)'  : 'var(--border-2)'}} title="Grammar" />
                <span className="progress-dot" style={{background: vs.logic    ? 'var(--logic)'    : 'var(--border-2)'}} title="Logic" />
                <span className="progress-dot" style={{background: vs.rhetoric ? 'var(--rhetoric)' : 'var(--border-2)'}} title="Rhetoric" />
              </div>
            );
          })}
        </div>
      </div>

      {/* Section 4: Module Information */}
      <div className="progress-section-card">
        <div className="card-header">
          <div className="card-icon cyan">&#x2139;&#xFE0F;</div>
          <div>
            <div className="card-title">Module Information</div>
          </div>
        </div>
        {moduleRows.map(function(r, i) {
          return (
            <div key={i} className="progress-info-row">
              <span style={{color:'var(--text-dim)'}}>{r[0]}</span>
              <span style={{color:'var(--text-bright)',fontWeight:500}}>{r[1]}</span>
            </div>
          );
        })}
      </div>

    </div>
  );
}

"""

html = html.replace('function App() {', COMPONENT + 'function App() {', 1)

# ─── 4. Add renderTab case for 'progress' ────────────────────────────────────
OLD_RENDER = "      case 'assessment':\n        return <AssessmentTab />;\n      case 'bsg':"
NEW_RENDER = "      case 'assessment':\n        return <AssessmentTab />;\n      case 'progress':\n        return <ProgressTab visitedStages={visitedStages} />;\n      case 'bsg':"

assert OLD_RENDER in html, "renderTab assessment case not found"
html = html.replace(OLD_RENDER, NEW_RENDER, 1)

# ─── 5. Hide level selector & level indicator for 'progress' tab ─────────────
# The App has two identical conditions — replace both
OLD_COND = "activeTab !== 'chain' && activeTab !== 'assessment' && activeTab !== 'bsg'"
NEW_COND = "activeTab !== 'chain' && activeTab !== 'assessment' && activeTab !== 'bsg' && activeTab !== 'progress'"

count = html.count(OLD_COND)
assert count == 2, f"Expected 2 occurrences of condition, found {count}"
html = html.replace(OLD_COND, NEW_COND)

# ─── 6. Bump version to 1.2.0 everywhere ─────────────────────────────────────
# (a) TOOL_VERSION variable
html = html.replace('var TOOL_VERSION = "1.1.0";', 'var TOOL_VERSION = "1.2.0";', 1)

# (b) MODULE_META version
html = html.replace('"version": "1.1.0"', '"version": "1.2.0"', 1)

# (c) Series badge in Header component
html = html.replace("'Module 1 of 8 \u00b7 DC-AI v1.1.0'", "'Module 1 of 8 \u00b7 DC-AI v1.2.0'", 1)

# (d) HTML <title>
html = html.replace(
    '<title>DC-AI-001: Power Density | DC-AI v1.1.0</title>',
    '<title>DC-AI-001: Power Density | DC-AI v1.2.0</title>',
    1
)

# ─── 7. Verify ────────────────────────────────────────────────────────────────
assert 'ProgressTab' in html, "ProgressTab component missing"
assert "id: 'progress'" in html, "progress tab in TABS missing"
assert 'var TOOL_VERSION = "1.2.0"' in html, "TOOL_VERSION not bumped"
assert '"version": "1.2.0"' in html, "MODULE_META version not bumped"
assert 'v1.2.0' in html, "v1.2.0 missing from output"
assert 'var TOOL_VERSION = "1.1.0"' not in html, "old version still present"
assert html.count('"plain":') == 45, "grammar facts changed"
assert html.count('"correct":') == 27, "assessment questions changed"

with open(WF, 'w', encoding='utf-8') as f:
    f.write(html)

print("[06] OK — Progress tab added, version bumped to 1.2.0")
print(f"     grammar facts    : {html.count(chr(34)+'plain'+chr(34)+':')}")
print(f"     questions (correct): {html.count(chr(34)+'correct'+chr(34)+':')}")
print(f"     TOOL_VERSION     : 1.2.0")
