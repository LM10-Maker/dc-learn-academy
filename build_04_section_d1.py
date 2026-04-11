#!/usr/bin/env python3
"""
build_04_section_d1.py
Section D part 1: Opens <script type="text/babel">, utility functions,
Header, LevelSelector, TabBar, ChainTab, GrammarTab, LogicTab components.
Output: section_d1.html
"""

import os

BASE = os.path.dirname(os.path.abspath(__file__))

# Use raw strings — no f-strings, no curly-brace interpolation from Python
section_d1 = r'''<script type="text/babel">
// ═══════════════════════════════════════════════════════════════
// UTILITY FUNCTIONS
// ═══════════════════════════════════════════════════════════════

function safeStore(key, val) {
  try { localStorage.setItem('dcai001_' + key, JSON.stringify(val)); } catch(e) {}
}
function safeLoad(key, fallback) {
  try {
    var v = localStorage.getItem('dcai001_' + key);
    return v !== null ? JSON.parse(v) : fallback;
  } catch(e) { return fallback; }
}
function shuffleArray(arr) {
  var a = arr.slice();
  for (var i = a.length - 1; i > 0; i--) {
    var j = Math.floor(Math.random() * (i + 1));
    var tmp = a[i]; a[i] = a[j]; a[j] = tmp;
  }
  return a;
}
function splitFixSteps(fixText) {
  if (!fixText) return [fixText];
  // Split on "Step N:" pattern
  var parts = fixText.split(/(?=Step \d+:)/);
  return parts.filter(function(p) { return p.trim().length > 0; });
}

// ═══════════════════════════════════════════════════════════════
// PERSONA CONFIG
// ═══════════════════════════════════════════════════════════════
var PERSONAS = [
  { key: 'asset_management', name: 'Conor',   role: 'Asset Manager (Fund)',            avatarClass: 'conor',   initial: 'C', icon: '🏦' },
  { key: 'technology',       name: 'Helena',  role: 'Chief Technology Officer (Colo)', avatarClass: 'helena',  initial: 'H', icon: '💻' },
  { key: 'technical',        name: 'Eoin',    role: 'MEP Retrofit Engineer',           avatarClass: 'eoin',    initial: 'E', icon: '🔧' },
  { key: 'compliance',       name: 'Rachel',  role: 'ESG & Regulatory Director',       avatarClass: 'rachel',  initial: 'R', icon: '📋' },
  { key: 'cost',             name: 'Padraig', role: 'Project QS / Cost Manager',       avatarClass: 'padraig', initial: 'P', icon: '💰' }
];

// ═══════════════════════════════════════════════════════════════
// HEADER COMPONENT
// ═══════════════════════════════════════════════════════════════
function Header({ theme, setTheme }) {
  return (
    <header className="app-header">
      <div className="header-left">
        <img src={LOGO_SRC} alt="LBE" className="header-logo" />
        <div className="header-divider" />
        <div className="header-title">
          <span className="header-title-main">DC-AI-001: Power Density</span>
          <span className="header-title-sub">AI-Ready Data Centre Investment Intelligence</span>
        </div>
      </div>
      <div className="header-right">
        <span className="series-badge">Module 1 of 8 · DC-AI v1.0</span>
        <button
          className="theme-btn"
          onClick={() => {
            var next = theme === 'dark' ? 'light' : 'dark';
            setTheme(next);
            safeStore('theme', next);
          }}
          title={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
        >
          {theme === 'dark' ? '☀️' : '🌙'}
        </button>
      </div>
    </header>
  );
}

// ═══════════════════════════════════════════════════════════════
// LEVEL SELECTOR COMPONENT
// ═══════════════════════════════════════════════════════════════
function LevelSelector({ selectedLevel, setSelectedLevel }) {
  return (
    <div className="level-selector-wrap">
      <div className="level-selector-label">Select Level</div>
      <div className="level-selector-row">
        {LEVELS.map(function(lvl, idx) {
          return (
            <button
              key={lvl.id}
              className={'level-btn' + (selectedLevel === idx ? ' active' : '')}
              onClick={() => { setSelectedLevel(idx); safeStore('level', idx); }}
            >
              <span className="level-btn-icon">{lvl.icon}</span>
              <span className="level-btn-id">{lvl.id}</span>
              <span className="level-btn-label">{lvl.title}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════════════════════════
// TAB BAR COMPONENT
// ═══════════════════════════════════════════════════════════════
var TABS = [
  { id: 'chain',      label: '🔗 Chain' },
  { id: 'grammar',    label: '📖 Grammar' },
  { id: 'logic',      label: '⚡ Logic' },
  { id: 'rhetoric',   label: '💬 Rhetoric' },
  { id: 'field',      label: '🏗️ Field Challenge' },
  { id: 'assessment', label: '✅ Assessment' },
  { id: 'bsg',        label: '📚 BSG' }
];

function TabBar({ activeTab, setActiveTab }) {
  return (
    <div className="tab-bar">
      {TABS.map(function(tab) {
        return (
          <button
            key={tab.id}
            className={'tab-btn' + (activeTab === tab.id ? ' active' : '')}
            onClick={() => { setActiveTab(tab.id); safeStore('tab', tab.id); }}
          >
            {tab.label}
          </button>
        );
      })}
    </div>
  );
}

// ═══════════════════════════════════════════════════════════════
// CHAIN TAB COMPONENT
// ═══════════════════════════════════════════════════════════════
function ChainTab({ selectedLevel, setSelectedLevel, setActiveTab }) {
  var level = LEVELS[selectedLevel];
  return (
    <div>
      <div className="card">
        <div className="card-header">
          <div className="card-icon blue">🔗</div>
          <div>
            <div className="card-title">Power Density Chain</div>
            <div className="card-subtitle">9-level progression from legacy density to the retrofit investment decision</div>
          </div>
        </div>
        <p style={{fontSize:'0.83rem', color:'var(--text-muted)', lineHeight:'1.65', marginBottom:'1.25rem'}}>
          Each level builds on the last. The chain shows why AI retrofits require re-evaluating every
          component from the grid connection to the rack PDU — and why the investment decision
          at Level 9 is only defensible when the engineering at Levels 1–8 is understood.
        </p>
        <div className="chain-grid">
          {LEVELS.map(function(lvl, idx) {
            return (
              <div
                key={lvl.id}
                className={'chain-level-card' + (selectedLevel === idx ? ' active' : '')}
                onClick={() => {
                  setSelectedLevel(idx);
                  safeStore('level', idx);
                  setActiveTab('grammar');
                  safeStore('tab', 'grammar');
                }}
              >
                <div className="chain-level-num">{lvl.id} · Level {lvl.level}</div>
                <div className="chain-level-icon">{lvl.icon}</div>
                <div className="chain-level-title">{lvl.title}</div>
                <div className="chain-level-subtitle">{lvl.subtitle}</div>
                <div className="chain-plain-english">{lvl.plainEnglish}</div>
                {lvl.retrofitRelevance && (
                  <div style={{marginTop:'0.5rem', padding:'0.45rem 0.65rem', background:'var(--amber-dim)', borderRadius:'var(--radius-sm)', fontSize:'0.73rem', color:'var(--text-muted)', lineHeight:'1.45'}}>
                    <strong style={{color:'var(--amber)', fontSize:'0.62rem', textTransform:'uppercase', letterSpacing:'0.07em'}}>Retrofit Relevance · </strong>
                    {lvl.retrofitRelevance}
                  </div>
                )}
                <div className="chain-crossrefs">
                  {(lvl.crossRefs || []).map(function(ref, ri) {
                    return <span key={ri} className="chain-crossref-tag">{ref}</span>;
                  })}
                </div>
                <div style={{marginTop:'0.6rem', fontSize:'0.68rem', color:'var(--accent)', fontWeight:600}}>
                  Click to explore →
                </div>
              </div>
            );
          })}
        </div>
      </div>
      {/* Currently selected level highlight */}
      <div className="card">
        <div className="card-header">
          <div className="card-icon amber">{level.icon}</div>
          <div>
            <div className="card-title">Currently Selected: {level.id} — {level.title}</div>
            <div className="card-subtitle">{level.subtitle}</div>
          </div>
        </div>
        <p style={{fontSize:'0.83rem', color:'var(--text-muted)', lineHeight:'1.65', marginBottom:'0.75rem'}}>{level.plainEnglish}</p>
        <div style={{marginBottom:'0.75rem'}}>
          <div className="section-label">Source Note</div>
          <p style={{fontSize:'0.78rem', color:'var(--text-faint)', fontStyle:'italic', lineHeight:'1.5'}}>{level.sourceNote}</p>
        </div>
        <div>
          <div className="section-label">Cross-References</div>
          <div className="crossrefs-row">
            {(level.crossRefs || []).map(function(ref, ri) {
              return <span key={ri} className="crossref-tag">{ref}</span>;
            })}
          </div>
        </div>
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════════════════════════
// GRAMMAR TAB COMPONENT
// ═══════════════════════════════════════════════════════════════
function GrammarTab({ selectedLevel }) {
  var level = LEVELS[selectedLevel];
  var grammar = level.grammar || {};
  var facts = grammar.facts || [];

  return (
    <div>
      {/* Retrofit relevance */}
      <div className="retrofit-box">
        <div className="section-label">Retrofit Relevance</div>
        <div className="retrofit-text">{level.retrofitRelevance}</div>
      </div>

      {/* Facts header */}
      <div className="card">
        <div className="card-header">
          <div className="card-icon blue">📖</div>
          <div>
            <div className="card-title">Grammar — {level.id}: {level.title}</div>
            <div className="card-subtitle">{facts.length} key terms with definitions, numbers, and standards</div>
          </div>
        </div>

        <div className="fact-grid">
          {facts.map(function(fact, fi) {
            var soWhat = SO_WHAT_MAP[fact.term] || fact.soWhat || '';
            return (
              <div key={fi} className="fact-card">
                <div className="fact-term">{fact.term}</div>
                <div className="fact-standard">{fact.standard}</div>
                <div style={{fontSize:'0.83rem', color:'var(--text-muted)', lineHeight:'1.6', marginBottom:'0.6rem'}}>
                  <strong style={{color:'var(--text)', fontSize:'0.72rem', textTransform:'uppercase', letterSpacing:'0.06em'}}>Definition · </strong>
                  {fact.definition}
                </div>
                <div className="fact-row">
                  <div className="fact-field">
                    <span className="fact-field-label">Plain English</span>
                    <span className="fact-field-value">{fact.plain}</span>
                  </div>
                  <div className="fact-field">
                    <span className="fact-field-label">By the Numbers</span>
                    <div className="fact-number-pill">{fact.number}</div>
                  </div>
                </div>
                <div className="so-what-box">
                  <strong>So what? </strong>{soWhat || fact.soWhat}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* What it looks like */}
      {grammar.whatItLooksLike && (
        <div className="card">
          <div className="card-header">
            <div className="card-icon cyan">👁️</div>
            <div>
              <div className="card-title">What It Looks Like On Site</div>
              <div className="card-subtitle">Observable indicators a professional would recognise</div>
            </div>
          </div>
          <div className="looks-like-box">{grammar.whatItLooksLike}</div>
        </div>
      )}

      {/* Site checklist */}
      {grammar.siteChecklist && grammar.siteChecklist.length > 0 && (
        <div className="card">
          <div className="card-header">
            <div className="card-icon green">✅</div>
            <div>
              <div className="card-title">Site Checklist</div>
              <div className="card-subtitle">What to check in the field for this level</div>
            </div>
          </div>
          <ul className="checklist">
            {grammar.siteChecklist.map(function(item, ii) {
              return <li key={ii}>{item}</li>;
            })}
          </ul>
        </div>
      )}

      {/* Source note */}
      <div style={{padding:'0.75rem 1rem', background:'var(--surface)', border:'1px solid var(--border)', borderRadius:'var(--radius-md)', marginBottom:'1rem'}}>
        <div className="section-label" style={{marginBottom:'0.3rem'}}>Sources for {level.id}</div>
        <p style={{fontSize:'0.76rem', color:'var(--text-faint)', fontStyle:'italic', lineHeight:'1.55'}}>{level.sourceNote}</p>
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════════════════════════
// LOGIC TAB COMPONENT
// ═══════════════════════════════════════════════════════════════
function LogicTab({ selectedLevel }) {
  var level = LEVELS[selectedLevel];
  var logic = level.logic || {};
  var ce = logic.causeAndEffect || [];
  var wl = logic.weakestLink || {};

  return (
    <div>
      {/* Constraint Lesson */}
      {logic.constraintLesson && (
        <div className="constraint-box">
          <div className="section-label">Fundamental Constraint</div>
          <div className="constraint-text">{logic.constraintLesson}</div>
        </div>
      )}

      {/* Cause & Effect */}
      <div className="card">
        <div className="card-header">
          <div className="card-icon amber">⚡</div>
          <div>
            <div className="card-title">Cause & Effect — {level.id}: {level.title}</div>
            <div className="card-subtitle">{ce.length} cause-and-effect chains showing real consequences</div>
          </div>
        </div>
        <div className="ce-list">
          {ce.map(function(entry, ei) {
            return (
              <div key={ei} className="ce-card">
                <div className="ce-section cause">
                  <div className="ce-section-label">Cause</div>
                  <div className="ce-section-text">{entry.cause}</div>
                </div>
                <div className="ce-section effect">
                  <div className="ce-section-label">Effect</div>
                  <div className="ce-section-text">{entry.effect}</div>
                </div>
                <div className="ce-section insight">
                  <div className="ce-section-label">Insight</div>
                  <div className="ce-section-text">{entry.insight}</div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Weakest Link */}
      {wl && wl.whatsWrong && (
        <div className="card">
          <div className="card-header">
            <div className="card-icon red">🔍</div>
            <div>
              <div className="card-title">The Weakest Link</div>
              <div className="card-subtitle">Common misconception corrected with engineering reasoning</div>
            </div>
          </div>
          <div className="weakest-link-card">
            <div className="wl-section">
              <div className="wl-label wrong">❌ Common Mistake</div>
              <div className="wl-text">{wl.whatsWrong}</div>
            </div>
            <div className="wl-section">
              <div className="wl-label right">✓ Correct Understanding</div>
              <div className="wl-text">{wl.whatsRight}</div>
            </div>
            {wl.howToGetThere && wl.howToGetThere.length > 0 && (
              <div className="wl-section">
                <div className="wl-label steps">→ How To Get There</div>
                <ul className="wl-steps-list">
                  {wl.howToGetThere.map(function(step, si) {
                    return <li key={si}>{step}</li>;
                  })}
                </ul>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
'''

out_path = os.path.join(BASE, 'section_d1.html')
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(section_d1)

lines = section_d1.count('\n') + 1
print(f'Written {out_path} ({lines} lines)')
print('build_04_section_d1.py COMPLETE')
