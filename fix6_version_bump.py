#!/usr/bin/env python3
"""Fix 6: Bump version to 2.4.0 in all locations and save as DC-AI-001_v2_4_0.html.
Verify: 27 questions, 45 facts, 9 levels."""
import re

src = '/home/user/dc-learn-academy/DC-AI-001_v2_3_0 (3).html'
dst = '/home/user/dc-learn-academy/DC-AI-001_v2_4_0.html'

with open(src, 'r', encoding='utf-8') as f:
    html = f.read()

count_230 = html.count('2.3.0')
print(f"Found {count_230} occurrences of '2.3.0'")

# Bump all version strings
html = html.replace('2.3.0', '2.4.0')
html = html.replace('v2_3_0', 'v2_4_0')

remaining = html.count('2.3.0')
assert remaining == 0, f"Still {remaining} occurrences of '2.3.0'"

# Verify 9 levels
level_values = set(re.findall(r'"level":\s*(\d+)', html))
print(f"Level values found: {sorted(level_values)} (expect 1-9)")
assert level_values == {'1','2','3','4','5','6','7','8','9'}, f"Unexpected levels: {level_values}"

# Verify 27 questions
q_k = html.count('"tier": "knowledge"')
q_c = html.count('"tier": "calculation"')
q_j = html.count('"tier": "judgement"')
total_q = q_k + q_c + q_j
print(f"Questions: knowledge={q_k}, calculation={q_c}, judgement={q_j}, total={total_q}")
assert total_q == 27, f"Expected 27 questions, found {total_q}"

# Verify 45 facts (5 per level across 9 levels)
facts_arrays = re.findall(r'"facts":\s*\[([^]]*(?:\{[^}]*\}[^]]*)*)\]', html, re.DOTALL)
total_facts = sum(len(re.findall(r'"term":\s*"[^"]+"', fa)) for fa in facts_arrays)
print(f"Grammar facts: {total_facts} (expect 45)")
assert total_facts == 45, f"Expected 45 facts, found {total_facts}"

# Save
with open(dst, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Fix 6 applied: Version bumped 2.3.0→2.4.0 ({count_230} locations), saved as DC-AI-001_v2_4_0.html")
print("Verified: 27 questions ✓  45 facts ✓  9 levels ✓")
