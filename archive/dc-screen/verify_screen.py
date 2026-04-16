#!/usr/bin/env python3
"""
DC-SCREEN VERIFICATION SCRIPT — v2.0.0
Auto-QA for all DC-Screen tools matching DC-*-001*.html
15 checks (S01–S15)
"""

import re
import sys
import os
import glob
from datetime import datetime

# ─── Helpers ───────────────────────────────────────────────────────────────────

def strip_css_blocks(text):
    """Remove <style>...</style> blocks to avoid false positives in CSS."""
    return re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)

def strip_comments(text):
    """Remove HTML comments."""
    return re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)

def strip_script_blocks(text):
    """Remove <script>...</script> blocks."""
    return re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)

# ─── Check functions ────────────────────────────────────────────────────────────

def check_s01_stale_values(text, fname):
    """S01 — Stale Canonical Values (FAIL)"""
    failures = []
    stale = [
        (r'\b83[,\s]?050\b', '83050 (old CRM value)'),
        (r'\b0\.295\b', '0.295 (old grid EF)'),
        (r'\b0\.185\b', '0.185 (old gas EF)'),
        (r'[€EUR\s]56\b', '€56 (old carbon tax)'),
        (r'\b63\.5\b', '63.5 (old carbon tax)'),
        (r'Les McGuinness', 'Les McGuinness (wrong name)'),
    ]
    for pattern, label in stale:
        if re.search(pattern, text):
            failures.append(label)
    return failures

def check_s02_banned_terms(text, fname):
    """S02 — Banned Terminology (FAIL)"""
    failures = []
    # Strip CSS blocks to avoid false positives on print-color-adjust: exact
    text_no_css = strip_css_blocks(text)
    # Strip HTML comments
    text_no_css = strip_comments(text_no_css)

    banned = [
        (r'\bstranding\b', 'stranding (use misalignment)'),
        (r'\bStranding Year\b', 'Stranding Year (use Misalignment Year)'),
        (r'CRU\s+compliance\b', 'CRU compliance (use CRU Readiness)'),
        (r'\bDEAP\b', 'DEAP (use NEAP for commercial)'),
        (r'\b100%\s+accurate\b', '100% accurate (use indicative)'),
        (r'\bquiz\b', 'quiz (use assessment)'),
        (r'\bElectrical Engineer\b', 'Electrical Engineer (use MEP Engineer for Mark persona)'),
        (r'\bHall 1\b|\bHall 2\b', 'Hall 1/Hall 2 (use Hall A/Hall B)'),
        (r'\bAoife\b|\bMarcus\b|\bSíle\b', 'Retired persona (Aoife/Marcus/Síle)'),
        (r'\bBallycoolin\b', 'Ballycoolin (retired facility)'),
    ]
    # Special handling for 'exact': only flag if NOT inside print-color-adjust CSS property
    exact_matches = re.findall(r'\bexact\b', text_no_css, re.IGNORECASE)
    # Filter out print-color-adjust: exact occurrences
    problematic_exact = []
    for m in re.finditer(r'\bexact\b', text_no_css, re.IGNORECASE):
        context = text_no_css[max(0, m.start()-50):m.end()+50]
        if 'print-color-adjust' not in context and '-webkit-print-color-adjust' not in context and 'calculation engine exactly' not in context:
            problematic_exact.append(context.strip())
    if problematic_exact:
        failures.append(f'exact (use indicative/screening-level) [{len(problematic_exact)} instance(s) in non-CSS context]')

    for pattern, label in banned:
        if re.search(pattern, text_no_css):
            failures.append(label)
    return failures

def check_s03_crrem_disclosure(text, fname):
    """S03 — CRREM Derivation Disclosure (FAIL = PI exposure)"""
    if not re.search(r'\bCRREM\b', text):
        return []  # No CRREM reference — check not applicable
    disclosures = [
        r'LBE-derived',
        r'derived by LBE',
        r'not CRREM-published',
        r'not published by CRREM',
    ]
    for d in disclosures:
        if re.search(d, text, re.IGNORECASE):
            return []
    return ['CRREM referenced but no derivation disclosure found']

def check_s04_disclaimer(text, fname):
    """S04 — Disclaimer Present (FAIL = PI exposure)"""
    patterns = [
        r'INDICATIVE SCREENING ASSESSMENT',
        r'independent desktop screening',
        r'not a certified energy audit',
        r'not\b.{0,30}investment recommendation',
    ]
    for p in patterns:
        if re.search(p, text, re.IGNORECASE | re.DOTALL):
            return []
    return ['No screening disclaimer found']

def check_s05_pi_statement(text, fname):
    """S05 — PI Statement Present (WARN only)"""
    if re.search(r'[Pp]rofessional [Ii]ndemnity', text):
        return []
    return ['No PI statement found']

def check_s06_version_consistency(text, fname):
    """S06 — Version Consistency (FAIL)"""
    # Extract tool ID from filename
    base = os.path.basename(fname)
    tool_match = re.match(r'(DC-[A-Z-]+-001)', base)
    if not tool_match:
        return []
    tool_id = tool_match.group(1)
    pattern = re.escape(tool_id) + r'\s+v([0-9]+\.[0-9]+\.[0-9]+)'
    versions = re.findall(pattern, text)
    if not versions:
        return []  # No versioned references found
    unique = set(versions)
    if len(unique) > 1:
        return [f'Version mismatch: {sorted(unique)}']
    return []

def check_s07_contact_email(text, fname):
    """S07 — Contact Email (FAIL)"""
    bad_email = re.search(r'les@legacybe\.ie', text, re.IGNORECASE)
    if bad_email:
        return ['Wrong email: les@legacybe.ie (use info@legacybe.ie or lmurphy@legacybe.ie)']
    return []

def check_s08_unicode_escapes(text, fname):
    """S08 — Unicode Escapes (WARN)"""
    # Count \uXXXX escapes not inside HTML comments
    text_no_comments = strip_comments(text)
    matches = re.findall(r'\\u[0-9a-fA-F]{4}', text_no_comments)
    if matches:
        return [f'{len(matches)} unicode escape(s)']
    return []

def check_s09_clonshaugh(text, fname):
    """S09 — Clonshaugh Reference Consistency (WARN)"""
    if not re.search(r'\bClonshaugh\b', text, re.IGNORECASE):
        return []
    warnings = []
    params = [
        (r'\b2\.4\b', '2.4 MW IT load'),
        (r'\b1\.5\b|\b1\.50\b', '1.5 PUE'),
    ]
    for pattern, label in params:
        if not re.search(pattern, text):
            warnings.append(f'Clonshaugh ref but missing {label}')
    return warnings

def check_s10_source_tiers(text, fname):
    """S10 — Source Tier Coverage (WARN/INFO)"""
    counts = {}
    for tier in ['T1', 'T2', 'T3', 'T4']:
        counts[tier] = len(re.findall(r'\b' + tier + r'\b', text))
    total = sum(counts.values())
    result = f"T1:{counts['T1']} T2:{counts['T2']} T3:{counts['T3']} T4:{counts['T4']}"
    if total == 0:
        return [f'No source tier markers ({result})']
    return [result]  # Always report as info

def check_s11_intel_language(text, fname):
    """S11 — Intelligence Layer Language (WARN)"""
    bad_patterns = [
        r"we'?ll design",
        r'we will design',
        r'we deliver',
        r'\binstall\b',
        r'\bspecify\b',
    ]
    good_patterns = [r'\bidentif', r'\bquantif', r'\bintelligence\b']
    warnings = []
    text_lower = text.lower()
    for p in bad_patterns:
        if re.search(p, text_lower):
            warnings.append(f'Prescriptive language found: {p}')
    has_good = any(re.search(p, text_lower) for p in good_patterns)
    if not has_good:
        warnings.append('Missing intelligence-layer positioning (identify/quantify/intelligence)')
    return warnings

def check_s12_canonical_values(text, fname):
    """S12 — Current Canonical Values Present (INFO)"""
    checks = [
        (r'\b0\.2241\b', 'Grid EF 0.2241'),
        (r'\b71\b', 'Carbon tax 71'),
        (r'149[,\s]?960', 'CRM 149960'),
    ]
    present = []
    absent = []
    for pattern, label in checks:
        if re.search(pattern, text):
            present.append(label)
        else:
            absent.append(label)
    result = []
    if present:
        result.append('Present: ' + ', '.join(present))
    if absent:
        result.append('Absent: ' + ', '.join(absent))
    return result

def check_s13_canonical_consistency(filepath, text, fname):
    """S13 — Fleet Canonical Consistency (FAIL)"""
    MASTER = {
        'grid_ef':            0.2241,
        'gas_ef':             0.205,
        'carbon_tax_current': 71,
        'carbon_tax_2030':    100,
        'crm_clearing_price': 149960,
        'electricity_price':  0.12,
        'free_cooling_hours': 7200,
        'taxonomy_pue':       1.3,
        'cru_renewable_pct':  80,
    }

    # (param_key, regex_pattern, capture_group_index)
    # Patterns match variable declarations or inline canonical usages.
    # Use (?<!\w) to avoid matching _-prefixed stress-test overrides.
    CHECKS = [
        # Grid EF
        ('grid_ef',
         r'(?<!\w)(?:GRID_?EF|GRID_?FACTOR|GRID_?CO2|GRID_?EMISSION_?FACTOR)\s*=\s*([\d.]+)',
         1),
        # Gas EF — named var or inline "X kgCO₂/kWh gas" pattern
        ('gas_ef',
         r'(?<!\w)(?:GAS_?EF|GAS_?CO2|gas_?co2_?per_?kwh)\s*=\s*([\d.]+)',
         1),
        ('gas_ef',
         r'gas(?:\s+factor|heating\s+at)\s+~?([\d.]+)\s*kgCO[₂2]',
         1),
        ('gas_ef',
         r'([\d.]+)\s*kgCO[₂2]/kWh\s*(?:gas|SEAI\s+Scope)',
         1),
        # Carbon tax current
        ('carbon_tax_current',
         r'(?<!\w)CARBON_?TAX(?:_?CURRENT)?\s*=\s*(\d+)',
         1),
        # Carbon tax 2030
        ('carbon_tax_2030',
         r'(?<!\w)CARBON_?TAX_?2030\s*=\s*(\d+)',
         1),
        # CRM clearing price
        ('crm_clearing_price',
         r'(?<!\w)CRM_?(?:CLEARING_?)?PRICE\s*=\s*([\d,]+)',
         1),
        # Electricity price — named var (local var elecRate also checked)
        ('electricity_price',
         r'(?<!\w)(?:ELEC_?(?:PRICE|RATE|TARIFF)|electricity_?(?:price|rate)|elecRate)\s*=\s*([\d.]+)',
         1),
        # Free cooling hours
        ('free_cooling_hours',
         r'(?<!\w)FREE_?COOLING_?HOURS?\s*=\s*(\d+)',
         1),
        # Taxonomy PUE
        ('taxonomy_pue',
         r'(?<!\w)(?:TAXONOMY_?PUE|EU_?TAXONOMY_?PUE)(?:_?THRESHOLD|_?LIMIT)?\s*=\s*([\d.]+)',
         1),
        # CRU renewable %
        ('cru_renewable_pct',
         r'(?<!\w)CRU_?RENEW(?:ABLE)?_?(?:TARGET|PCT|PERCENT)?\s*=\s*(\d+)',
         1),
    ]

    failures = []
    seen = set()  # deduplicate same param+value combinations

    for param_key, pattern, group_idx in CHECKS:
        for m in re.finditer(pattern, text, re.IGNORECASE):
            val_str = m.group(group_idx).replace(',', '')
            try:
                val = float(val_str)
            except ValueError:
                continue
            master_val = MASTER[param_key]
            # Tolerance: exact for integers, 0.0001 for floats
            tol = 0.0001 if '.' in str(master_val) else 0.5
            if abs(val - master_val) > tol:
                lineno = text[:m.start()].count('\n') + 1
                key = (param_key, val, lineno)
                if key not in seen:
                    seen.add(key)
                    failures.append(
                        f'{fname}:{lineno} — {param_key}: found {val}, master={master_val}'
                    )
    return failures

def check_s14_regulatory_currency(text, fname):
    """S14 — Regulatory Reference Currency (WARN/FAIL)"""
    REG_TERMS = [
        ('CRU/', r'CRU/'),
        ('EED',  r'\bEED\b'),
        ('F-Gas', r'F-[Gg]as'),
        ('Finance Act', r'Finance\s+Act'),
        ('CRREM', r'\bCRREM\b'),
    ]

    issues = []

    for reg_name, pat in REG_TERMS:
        matches = list(re.finditer(pat, text))
        if not matches:
            continue

        # Collect all valid years found near any occurrence of this term.
        # "Valid" = not part of a regulation ID (year followed by /)
        #           and not part of a document code (year preceded by : or -)
        all_years = []
        fail_lines = []

        for m in matches:
            ctx_start = max(0, m.start() - 40)
            ctx_end   = min(len(text), m.end() + 80)
            ctx       = text[ctx_start:ctx_end]

            for ym in re.finditer(r'\b(20\d{2})\b', ctx):
                year = int(ym.group(1))
                # Position of year within context string
                ypos   = ym.start()
                before = ctx[ypos - 1] if ypos > 0 else ''
                after  = ctx[ym.end()]  if ym.end() < len(ctx) else ''
                # Skip regulation IDs (2023/1791) and document codes (CP1:2020)
                if after == '/' or before in (':', '-'):
                    continue
                all_years.append(year)
                if year <= 2023:
                    lineno = text[:m.start()].count('\n') + 1
                    fail_lines.append((year, lineno))

        if not all_years:
            # Term appears but never with a year — WARN
            lineno = text[:matches[0].start()].count('\n') + 1
            issues.append(f'WARN:{reg_name}:line {lineno}')
        elif max(all_years) >= 2024:
            # At least one current citation — PASS
            pass
        else:
            # All detected years are ≤ 2023 — FAIL
            worst_year, worst_line = min(fail_lines, key=lambda x: x[0])
            issues.append(f'FAIL:{reg_name}:{worst_year}:line {worst_line}')

    return issues

def check_s15_duplicate_ids(text, fname):
    """S15 — Duplicate Element IDs (FAIL)"""
    from collections import Counter
    ids = re.findall(r'\bid=["\']([^"\']+)["\']', text, re.IGNORECASE)
    counts = Counter(id_val.strip() for id_val in ids if id_val.strip())
    dups = sorted(id_val for id_val, cnt in counts.items() if cnt > 1)
    return [f'Duplicate id="{d}"' for d in dups]

# ─── Main ───────────────────────────────────────────────────────────────────────

def run_checks(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        text = f.read()

    fname = os.path.basename(filepath)
    results = {}

    s01 = check_s01_stale_values(text, fname)
    s02 = check_s02_banned_terms(text, fname)
    s03 = check_s03_crrem_disclosure(text, fname)
    s04 = check_s04_disclaimer(text, fname)
    s05 = check_s05_pi_statement(text, fname)
    s06 = check_s06_version_consistency(text, fname)
    s07 = check_s07_contact_email(text, fname)
    s08 = check_s08_unicode_escapes(text, fname)
    s09 = check_s09_clonshaugh(text, fname)
    s10 = check_s10_source_tiers(text, fname)
    s11 = check_s11_intel_language(text, fname)
    s12 = check_s12_canonical_values(text, fname)
    s13 = check_s13_canonical_consistency(filepath, text, fname)
    s14 = check_s14_regulatory_currency(text, fname)
    s15 = check_s15_duplicate_ids(text, fname)

    # S14: split into FAILs and WARNs
    s14_fails = [i.split(':', 3)[1:] for i in s14 if i.startswith('FAIL:')]
    s14_warns = [i.split(':', 2)[1:] for i in s14 if i.startswith('WARN:')]
    s14_fail_msgs = [f'{r} cites year {y} ({ln})' for r, y, ln in s14_fails]
    s14_warn_msgs = [f'{r} — no year ref ({ln})' for r, ln in s14_warns]

    return {
        'S01': ('FAIL', s01)  if s01          else ('PASS', []),
        'S02': ('FAIL', s02)  if s02          else ('PASS', []),
        'S03': ('FAIL', s03)  if s03          else ('PASS', []),
        'S04': ('FAIL', s04)  if s04          else ('PASS', []),
        'S05': ('WARN', s05)  if s05          else ('PASS', []),
        'S06': ('FAIL', s06)  if s06          else ('PASS', []),
        'S07': ('FAIL', s07)  if s07          else ('PASS', []),
        'S08': ('WARN', s08)  if s08          else ('PASS', []),
        'S09': ('WARN', s09)  if s09          else ('PASS', []),
        'S10': ('INFO', s10),
        'S11': ('WARN', s11)  if s11          else ('PASS', []),
        'S12': ('INFO', s12),
        'S13': ('FAIL', s13)  if s13          else ('PASS', []),
        'S14': ('FAIL', s14_fail_msgs) if s14_fail_msgs else
               ('WARN', s14_warn_msgs) if s14_warn_msgs else ('PASS', []),
        'S15': ('FAIL', s15)  if s15          else ('PASS', []),
    }

def main():
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    pattern = os.path.join(repo_dir, 'DC-*-001*.html')
    files = sorted(glob.glob(pattern))

    if not files:
        print('No DC-*-001*.html files found.')
        sys.exit(1)

    print('DC-SCREEN VERIFICATION REPORT — v2.0.0')
    print(f'Date: {datetime.now().strftime("%Y-%m-%d %H:%M")}')
    print(f'Files scanned: {len(files)}')
    print('═' * 60)

    total_pass = 0
    total_fail = 0
    total_warn = 0
    blocking_failures = []

    BLOCKING    = {'S01', 'S02', 'S03', 'S04', 'S06', 'S07', 'S13', 'S14', 'S15'}
    WARN_CHECKS = {'S05', 'S08', 'S09', 'S11'}
    INFO_CHECKS = {'S10', 'S12'}

    check_labels = {
        'S01': 'Stale Values       ',
        'S02': 'Banned Terms       ',
        'S03': 'CRREM Disclosure   ',
        'S04': 'Disclaimer         ',
        'S05': 'PI Statement       ',
        'S06': 'Version Match      ',
        'S07': 'Contact Email      ',
        'S08': 'Unicode Escapes    ',
        'S09': 'Clonshaugh Params  ',
        'S10': 'Source Tiers       ',
        'S11': 'Intel Language     ',
        'S12': 'Canonical Values   ',
        'S13': 'Canon Consistency  ',
        'S14': 'Reg Reference Yr   ',
        'S15': 'Duplicate IDs      ',
    }

    ALL_CHECKS = [
        'S01','S02','S03','S04','S05','S06','S07',
        'S08','S09','S10','S11','S12','S13','S14','S15',
    ]

    file_results = {}

    for filepath in files:
        fname = os.path.basename(filepath)
        print(f'\n{fname}')
        checks = run_checks(filepath)
        file_results[fname] = checks

        file_pass = True
        for key in ALL_CHECKS:
            status, details = checks[key]
            label = check_labels[key]

            if key in INFO_CHECKS:
                info_str = ' | '.join(details) if details else ''
                print(f'  {key} {label}  {info_str}')
                continue

            if status == 'FAIL':
                detail_str = ' — ' + '; '.join(details) if details else ''
                print(f'  {key} {label}  FAIL{detail_str}')
                if key in BLOCKING:
                    file_pass = False
                    total_fail += 1
            elif status == 'WARN':
                detail_str = ' (' + '; '.join(details) + ')' if details else ''
                print(f'  {key} {label}  WARN{detail_str}')
                total_warn += 1
            else:
                print(f'  {key} {label}  PASS')

        if file_pass:
            total_pass += 1
        else:
            blocking_failures.append(fname)

    print('\n' + '═' * 60)
    print('SUMMARY')
    print(f'  {"Check":<22}  {"Description":<28}  {"Role"}')
    print(f'  {"─"*22}  {"─"*28}  {"─"*10}')
    summary_rows = [
        ('S01', 'Stale Canonical Values',    'BLOCKING'),
        ('S02', 'Banned Terminology',        'BLOCKING'),
        ('S03', 'CRREM Disclosure',          'BLOCKING'),
        ('S04', 'Disclaimer Present',        'BLOCKING'),
        ('S05', 'PI Statement',              'WARN'),
        ('S06', 'Version Consistency',       'BLOCKING'),
        ('S07', 'Contact Email',             'BLOCKING'),
        ('S08', 'Unicode Escapes',           'WARN'),
        ('S09', 'Clonshaugh Params',         'WARN'),
        ('S10', 'Source Tier Coverage',      'INFO'),
        ('S11', 'Intel Layer Language',      'WARN'),
        ('S12', 'Canonical Values Present',  'INFO'),
        ('S13', 'Fleet Canon Consistency',   'BLOCKING'),
        ('S14', 'Reg Reference Currency',    'BLOCKING'),
        ('S15', 'Duplicate Element IDs',     'BLOCKING'),
    ]
    for chk, desc, role in summary_rows:
        print(f'  {chk:<22}  {desc:<28}  {role}')

    print()
    print(f'  PASS: {total_pass}/{len(files)} tools clean')
    print(f'  FAIL: {total_fail} blocking issue(s)')
    print(f'  WARN: {total_warn} non-blocking flag(s)')

    if blocking_failures:
        print('\nBLOCKING FAILURES:')
        for f in blocking_failures:
            checks = file_results[f]
            for key in BLOCKING:
                status, details = checks[key]
                if status == 'FAIL':
                    print(f'  {f}: {key} — {"; ".join(details)}')
        print('\nSHIP CONDITION: NOT MET —', total_fail, 'blocking failure(s)')
    else:
        print('\nSHIP CONDITION: MET — 0 blocking failures')

    return 0 if not blocking_failures else 1

if __name__ == '__main__':
    sys.exit(main())
