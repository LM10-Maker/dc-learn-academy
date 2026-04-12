"""patch_04_two_column.py — 2-column layout CSS + sidebar shell in App"""
F = "DC-AI-001_v2_0_0.html"

CSS = """
    /* ─── TWO-COLUMN LAYOUT ─────────────────────────────────────── */
    .content-with-sidebar {
      display: grid;
      grid-template-columns: 1fr 300px;
      gap: 0;
      flex: 1;
      align-items: start;
      max-width: 1200px;
      width: 100%;
      margin: 0 auto;
    }
    .main-col { min-width: 0; }
    .sidebar-col {
      border-left: 1px solid var(--border);
      padding: 1.25rem 1rem;
      display: flex;
      flex-direction: column;
      gap: 1rem;
      position: sticky;
      top: 0;
      max-height: 100vh;
      overflow-y: auto;
    }
    .sidebar-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 1rem;
    }
    .sidebar-card-title {
      font-size: 0.8rem;
      font-weight: 600;
      color: var(--text-bright);
      margin-bottom: 0.6rem;
      padding-bottom: 0.4rem;
      border-bottom: 1px solid var(--border);
    }
    @media (max-width: 900px) {
      .content-with-sidebar { grid-template-columns: 1fr; }
      .sidebar-col { display: none; }
    }
"""

# Replace `<main className="main-content">{renderTab()}</main>` with 2-col wrapper
OLD_MAIN = '      {/* Main content */}\n      <main className="main-content">\n        {renderTab()}\n      </main>'
NEW_MAIN = '''      {/* Two-column: main + sidebar */}
      <div className="content-with-sidebar">
        <main className="main-col main-content">
          {renderTab()}
        </main>
        <aside className="sidebar-col">
          <SidebarCalculator selectedLevel={levelIdx} />
          <SidebarFacility />
          <SidebarMethodology />
        </aside>
      </div>'''

html = open(F, encoding="utf-8").read()
assert "/* ─── RESET & BASE" in html
assert OLD_MAIN in html, f"Main anchor not found"

html = html.replace("    /* ─── RESET & BASE", CSS + "    /* ─── RESET & BASE", 1)
html = html.replace(OLD_MAIN, NEW_MAIN, 1)
open(F, "w", encoding="utf-8").write(html)
print("patch_04 done — 2-column layout applied")
