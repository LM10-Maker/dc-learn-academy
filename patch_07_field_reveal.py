"""patch_07_field_reveal.py — hide Field Challenge fix by default; add Show the Fix button"""
F = "DC-AI-001_v2_0_0.html"

CSS = """
    /* ─── FIELD CHALLENGE REVEAL ────────────────────────────────── */
    .show-fix-btn {
      display: inline-flex; align-items: center; gap: 6px;
      padding: 8px 18px; margin-top: 0.75rem;
      font-size: 0.82rem; font-weight: 600; cursor: pointer;
      border: 1px solid var(--logic); border-radius: var(--radius-sm);
      background: rgba(217,119,6,0.08); color: var(--logic);
      transition: all var(--transition);
    }
    .show-fix-btn:hover { background: rgba(217,119,6,0.18); }
    .fix-reveal-box { margin-top: 0.75rem; animation: fadeIn 0.2s ease; }
    @keyframes fadeIn { from { opacity:0; transform:translateY(-4px); } to { opacity:1; transform:none; } }
"""

# Replace the fix section in FieldChallengeTab — wrap it with state toggle
OLD_FIX = r"""function FieldChallengeTab({ selectedLevel }) {
  var level = LEVELS[selectedLevel];
  var scenario = level.scenario || {};
  var fixSteps = splitFixSteps(scenario.fix || '');

  return ("""

NEW_FIX = r"""function FieldChallengeTab({ selectedLevel }) {
  var level = LEVELS[selectedLevel];
  var scenario = level.scenario || {};
  var fixSteps = splitFixSteps(scenario.fix || '');
  var [fixOpen, setFixOpen] = React.useState(false);

  return ("""

OLD_FIX_SECTION = r"""          {/* Fix — step by step */}
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
          </div>"""

NEW_FIX_SECTION = r"""          {/* Fix — hidden by default, revealed on click */}
          <div className="scenario-section">
            <button className="show-fix-btn" onClick={function(){setFixOpen(function(p){return !p;});}}>
              🔧 {fixOpen ? 'Hide the Fix ▲' : 'Show the Fix ▼'}
            </button>
            {fixOpen && (
              <div className="fix-reveal-box">
                <div className="scenario-label fix" style={{marginBottom:'0.5rem'}}>Step-by-Step Solution</div>
                {fixSteps.length > 1 ? (
                  <ul className="fix-steps">
                    {fixSteps.map(function(step, si) {
                      return (
                        <li key={si} style={{
                          background:'var(--surface-3)',border:'1px solid var(--border)',
                          borderRadius:'var(--radius-sm)',padding:'0.65rem 0.9rem',
                          fontSize:'0.82rem',color:'var(--text-muted)',lineHeight:'1.6',
                          marginBottom:'0.4rem'
                        }}>{step.trim()}</li>
                      );
                    })}
                  </ul>
                ) : (
                  <div className="scenario-text">{scenario.fix}</div>
                )}
              </div>
            )}
          </div>"""

html = open(F, encoding="utf-8").read()
for label, old in [("func sig", OLD_FIX), ("fix section", OLD_FIX_SECTION)]:
    assert old in html, f"{label} not found"
html = html.replace("    /* ─── RESET & BASE", CSS + "    /* ─── RESET & BASE", 1)
html = html.replace(OLD_FIX, NEW_FIX, 1)
html = html.replace(OLD_FIX_SECTION, NEW_FIX_SECTION, 1)
open(F, "w", encoding="utf-8").write(html)
print("patch_07 done — Field Challenge fix hidden by default")
