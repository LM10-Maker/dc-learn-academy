#!/usr/bin/env python3
"""Fix 2: Tighten spacing.
Chain card padding: 0.6rem 0.8rem.
Grammar fact gap: 0.4rem.
Section gaps: 0.75rem (card margin-bottom).
Card border-radius: 8px.
Remove excessive margins between inner elements (card-header margin-bottom).
"""

with open('/home/user/dc-learn-academy/DC-AI-001_v2_1_0.html', 'r') as f:
    content = f.read()

changes = [
    # Chain card padding
    ('      padding: 0.75rem 1rem;\n      cursor: default;',
     '      padding: 0.6rem 0.8rem;\n      cursor: default;'),

    # Grammar fact gap
    ('    .fact-grid { display: grid; gap: 1rem; }',
     '    .fact-grid { display: grid; gap: 0.4rem; }'),

    # Card margin-bottom (section gaps → 0.75rem)
    ('      margin-bottom: 1.25rem;\n      box-shadow: var(--shadow);',
     '      margin-bottom: 0.75rem;\n      box-shadow: var(--shadow);'),

    # radius-md: 10px → 8px
    ('      --radius-md: 10px;',
     '      --radius-md: 8px;'),

    # radius-lg: 12px → 8px
    ('      --radius-lg: 12px;',
     '      --radius-lg: 8px;'),

    # card-header margin-bottom: 1rem → 0.75rem
    ('      margin-bottom: 1rem;\n      padding-bottom: 0.75rem;\n      border-bottom: 1px solid var(--border);',
     '      margin-bottom: 0.75rem;\n      padding-bottom: 0.6rem;\n      border-bottom: 1px solid var(--border);'),
]

for old, new in changes:
    if old in content:
        content = content.replace(old, new, 1)
        print(f"  replaced: {old[:60].strip()!r}")
    else:
        print(f"  WARN – not found: {old[:60].strip()!r}")

with open('/home/user/dc-learn-academy/DC-AI-001_v2_1_0.html', 'w') as f:
    f.write(content)

print("Fix 2 applied: spacing tightened")
