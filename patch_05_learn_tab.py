"""patch_05_learn_tab.py — merge Grammar/Logic/Rhetoric into Learn tab; update TABS + renderTab"""
F = "DC-AI-001_v2_0_0.html"

OLD_TABS = """var TABS = [
  { id: 'chain',      label: 'Chain' },
  { id: 'grammar',    label: 'Grammar' },
  { id: 'logic',      label: 'Logic' },
  { id: 'rhetoric',   label: 'Rhetoric' },
  { id: 'field',      label: 'Field Challenge' },
  { id: 'assessment', label: 'Assessment' },
  { id: 'bsg',        label: 'Reference' }
];"""

NEW_TABS = """var TABS = [
  { id: 'chain',      label: 'Chain' },
  { id: 'learn',      label: 'Learn' },
  { id: 'field',      label: 'Field Challenges' },
  { id: 'assessment', label: 'Assessment' },
  { id: 'progress',   label: 'Progress' },
  { id: 'reference',  label: 'Reference' }
];"""

LEARN_COMPONENT = r"""
// ═══════════════════════════════════════════════════════════════
// LEARN TAB — Grammar | Logic | Rhetoric with stage selector
// ═══════════════════════════════════════════════════════════════
function LearnTab({ selectedLevel, visitedStages }) {
  var level = LEVELS[selectedLevel];
  var vs = (visitedStages && visitedStages[selectedLevel]) || {};
  var [stage, setStage] = React.useState('grammar');
  var STAGES = [
    { id: 'grammar',  label: 'Grammar',  color: 'var(--grammar)' },
    { id: 'logic',    label: 'Logic',    color: 'var(--logic)' },
    { id: 'rhetoric', label: 'Rhetoric', color: 'var(--rhetoric)' }
  ];
  return (
    <div>
      <div style={{background:'var(--surface)',borderBottom:'1px solid var(--border)',padding:'0.9rem 1.5rem'}}>
        <div style={{display:'flex',alignItems:'center',gap:'0.6rem',marginBottom:'0.5rem'}}>
          <span style={{fontSize:'1.3rem'}}>{level.icon}</span>
          <div>
            <div style={{fontSize:'1rem',fontWeight:600,color:'var(--text-bright)'}}>Level {level.level}: {level.title}</div>
            <div style={{fontSize:'0.75rem',fontFamily:'var(--font-mono)',color:'var(--text-dim)'}}>{level.subtitle}</div>
          </div>
        </div>
        {level.retrofitRelevance && (
          <div style={{background:'rgba(217,119,6,0.08)',border:'1px solid var(--logic)',borderRadius:'var(--radius-sm)',padding:'0.5rem 0.8rem',fontSize:'0.78rem',color:'var(--text)',marginBottom:'0.6rem'}}>
            <strong style={{color:'var(--logic)'}}>Retrofit Relevance: </strong>{level.retrofitRelevance}
          </div>
        )}
        <div style={{display:'flex',gap:'0.5rem'}}>
          {STAGES.map(function(s) {
            var active = stage === s.id;
            var done = vs[s.id];
            return (
              <button key={s.id} onClick={function(){setStage(s.id);}} style={{
                padding:'5px 16px',borderRadius:'20px',fontSize:'0.8rem',fontWeight:active?600:400,
                border:'1px solid '+(active?s.color:'var(--border)'),cursor:'pointer',
                background:active?s.color:'transparent',color:active?'#fff':'var(--text-dim)',
                transition:'all 0.15s ease'
              }}>
                {s.label}{done?' ✓':''}
              </button>
            );
          })}
        </div>
      </div>
      <div className="main-content">
        {stage === 'grammar'  && <GrammarTab  selectedLevel={selectedLevel} />}
        {stage === 'logic'    && <LogicTab    selectedLevel={selectedLevel} />}
        {stage === 'rhetoric' && <RhetoricTab selectedLevel={selectedLevel} />}
      </div>
    </div>
  );
}
"""

OLD_RENDER = """    switch (activeTab) {
      case 'chain':
        return <ChainTab selectedLevel={levelIdx} setSelectedLevel={setSelectedLevel} setActiveTab={setActiveTab} />;
      case 'grammar':
        return <GrammarTab selectedLevel={levelIdx} />;
      case 'logic':
        return <LogicTab selectedLevel={levelIdx} />;
      case 'rhetoric':
        return <RhetoricTab selectedLevel={levelIdx} />;
      case 'field':
        return <FieldChallengeTab selectedLevel={levelIdx} />;
      case 'assessment':
        return <AssessmentTab />;
      case 'bsg':
        return <BSGTab />;
      default:
        return <ChainTab selectedLevel={levelIdx} setSelectedLevel={setSelectedLevel} setActiveTab={setActiveTab} />;
    }"""

NEW_RENDER = """    switch (activeTab) {
      case 'chain':
        return <ChainTab selectedLevel={levelIdx} setSelectedLevel={setSelectedLevel} setActiveTab={setActiveTab} />;
      case 'learn':
        return <LearnTab selectedLevel={levelIdx} visitedStages={visitedStages} />;
      case 'grammar':
        return <GrammarTab selectedLevel={levelIdx} />;
      case 'logic':
        return <LogicTab selectedLevel={levelIdx} />;
      case 'rhetoric':
        return <RhetoricTab selectedLevel={levelIdx} />;
      case 'field':
        return <FieldChallengeTab selectedLevel={levelIdx} />;
      case 'assessment':
        return <AssessmentTab />;
      case 'progress':
        return <ProgressTab selectedLevel={levelIdx} visitedStages={visitedStages} />;
      case 'reference':
      case 'bsg':
        return <BSGTab />;
      default:
        return <ChainTab selectedLevel={levelIdx} setSelectedLevel={setSelectedLevel} setActiveTab={setActiveTab} />;
    }"""

INJECT_BEFORE = "// ═══════════════════════════════════════════════════════════════\n// CHAIN TAB COMPONENT"

html = open(F, encoding="utf-8").read()
for label, old in [("TABS", OLD_TABS), ("renderTab", OLD_RENDER), ("inject anchor", INJECT_BEFORE)]:
    assert old in html, f"{label} anchor not found"
html = html.replace(OLD_TABS, NEW_TABS, 1)
html = html.replace(OLD_RENDER, NEW_RENDER, 1)
html = html.replace(INJECT_BEFORE, LEARN_COMPONENT + INJECT_BEFORE, 1)
open(F, "w", encoding="utf-8").write(html)
print("patch_05 done — Learn tab merged, TABS updated, renderTab updated")
