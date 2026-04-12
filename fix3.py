#!/usr/bin/env python3
"""Fix 3: Compact persona relevance map.
Each row: [L badge] Title — one sentence — [Rhetoric →].
Max section height 350px with overflow-y auto.
"""

with open('/home/user/dc-learn-academy/DC-AI-001_v2_1_0.html', 'r') as f:
    content = f.read()

old_map = (
    '          {activePersona && (\n'
    '            <div>\n'
    '              <div style={{fontSize:\'0.7rem\',fontWeight:600,textTransform:\'uppercase\',letterSpacing:\'0.08em\',color:\'var(--text-faint)\',marginBottom:\'0.5rem\'}}>\n'
    '                Where This Perspective Is Richest\n'
    '              </div>\n'
    '              {LEVELS.map(function(lvl,li){\n'
    '                var tw = (RHETORIC_TAKEAWAYS[lvl.id]||{})[activePersona];\n'
    '                if (!tw) return null;\n'
    '                return (\n'
    '                  <div key={li} style={{display:\'flex\',gap:\'0.75rem\',alignItems:\'flex-start\',padding:\'0.5rem 0\',borderBottom:\'1px solid var(--border)\'}}>\n'
    '                    <span style={{fontSize:\'1rem\',flexShrink:0}}>{lvl.icon}</span>\n'
    '                    <div style={{flex:1,minWidth:0}}>\n'
    '                      <div style={{fontSize:\'0.75rem\',fontWeight:600,color:\'var(--text-bright)\'}}>{lvl.id}: {lvl.title}</div>\n'
    '                      <div style={{fontSize:\'0.75rem\',color:\'var(--text-muted)\',lineHeight:\'1.5\',marginTop:\'2px\'}}>{tw}</div>\n'
    '                    </div>\n'
    '                    <button onClick={function(){setSelectedLevel(li);setActiveTab(\'learn\');}} style={{flexShrink:0,fontSize:\'0.7rem\',padding:\'2px 8px\',borderRadius:\'10px\',border:\'1px solid var(--border)\',background:\'transparent\',color:\'var(--text-dim)\',cursor:\'pointer\'}}>Learn \u2192</button>\n'
    '                  </div>\n'
    '                );\n'
    '              })}\n'
    '            </div>\n'
    '          )}'
)

new_map = (
    '          {activePersona && (\n'
    '            <div style={{maxHeight:\'350px\',overflowY:\'auto\'}}>\n'
    '              <div style={{fontSize:\'0.65rem\',fontWeight:600,textTransform:\'uppercase\',letterSpacing:\'0.08em\',color:\'var(--text-faint)\',marginBottom:\'0.4rem\'}}>\n'
    '                Where This Perspective Is Richest\n'
    '              </div>\n'
    '              {LEVELS.map(function(lvl,li){\n'
    '                var tw = (RHETORIC_TAKEAWAYS[lvl.id]||{})[activePersona];\n'
    '                if (!tw) return null;\n'
    '                var sentence = tw.split(/\\.\\s+/)[0] + \'.\';\n'
    '                return (\n'
    '                  <div key={li} style={{display:\'flex\',alignItems:\'center\',gap:\'0.4rem\',padding:\'0.25rem 0\',borderBottom:\'1px solid var(--border)\',overflow:\'hidden\'}}>\n'
    '                    <span style={{fontSize:\'0.6rem\',fontWeight:700,color:\'var(--lbe-green)\',flexShrink:0,background:\'var(--green-dim)\',borderRadius:\'3px\',padding:\'1px 4px\'}}>{lvl.id}</span>\n'
    '                    <span style={{fontSize:\'0.73rem\',fontWeight:600,color:\'var(--text-bright)\',flexShrink:0,whiteSpace:\'nowrap\'}}>{lvl.title}</span>\n'
    '                    <span style={{fontSize:\'0.71rem\',color:\'var(--text-muted)\',flex:1,overflow:\'hidden\',textOverflow:\'ellipsis\',whiteSpace:\'nowrap\'}}>— {sentence}</span>\n'
    '                    <button onClick={function(){setSelectedLevel(li);setActiveTab(\'rhetoric\');}} style={{flexShrink:0,fontSize:\'0.62rem\',padding:\'1px 5px\',borderRadius:\'8px\',border:\'1px solid var(--rhetoric)\',background:\'transparent\',color:\'var(--rhetoric)\',cursor:\'pointer\',whiteSpace:\'nowrap\'}}>Rhetoric \u2192</button>\n'
    '                  </div>\n'
    '                );\n'
    '              })}\n'
    '            </div>\n'
    '          )}'
)

assert old_map in content, "Persona relevance map not found"
content = content.replace(old_map, new_map, 1)

with open('/home/user/dc-learn-academy/DC-AI-001_v2_1_0.html', 'w') as f:
    f.write(content)

print("Fix 3 applied: compact persona relevance map")
