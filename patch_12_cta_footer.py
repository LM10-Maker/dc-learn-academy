"""patch_12_cta_footer.py — replace single-line footer with two-column CTA + 2-tier footer"""
F = "DC-AI-001_v2_0_0.html"

CSS = """
    /* ─── CTA SECTION ───────────────────────────────────────────── */
    .cta-section {
      display: grid; grid-template-columns: 1fr 1fr;
      gap: 1rem; padding: 1.5rem;
      background: var(--surface); border-top: 1px solid var(--border);
    }
    .cta-card {
      background: var(--panel); border: 1px solid var(--border);
      border-radius: var(--radius-md); padding: 1.1rem;
    }
    .cta-card h4 { font-size: 0.88rem; font-weight: 600; color: var(--text-bright); margin-bottom: 0.35rem; }
    .cta-card p  { font-size: 0.78rem; color: var(--text-muted); line-height: 1.5; margin-bottom: 0.75rem; }
    .cta-btn {
      display: inline-block; padding: 7px 16px;
      border-radius: var(--radius-sm); font-size: 0.78rem; font-weight: 600;
      border: 1px solid var(--lbe-green); color: var(--lbe-green);
      background: rgba(22,163,74,0.06); text-decoration: none;
      transition: all var(--transition);
    }
    .cta-btn:hover { background: rgba(22,163,74,0.15); text-decoration: none; }
    /* ─── FOOTER 2-TIER ─────────────────────────────────────────── */
    .footer-nav-row {
      display: flex; align-items: center; justify-content: space-between;
      padding: 0.7rem 1.5rem; background: var(--surface);
      border-top: 1px solid var(--border); font-size: 0.78rem;
    }
    .footer-nav-link {
      color: var(--text-dim); padding: 4px 10px; border: 1px solid var(--border);
      border-radius: 14px; font-size: 0.75rem; transition: all var(--transition);
    }
    .footer-nav-link.disabled { opacity: 0.35; pointer-events: none; }
    .footer-nav-link:hover { background: var(--panel); text-decoration: none; }
    .footer-copy-row {
      display: flex; align-items: center; justify-content: space-between;
      padding: 0.5rem 1.5rem; background: var(--panel);
      border-top: 1px solid var(--border); font-size: 0.72rem;
    }
    @media (max-width: 600px) {
      .cta-section { grid-template-columns: 1fr; }
    }
"""

OLD_FOOTER = """      {/* Footer */}
      <footer className="app-footer">
        <div className="footer-inner">
          <div className="footer-left">
            <span className="footer-copyright">&copy; 2026 Legacy Business Engineers Ltd &middot; DC-AI Series &middot; Module 1 of 8</span>
            <span className="footer-cta">Need to know where your facility stands on AI readiness?</span>
          </div>
          <div className="footer-right">
            <a href="mailto:lmurphy@legacybe.ie" className="footer-contact">lmurphy@legacybe.ie</a>
            <span className="footer-version">DC-AI-001 v{TOOL_VERSION}</span>
          </div>
        </div>
      </footer>"""

NEW_FOOTER = r"""      {/* CTA section */}
      <div className="cta-section">
        <div className="cta-card">
          <h4>Need to know where your facility stands on AI readiness?</h4>
          <p>Legacy Business Engineers delivers independent AI readiness assessments for data centre owners and asset managers across Ireland and the UK.</p>
          <a href="mailto:lmurphy@legacybe.ie" className="cta-btn">Learn about AI Readiness Assessment →</a>
        </div>
        <div className="cta-card">
          <h4>Questions or feedback on this content?</h4>
          <p>We improve every module based on feedback from practitioners. If something is wrong, unclear, or missing — tell us.</p>
          <a href="mailto:lmurphy@legacybe.ie" className="cta-btn">Send Us a Message</a>
        </div>
      </div>

      {/* Footer — 2-tier */}
      <div className="footer-nav-row">
        <span className="footer-nav-link disabled">← First module</span>
        <span style={{fontSize:'0.78rem',color:'var(--text-muted)',fontFamily:'var(--font-mono)'}}>Module 1 of 8 · DC-AI v{TOOL_VERSION}</span>
        <a href="#" className="footer-nav-link">DC-AI-002: Cooling →</a>
      </div>
      <div className="footer-copy-row">
        <span style={{color:'var(--text-muted)'}}>© 2026 Legacy Business Engineers Ltd</span>
        <span style={{display:'flex',gap:'1rem'}}>
          <a href="https://legacybe.ie" style={{color:'var(--text-dim)'}}>legacybe.ie</a>
          <a href="mailto:lmurphy@legacybe.ie" style={{color:'var(--text-dim)'}}>Contact</a>
        </span>
      </div>"""

html = open(F, encoding="utf-8").read()
assert OLD_FOOTER in html, "Footer anchor not found"
html = html.replace("    /* ─── RESET & BASE", CSS + "    /* ─── RESET & BASE", 1)
html = html.replace(OLD_FOOTER, NEW_FOOTER, 1)
open(F, "w", encoding="utf-8").write(html)
print("patch_12 done — two-column CTA + 2-tier footer applied")
