import re

with open("/home/user/dc-learn-academy/DC-AI-001_v3_0_0.html", encoding='utf-8') as f:
    h = f.read()

errors = []
warnings = []

def check(cond, label, note=""):
    if cond:
        print(f"  PASS  {label}")
    else:
        print(f"  FAIL  {label}" + (f" — {note}" if note else ""))
        errors.append(label)

# ── Identity ─────────────────────────────────────────────────────────────────
check('const TOOL_ID = "DC-AI-001";' in h,       'TOOL_ID = DC-AI-001')
check('const TOOL_VERSION = "3.0.0";' in h,       'TOOL_VERSION = 3.0.0')
check('v3.0.0' in h,                               'v3.0.0 in file')
check('Data Centre Power Density' in h,            'hero title: Power Density')
check('Module 1 of 8' in h,                        'series: Module 1 of 8')
check('DC-AI Series' in h,                         'series label: DC-AI Series')
# DC-LEARN-002 should not appear in identity/template code, only allowed in content data
dc002_in_code = [l.strip() for l in h.split('\n') if 'DC-LEARN-002' in l and '"DC-LEARN-002' not in l and "'DC-LEARN-002" not in l]
check(len(dc002_in_code) == 0,                     f'no DC-LEARN-002 in code/identity (found {len(dc002_in_code)}: {dc002_in_code[:1]})')
check('5.13.7' not in h,                           'no v5.13.7 remains')
check('dc002_' not in h,                           'no dc002_ storage keys remain')

# ── Personas ──────────────────────────────────────────────────────────────────
for name in ['conor', 'helena', 'eoin', 'rachel', 'padraig']:
    check(f'"{name}"' in h or f"'{name}'" in h,   f'persona key: {name}')
for old in ['declan', '"ann"', '"mark"', '"sarah"', '"tom"']:
    check(old not in h,                            f'no old persona key: {old}')

# ── Data counts ──────────────────────────────────────────────────────────────
aq_count = len(re.findall(r'"q"\s*:', h))
check(aq_count == 27,                              f'27 assessment questions (found {aq_count})')

# Count LEVELS entries
lm = re.findall(r'"level"\s*:\s*(\d+)', h)
levels_in_levels = [x for x in lm if 1 <= int(x) <= 9]
check(len(set(levels_in_levels)) == 9,             f'9 unique levels (found {len(set(levels_in_levels))})')

# 5 grammar facts per level (45 total)
facts = re.findall(r'"text"\s*:\s*"[^"]{10}', h)
# Better: count grammar.facts arrays
fact_pat = len(re.findall(r'"facts"\s*:\s*\[', h))
check(fact_pat >= 9,                               f'>= 9 facts arrays (found {fact_pat})')

# Glossary — count term entries
# Glossary: count "term": entries within the GLOSSARY_002 block
m_g1 = re.search(r'const GLOSSARY_002\s*=', h)
m_g2 = re.search(r'const BIBLIOGRAPHY_002\s*=', h)
gloss_block = h[m_g1.start():m_g2.start()] if (m_g1 and m_g2) else ''
gloss = len(re.findall(r'"term"\s*:', gloss_block))
check(gloss == 40,                                 f'40 glossary terms (found {gloss})')

# Bibliography: count "title": entries within the BIBLIOGRAPHY_002 block
bib_start = h.find('const BIBLIOGRAPHY_002')
bib_end   = h.find('const SO_WHAT_MAP', bib_start)
bib_block = h[bib_start:bib_end] if bib_end > bib_start else ''
bib = len(re.findall(r'"title"\s*:', bib_block))
check(bib >= 16,                                   f'>= 16 bibliography sources (found {bib})')

# ── Feature checks ────────────────────────────────────────────────────────────
check('function SidebarCalculator' in h,           'SidebarCalculator component present')
check('function SidebarFacility' in h,             'SidebarFacility component present')
check('cascadeResults' in h,                       'cascadeResults state present')
check('onCascadeResult' in h,                      'onCascadeResult handler present')
check('<SidebarCalculator' in h,                   'SidebarCalculator in render')
check('<SidebarFacility' in h,                     'SidebarFacility in render')
check('cascadeResults={cascadeResults}' in h,      'cascadeResults passed to ChainTab')

# ── cascadeCheck functions in LEVELS ─────────────────────────────────────────
cc_count = len(re.findall(r'"cascadeCheck"\s*:', h))
check(cc_count == 9,                               f'9 cascadeCheck functions (found {cc_count})')

# ── SO_WHAT_MAP and RHETORIC_TAKEAWAYS ───────────────────────────────────────
check('const SO_WHAT_MAP' in h,                    'SO_WHAT_MAP declared')
check('const RHETORIC_TAKEAWAYS' in h,             'RHETORIC_TAKEAWAYS declared')

# ── CSS intact (spot-check key rules) ────────────────────────────────────────
check('--bg:#0d1117' in h,                         'CSS variable --bg preserved')
check('.persona-btn' in h,                         '.persona-btn CSS preserved')
check('.sidebar-card' in h,                        '.sidebar-card CSS preserved')

# ── Footer copyright ──────────────────────────────────────────────────────────
check('© 2026 Legacy Business Engineers Ltd' in h, 'footer copyright intact')

# ── CDN check (no jsdelivr in script src, only cdnjs) ────────────────────────
cdn_scripts = re.findall(r'<script src="([^"]+)"', h)
bad_cdns = [u for u in cdn_scripts if 'jsdelivr' in u and 'supabase' not in u]
check(len(bad_cdns) == 0,                          f'CDN: only cdnjs (bad non-supabase jsdelivr: {bad_cdns})')

print(f"\n{'='*50}")
print(f"Result: {len(errors)} failures")
if errors:
    print("FAILURES:")
    for e in errors: print(f"  - {e}")
else:
    print("ALL CHECKS PASSED")
