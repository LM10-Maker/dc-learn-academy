#!/usr/bin/env python3
"""
polish2_03_cta.py
ITEM 3: CTA SECTION ABOVE FOOTER
Reads/writes DC-AI-001_v1_2_0.html
"""

WF = 'DC-AI-001_v1_2_0.html'

with open(WF, 'r', encoding='utf-8') as f:
    html = f.read()

# ─── 1. CSS ───────────────────────────────────────────────────────────────────
CSS = r"""
    /* ─── CTA SECTION ───────────────────────────────────────────────── */
    .cta-section {
      background: var(--panel);
      border-top: 1px solid var(--border);
      padding: 3rem 1.5rem;
      width: 100%;
    }
    .cta-inner {
      max-width: 1100px;
      margin: 0 auto;
      display: grid;
      grid-template-columns: 60fr 40fr;
      gap: 1.5rem;
    }
    .cta-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      padding: 1.5rem;
    }
    .cta-heading {
      font-size: 1rem;
      font-weight: 700;
      color: var(--text-bright);
      line-height: 1.4;
      margin-bottom: 0.6rem;
      letter-spacing: -0.01em;
    }
    .cta-body {
      font-size: 0.83rem;
      color: var(--text-muted);
      line-height: 1.65;
      margin-bottom: 1rem;
    }
    .cta-btn {
      display: inline-block;
      padding: 0.6rem 1.2rem;
      border-radius: var(--radius-md);
      font-size: 0.82rem;
      font-weight: 600;
      text-decoration: none;
      cursor: pointer;
      border: none;
      font-family: inherit;
    }
    .cta-btn:hover { opacity: 0.9; text-decoration: none; }
    .cta-btn-green   { background: var(--lbe-green); color: #fff; }
    .cta-btn-grammar { background: var(--grammar);   color: #fff; }
    @media (max-width: 680px) {
      .cta-inner { grid-template-columns: 1fr; }
      .cta-section { padding: 2rem 1rem; }
    }
"""

html = html.replace('  </style>', CSS + '  </style>', 1)

# ─── 2. CTASection component (insert before function App()) ──────────────────
COMPONENT = r"""
// ═══════════════════════════════════════════════════════════════
// CTA SECTION COMPONENT
// ═══════════════════════════════════════════════════════════════
function CTASection() {
  return (
    <section className="cta-section">
      <div className="cta-inner">
        <div className="cta-card">
          <div className="cta-heading">Need to know where your facility stands on AI readiness?</div>
          <div className="cta-body">From desktop screening (&euro;8,500) to full programme management (&euro;360,000) &mdash; LBE&rsquo;s service ladder starts where the platform stops.</div>
          <a href="https://legacybe.ie" className="cta-btn cta-btn-green" target="_blank" rel="noopener noreferrer">Learn about AI Readiness Assessment &#x2192;</a>
        </div>
        <div className="cta-card">
          <div className="cta-heading">Questions or feedback on this content?</div>
          <div className="cta-body">Technical corrections, suggestions, or industry perspective welcome.</div>
          <a href="mailto:lmurphy@legacybe.ie" className="cta-btn cta-btn-grammar">Send Us a Message &#x2192;</a>
        </div>
      </div>
    </section>
  );
}

"""

html = html.replace('function App() {', COMPONENT + 'function App() {', 1)

# ─── 3. Insert CTASection before footer in App return ────────────────────────
OLD_FOOTER = "      {/* Footer */}\n      <footer className=\"app-footer\">"
NEW_FOOTER = "      {/* CTA */}\n      <CTASection />\n\n      {/* Footer */}\n      <footer className=\"app-footer\">"

html = html.replace(OLD_FOOTER, NEW_FOOTER, 1)

# ─── 4. Verify ────────────────────────────────────────────────────────────────
assert 'CTASection' in html, "CTASection missing"
assert 'cta-section' in html, "cta-section CSS missing"
assert 'lmurphy@legacybe.ie' in html, "contact email missing"
assert html.count('"plain":') == 45, "grammar facts changed"
assert html.count('"correct":') == 27, "assessment questions changed"

with open(WF, 'w', encoding='utf-8') as f:
    f.write(html)

print("[03] OK — CTA section above footer added")
