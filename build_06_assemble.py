#!/usr/bin/env python3
"""
build_06_assemble.py
Assembles all section files into DC-AI-001_v1_0_0.html.
Runs verification checks.
"""

import os
import re
import json

BASE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(BASE, 'DC-AI-001_v1_0_0.html')

# ─── 1. Read section files ────────────────────────────────────────────────────
sections = ['section_a.html', 'section_bc.html', 'section_d1.html', 'section_d2.html']
parts = []
for s in sections:
    p = os.path.join(BASE, s)
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()
    parts.append(content)
    print(f'  {s}: {len(content.splitlines()):>5} lines, {len(content):>8} chars')

full_html = ''.join(parts)

# ─── 2. Write output ──────────────────────────────────────────────────────────
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(full_html)
print(f'\nWritten: {OUT}')

# ─── 3. Verification ──────────────────────────────────────────────────────────
lines      = full_html.count('\n') + 1
chars      = len(full_html)
kb         = chars / 1024

print(f'\n=== VERIFICATION ===')
print(f'Line count:     {lines:,} (target 3,000–5,000)')
print(f'File size:      {kb:.1f} KB (target 400–800 KB)')

# Count key markers
def count_re(pattern, text):
    return len(re.findall(pattern, text))

# Fact terms — JSON key "term" appears 45 times in LEVELS data + glossary
term_count = count_re(r'"term"\s*:', full_html)
# Questions — "q" key
q_count = count_re(r'"q"\s*:', full_html)
# asset_management persona entries in LEVELS
am_count = count_re(r'asset_management', full_html)

print(f'"term" keys:    {term_count} (want >= 45+glossary)')
print(f'"q" keys:       {q_count} (want 27)')
print(f'asset_management refs: {am_count} (want >= 18)')

# Level count check
levels_check = count_re(r'"level"\s*:\s*\d', full_html)
print(f'"level" keys:   {levels_check} (want >= 9+27 from levels+questions)')

# Check all 9 level ids present
for i in range(1, 10):
    lid = f'"L{i}"'
    if lid in full_html:
        print(f'  ✓ L{i} present')
    else:
        print(f'  ✗ L{i} MISSING')

# Check React/Babel CDN
if 'cdnjs.cloudflare.com' in full_html and 'babel' in full_html.lower():
    print('CDN: ✓ cdnjs.cloudflare.com + Babel')
else:
    print('CDN: ✗ CHECK CDN LINKS')

# Check no unpkg
if 'unpkg.com' in full_html:
    print('WARNING: unpkg.com found — should use cdnjs only')
else:
    print('CDN: ✓ No unpkg references')

# Check logo
if 'LOGO_SRC' in full_html and 'data:image' in full_html:
    print('Logo: ✓ base64 logo present')
else:
    print('Logo: ✗ logo missing or wrong format')

# Check personas
for persona in ['asset_management', 'technology', 'technical', 'compliance', 'cost']:
    if persona in full_html:
        print(f'Persona {persona}: ✓')
    else:
        print(f'Persona {persona}: ✗ MISSING')

# Line count warning
if lines < 3000:
    print(f'\nWARNING: Only {lines} lines — target is 3,000+')
elif lines > 5000:
    print(f'\nNOTE: {lines} lines — above 5,000 target but content justified by DNA size')
else:
    print(f'\nLine count PASS: {lines} lines within 3,000–5,000 target')

# Size check
if kb < 400:
    print(f'WARNING: {kb:.1f} KB — target is 400+ KB (data JSON drives most of the size)')
elif kb > 800:
    print(f'NOTE: {kb:.1f} KB — above 800 KB target (logo base64 adds size)')
else:
    print(f'Size PASS: {kb:.1f} KB')

# Copy to outputs if it exists
outputs_dir = '/mnt/user-data/outputs'
if os.path.isdir(outputs_dir):
    import shutil
    dest = os.path.join(outputs_dir, 'DC-AI-001_v1_0_0.html')
    shutil.copy2(OUT, dest)
    print(f'\nCopied to {dest}')
else:
    print(f'\nOutputs dir not found at {outputs_dir} — file is in repo root')

print('\nbuild_06_assemble.py COMPLETE')
print(f'Output: {OUT}')
