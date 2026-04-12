#!/usr/bin/env python3
"""
polish_01_css.py
Replace CSS variables block with DC-LEARN fleet standard v1.1.
Reads DC-AI-001_v1_0_0.html -> DC-AI-001_v1_1_0.html
"""

SRC  = '/home/user/dc-learn-academy/DC-AI-001_v1_0_0.html'
DEST = '/home/user/dc-learn-academy/DC-AI-001_v1_1_0.html'

with open(SRC, 'r', encoding='utf-8') as f:
    html = f.read()

replaced = []

def rep(old, new, tag):
    global html
    if old not in html:
        # Show context for debugging
        # Find longest common prefix
        for i, c in enumerate(old):
            if i >= len(html) or c != html[i]:
                break
        raise ValueError(f'[MISS:{tag}] not found in source. First miss near char {i}: {repr(old[max(0,i-20):i+20])}')
    html = html.replace(old, new, 1)
    replaced.append(tag)

# ==============================================================================
# 1. CSS THEME VARIABLES — full block replacement
# ==============================================================================
# Read exact anchor from file (avoids Unicode dash-count issues in script source)
CSS_VARS_START = "    /* \u2500\u2500\u2500 CSS VARIABLES"
CSS_VARS_END   = "\n    }"   # end of [data-theme="light"] block

# Find precise boundaries in the source
start_idx = html.index(CSS_VARS_START)
# The light theme block ends — find the closing brace after 'tag-text' / 'shadow-lg'
# We know the light theme ends before the RESET & BASE comment
reset_marker = "\n    /* \u2500\u2500\u2500 RESET"
end_idx = html.index(reset_marker, start_idx)

OLD_VARS = html[start_idx:end_idx]

NEW_VARS = """    /* \u2500\u2500\u2500 CSS VARIABLES \u2014 DC-LEARN fleet standard v1.1 \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 */
    :root {
      --font-sans: 'IBM Plex Sans', system-ui, -apple-system, sans-serif;
      --font-mono: 'IBM Plex Mono', monospace;
      --radius-sm: 6px;
      --radius-md: 10px;
      --radius-lg: 12px;
    }

    /* Dark theme \u2014 DC-LEARN three-tier depth model */
    :root, [data-theme="dark"] {
      /* Depth tiers */
      --bg:            #0F1117;
      --surface:       #181C20;
      --panel:         #1E2228;
      --surface-2:     #1E2228;
      --surface-3:     #242930;
      --border:        #2A2F38;
      --border-2:      #363C47;
      /* Four-tier text hierarchy */
      --text:          #C8CCD4;
      --text-bright:   #F0F2F5;
      --text-dim:      #8B919A;
      --text-muted:    #5A6170;
      --text-faint:    #5A6170;
      /* Stage colours */
      --grammar:       #2563EB;
      --logic:         #d97706;
      --rhetoric:      #7c3aed;
      --lbe-green:     #16a34a;
      /* Semantic */
      --success:       #16a34a;
      --warn:          #d97706;
      --error:         #dc2626;
      /* Compatibility aliases for existing CSS classes */
      --accent:        #2563EB;
      --accent-hover:  #1d4ed8;
      --accent-dim:    rgba(37,99,235,0.15);
      --accent-glow:   rgba(37,99,235,0.08);
      --green:         #16a34a;
      --green-dim:     rgba(22,163,74,0.15);
      --amber:         #d97706;
      --amber-dim:     rgba(217,119,6,0.15);
      --red:           #dc2626;
      --red-dim:       rgba(220,38,38,0.15);
      --purple:        #7c3aed;
      --purple-dim:    rgba(124,58,237,0.15);
      --cyan:          #0891b2;
      --cyan-dim:      rgba(8,145,178,0.15);
      --tag-bg:        #1E2228;
      --tag-text:      #93c5fd;
      --shadow:        0 4px 24px rgba(0,0,0,0.4);
      --shadow-lg:     0 8px 40px rgba(0,0,0,0.6);
      /* Transitions \u2014 spec 11 */
      --transition:         0.15s ease;
      --transition-level:   0.20s ease;
      --transition-theme:   0.20s ease;
    }

    /* Light theme \u2014 DC-LEARN light variant */
    [data-theme="light"] {
      --bg:            #F5F5F5;
      --surface:       #FFFFFF;
      --panel:         #F0F0F0;
      --surface-2:     #F0F0F0;
      --surface-3:     #E8E8E8;
      --border:        #E0E0E0;
      --border-2:      #CCCCCC;
      --text:          #2D3748;
      --text-bright:   #1A202C;
      --text-dim:      #718096;
      --text-muted:    #A0AEC0;
      --text-faint:    #A0AEC0;
      --grammar:       #2563EB;
      --logic:         #d97706;
      --rhetoric:      #7c3aed;
      --lbe-green:     #16a34a;
      --success:       #16a34a;
      --warn:          #d97706;
      --error:         #dc2626;
      --accent:        #2563EB;
      --accent-hover:  #1d4ed8;
      --accent-dim:    rgba(37,99,235,0.10);
      --accent-glow:   rgba(37,99,235,0.05);
      --green:         #16a34a;
      --green-dim:     rgba(22,163,74,0.10);
      --amber:         #d97706;
      --amber-dim:     rgba(217,119,6,0.10);
      --red:           #dc2626;
      --red-dim:       rgba(220,38,38,0.10);
      --purple:        #7c3aed;
      --purple-dim:    rgba(124,58,237,0.10);
      --cyan:          #0891b2;
      --cyan-dim:      rgba(8,145,178,0.10);
      --tag-bg:        #F0F0F0;
      --tag-text:      #2563eb;
      --shadow:        0 2px 12px rgba(0,0,0,0.08);
      --shadow-lg:     0 6px 24px rgba(0,0,0,0.12);
      --transition:         0.15s ease;
      --transition-level:   0.20s ease;
      --transition-theme:   0.20s ease;
    }"""

rep(OLD_VARS, NEW_VARS, 'CSS variables block')

# ==============================================================================
# 2. Semantic colour tweaks that depend on new var names
# ==============================================================================

rep(
    "background: linear-gradient(135deg, var(--surface) 0%, var(--surface-2) 100%);",
    "background: linear-gradient(135deg, var(--surface) 0%, var(--panel) 100%);",
    'hero banner gradient'
)

rep(
    "      color: var(--text);\n      letter-spacing: -0.02em;\n      margin-bottom: 0.4rem;\n    }\n    .hero-disclaimer",
    "      color: var(--text-bright);\n      letter-spacing: -0.02em;\n      margin-bottom: 0.4rem;\n    }\n    .hero-disclaimer",
    'hero-title colour'
)

rep(
    "    .hero-module-id {\n      font-size: 0.72rem;\n      font-weight: 600;\n      color: var(--accent);",
    "    .hero-module-id {\n      font-size: 0.72rem;\n      font-weight: 600;\n      color: var(--grammar);",
    'hero-module-id colour'
)

rep(
    "    .card-title {\n      font-size: 1rem;\n      font-weight: 600;\n      color: var(--text);\n      letter-spacing: -0.01em;\n    }",
    "    .card-title {\n      font-size: 1rem;\n      font-weight: 600;\n      color: var(--text-bright);\n      letter-spacing: -0.01em;\n    }",
    'card-title colour'
)

rep(
    "      transition: background var(--transition), border-color var(--transition);\n    }\n    .theme-btn:hover",
    "      transition: background var(--transition-theme), border-color var(--transition-theme), color var(--transition-theme);\n    }\n    .theme-btn:hover",
    'theme-btn transition'
)

rep(
    "      background: var(--surface-2);\n      border: 1px solid var(--border);\n      border-radius: 20px;",
    "      background: var(--panel);\n      border: 1px solid var(--border);\n      border-radius: 20px;",
    'series-badge background'
)

# ==============================================================================
# 3. Card background: surface-2 -> panel for depth clarity
# ==============================================================================

rep(
    "    .fact-card {\n      background: var(--surface-2);\n      border: 1px solid var(--border);\n      border-radius: var(--radius-md);\n      padding: 1.1rem 1.2rem;\n      border-left: 3px solid var(--accent);\n    }",
    "    .fact-card {\n      background: var(--panel);\n      border: 1px solid var(--border);\n      border-radius: var(--radius-md);\n      padding: 1.1rem 1.2rem;\n      border-left: 3px solid var(--grammar);\n    }",
    'fact-card background+border'
)

rep(
    "    .fact-term {\n      font-size: 0.95rem;\n      font-weight: 700;\n      color: var(--text);",
    "    .fact-term {\n      font-size: 0.95rem;\n      font-weight: 700;\n      color: var(--text-bright);",
    'fact-term colour'
)

rep(
    "    .fact-standard {\n      font-size: 0.72rem;\n      font-family: var(--font-mono);\n      color: var(--accent);",
    "    .fact-standard {\n      font-size: 0.72rem;\n      font-family: var(--font-mono);\n      color: var(--grammar);",
    'fact-standard colour'
)

rep(
    "    .so-what-box {\n      background: var(--green-dim);\n      border: 1px solid var(--green);\n      border-radius: var(--radius-sm);\n      padding: 0.6rem 0.9rem;\n      margin-top: 0.75rem;\n      font-size: 0.82rem;\n      color: var(--text);\n      line-height: 1.55;\n    }\n    .so-what-box strong { color: var(--green); font-weight: 600; }",
    "    .so-what-box {\n      background: var(--accent-dim);\n      border: 1px solid var(--grammar);\n      border-left: 3px solid var(--grammar);\n      border-radius: var(--radius-sm);\n      padding: 0.6rem 0.9rem;\n      margin-top: 0.75rem;\n      font-size: 0.82rem;\n      color: var(--text);\n      line-height: 1.55;\n    }\n    .so-what-box strong { color: var(--grammar); font-weight: 600; }",
    'so-what-box grammar style'
)

rep(
    "    .ce-card {\n      background: var(--surface-2);\n      border: 1px solid var(--border);",
    "    .ce-card {\n      background: var(--panel);\n      border: 1px solid var(--border);",
    'ce-card background'
)

rep(
    "    .chain-level-card {\n      background: var(--surface-2);\n      border: 1px solid var(--border);",
    "    .chain-level-card {\n      background: var(--panel);\n      border: 1px solid var(--border);",
    'chain-level-card background'
)

rep(
    "    .persona-card {\n      background: var(--surface-2);\n      border: 1px solid var(--border);",
    "    .persona-card {\n      background: var(--panel);\n      border: 1px solid var(--border);",
    'persona-card background'
)

rep(
    "    .glossary-item {\n      background: var(--surface-2);\n      border: 1px solid var(--border);",
    "    .glossary-item {\n      background: var(--panel);\n      border: 1px solid var(--border);",
    'glossary-item background'
)

rep(
    "    .bib-item {\n      background: var(--surface-2);\n      border: 1px solid var(--border);",
    "    .bib-item {\n      background: var(--panel);\n      border: 1px solid var(--border);",
    'bib-item background'
)

rep(
    "    .weakest-link-card {\n      background: var(--surface-2);\n      border: 1px solid var(--border);",
    "    .weakest-link-card {\n      background: var(--panel);\n      border: 1px solid var(--border);",
    'weakest-link-card background'
)

rep(
    "    .scenario-card {\n      background: var(--surface-2);\n      border: 1px solid var(--border);",
    "    .scenario-card {\n      background: var(--panel);\n      border: 1px solid var(--border);",
    'scenario-card background'
)

rep(
    "      background: var(--surface-2);\n      border: 1.5px solid var(--border);\n      border-radius: var(--radius-md);\n      padding: 0.8rem 1rem;\n      font-size: 0.83rem;\n      color: var(--text-muted);",
    "      background: var(--panel);\n      border: 1.5px solid var(--border);\n      border-radius: var(--radius-md);\n      padding: 0.8rem 1rem;\n      font-size: 0.83rem;\n      color: var(--text-dim);",
    'q-option-btn background+colour'
)

# ==============================================================================
# 4. Assessment progress bar and tier badge
# ==============================================================================

rep(
    "      background: var(--accent);\n      border-radius: 2px;\n      transition: width 0.3s ease;",
    "      background: linear-gradient(90deg, var(--grammar) 0%, var(--rhetoric) 100%);\n      border-radius: 2px;\n      transition: width 0.3s ease;",
    'progress-bar-fill gradient'
)

rep(
    "    .q-tier-badge.knowledge   { background: var(--cyan-dim);   color: var(--cyan); }",
    "    .q-tier-badge.knowledge   { background: var(--accent-dim); color: var(--grammar); }",
    'q-tier-badge knowledge colour'
)

# ==============================================================================
# 5. Footer CSS — full-width DC-LEARN bar
# ==============================================================================

rep(
    "    .app-footer {\n      background: var(--surface);\n      border-top: 1px solid var(--border);\n      padding: 0.9rem 1.5rem;\n      display: flex;\n      align-items: center;\n      justify-content: space-between;\n      flex-wrap: wrap;\n      gap: 0.5rem;\n    }\n    .footer-text { font-size: 0.72rem; color: var(--text-faint); }\n    .footer-version {\n      font-size: 0.67rem;\n      font-family: var(--font-mono);\n      color: var(--text-faint);\n      background: var(--surface-2);\n      padding: 2px 8px;\n      border-radius: 4px;\n    }",
    "    .app-footer {\n      background: var(--panel);\n      border-top: 1px solid var(--border);\n      padding: 1rem 1.5rem;\n      width: 100%;\n    }\n    .footer-inner {\n      max-width: 1100px;\n      margin: 0 auto;\n      display: flex;\n      align-items: center;\n      justify-content: space-between;\n      flex-wrap: wrap;\n      gap: 0.75rem;\n    }\n    .footer-left { display: flex; flex-direction: column; gap: 3px; }\n    .footer-right { display: flex; align-items: center; gap: 1rem; }\n    .footer-copyright { font-size: 0.72rem; color: var(--text-muted); }\n    .footer-cta { font-size: 0.72rem; color: var(--text-dim); font-style: italic; }\n    .footer-contact { font-size: 0.72rem; color: var(--text-muted); }\n    .footer-version {\n      font-size: 0.67rem;\n      font-family: var(--font-mono);\n      color: var(--text-muted);\n      background: var(--surface);\n      border: 1px solid var(--border);\n      padding: 2px 8px;\n      border-radius: 4px;\n    }",
    'footer CSS'
)

# ==============================================================================
# Write output
# ==============================================================================
with open(DEST, 'w', encoding='utf-8') as f:
    f.write(html)

lines = html.count('\n')
print(f"OK  {DEST.split('/')[-1]} written  ({lines} lines)")
print(f"    {len(replaced)} replacements applied:")
for r in replaced:
    print(f"      \u2713 {r}")
