#!/usr/bin/env python3
"""Fix 5: After cascade calc runs, show PASS/FAIL badge + reason inline
on each chain card row. Green/red left border. Store results in state.
"""

with open('/home/user/dc-learn-academy/DC-AI-001_v2_1_0.html', 'r') as f:
    content = f.read()

# 1. Add cascadeResults state to App component
old_app_state = (
    '  var [visitedStages, setVisitedStages] = React.useState(safeLoad(\'visitedStages\', {}));\n'
    '\n'
    '  // Apply theme to document'
)
new_app_state = (
    '  var [visitedStages, setVisitedStages] = React.useState(safeLoad(\'visitedStages\', {}));\n'
    '  var [cascadeResults, setCascadeResults] = React.useState(safeLoad(\'cascadeResults\', {}));\n'
    '\n'
    '  function onCascadeResult(lvlIdx, res) {\n'
    '    setCascadeResults(function(p) {\n'
    '      var n = Object.assign({}, p); n[lvlIdx] = res;\n'
    '      safeStore(\'cascadeResults\', n); return n;\n'
    '    });\n'
    '  }\n'
    '\n'
    '  // Apply theme to document'
)
assert old_app_state in content, "App state not found"
content = content.replace(old_app_state, new_app_state, 1)

# 2. Pass cascadeResults/onCascadeResult to ChainTab and SidebarCalculator
old_chain_render = (
    '        return <ChainTab selectedLevel={levelIdx} setSelectedLevel={setSelectedLevel} setActiveTab={setActiveTab} />;'
)
new_chain_render = (
    '        return <ChainTab selectedLevel={levelIdx} setSelectedLevel={setSelectedLevel} setActiveTab={setActiveTab} cascadeResults={cascadeResults} />;'
)
assert old_chain_render in content, "ChainTab render not found"
content = content.replace(old_chain_render, new_chain_render, 1)

old_sidebar_calc = (
    '          <SidebarCalculator selectedLevel={levelIdx} />'
)
new_sidebar_calc = (
    '          <SidebarCalculator selectedLevel={levelIdx} onCascadeResult={onCascadeResult} />'
)
assert old_sidebar_calc in content, "SidebarCalculator render not found"
content = content.replace(old_sidebar_calc, new_sidebar_calc, 1)

# 3. Update SidebarCalculator to call onCascadeResult
old_sidebar_fn = (
    'function SidebarCalculator({ selectedLevel }) {'
)
new_sidebar_fn = (
    'function SidebarCalculator({ selectedLevel, onCascadeResult }) {'
)
assert old_sidebar_fn in content, "SidebarCalculator function not found"
content = content.replace(old_sidebar_fn, new_sidebar_fn, 1)

old_run_check = (
    '  function runCheck() {\n'
    '    if (!cascadeCheck) { setResult({pass:false,reason:\'No cascade check for this level.\'}); return; }\n'
    '    try { setResult(cascadeCheck({rackCount:Number(rackCount),targetKW:Number(targetKW)})); }\n'
    '    catch(e) { setResult({pass:false,reason:\'Calculation error: \'+e.message}); }\n'
    '  }'
)
new_run_check = (
    '  function runCheck() {\n'
    '    if (!cascadeCheck) { var r={pass:false,reason:\'No cascade check for this level.\'}; setResult(r); if(onCascadeResult) onCascadeResult(selectedLevel,r); return; }\n'
    '    try {\n'
    '      var r = cascadeCheck({rackCount:Number(rackCount),targetKW:Number(targetKW)});\n'
    '      setResult(r);\n'
    '      if (onCascadeResult) onCascadeResult(selectedLevel, r);\n'
    '    } catch(e) {\n'
    '      var r = {pass:false,reason:\'Calculation error: \'+e.message};\n'
    '      setResult(r);\n'
    '      if (onCascadeResult) onCascadeResult(selectedLevel, r);\n'
    '    }\n'
    '  }'
)
assert old_run_check in content, "runCheck function not found"
content = content.replace(old_run_check, new_run_check, 1)

# 4. Update ChainTab to accept cascadeResults and show badges
old_chain_fn = (
    'function ChainTab({ selectedLevel, setSelectedLevel, setActiveTab }) {'
)
new_chain_fn = (
    'function ChainTab({ selectedLevel, setSelectedLevel, setActiveTab, cascadeResults }) {'
)
assert old_chain_fn in content, "ChainTab function signature not found"
content = content.replace(old_chain_fn, new_chain_fn, 1)

# 5. Add PASS/FAIL badge in chain card row (after subtitle, before chevron)
old_chain_row = (
    '                  <div style={{flex:1}}>\n'
    '                    <div className="chain-level-num">{lvl.id}: {lvl.title}</div>\n'
    '                    <div className="chain-level-subtitle">{lvl.subtitle}</div>\n'
    '                  </div>\n'
    '                  <div style={{fontSize:\'0.75rem\', color:\'var(--text-muted)\'}}>{isExpanded ? \'▲\' : \'▼\'}</div>'
)
new_chain_row = (
    '                  <div style={{flex:1}}>\n'
    '                    <div className="chain-level-num">{lvl.id}: {lvl.title}</div>\n'
    '                    <div className="chain-level-subtitle">{lvl.subtitle}</div>\n'
    '                  </div>\n'
    '                  {cascadeResults && cascadeResults[idx] && (\n'
    '                    <span style={{fontSize:\'0.6rem\',fontWeight:700,padding:\'1px 5px\',borderRadius:\'4px\',flexShrink:0,\n'
    '                      background:cascadeResults[idx].pass?\'rgba(74,124,89,0.15)\':\' rgba(220,38,38,0.15)\',\n'
    '                      color:cascadeResults[idx].pass?\'var(--lbe-green)\':\' var(--error)\'}}>\n'
    '                      {cascadeResults[idx].pass ? \'✓ PASS\' : \'✗ FAIL\'}\n'
    '                    </span>\n'
    '                  )}\n'
    '                  <div style={{fontSize:\'0.75rem\', color:\'var(--text-muted)\'}}>{isExpanded ? \'▲\' : \'▼\'}</div>'
)
assert old_chain_row in content, "chain card row not found"
content = content.replace(old_chain_row, new_chain_row, 1)

# 6. Add green/red left border to chain card when result available
old_card_style = (
    '                className={\'chain-level-card\' + (selectedLevel === idx ? \' active\' : \'\') + (lvl.id === \'L9\' ? \' l9\' : \'\')}\n'
    '                style={selectedLevel === idx ? {borderLeft: \'2px solid \' + (lvl.id === \'L9\' ? \'var(--rhetoric)\' : \'var(--lbe-green)\')} : {}}'
)
new_card_style = (
    '                className={\'chain-level-card\' + (selectedLevel === idx ? \' active\' : \'\') + (lvl.id === \'L9\' ? \' l9\' : \'\')}\n'
    '                style={Object.assign(\n'
    '                  selectedLevel === idx ? {borderLeft: \'2px solid \' + (lvl.id === \'L9\' ? \'var(--rhetoric)\' : \'var(--lbe-green)\')} : {},\n'
    '                  cascadeResults && cascadeResults[idx] ? {borderLeft: \'3px solid \' + (cascadeResults[idx].pass ? \'var(--lbe-green)\' : \'var(--error)\')} : {}\n'
    '                )}'
)
assert old_card_style in content, "chain card style not found"
content = content.replace(old_card_style, new_card_style, 1)

with open('/home/user/dc-learn-academy/DC-AI-001_v2_1_0.html', 'w') as f:
    f.write(content)

print("Fix 5 applied: PASS/FAIL badges on chain card rows")
