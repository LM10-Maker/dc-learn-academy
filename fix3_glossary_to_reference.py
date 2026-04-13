#!/usr/bin/env python3
"""Fix 3: Remove GlossaryBibToggle from LearnTab bottom; BSGTab is already the reference tab."""

src = '/home/user/dc-learn-academy/DC-AI-001_v2_3_0 (3).html'
with open(src, 'r', encoding='utf-8') as f:
    html = f.read()

# Remove the GlossaryBibToggle block from the bottom of LearnTab
OLD3 = """      <div style={{marginTop:20}}>
        <GlossaryBibToggle/>
      </div>
    </div>
  );
}
// ═══════════════════════════════════════════════════════════════
// CHAIN TAB COMPONENT"""
NEW3 = """    </div>
  );
}
// ═══════════════════════════════════════════════════════════════
// CHAIN TAB COMPONENT"""
assert OLD3 in html, "Fix3: GlossaryBibToggle block in LearnTab not found"
html = html.replace(OLD3, NEW3, 1)

with open(src, 'w', encoding='utf-8') as f:
    f.write(html)
print("Fix 3 applied: GlossaryBibToggle removed from LearnTab; reference tab (BSGTab) unchanged.")
