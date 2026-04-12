#!/usr/bin/env python3
"""
polish_06_verify.py
1. Idempotent version bump 1.0.0 -> 1.1.0 across all 4 reference points
2. Verify all 12 spec items are present in the output
3. Verify content integrity (no data changed)
4. Report pass/fail
Reads/writes DC-AI-001_v1_1_0.html in place.
"""

TARGET = '/home/user/dc-learn-academy/DC-AI-001_v1_1_0.html'

with open(TARGET, 'r', encoding='utf-8') as f:
    html = f.read()

bumped = []
errors = []

def ensure(old, new, tag):
    """Idempotent replace: apply only if new not already present."""
    global html
    if new in html:
        bumped.append(f'{tag} [already correct]')
        return
    if old not in html:
        errors.append(f'VERSION MISS [{tag}]')
        return
    html = html.replace(old, new, 1)
    bumped.append(tag)

def chk(needle, label):
    if needle not in html:
        errors.append(f'MISS [{label}]')
    else:
        print(f"  \u2713 {label}")

# ==============================================================================
# 1. Version bump — 4 reference points (idempotent)
# ==============================================================================
ensure('DC-AI-001: Power Density | DC-AI v1.1</title>',
       'DC-AI-001: Power Density | DC-AI v1.1.0</title>',
       'title tag')
ensure('var TOOL_VERSION = "1.0.0"',
       'var TOOL_VERSION = "1.1.0"',
       'TOOL_VERSION constant')
ensure('Module 1 of 8 \u00b7 DC-AI v1.1</span>',
       'Module 1 of 8 \u00b7 DC-AI v1.1.0</span>',
       'series badge')
ensure('"version": "1.0.0"',
       '"version": "1.1.0"',
       'JSON version field')

print(f"Version reference points ({len(bumped)}/4):")
for b in bumped:
    print(f"  \u2713 {b}")

# ==============================================================================
# 2. Spec item verification
# ==============================================================================
print("\n--- Spec Item Verification ---")

# Spec 1: CSS variables
chk('--grammar:       #2563EB',         'spec 1: --grammar hex')
chk('--logic:         #d97706',         'spec 1: --logic hex')
chk('--rhetoric:      #7c3aed',         'spec 1: --rhetoric hex')
chk('--text-bright:',                   'spec 1: --text-bright present')
chk('--text-dim:',                      'spec 1: --text-dim present')
chk('--panel:',                         'spec 1: --panel depth tier')
chk('[data-theme="light"]',             'spec 1: light theme block')

# Spec 2: Level selector
chk('width: 80px;',                     'spec 2: btn 80px wide')
chk('height: 72px;',                    'spec 2: btn 72px tall')
chk('gap: 8px;',                        'spec 2: 8px gap')
chk('rgba(37,99,235,0.15)',             'spec 2: grammar 15% selected')
chk('border: 2px solid var(--grammar)', 'spec 2: 2px grammar border')
chk('level-btn-badge',                  'spec 2: L1-L9 badge')
chk('scroll-snap-type: x mandatory',    'spec 2: horizontal scroll snap')

# Spec 3: Chain tab
chk('WebkitLineClamp:3',                'spec 3: 3-line clamp')
chk('Read more...',                     'spec 3: Read more button')
chk('See related \u2192',                    'spec 3: See related button')
chk("lvl.id === 'L9' ? 'var(--rhetoric)'", 'spec 3: L9 rhetoric border')
chk("borderLeft: '2px solid '",         'spec 3: 2px left border active card')

# Spec 4 + 12: Tab bar
chk('position: sticky;',               'spec 4+12: tab sticky')
chk('z-index: 10;',                    'spec 4+12: z-index 10')
chk("label: 'Chain'",                  'spec 4: Chain no emoji')
chk("label: 'Reference'",              'spec 8: BSG -> Reference')
chk('data-tab={tab.id}',               'spec 4: data-tab on buttons')
chk("data-tab='grammar']",             'spec 4: grammar active colour')

# Spec 5: Eoin diagnostic
chk('persona-card-diagnostic',         'spec 5: diagnostic card class')
chk('diagnostic-badge',                'spec 5: diagnostic badge class')
chk('DIAGNOSTIC',                      'spec 5: DIAGNOSTIC text')
chk('border: 1px dashed var(--text-dim)', 'spec 5: dashed border CSS')

# Spec 6: Avatar colours
chk('.persona-avatar.conor   { background: #2563EB; color: #fff; }', 'spec 6: Conor')
chk('.persona-avatar.helena  { background: #7c3aed; color: #fff; }', 'spec 6: Helena')
chk('.persona-avatar.eoin    { background: #16a34a; color: #fff; }', 'spec 6: Eoin')
chk('.persona-avatar.rachel  { background: #d97706; color: #fff; }', 'spec 6: Rachel')
chk('.persona-avatar.padraig { background: #6b7280; color: #fff; }', 'spec 6: Padraig')

# Spec 7: Assessment
chk('color: var(--grammar);',          'spec 7: knowledge = grammar blue')
chk('color: var(--logic);',            'spec 7: calculation = logic amber')
chk('color: var(--rhetoric);',         'spec 7: judgement = rhetoric purple')
chk('grammar) 0%, var(--rhetoric)',    'spec 7: progress gradient')
chk('q-option-btn.correct',            'spec 7: correct styling')
chk('q-option-btn.incorrect',          'spec 7: wrong styling')

# Spec 9: Progress dots
chk('level-progress-dots',             'spec 9: dots container')
chk('level-progress-dot grammar',      'spec 9: grammar dot in JSX')
chk('.level-progress-dot.grammar.done  { background: var(--grammar)', 'spec 9: dot done CSS')

# Spec 10: Footer
chk('footer-inner',                    'spec 10: footer-inner')
chk('footer-copyright',                'spec 10: copyright class')
chk('footer-cta',                      'spec 10: CTA class')
chk('lmurphy@legacybe.ie',             'spec 10: contact email')
chk('DC-AI-001 v{TOOL_VERSION}',       'spec 10: version in footer')

# Spec 11: Transitions
chk('--transition:         0.15s ease', 'spec 11: 150ms tab')
chk('--transition-level:   0.20s ease', 'spec 11: 200ms level')
chk('--transition-theme:   0.20s ease', 'spec 11: 200ms theme')

# ==============================================================================
# 3. Content integrity
# ==============================================================================
print("\n--- Content Integrity ---")
chk('Can This Facility Handle AI Workloads?', 'hero title')
chk('Clonshaugh',                            'Clonshaugh data')
chk('5 MVA MIC',                             'MIC technical data')
chk('EN 50600-2-2',                          'standards reference')
chk('MEP Retrofit Engineer',                 'Eoin persona role')
chk('ESG & Regulatory Director',             'Rachel persona role')

# ==============================================================================
# 4. Version count sanity
# ==============================================================================
stale = html.count('1.0.0')
c110  = html.count('1.1.0')
cv110 = html.count('v1.1.0')
print(f"\n--- Version counts ---")
print(f"  '1.0.0' remaining : {stale}  (must be 0)")
print(f"  '1.1.0' present   : {c110}   (TOOL_VERSION + JSON + 2xv1.1.0 = 4)")
print(f"  'v1.1.0' present  : {cv110}  (title + series badge = 2)")

if stale > 0:
    errors.append(f"Stale '1.0.0' found {stale} times")
if c110 < 4:
    errors.append(f"Expected >=4 '1.1.0' occurrences, found {c110}")
if cv110 < 2:
    errors.append(f"Expected 2 'v1.1.0' occurrences, found {cv110}")

# ==============================================================================
# Write and summarise
# ==============================================================================
with open(TARGET, 'w', encoding='utf-8') as f:
    f.write(html)

lines = html.count('\n')
print(f"\n--- Summary ---")
print(f"  {TARGET.split('/')[-1]}  ({lines} lines)")

if errors:
    print(f"\n  FAILURES ({len(errors)}):")
    for e in errors:
        print(f"    \u2717 {e}")
    raise SystemExit(1)
else:
    print(f"\n  ALL CHECKS PASSED \u2014 DC-AI-001_v1_1_0.html is ready")
