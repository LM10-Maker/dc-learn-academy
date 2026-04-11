#!/usr/bin/env python3
"""
build_05_section_d2.py
Section D part 2: RhetoricTab, FieldChallengeTab, AssessmentTab, BSGTab,
App component, ReactDOM.createRoot render, plus closing </script></body></html>.
Output: section_d2.html
"""

import os

BASE = os.path.dirname(os.path.abspath(__file__))

section_d2 = r'''
// ═══════════════════════════════════════════════════════════════
// RHETORIC TAB COMPONENT
// ═══════════════════════════════════════════════════════════════
function RhetoricTab({ selectedLevel }) {
  var level = LEVELS[selectedLevel];
  var rhetoric = level.rhetoric || {};
  var levelKey = level.id;  // 'L1'..'L9'
  var takeaways = (RHETORIC_TAKEAWAYS && RHETORIC_TAKEAWAYS[levelKey]) || {};

  return (
    <div>
      <div className="card">
        <div className="card-header">
          <div className="card-icon purple">💬</div>
          <div>
            <div className="card-title">Rhetoric — {level.id}: {level.title}</div>
            <div className="card-subtitle">Five professional perspectives on the same engineering facts</div>
          </div>
        </div>
        <p style={{fontSize:'0.82rem', color:'var(--text-muted)', lineHeight:'1.6', marginBottom:'1rem'}}>
          Same level, five different lenses. Each professional cares about different aspects of
          AI retrofit density — these are their authentic voices on {level.title.toLowerCase()}.
        </p>
        <div className="persona-grid">
          {PERSONAS.map(function(persona) {
            var text = rhetoric[persona.key] || '';
            var takeaway = takeaways[persona.key] || '';
            if (!text) return null;
            return (
              <div key={persona.key} className="persona-card">
                <div className="persona-header">
                  <div className={'persona-avatar ' + persona.avatarClass}>{persona.initial}</div>
                  <div>
                    <div className="persona-name">{persona.icon} {persona.name}</div>
                    <div className="persona-role">{persona.role}</div>
                  </div>
                </div>
                <div className="persona-body">
                  <div className="persona-text">{text}</div>
                  {takeaway && (
                    <div className="persona-takeaway">
                      <strong>Key Takeaway</strong>
                      {takeaway}
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════════════════════════
// FIELD CHALLENGE TAB COMPONENT
// ═══════════════════════════════════════════════════════════════
function FieldChallengeTab({ selectedLevel }) {
  var level = LEVELS[selectedLevel];
  var scenario = level.scenario || {};
  var fixSteps = splitFixSteps(scenario.fix || '');

  return (
    <div>
      <div className="card">
        <div className="card-header">
          <div className="card-icon amber">🏗️</div>
          <div>
            <div className="card-title">Field Challenge — {level.id}: {level.title}</div>
            <div className="card-subtitle">{scenario.title || 'Real-world scenario from Clonshaugh DC'}</div>
          </div>
        </div>
        <p style={{fontSize:'0.78rem', color:'var(--text-faint)', fontStyle:'italic', marginBottom:'1rem'}}>
          Fictional reference facility (Clonshaugh DC). All figures are indicative and sourced — not a substitute for site-specific engineering assessment.
        </p>

        <div className="scenario-card">
          {/* Situation */}
          <div className="scenario-section">
            <div className="scenario-label situation">Situation</div>
            <div className="scenario-text">{scenario.situation}</div>
          </div>

          {/* Challenge */}
          <div className="scenario-section">
            <div className="scenario-label challenge">Challenge</div>
            <div className="scenario-text" style={{fontWeight:600, color:'var(--text)', fontSize:'0.9rem'}}>
              {scenario.challenge}
            </div>
          </div>

          {/* Fix — step by step */}
          <div className="scenario-section">
            <div className="scenario-label fix">Step-by-Step Solution</div>
            {fixSteps.length > 1 ? (
              <ul className="fix-steps">
                {fixSteps.map(function(step, si) {
                  return (
                    <li key={si} style={{
                      background: 'var(--surface-3)',
                      border: '1px solid var(--border)',
                      borderRadius: 'var(--radius-sm)',
                      padding: '0.65rem 0.9rem',
                      fontSize: '0.82rem',
                      color: 'var(--text-muted)',
                      lineHeight: '1.6'
                    }}>
                      {step.trim()}
                    </li>
                  );
                })}
              </ul>
            ) : (
              <div className="scenario-text">{scenario.fix}</div>
            )}
          </div>
        </div>
      </div>

      {/* Cross-references */}
      <div style={{padding:'0.75rem 1rem', background:'var(--surface)', border:'1px solid var(--border)', borderRadius:'var(--radius-md)'}}>
        <div className="section-label" style={{marginBottom:'0.4rem'}}>Related Levels</div>
        <div className="crossrefs-row">
          {(level.crossRefs || []).map(function(ref, ri) {
            return <span key={ri} className="crossref-tag">{ref}</span>;
          })}
        </div>
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════════════════════════
// ASSESSMENT TAB COMPONENT
// ═══════════════════════════════════════════════════════════════
function AssessmentTab() {
  var [shuffledQs, setShuffledQs] = React.useState(function() {
    return shuffleArray(ASSESSMENT_QUESTIONS);
  });
  var [current, setCurrent] = React.useState(safeLoad('aq_current', 0));
  var [answers, setAnswers] = React.useState(safeLoad('aq_answers', {}));
  var [selected, setSelected] = React.useState(null);
  var [revealed, setRevealed] = React.useState(false);
  var [done, setDone] = React.useState(false);

  var total = shuffledQs.length;
  var q = shuffledQs[current] || {};
  var correctIdx = q.correct;
  var answered = Object.keys(answers).length;

  function handleOption(optIdx) {
    if (revealed) return;
    setSelected(optIdx);
  }

  function handleReveal() {
    if (selected === null) return;
    setRevealed(true);
    var newAnswers = Object.assign({}, answers);
    newAnswers[current] = { selected: selected, correct: selected === correctIdx };
    setAnswers(newAnswers);
    safeStore('aq_answers', newAnswers);
  }

  function handleNext() {
    if (current < total - 1) {
      setCurrent(current + 1);
      safeStore('aq_current', current + 1);
      setSelected(null);
      setRevealed(false);
    } else {
      setDone(true);
    }
  }

  function handlePrev() {
    if (current > 0) {
      setCurrent(current - 1);
      safeStore('aq_current', current - 1);
      var prevAnswer = answers[current - 1];
      setSelected(prevAnswer ? prevAnswer.selected : null);
      setRevealed(prevAnswer ? true : false);
    }
  }

  function handleRestart() {
    setShuffledQs(shuffleArray(ASSESSMENT_QUESTIONS));
    setCurrent(0);
    setAnswers({});
    setSelected(null);
    setRevealed(false);
    setDone(false);
    safeStore('aq_current', 0);
    safeStore('aq_answers', {});
  }

  if (done) {
    var score = Object.values(answers).filter(function(a) { return a.correct; }).length;
    var pct = Math.round((score / total) * 100);
    var label = pct >= 80 ? '🏆 Excellent' : pct >= 60 ? '✅ Good Pass' : pct >= 40 ? '📖 Keep Studying' : '🔄 Review Recommended';
    return (
      <div className="card assessment-score">
        <div className="score-circle">
          <span className="score-num">{score}</span>
          <span className="score-denom">/ {total}</span>
        </div>
        <div className="score-label">{label}</div>
        <div className="score-pct">{pct}% — {score} correct out of {total} questions</div>
        <p style={{fontSize:'0.82rem', color:'var(--text-muted)', maxWidth:'400px', margin:'0.75rem auto 0', lineHeight:'1.6'}}>
          {pct >= 80
            ? 'Strong performance across all 9 levels. You understand the power density chain from legacy infrastructure through to the retrofit investment decision.'
            : pct >= 60
            ? 'Good foundation. Review the levels where you missed questions and revisit the Grammar and Logic tabs for those specific areas.'
            : 'The module covers significant technical depth. Work through the Grammar and Logic tabs for each level before re-attempting the assessment.'}
        </p>
        <button className="restart-btn" onClick={handleRestart}>Restart Assessment</button>
      </div>
    );
  }

  var optionLetters = ['A', 'B', 'C', 'D'];
  var prevAnswerState = answers[current];
  var displaySelected = revealed ? (prevAnswerState ? prevAnswerState.selected : selected) : selected;
  var isCorrect = revealed && displaySelected === correctIdx;

  return (
    <div>
      <div className="assessment-header">
        <div className="assessment-progress">
          Question {current + 1} of {total} · {answered} answered
        </div>
        <div style={{fontSize:'0.78rem', color:'var(--text-faint)'}}>
          Score: {Object.values(answers).filter(function(a){return a.correct;}).length} / {answered}
        </div>
      </div>
      <div className="progress-bar-wrap">
        <div className="progress-bar-fill" style={{width: ((current / total) * 100) + '%'}} />
      </div>

      <div className="q-card">
        <div className="q-meta">
          <span className="q-level-badge">L{q.level}</span>
          <span className={'q-tier-badge ' + (q.tier || 'knowledge')}>{q.tier || 'knowledge'}</span>
          <span className="q-id">{q.id}</span>
        </div>
        <div className="q-text">{q.q}</div>
        <div className="q-options">
          {(q.options || []).map(function(opt, oi) {
            var cls = 'q-option-btn';
            if (revealed) {
              if (oi === correctIdx) cls += ' correct';
              else if (oi === displaySelected && oi !== correctIdx) cls += ' incorrect';
            } else if (oi === selected) {
              cls += ' selected';
            }
            return (
              <button
                key={oi}
                className={cls}
                onClick={() => handleOption(oi)}
                disabled={revealed}
              >
                <span className="q-option-letter">{optionLetters[oi]}</span>
                <span>{opt}</span>
              </button>
            );
          })}
        </div>

        {revealed && q.explain && (
          <div className={'q-explain' + (isCorrect ? '' : ' wrong')}>
            <div className="q-explain-label">{isCorrect ? '✓ Correct' : '✗ Incorrect'}</div>
            {q.explain}
          </div>
        )}

        <div className="q-nav">
          <button
            className="q-nav-btn secondary"
            onClick={handlePrev}
            disabled={current === 0}
          >
            ← Previous
          </button>
          <div style={{display:'flex', gap:'0.5rem'}}>
            {!revealed && selected !== null && (
              <button className="q-nav-btn primary" onClick={handleReveal}>
                Check Answer
              </button>
            )}
            {revealed && (
              <button className="q-nav-btn primary" onClick={handleNext}>
                {current < total - 1 ? 'Next →' : 'See Results'}
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════════════════════════
// BSG TAB COMPONENT (Bibliography, Glossary)
// ═══════════════════════════════════════════════════════════════
function BSGTab() {
  var [bsgTab, setBsgTab] = React.useState('glossary');
  var [search, setSearch] = React.useState('');

  var filteredGlossary = GLOSSARY.filter(function(item) {
    if (!search) return true;
    var q = search.toLowerCase();
    return (item.term || '').toLowerCase().includes(q) ||
           (item.definition || '').toLowerCase().includes(q);
  });

  return (
    <div>
      <div className="card">
        <div className="card-header">
          <div className="card-icon cyan">📚</div>
          <div>
            <div className="card-title">Bibliography, Glossary</div>
            <div className="card-subtitle">{GLOSSARY.length} terms · {BIBLIOGRAPHY.length} sources</div>
          </div>
        </div>

        <div className="bsg-tab-bar">
          <button
            className={'bsg-tab-btn' + (bsgTab === 'glossary' ? ' active' : '')}
            onClick={() => setBsgTab('glossary')}
          >
            📖 Glossary ({GLOSSARY.length} terms)
          </button>
          <button
            className={'bsg-tab-btn' + (bsgTab === 'bibliography' ? ' active' : '')}
            onClick={() => setBsgTab('bibliography')}
          >
            📚 Bibliography ({BIBLIOGRAPHY.length} sources)
          </button>
        </div>

        {bsgTab === 'glossary' && (
          <div>
            <input
              className="glossary-search"
              type="text"
              placeholder="Search glossary terms..."
              value={search}
              onChange={function(e) { setSearch(e.target.value); }}
            />
            {filteredGlossary.length === 0 ? (
              <p style={{color:'var(--text-faint)', fontSize:'0.83rem', textAlign:'center', padding:'1rem'}}>
                No terms match "{search}"
              </p>
            ) : (
              <div className="glossary-grid">
                {filteredGlossary.map(function(item, gi) {
                  return (
                    <div key={gi} className="glossary-item">
                      <div className="glossary-term">{item.term}</div>
                      <div className="glossary-def">{item.definition}</div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        )}

        {bsgTab === 'bibliography' && (
          <div className="bib-list">
            {BIBLIOGRAPHY.map(function(src, bi) {
              return (
                <div key={bi} className="bib-item">
                  <span className={'bib-tier ' + (src.tier || 'T3')}>{src.tier || 'T3'}</span>
                  <div className="bib-content">
                    <div className="bib-title">{src.title}</div>
                    <div className="bib-meta">
                      {src.type && <span style={{textTransform:'capitalize'}}>{src.type}</span>}
                      {src.year && <span> · {src.year}</span>}
                    </div>
                    {src.usage && <div className="bib-usage">{src.usage}</div>}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════════════════════════
// APP COMPONENT
// ═══════════════════════════════════════════════════════════════
function App() {
  var [theme, setTheme] = React.useState(safeLoad('theme', 'dark'));
  var [selectedLevel, setSelectedLevel] = React.useState(safeLoad('level', 0));
  var [activeTab, setActiveTab] = React.useState(safeLoad('tab', 'chain'));

  // Apply theme to document
  React.useEffect(function() {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  // Clamp selectedLevel to valid range
  var levelIdx = Math.max(0, Math.min(LEVELS.length - 1, selectedLevel));
  var currentLevel = LEVELS[levelIdx];

  function renderTab() {
    switch (activeTab) {
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
    }
  }

  return (
    <div className="app-container">
      <Header theme={theme} setTheme={setTheme} />

      {/* Hero */}
      <div className="hero-banner">
        <div className="hero-module-id">DC-AI-001 · Power Density</div>
        <div className="hero-title">Can This Facility Handle AI Workloads?</div>
        <div className="hero-disclaimer">
          {MODULE_META.hero_disclaimer || 'Fictional reference facility (Clonshaugh DC). All figures are indicative and sourced — not a substitute for site-specific engineering assessment.'}
        </div>
      </div>

      {/* Level selector (hidden on chain and assessment tabs) */}
      {activeTab !== 'chain' && activeTab !== 'assessment' && activeTab !== 'bsg' && (
        <LevelSelector selectedLevel={levelIdx} setSelectedLevel={setSelectedLevel} />
      )}

      {/* Tab bar */}
      <TabBar activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Current level indicator (not shown on chain/assessment/bsg) */}
      {activeTab !== 'chain' && activeTab !== 'assessment' && activeTab !== 'bsg' && (
        <div style={{
          background: 'var(--surface-2)',
          borderBottom: '1px solid var(--border)',
          padding: '0.4rem 1.5rem',
          display: 'flex',
          alignItems: 'center',
          gap: '0.6rem',
          fontSize: '0.78rem',
          color: 'var(--text-muted)'
        }}>
          <span style={{fontSize:'1rem'}}>{currentLevel.icon}</span>
          <strong style={{color:'var(--text)'}}>{currentLevel.id}: {currentLevel.title}</strong>
          <span>·</span>
          <span style={{color:'var(--text-faint)'}}>{currentLevel.subtitle}</span>
        </div>
      )}

      {/* Main content */}
      <main className="main-content">
        {renderTab()}
      </main>

      {/* Footer */}
      <footer className="app-footer">
        <span className="footer-text">
          © 2026 Legacy Business Engineers Ltd · DC-AI Series · Module 1 of 8
        </span>
        <span className="footer-version">v{TOOL_VERSION}</span>
      </footer>
    </div>
  );
}

// ═══════════════════════════════════════════════════════════════
// RENDER
// ═══════════════════════════════════════════════════════════════
var root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
</script>
</body>
</html>
'''

out_path = os.path.join(BASE, 'section_d2.html')
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(section_d2)

lines = section_d2.count('\n') + 1
print(f'Written {out_path} ({lines} lines)')
print('build_05_section_d2.py COMPLETE')
