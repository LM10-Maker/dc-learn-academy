#!/usr/bin/env python3
"""Fix 2: Wire stage completion buttons to visitedStages state."""

src = '/home/user/dc-learn-academy/DC-AI-001_v2_3_0 (3).html'
with open(src, 'r', encoding='utf-8') as f:
    html = f.read()

# 2a: Grammar button — add disabled={done}
OLD2a = """      <button className={'completion-btn btn-grammar'+(done?' done':'')} onClick={onComplete}>
        {done ? '✓ Key facts memorised' : "I've memorised the key facts"}
      </button>"""
NEW2a = """      <button className={'completion-btn btn-grammar'+(done?' done':'')} onClick={done?undefined:onComplete} disabled={done}>
        {done ? '✓ Complete' : "I've memorised the key facts"}
      </button>"""
assert OLD2a in html, "Fix2a: grammar button not found"
html = html.replace(OLD2a, NEW2a, 1)

# 2b: Logic button — add disabled={done}
OLD2b = """      <button className={'completion-btn btn-logic'+(done?' done':'')} onClick={onComplete}>
        {done ? '✓ Consequences understood' : 'I understand the consequences'}
      </button>"""
NEW2b = """      <button className={'completion-btn btn-logic'+(done?' done':'')} onClick={done?undefined:onComplete} disabled={done}>
        {done ? '✓ Complete' : 'I understand the consequences'}
      </button>"""
assert OLD2b in html, "Fix2b: logic button not found"
html = html.replace(OLD2b, NEW2b, 1)

# 2c: Rhetoric button — add disabled={done}
OLD2c = """      <button className={'completion-btn btn-rhetoric'+(done?' done':'')} onClick={onComplete} style={{marginTop:16}}>
        {done ? '✓ Can explain to stakeholders' : 'I can explain it to each stakeholder'}
      </button>"""
NEW2c = """      <button className={'completion-btn btn-rhetoric'+(done?' done':'')} onClick={done?undefined:onComplete} disabled={done} style={{marginTop:16}}>
        {done ? '✓ Complete' : 'I can explain it to each stakeholder'}
      </button>"""
assert OLD2c in html, "Fix2c: rhetoric button not found"
html = html.replace(OLD2c, NEW2c, 1)

# 2d: LearnTab — use visitedStages for done state; accept+use setVisitedStages
OLD2d = """function LearnTab({ selectedLevel, setSelectedLevel, visitedStages, progress, setProgress }) {
  var level = LEVELS[selectedLevel];
  var p = (progress && progress[level.id]) || {};
  var [stage, setStage] = React.useState('grammar');
  var [rhetPersonaInit, setRhetPersona] = React.useState(null);
  var stageClass = function(s) { var active=stage===s; var done=p[s]; if(active) return 'triv-btn active-'+s; if(done) return 'triv-btn done-'+s; return 'triv-btn'; };
  var handleComplete = function(s) { if(setProgress) setProgress(function(prev){return Object.assign({},prev,{[level.id]:Object.assign({},prev[level.id]||{},{[s]:true})}); }); };"""
NEW2d = """function LearnTab({ selectedLevel, setSelectedLevel, visitedStages, setVisitedStages, progress, setProgress }) {
  var level = LEVELS[selectedLevel];
  var p = (visitedStages && visitedStages[selectedLevel]) || {};
  var [stage, setStage] = React.useState('grammar');
  var [rhetPersonaInit, setRhetPersona] = React.useState(null);
  var stageClass = function(s) { var active=stage===s; var done=p[s]; if(active) return 'triv-btn active-'+s; if(done) return 'triv-btn done-'+s; return 'triv-btn'; };
  var handleComplete = function(s) {
    if (setVisitedStages) setVisitedStages(function(prev) {
      var next = Object.assign({}, prev);
      next[selectedLevel] = Object.assign({}, next[selectedLevel] || {});
      next[selectedLevel][s] = true;
      safeStore('visitedStages', next);
      return next;
    });
  };"""
assert OLD2d in html, "Fix2d: LearnTab signature not found"
html = html.replace(OLD2d, NEW2d, 1)

# 2e: Pass setVisitedStages to LearnTab in App renderTab
OLD2e = "        return <LearnTab selectedLevel={levelIdx} visitedStages={visitedStages} />;"
NEW2e = "        return <LearnTab selectedLevel={levelIdx} visitedStages={visitedStages} setVisitedStages={setVisitedStages} />;"
assert OLD2e in html, "Fix2e: LearnTab call in renderTab not found"
html = html.replace(OLD2e, NEW2e, 1)

with open(src, 'w', encoding='utf-8') as f:
    f.write(html)
print("Fix 2 applied: Stage completion buttons wired to visitedStages.")
