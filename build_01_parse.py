#!/usr/bin/env python3
"""
build_01_parse.py
Phase 1: Parse DNA_DC_AI_001_v1_0.md (YAML) into JSON files.
Also extracts the base64 logo string from LBE_LOGO_CONST.md.
Outputs: levels.json, assessment.json, companions.json, meta.json, logo.txt
"""

import yaml
import json
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))

# ─── 1. Read and parse the DNA YAML file ──────────────────────────────────────
dna_path = os.path.join(BASE, 'DNA_DC_AI_001_v1_0.md')
print(f'Reading {dna_path} ...')
with open(dna_path, 'r', encoding='utf-8') as f:
    raw = f.read()

# Strip leading YAML comment lines that start with #
# (yaml.safe_load handles them natively, but strip the # file header)
dna = yaml.safe_load(raw)
print('YAML parsed OK')

# ─── 2. Extract top-level sections ────────────────────────────────────────────
meta             = dna.get('meta', {})
levels           = dna.get('levels', [])
assessment_block = dna.get('assessment', {})
so_what_map      = dna.get('so_what_map', {})
rhetoric_tak     = dna.get('rhetoric_takeaways', {})
glossary         = dna.get('glossary', [])
bibliography     = dna.get('bibliography', [])

print(f'Levels:      {len(levels)}')
print(f'Questions:   {len(assessment_block.get("questions", []))}')
print(f'so_what_map: {len(so_what_map)}')
print(f'Glossary:    {len(glossary)}')
print(f'Bibliography:{len(bibliography)}')

# ─── 3. Validate counts ───────────────────────────────────────────────────────
assert len(levels) == 9, f'Expected 9 levels, got {len(levels)}'
assert len(assessment_block.get('questions', [])) >= 27, 'Expected >= 27 questions'
assert len(so_what_map) >= 40, f'Expected >= 40 so_what entries, got {len(so_what_map)}'

# ─── 4. Write JSON files ──────────────────────────────────────────────────────
def jdump(obj, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    print(f'Written {path}')

jdump(levels, os.path.join(BASE, 'levels.json'))
jdump(assessment_block, os.path.join(BASE, 'assessment.json'))
jdump({'so_what_map': so_what_map, 'rhetoric_takeaways': rhetoric_tak,
       'glossary': glossary, 'bibliography': bibliography},
      os.path.join(BASE, 'companions.json'))
jdump(meta, os.path.join(BASE, 'meta.json'))

# ─── 5. Extract logo from LBE_LOGO_CONST.md ───────────────────────────────────
logo_path = os.path.join(BASE, 'LBE_LOGO_CONST.md')
print(f'Reading logo from {logo_path} ...')
with open(logo_path, 'r', encoding='utf-8') as f:
    logo_raw = f.read()

# Try various formats the logo file might use
logo_b64 = None

# Format 1: data URI on its own line
m = re.search(r'(data:image/[^;]+;base64,[A-Za-z0-9+/=\s]+)', logo_raw)
if m:
    logo_b64 = m.group(1).replace('\n', '').replace('\r', '').strip()

# Format 2: const LOGO_SRC = "...";
if not logo_b64:
    m = re.search(r'LOGO_SRC\s*=\s*["\']([^"\']+)["\']', logo_raw)
    if m:
        logo_b64 = m.group(1).strip()

# Format 3: just the raw base64 string (after stripping markdown)
if not logo_b64:
    # Strip markdown comment lines and grab remaining content
    lines = [l.strip() for l in logo_raw.splitlines() if l.strip() and not l.startswith('#')]
    candidate = ''.join(lines)
    if len(candidate) > 100:
        # Could be a raw base64 blob — wrap it
        if not candidate.startswith('data:'):
            candidate = 'data:image/svg+xml;base64,' + candidate
        logo_b64 = candidate

if logo_b64:
    logo_out = os.path.join(BASE, 'logo.txt')
    with open(logo_out, 'w', encoding='utf-8') as f:
        f.write(logo_b64)
    print(f'Logo extracted: {len(logo_b64)} chars -> {logo_out}')
else:
    print('WARNING: could not extract logo — will use fallback SVG')
    fallback = 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMjAgNDAiPjx0ZXh0IHk9IjI4IiBmb250LXNpemU9IjE4IiBmb250LXdlaWdodD0iNzAwIiBmb250LWZhbWlseT0iSUJNIFBsZXggU2Fucyx6YWRhbnMtc2VyaWYiIGZpbGw9IiNmZmZmZmYiPkxCRTwvdGV4dD48L3N2Zz4='
    logo_out = os.path.join(BASE, 'logo.txt')
    with open(logo_out, 'w', encoding='utf-8') as f:
        f.write(fallback)

print('\nbuild_01_parse.py COMPLETE')
