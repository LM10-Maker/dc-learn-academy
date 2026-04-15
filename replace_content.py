import json, re

DST = "/home/user/dc-learn-academy/DC-AI-001_v3_0_0.html"
with open(DST, encoding='utf-8') as f: h = f.read()
with open("/home/user/dc-learn-academy/data.json", encoding='utf-8') as f: d = json.load(f)

def bracket_end(text, pos):
    """Return index after the closing bracket matching text[pos]."""
    open_ch = text[pos]; close_ch = ']' if open_ch == '[' else '}'
    depth = 0; in_str = None; i = pos
    while i < len(text):
        c = text[i]
        if in_str:
            if c == '\\': i += 2; continue
            if c == in_str: in_str = None
        else:
            if c in ('"', "'", '`'): in_str = c
            elif c == open_ch: depth += 1
            elif c == close_ch:
                depth -= 1
                if depth == 0: return i + 1
        i += 1
    return -1

def replace_const(src, decl_prefix, new_value):
    """Replace 'const/var NAME = [...]' or '{...}' with new_value."""
    pat = re.compile(re.escape(decl_prefix) + r'\s*')
    m = pat.search(src)
    if not m:
        print(f"  WARN: not found: {repr(decl_prefix)}")
        return src
    start_val = m.end()
    end_val = bracket_end(src, start_val)
    if end_val < 0:
        print(f"  WARN: bracket not closed for {repr(decl_prefix)}")
        return src
    # consume trailing semicolon
    end_stmt = end_val
    if end_stmt < len(src) and src[end_stmt] == ';': end_stmt += 1
    result = src[:m.start()] + decl_prefix + ' ' + new_value + ';' + src[end_stmt:]
    print(f"  OK: replaced {repr(decl_prefix)} ({end_stmt - m.start()} → {len(new_value)+len(decl_prefix)+2} chars)")
    return result

# Rename rhetoric persona keys in LEVELS_raw (role-based → name-based)
levels_raw = d['LEVELS_raw']
for old, new in [('asset_management', 'conor'), ('technology', 'helena'),
                 ('technical', 'eoin'), ('compliance', 'rachel'), ('cost', 'padraig')]:
    levels_raw = levels_raw.replace(f'"{old}":', f'"{new}":')
    count = levels_raw.count(f'"{new}":')
    print(f"  Renamed {old} → {new} ({count} occurrences)")

# Replace constants
h = replace_const(h, 'const LEVELS =', levels_raw)
h = replace_const(h, 'const ASSESSMENT_QUESTIONS =', d['ASSESSMENT_QUESTIONS_raw'])
h = replace_const(h, 'const GLOSSARY_002 =', d['GLOSSARY_raw'])
h = replace_const(h, 'const BIBLIOGRAPHY_002 =', d['BIBLIOGRAPHY_raw'])
h = replace_const(h, 'const CLONSHAUGH =', d['CLONSHAUGH_raw'])

# Replace LOGO_SRC (same content, but replace for correctness)
logo_pat = re.compile(r'const LOGO_SRC\s*=\s*"data:image/png;base64,[^"]+";')
m = logo_pat.search(h)
if m:
    h = h[:m.start()] + f'const LOGO_SRC = "{d["LOGO_SRC"]}";' + h[m.end():]
    print("  OK: replaced LOGO_SRC")

# Insert SO_WHAT_MAP and RHETORIC_TAKEAWAYS after BIBLIOGRAPHY_002 block
# Find end of BIBLIOGRAPHY_002 declaration
m2 = re.search(r'const BIBLIOGRAPHY_002\s*=', h)
if m2:
    end_bib = bracket_end(h, h.index('[', m2.start()))
    end_stmt = end_bib
    if end_stmt < len(h) and h[end_stmt] == ';': end_stmt += 1
    insert = (f'\nconst SO_WHAT_MAP = {d["SO_WHAT_MAP_raw"]};\n'
              f'const RHETORIC_TAKEAWAYS = {d["RHETORIC_TAKEAWAYS_raw"]};\n')
    h = h[:end_stmt] + insert + h[end_stmt:]
    print(f"  OK: inserted SO_WHAT_MAP ({len(d['SO_WHAT_MAP_raw'])} chars) and RHETORIC_TAKEAWAYS ({len(d['RHETORIC_TAKEAWAYS_raw'])} chars)")

with open(DST, 'w', encoding='utf-8') as f: f.write(h)
print(f"\nScript 4 complete. File: {len(h)} chars, {h.count(chr(10))+1} lines")
