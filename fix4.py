#!/usr/bin/env python3
"""Fix 4: Shrink cross-ref pills to 0.65rem, --text-muted, --panel bg.
Max 30 chars per pill. No module IDs — short labels only.
"""
import re

with open('/home/user/dc-learn-academy/DC-AI-001_v2_1_0.html', 'r') as f:
    content = f.read()

# 1. CSS: update .crossref-tag and .chain-crossref-tag
old_crossref_tag = (
    '    .crossref-tag {\n'
    '      font-size: 0.7rem;\n'
    '      background: var(--tag-bg);\n'
    '      color: var(--tag-text);\n'
    '      border-radius: 4px;\n'
    '      padding: 3px 9px;\n'
    '      border: 1px solid transparent;\n'
    '    }'
)
new_crossref_tag = (
    '    .crossref-tag {\n'
    '      font-size: 0.65rem;\n'
    '      background: var(--panel);\n'
    '      color: var(--text-muted);\n'
    '      border-radius: 4px;\n'
    '      padding: 2px 7px;\n'
    '      border: 1px solid var(--border);\n'
    '    }'
)
assert old_crossref_tag in content, ".crossref-tag CSS not found"
content = content.replace(old_crossref_tag, new_crossref_tag, 1)

old_chain_tag = (
    '    .chain-crossref-tag {\n'
    '      font-size: 0.66rem;\n'
    '      background: var(--tag-bg);\n'
    '      color: var(--tag-text);\n'
    '      border-radius: 4px;\n'
    '      padding: 2px 7px;\n'
    '    }'
)
new_chain_tag = (
    '    .chain-crossref-tag {\n'
    '      font-size: 0.65rem;\n'
    '      background: var(--panel);\n'
    '      color: var(--text-muted);\n'
    '      border-radius: 4px;\n'
    '      padding: 2px 7px;\n'
    '      border: 1px solid var(--border);\n'
    '    }'
)
assert old_chain_tag in content, ".chain-crossref-tag CSS not found"
content = content.replace(old_chain_tag, new_chain_tag, 1)

# 2. Add shortRef helper after splitFixSteps function
old_helper_anchor = 'function splitFixSteps(fixText) {'
assert old_helper_anchor in content, "splitFixSteps not found"
short_ref_fn = (
    'function shortRef(ref) {\n'
    '  var m = ref.match(/\\(([^)]+)\\)/);\n'
    '  var label = m ? m[1] : ref.replace(/^[A-Z][A-Z0-9-]+\\s+L\\d+\\s*/, \'\');\n'
    '  return label.length > 30 ? label.substring(0, 27) + \'...\' : label;\n'
    '}\n'
    '\n'
)
content = content.replace(old_helper_anchor, short_ref_fn + old_helper_anchor, 1)

# 3. Apply shortRef to chain crossref tags (ChainTab expanded section)
old_chain_ref_render = (
    '                        {lvl.crossRefs.map(function(ref, ri) {\n'
    '                          return <span key={ri} className="chain-crossref-tag">{ref}</span>;\n'
    '                        })}'
)
new_chain_ref_render = (
    '                        {lvl.crossRefs.map(function(ref, ri) {\n'
    '                          return <span key={ri} className="chain-crossref-tag">{shortRef(ref)}</span>;\n'
    '                        })}'
)
assert old_chain_ref_render in content, "chain crossref render not found"
content = content.replace(old_chain_ref_render, new_chain_ref_render, 1)

# 4. Apply shortRef to level detail crossrefs (second card in ChainTab)
old_level_ref_render = (
    '            {(level.crossRefs || []).map(function(ref, ri) {\n'
    '              return <span key={ri} className="crossref-tag">{ref}</span>;\n'
    '            })}'
)
new_level_ref_render = (
    '            {(level.crossRefs || []).map(function(ref, ri) {\n'
    '              return <span key={ri} className="crossref-tag">{shortRef(ref)}</span>;\n'
    '            })}'
)
count = content.count(old_level_ref_render)
assert count >= 1, f"level crossref render not found (count={count})"
content = content.replace(old_level_ref_render, new_level_ref_render)

# 5. Apply shortRef to FieldChallengeTab crossrefs
old_field_ref_render = (
    '          {(level.crossRefs || []).map(function(ref, ri) {\n'
    '            return <span key={ri} className="crossref-tag">{ref}</span>;\n'
    '          })}'
)
new_field_ref_render = (
    '          {(level.crossRefs || []).map(function(ref, ri) {\n'
    '            return <span key={ri} className="crossref-tag">{shortRef(ref)}</span>;\n'
    '          })}'
)
count = content.count(old_field_ref_render)
assert count >= 1, f"field crossref render not found (count={count})"
content = content.replace(old_field_ref_render, new_field_ref_render)

with open('/home/user/dc-learn-academy/DC-AI-001_v2_1_0.html', 'w') as f:
    f.write(content)

print("Fix 4 applied: cross-ref pills shrunk, short labels only")
