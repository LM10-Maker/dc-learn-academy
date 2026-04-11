#!/usr/bin/env python3
"""
build_03_section_bc.py
Section B: Logo constant in a plain <script> tag (before Babel).
Section C: All data constants (LEVELS, SO_WHAT_MAP, etc.) in a plain <script> tag.
Output: section_bc.html
"""

import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))

# ─── Load parsed data ─────────────────────────────────────────────────────────
with open(os.path.join(BASE, 'logo.txt'), 'r', encoding='utf-8') as f:
    logo_b64 = f.read().strip()

with open(os.path.join(BASE, 'meta.json'), 'r', encoding='utf-8') as f:
    meta = json.load(f)

with open(os.path.join(BASE, 'levels.json'), 'r', encoding='utf-8') as f:
    levels = json.load(f)

with open(os.path.join(BASE, 'assessment.json'), 'r', encoding='utf-8') as f:
    assessment = json.load(f)

with open(os.path.join(BASE, 'companions.json'), 'r', encoding='utf-8') as f:
    companions = json.load(f)

so_what_map       = companions['so_what_map']
rhetoric_tak      = companions['rhetoric_takeaways']
glossary          = companions['glossary']
bibliography      = companions['bibliography']
questions         = assessment['questions']

# ─── Section B: Logo script (plain, before Babel) ─────────────────────────────
section_b = '<script>\n'
section_b += 'var LOGO_SRC = "' + logo_b64 + '";\n'
section_b += '</script>\n'

# ─── Section C: Data constants ────────────────────────────────────────────────
opts = dict(ensure_ascii=False, indent=2)
section_c  = '<script>\n'
section_c += 'var TOOL_VERSION = "1.0.0";\n'
section_c += 'var MODULE_META = ' + json.dumps(meta, **opts) + ';\n'
section_c += 'var LEVELS = ' + json.dumps(levels, **opts) + ';\n'
section_c += 'var SO_WHAT_MAP = ' + json.dumps(so_what_map, **opts) + ';\n'
section_c += 'var RHETORIC_TAKEAWAYS = ' + json.dumps(rhetoric_tak, **opts) + ';\n'
section_c += 'var ASSESSMENT_QUESTIONS = ' + json.dumps(questions, **opts) + ';\n'
section_c += 'var GLOSSARY = ' + json.dumps(glossary, **opts) + ';\n'
section_c += 'var BIBLIOGRAPHY = ' + json.dumps(bibliography, **opts) + ';\n'
section_c += '</script>\n'

out = section_b + section_c

out_path = os.path.join(BASE, 'section_bc.html')
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(out)

lines = out.count('\n') + 1
print(f'Written {out_path} ({lines} lines)')

# Verification counts
import re
print(f'  LEVELS entries: {len(levels)}')
print(f'  Questions:      {len(questions)}')
print(f'  so_what_map:    {len(so_what_map)}')
print(f'  Glossary:       {len(glossary)}')
print(f'  Bibliography:   {len(bibliography)}')
print(f'  Logo chars:     {len(logo_b64)}')
print('build_03_section_bc.py COMPLETE')
