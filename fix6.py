#!/usr/bin/env python3
"""Fix 6: Remove empty card-icon divs.
Delete <div className="card-icon ..."></div> elements with no content.
"""
import re

with open('/home/user/dc-learn-academy/DC-AI-001_v2_1_0.html', 'r') as f:
    content = f.read()

# Match empty card-icon divs (may have only whitespace inside)
# Pattern: <div className="card-icon WORD"></div> on its own line, possibly indented
pattern = re.compile(
    r'[ \t]*<div className="card-icon [a-z]+">\s*</div>\n',
)

matches = pattern.findall(content)
print(f"  Found {len(matches)} empty card-icon divs to remove")
for m in matches:
    print(f"    {m.rstrip()!r}")

content = pattern.sub('', content)

with open('/home/user/dc-learn-academy/DC-AI-001_v2_1_0.html', 'w') as f:
    f.write(content)

print("Fix 6 applied: empty card-icon divs removed")
