#!/usr/bin/env python3
"""Fix 8: Remove card-icon divs from sidebar titles. Just bold text.
Removes the non-empty card-icon amber div (contains {level.icon})
from the ChainTab "Currently Selected" card header.
"""

with open('/home/user/dc-learn-academy/DC-AI-001_v2_1_0.html', 'r') as f:
    content = f.read()

# Remove the card-icon amber div that carries level.icon in ChainTab
old_icon = (
    '          <div className="card-icon amber">{level.icon}</div>\n'
)
assert old_icon in content, "card-icon amber not found"
content = content.replace(old_icon, '', 1)

# Also ensure sidebar-card-title is styled bold in CSS (already is,
# but add font-weight: 700 explicitly to make it stand out)
old_sidebar_title_css = (
    '    .sidebar-card-title {\n'
    '      font-size: 0.8rem;\n'
    '      font-weight: 600;\n'
    '      color: var(--text-bright);\n'
    '      margin-bottom: 0.6rem;\n'
    '      padding-bottom: 0.4rem;\n'
    '      border-bottom: 1px solid var(--border);\n'
    '    }'
)
new_sidebar_title_css = (
    '    .sidebar-card-title {\n'
    '      font-size: 0.8rem;\n'
    '      font-weight: 700;\n'
    '      color: var(--text-bright);\n'
    '      margin-bottom: 0.6rem;\n'
    '      padding-bottom: 0.4rem;\n'
    '      border-bottom: 1px solid var(--border);\n'
    '    }'
)
assert old_sidebar_title_css in content, "sidebar-card-title CSS not found"
content = content.replace(old_sidebar_title_css, new_sidebar_title_css, 1)

with open('/home/user/dc-learn-academy/DC-AI-001_v2_1_0.html', 'w') as f:
    f.write(content)

print("Fix 8 applied: card-icon removed from sidebar titles, bold text")
