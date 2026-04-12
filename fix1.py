#!/usr/bin/env python3
"""Fix 1: Collapse grammar facts by default.
Each fact shows only the term name as a clickable row.
Click expands to show definition, plain English, numbers, soWhat.
Same expand/collapse pattern as chain cards (state toggle, ▼/▲ chevron).
"""

with open('/home/user/dc-learn-academy/DC-AI-001_v2_1_0.html', 'r') as f:
    content = f.read()

# 1. Add expandedFacts state to GrammarTab
old_state = ('  var [expandedEnglish, setExpandedEnglish] = React.useState({});\n'
             '\n'
             '  return (\n'
             '    <div>\n'
             '      {/* Retrofit relevance */}')
new_state = ('  var [expandedEnglish, setExpandedEnglish] = React.useState({});\n'
             '  var [expandedFacts, setExpandedFacts] = React.useState({});\n'
             '\n'
             '  return (\n'
             '    <div>\n'
             '      {/* Retrofit relevance */}')
assert old_state in content, "State declaration not found"
content = content.replace(old_state, new_state, 1)

# 2. Replace fact card body — collapsed by default, expand on click
old_card = (
    '            return (\n'
    '              <div key={fi} className="fact-card">\n'
    '                <div className="fact-term">{fact.term}</div>\n'
    '                <div className="fact-standard">{fact.standard}</div>\n'
    '                <div style={{fontSize:\'0.83rem\', color:\'var(--text-muted)\', lineHeight:\'1.6\', marginBottom:\'0.6rem\'}}>\n'
    '                  <strong style={{color:\'var(--text)\', fontSize:\'0.72rem\', textTransform:\'uppercase\', letterSpacing:\'0.06em\'}}>Definition · </strong>\n'
    '                  {fact.definition}\n'
    '                </div>\n'
    '                <div className="fact-row">\n'
    '                  <div className="fact-field">\n'
    '                    <span className="fact-field-label">By the Numbers</span>\n'
    '                    <div className="fact-number-pill">{fact.number}</div>\n'
    '                  </div>\n'
    '                </div>\n'
    '                {fact.plain && (\n'
    '                  <>\n'
    '                    <button className="clarify-btn" onClick={function(){ setExpandedEnglish(function(p){ var n=Object.assign({},p); n[fi]=!p[fi]; return n; }); }}>\n'
    '                      Clarify {clarifyOpen ? \'▲\' : \'▼\'}\n'
    '                    </button>\n'
    '                    {clarifyOpen && <div className="clarify-box">{fact.plain}</div>}\n'
    '                  </>\n'
    '                )}\n'
    '                <div className="so-what-box">\n'
    '                  <strong>So what? </strong>{soWhat || fact.soWhat}\n'
    '                </div>\n'
    '              </div>\n'
    '            );'
)
new_card = (
    '            var factOpen = !!(expandedFacts && expandedFacts[fi]);\n'
    '            return (\n'
    '              <div key={fi} className="fact-card">\n'
    '                <div\n'
    '                  style={{display:\'flex\',alignItems:\'center\',justifyContent:\'space-between\',cursor:\'pointer\',gap:\'0.5rem\'}}\n'
    '                  onClick={function(){ setExpandedFacts(function(p){ var n=Object.assign({},p); n[fi]=!p[fi]; return n; }); }}\n'
    '                >\n'
    '                  <div className="fact-term" style={{marginBottom:0}}>{fact.term}</div>\n'
    '                  <div style={{fontSize:\'0.75rem\',color:\'var(--text-muted)\',flexShrink:0}}>{factOpen ? \'▲\' : \'▼\'}</div>\n'
    '                </div>\n'
    '                {factOpen && (\n'
    '                  <div style={{marginTop:\'0.6rem\',paddingTop:\'0.6rem\',borderTop:\'1px solid var(--border)\'}}>\n'
    '                    <div className="fact-standard">{fact.standard}</div>\n'
    '                    <div style={{fontSize:\'0.83rem\', color:\'var(--text-muted)\', lineHeight:\'1.6\', marginBottom:\'0.6rem\'}}>\n'
    '                      <strong style={{color:\'var(--text)\', fontSize:\'0.72rem\', textTransform:\'uppercase\', letterSpacing:\'0.06em\'}}>Definition · </strong>\n'
    '                      {fact.definition}\n'
    '                    </div>\n'
    '                    <div className="fact-row">\n'
    '                      <div className="fact-field">\n'
    '                        <span className="fact-field-label">By the Numbers</span>\n'
    '                        <div className="fact-number-pill">{fact.number}</div>\n'
    '                      </div>\n'
    '                    </div>\n'
    '                    {fact.plain && (\n'
    '                      <>\n'
    '                        <button className="clarify-btn" onClick={function(e){ e.stopPropagation(); setExpandedEnglish(function(p){ var n=Object.assign({},p); n[fi]=!p[fi]; return n; }); }}>\n'
    '                          Clarify {clarifyOpen ? \'▲\' : \'▼\'}\n'
    '                        </button>\n'
    '                        {clarifyOpen && <div className="clarify-box">{fact.plain}</div>}\n'
    '                      </>\n'
    '                    )}\n'
    '                    <div className="so-what-box">\n'
    '                      <strong>So what? </strong>{soWhat || fact.soWhat}\n'
    '                    </div>\n'
    '                  </div>\n'
    '                )}\n'
    '              </div>\n'
    '            );'
)
assert old_card in content, "Fact card body not found"
content = content.replace(old_card, new_card, 1)

with open('/home/user/dc-learn-academy/DC-AI-001_v2_1_0.html', 'w') as f:
    f.write(content)

print("Fix 1 applied: grammar facts collapse by default")
