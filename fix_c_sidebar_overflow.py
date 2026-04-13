#!/usr/bin/env python3
"""
Fix C: Fix sidebar text overflow in light theme.
- Add word-wrap: break-word + overflow-wrap: break-word to .sidebar-card-title
- Reduce .sidebar-card-title font-size from 0.8rem to 0.75rem
- Add word-wrap rule for .sidebar-col p (sidebar paragraph text)
- Bump version 2.1.0 → 2.2.0 everywhere
Reads/writes DC-AI-001_v2_2_0.html in place.
"""

FILE = "DC-AI-001_v2_2_0.html"

# ── 1. Patch .sidebar-card-title: add word-wrap, reduce font ──────────────
OLD_CSS = """\
    .sidebar-card-title {
      font-size: 0.8rem;
      font-weight: 700;
      color: var(--text-bright);
      margin-bottom: 0.6rem;
      padding-bottom: 0.4rem;
      border-bottom: 1px solid var(--border);
    }"""

NEW_CSS = """\
    .sidebar-card-title {
      font-size: 0.75rem;
      font-weight: 700;
      color: var(--text-bright);
      margin-bottom: 0.6rem;
      padding-bottom: 0.4rem;
      border-bottom: 1px solid var(--border);
      word-wrap: break-word;
      overflow-wrap: break-word;
    }
    .sidebar-col p {
      word-wrap: break-word;
      overflow-wrap: break-word;
    }"""

# ── 2. Reduce Methodology description font to 0.75rem ─────────────────────
# SidebarMethodology item description: fontSize:'0.71rem' → '0.75rem'
# Targeted by surrounding context to avoid touching other 0.71rem occurrences
OLD_METHOD_DESC = """\
          <div style={{fontSize:'0.71rem',color:'var(--text-muted)',lineHeight:'1.5'}}>{it[1]}</div>"""

NEW_METHOD_DESC = """\
          <div style={{fontSize:'0.75rem',color:'var(--text-muted)',lineHeight:'1.5'}}>{it[1]}</div>"""

# ── 3. Version bump 2.1.0 → 2.2.0 ─────────────────────────────────────────
VERSION_PAIRS = [
    ('DC-AI v2.1.0', 'DC-AI v2.2.0'),
    ('var TOOL_VERSION = "2.1.0";', 'var TOOL_VERSION = "2.2.0";'),
    ('"version": "2.1.0"', '"version": "2.2.0"'),
    ("['Version', '2.1.0']", "['Version', '2.2.0']"),
]

with open(FILE, "r", encoding="utf-8") as f:
    html = f.read()

# Apply CSS fix
assert OLD_CSS in html, "Fix C: .sidebar-card-title block not found"
html = html.replace(OLD_CSS, NEW_CSS, 1)

# Apply methodology description font fix
assert OLD_METHOD_DESC in html, "Fix C: methodology description div not found"
html = html.replace(OLD_METHOD_DESC, NEW_METHOD_DESC, 1)

# Apply version bumps
for old_v, new_v in VERSION_PAIRS:
    count = html.count(old_v)
    assert count > 0, f"Fix C: version string not found: {old_v!r}"
    html = html.replace(old_v, new_v)

# ── 4. Verify counts ───────────────────────────────────────────────────────
import re
q_count = len(re.findall(r'"q"\s*:', html))
assert q_count == 27, f"Question count mismatch: expected 27, got {q_count}"

# Count grammar facts: only those in LEVELS data (before GLOSSARY section)
levels_start = html.find('var LEVELS')
glossary_start = html.find('var GLOSSARY')
levels_only = html[levels_start:glossary_start]
t_count = len(re.findall(r'"term"\s*:', levels_only))
assert t_count == 45, f"Fact count mismatch: expected 45, got {t_count}"

with open(FILE, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Fix C applied: sidebar word-wrap, font reduction, version → 2.2.0 → {FILE}")
print(f"  Verified: {q_count} questions, {t_count} facts")
