import json, re

SRC = "/home/user/dc-learn-academy/DC-AI-001_v2_4_0 (1).html"

with open(SRC, encoding='utf-8') as f:
    html = f.read()

def extract_js_value(text, var_name, start_char):
    """Extract a JS block value (array or object) by bracket-matching."""
    pat = re.compile(r'var\s+' + re.escape(var_name) + r'\s*=\s*' + re.escape(start_char))
    m = pat.search(text)
    if not m:
        return None
    pos = m.end() - 1  # position of opening bracket
    depth = 0
    in_str = None
    i = pos
    while i < len(text):
        c = text[i]
        if in_str:
            if c == '\\':
                i += 2
                continue
            if c == in_str:
                in_str = None
        else:
            if c in ('"', "'", '`'):
                in_str = c
            elif c in ('{', '['):
                depth += 1
            elif c in ('}', ']'):
                depth -= 1
                if depth == 0:
                    return text[pos:i+1]
        i += 1
    return None

def extract_logo(text):
    m = re.search(r'var\s+LOGO_SRC\s*=\s*"(data:image/png;base64,[^"]+)"', text)
    return m.group(1) if m else None

# Extract raw JS strings
data = {}
data['LEVELS_raw']               = extract_js_value(html, 'LEVELS', '[')
data['ASSESSMENT_QUESTIONS_raw'] = extract_js_value(html, 'ASSESSMENT_QUESTIONS', '[')
data['GLOSSARY_raw']             = extract_js_value(html, 'GLOSSARY', '[')
data['BIBLIOGRAPHY_raw']         = extract_js_value(html, 'BIBLIOGRAPHY', '[')
data['RHETORIC_TAKEAWAYS_raw']   = extract_js_value(html, 'RHETORIC_TAKEAWAYS', '{')
data['SO_WHAT_MAP_raw']          = extract_js_value(html, 'SO_WHAT_MAP', '{')
data['PERSONAS_raw']             = extract_js_value(html, 'PERSONAS', '[')
data['LOGO_SRC']                 = extract_logo(html)

# Construct CLONSHAUGH from SidebarFacility data in the DC-AI file
data['CLONSHAUGH_raw'] = (
    '{name:"Clonshaugh Reference DC",year:2012,racks:200,currentKW:8,targetKW:40,'
    'currentPUE:1.50,targetPUE:1.20,mic_mva:5,mic_util:0.85,bus_section_a:1600,'
    'bus_util:0.73,voltage:415,pf:0.85}'
)

# Report extraction results
for key, val in data.items():
    if val is None:
        print(f"MISSING: {key}")
    elif key == 'LOGO_SRC':
        print(f"OK: {key} ({len(val)} chars)")
    else:
        print(f"OK: {key} ({len(val)} chars)")

out = "/home/user/dc-learn-academy/data.json"
with open(out, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)
print(f"\nSaved to {out}")
