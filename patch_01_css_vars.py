"""
patch_01_css_vars.py
ONLY changes: CSS variables comment header (v1.1 → v2.0),
              <title> version string,
              series-badge version string in JSX.
Input:  DC-AI-001_v1_1_0.html
Output: DC-AI-001_v2_0_0.html
Zero content changes.
"""

SRC  = "DC-AI-001_v1_1_0.html"
DEST = "DC-AI-001_v2_0_0.html"

REPLACEMENTS = [
    # 1. CSS variables comment header
    (
        "/* ─── CSS VARIABLES — DC-LEARN fleet standard v1.1 ──────────────── */",
        "/* ─── CSS VARIABLES — DC-LEARN fleet standard v2.0 ──────────────── */"
    ),
    # 2. <title> tag
    (
        "<title>DC-AI-001: Power Density | DC-AI v1.1.0</title>",
        "<title>DC-AI-001: Power Density | DC-AI v2.0.0</title>"
    ),
    # 3. series-badge in JSX (appears once in Header component)
    (
        "Module 1 of 8 · DC-AI v1.1.0",
        "Module 1 of 8 · DC-AI v2.0.0"
    ),
    # 4. TOOL_VERSION constant
    (
        'var TOOL_VERSION = "1.1.0";',
        'var TOOL_VERSION = "2.0.0";'
    ),
    # 5. MODULE_META version field
    (
        '"version": "1.1.0"',
        '"version": "2.0.0"'
    ),
]

with open(SRC, "r", encoding="utf-8") as f:
    html = f.read()

changes = 0
for old, new in REPLACEMENTS:
    count = html.count(old)
    if count == 0:
        print(f"  WARN: not found — {old[:60]}")
    else:
        html = html.replace(old, new)
        changes += count
        print(f"  OK ({count}x): {old[:60]}")

with open(DEST, "w", encoding="utf-8") as f:
    f.write(html)

print(f"\nWrote {DEST}  ({changes} substitutions)")
