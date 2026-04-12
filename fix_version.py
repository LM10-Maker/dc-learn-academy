#!/usr/bin/env python3
"""Final: Version bump to 2.1.0. Verify 27 questions, 45 facts."""

with open('/home/user/dc-learn-academy/DC-AI-001_v2_1_0.html', 'r') as f:
    content = f.read()

replacements = [
    ('DC-AI-001: Power Density | DC-AI v2.0.0',
     'DC-AI-001: Power Density | DC-AI v2.1.0'),
    ("var TOOL_VERSION = \"2.0.0\";",
     'var TOOL_VERSION = "2.1.0";'),
    ('"version": "2.0.0",',
     '"version": "2.1.0",'),
    ("['Version', '2.0.0'],",
     "['Version', '2.1.0'],"),
    ("Module 1 of 8 · DC-AI v2.0.0",
     "Module 1 of 8 · DC-AI v2.1.0"),
]

for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        print("  bumped: " + repr(old)[:60])
    else:
        print("  WARN not found: " + repr(old)[:60])

# Verify question and fact counts
import re

# Count assessment questions (objects with "q": field in ASSESSMENT_QUESTIONS)
q_matches = re.findall(r'"q"\s*:', content)
print(f"\n  Assessment questions found: {len(q_matches)}")
assert len(q_matches) == 27, f"Expected 27 questions, got {len(q_matches)}"

# Count grammar facts — only "term" fields inside "facts" arrays
facts_blocks = re.findall(r'"facts"\s*:\s*\[([^\]]*(?:\[[^\]]*\])*[^\]]*)\]', content, re.DOTALL)
total_facts = sum(len(re.findall(r'"term"\s*:', blk)) for blk in facts_blocks)
print(f"  Grammar fact terms found: {total_facts}")
assert total_facts == 45, f"Expected 45 facts, got {total_facts}"

with open('/home/user/dc-learn-academy/DC-AI-001_v2_1_0.html', 'w') as f:
    f.write(content)

print("\nVersion bumped to 2.1.0. Verification passed.")
