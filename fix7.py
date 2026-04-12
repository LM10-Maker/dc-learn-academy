#!/usr/bin/env python3
"""Fix 7: Update left CTA copy.
Title: "From learning to practice"
Body: AI Readiness Assessment with pricing
Button: link to legacybe.ie
"""

with open('/home/user/dc-learn-academy/DC-AI-001_v2_1_0.html', 'r') as f:
    content = f.read()

old_left_cta = (
    '        <div className="cta-card">\n'
    '          <h4>Need to know where your facility stands on AI readiness?</h4>\n'
    '          <p>Legacy Business Engineers delivers independent AI readiness assessments for data centre owners and asset managers across Ireland and the UK.</p>\n'
    '          <a href="mailto:lmurphy@legacybe.ie" className="cta-btn">Learn about AI Readiness Assessment \u2192</a>\n'
    '        </div>'
)
new_left_cta = (
    '        <div className="cta-card">\n'
    '          <h4>From learning to practice</h4>\n'
    '          <p>The DC-AI series is built around Legacy Business Engineers\' AI Readiness Assessment — a structured on-site review covering power, cooling, structure, and grid capacity. Fixed-price from \u20ac4,500. Delivered within 10 working days.</p>\n'
    '          <a href="https://legacybe.ie" className="cta-btn" target="_blank" rel="noopener">Start Your Assessment \u2192</a>\n'
    '        </div>'
)
assert old_left_cta in content, "Left CTA card not found"
content = content.replace(old_left_cta, new_left_cta, 1)

with open('/home/user/dc-learn-academy/DC-AI-001_v2_1_0.html', 'w') as f:
    f.write(content)

print("Fix 7 applied: left CTA copy updated")
