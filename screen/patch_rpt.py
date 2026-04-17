#!/usr/bin/env python3
"""
DC-RPT-001 Full WC A+ Audit Patch
Applies structural and content changes per spec.
"""

import re

SRC = '/home/user/dc-screen/DC-RPT-001_v1_0_3.html'

with open(SRC, 'r', encoding='utf-8') as f:
    c = f.read()

changes = []

# ═══════════════════════════════════════════════════════
# 1. FONTS — Google Fonts in <head>
# ═══════════════════════════════════════════════════════
OLD = '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
NEW = '''<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Sans+3:ital,wght@0,400;0,600;0,700;1,400&family=Source+Serif+4:wght@400;600&display=swap" rel="stylesheet">'''
assert c.count(OLD) == 1, f"FONT: expected 1 match, got {c.count(OLD)}"
c = c.replace(OLD, NEW); changes.append('1. Google Fonts added')

# ═══════════════════════════════════════════════════════
# 2. @page margins → 14mm sides
# ═══════════════════════════════════════════════════════
OLD = '    size: A4 portrait;\n    margin: 14mm 12mm 20mm 12mm;'
NEW = '    size: A4 portrait;\n    margin: 14mm 14mm 20mm 14mm;'
assert c.count(OLD) == 1
c = c.replace(OLD, NEW); changes.append('2. @page margins 14mm sides')

# ═══════════════════════════════════════════════════════
# 3. .a4-page padding → 14mm sides
# ═══════════════════════════════════════════════════════
OLD = '  padding: 14mm 12mm 20mm 12mm;\n  background: white;\n  position: relative;'
NEW = '  padding: 14mm 14mm 20mm 14mm;\n  background: white;\n  position: relative;'
assert c.count(OLD) == 1
c = c.replace(OLD, NEW); changes.append('3. .a4-page padding 14mm sides')

# ═══════════════════════════════════════════════════════
# 4. Cover CSS padding → 20mm 14mm 16mm 14mm
# ═══════════════════════════════════════════════════════
OLD = '  padding: 20mm 16mm 16mm 16mm;\n  background: white;\n  position: relative;'
NEW = '  padding: 20mm 14mm 16mm 14mm;\n  background: white;\n  position: relative;'
assert c.count(OLD) == 1
c = c.replace(OLD, NEW); changes.append('4. Cover CSS padding')

# ═══════════════════════════════════════════════════════
# 5. Cover print padding → 20mm 14mm 16mm 14mm
# ═══════════════════════════════════════════════════════
OLD = '    padding: 20mm 16mm 16mm 16mm;\n    min-height: 267mm; /* A4 minus @page margins */'
NEW = '    padding: 20mm 14mm 16mm 14mm;\n    min-height: 267mm; /* A4 minus @page margins */'
assert c.count(OLD) == 1
c = c.replace(OLD, NEW); changes.append('5. Cover print padding')

# ═══════════════════════════════════════════════════════
# 6. .page-footer CSS → 3-col grid
# ═══════════════════════════════════════════════════════
OLD = '''/* ---------- PAGE FOOTER ---------- */
.page-footer {
  position: absolute;
  bottom: 12mm;
  left: 12mm;
  right: 12mm;
  display: flex;
  justify-content: space-between;
  font-size: 7.5pt;
  color: var(--dc-gray-light);
  border-top: 1px solid #e5e7eb;
  padding-top: 6px;
}'''
NEW = '''/* ---------- PAGE FOOTER ---------- */
.page-footer {
  position: absolute;
  bottom: 6mm;
  left: 14mm;
  right: 14mm;
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 0;
  font-size: 7.5pt;
  color: var(--dc-gray-light);
  border-top: 1px solid #e5e7eb;
  padding-top: 6px;
}
.page-footer span:nth-child(2) { text-align: center; }
.page-footer span:last-child { text-align: right; }'''
assert c.count(OLD) == 1
c = c.replace(OLD, NEW); changes.append('6. .page-footer 3-col grid')

# ═══════════════════════════════════════════════════════
# 7. Remove position:fixed from .page-footer in @media print
# ═══════════════════════════════════════════════════════
OLD = '''  .page-footer {
    position: fixed;
  }

  .intensity-card .card-band,'''
NEW = '''  .intensity-card .card-band,'''
assert c.count(OLD) == 1
c = c.replace(OLD, NEW); changes.append('7. Remove position:fixed from print CSS')

# ═══════════════════════════════════════════════════════
# 8. TOOL_META version 1.2.0 → 1.2.1
# ═══════════════════════════════════════════════════════
OLD = "    version: '1.2.0',"
NEW = "    version: '1.2.1',"
assert c.count(OLD) == 1
c = c.replace(OLD, NEW); changes.append('8. TOOL_META version 1.2.1')

# ═══════════════════════════════════════════════════════
# 9. project_ref LBE-DC-CPS → LBE-SCR
# ═══════════════════════════════════════════════════════
OLD = "      project_ref: 'LBE-DC-CPS-2026-001',"
NEW = "      project_ref: 'LBE-SCR-2026-001',"
assert c.count(OLD) == 1
c = c.replace(OLD, NEW); changes.append('9. project_ref prefix LBE-SCR')

# ═══════════════════════════════════════════════════════
# 10. Cover "Prepared by" text
# ═══════════════════════════════════════════════════════
OLD = '        <div><strong>Prepared by:</strong> Legacy Business Engineers Ltd &mdash; <strong>CEng MIEI</strong></div>'
NEW = '        <div><strong>Prepared by:</strong> Les Murphy CEng MIEI MBA, Legacy Business Engineers Ltd</div>'
assert c.count(OLD) == 1
c = c.replace(OLD, NEW); changes.append('10. Cover Prepared by text')

# ═══════════════════════════════════════════════════════
# 11. RED 2 — remediation → retrofit, section title renames
# ═══════════════════════════════════════════════════════
OLD = '        <h2>Compliance Risk Register</h2>'
NEW = '        <h2>Regulatory Exposure Summary</h2>'
assert c.count(OLD) == 1
c = c.replace(OLD, NEW); changes.append('11a. Compliance Risk Register → Regulatory Exposure Summary')

OLD = '        <h2>Remediation Options &amp; Economics</h2>'
NEW = '        <h2>Retrofit Options &amp; Economics</h2>'
assert c.count(OLD) == 1
c = c.replace(OLD, NEW); changes.append('11b. Remediation Options → Retrofit Options')

OLD = 'produces a phased remediation programme'
NEW = 'produces a phased retrofit programme'
assert c.count(OLD) == 1
c = c.replace(OLD, NEW); changes.append('11c. phased remediation → phased retrofit')

# ═══════════════════════════════════════════════════════
# 12. RED 3 — Delivery time strings
# ═══════════════════════════════════════════════════════
OLD = "Delivered in 2\u20134 weeks.'"
NEW = "typically 6\u20138 weeks from receipt of data pack.'"
assert c.count(OLD) == 1
c = c.replace(OLD, NEW); changes.append('12a. Delivery 2-4 weeks → 6-8 weeks')

OLD = "Delivered in 2\u20133 weeks.'"
NEW = "typically 4\u20136 weeks.'"
assert c.count(OLD) == 1
c = c.replace(OLD, NEW); changes.append('12b. Delivery 2-3 weeks → 4-6 weeks')

# ═══════════════════════════════════════════════════════
# 13. AMBER 7 — old page2 header: update h1, subtitle, right panel
#     to use consistent "Asset Carbon Risk Screening" and page3 IDs
# ═══════════════════════════════════════════════════════
OLD = '''          <div class="header-titles">
            <h1>Carbon &amp; Regulatory Exposure — Investment Actions</h1>
            <div class="subtitle" id="rptFacilityName2">—</div>
          </div>
        </div>
        <div class="header-right">
          <span id="rptRef2">—</span>
        </div>'''
NEW = '''          <div class="header-titles">
            <h1>Asset Carbon Risk Screening</h1>
            <div class="subtitle">Investment Screening — Carbon, Regulatory &amp; Retrofit Economics</div>
          </div>
        </div>
        <div class="header-right">
          <strong id="rptFacilityName3">—</strong><br>
          <span id="rptDate3">—</span><br>
          <span id="rptRef3">—</span>
        </div>'''
assert c.count(OLD) == 1
c = c.replace(OLD, NEW); changes.append('13. Old page2 header → Asset Carbon Risk Screening + page3 IDs')

# ═══════════════════════════════════════════════════════
# 14. JS footer setText calls — update to new format and IDs
# ═══════════════════════════════════════════════════════
OLD = '''    // ── Page footers ──
    var footerDate = today;
    setText('footer1Left', 'DC-RPT-001 v1.2.1 | Asset Carbon Risk Screening | ' + footerDate);
    setText('footer2Left', 'DC-RPT-001 v1.2.1 | Asset Carbon Risk Screening | ' + footerDate);'''
NEW = '''    // ── Page footers + dynamic header elements ──
    var footerDate = today;
    var footerLeftText = 'Asset Carbon Risk Screening | Legacy Business Engineers Ltd | ' + footerDate;
    setText('footerP1Left', footerLeftText);
    setText('footerP2Left', footerLeftText);
    setText('footerP3Left', footerLeftText);
    setText('footerP4Left', footerLeftText);
    // Dynamic header metadata for pages 2, 3, 4
    setText('rptFacilityName2', inp.facility_name);
    setText('rptDate2', today);
    setText('rptRef2', inp.project_ref);
    setText('rptFacilityName3', inp.facility_name);
    setText('rptDate3', today);
    setText('rptRef3', inp.project_ref);
    setText('rptFacilityName4', inp.facility_name);
    setText('rptDate4', today);
    setText('rptRef4', inp.project_ref);
    // Set logos for dynamically-inserted page headers
    var dynLogos = document.querySelectorAll('.header-logo-dynamic');
    for (var di = 0; di < dynLogos.length; di++) { dynLogos[di].src = LOGO_SRC; }'''
assert c.count(OLD) == 1
c = c.replace(OLD, NEW); changes.append('14. JS footer setText calls updated')

# ═══════════════════════════════════════════════════════
# 15. JS: remove old rptFacilityName2/rptRef2 setText calls
#     (now handled in the footer block above)
# ═══════════════════════════════════════════════════════
OLD = '''    // ── Header (pages 1 & 2) ──
    setText('rptFacilityName', inp.facility_name);
    setText('rptDate', today);
    setText('rptRef', inp.project_ref);
    setText('rptFacilityName2', inp.facility_name);
    setText('rptRef2', inp.project_ref);'''
NEW = '''    // ── Header (page 1) ──
    setText('rptFacilityName', inp.facility_name);
    setText('rptDate', today);
    setText('rptRef', inp.project_ref);'''
assert c.count(OLD) == 1
c = c.replace(OLD, NEW); changes.append('15. Remove redundant old header setText calls')

# ═══════════════════════════════════════════════════════
# 16. STRUCTURAL — Rename old PAGE 2 comment and id to page3
# ═══════════════════════════════════════════════════════
OLD = '    <!-- ══════════════ PAGE 2: Exposure & Actions ══════════════ -->\n    <div class="a4-page page-break" id="page2">'
NEW = '    <!-- ══════════════ PAGE 3: Regulatory Exposure & Retrofit Options ══════════════ -->\n    <div class="a4-page page-break" id="page3">'
assert c.count(OLD) == 1
c = c.replace(OLD, NEW); changes.append('16. Old page2 renamed to page3')

# ═══════════════════════════════════════════════════════
# 17. STRUCTURAL — Split page1 at hold model
#     Replace hold model + CRREM + old footer with:
#     page1-footer + close page1 + new page2 (hold model + CRREM + page2-footer)
# ═══════════════════════════════════════════════════════
OLD = '''      <!-- 10-Year Hold Model — Scenario Comparison -->
      <div id="holdModelSection" style="margin-bottom:14px">
        <h2 style="font-size:13pt;margin-bottom:8px;padding-bottom:4px;border-bottom:1px solid #e5e7eb">10-Year Hold Model</h2>
        <div id="holdModelContent"></div>
      </div>

      <!-- CRREM Position -->
      <div class="crrem-section">
        <h2>Regulatory Alignment Status</h2>
        <div id="crremBox" class="crrem-box aligned">
          <div class="crrem-headline" id="crremHeadline">—</div>
          <div class="crrem-detail" id="crremDetail">—</div>
        </div>
      </div>

      <div class="page-footer">
        <span id="footer1Left">DC-RPT-001 v1.2.1 | Asset Carbon Risk Screening | —</span>
        <span>&copy; 2026 Legacy Business Engineers Ltd | Private &amp; Confidential</span>
      </div>
    </div>'''
NEW = '''      <div class="page-footer">
        <span id="footerP1Left">Asset Carbon Risk Screening | Legacy Business Engineers Ltd | —</span>
        <span>&copy; 2026 Legacy Business Engineers Ltd | Private &amp; Confidential</span>
        <span>Page 1 of 5</span>
      </div>
    </div>

    <!-- ══════════════ PAGE 2: Hold Model + CRREM Status ══════════════ -->
    <div class="a4-page page-break" id="page2">

      <div class="report-header">
        <div class="header-left">
          <img id="headerLogoP2" class="logo-circle header-logo-dynamic" alt="LBE Logo" onerror="this.style.display=\'none\'">
          <div class="header-titles">
            <h1>Asset Carbon Risk Screening</h1>
            <div class="subtitle">Investment Screening — Carbon, Regulatory &amp; Retrofit Economics</div>
          </div>
        </div>
        <div class="header-right">
          <strong id="rptFacilityName2">—</strong><br>
          <span id="rptDate2">—</span><br>
          <span id="rptRef2">—</span>
        </div>
      </div>

      <!-- 10-Year Hold Model — Scenario Comparison -->
      <div id="holdModelSection" style="margin-bottom:14px">
        <h2 style="font-size:13pt;margin-bottom:8px;padding-bottom:4px;border-bottom:1px solid #e5e7eb">10-Year Hold Model</h2>
        <div id="holdModelContent"></div>
      </div>

      <!-- CRREM Position -->
      <div class="crrem-section">
        <h2>Regulatory Alignment Status</h2>
        <div id="crremBox" class="crrem-box aligned">
          <div class="crrem-headline" id="crremHeadline">—</div>
          <div class="crrem-detail" id="crremDetail">—</div>
        </div>
      </div>

      <div class="page-footer">
        <span id="footerP2Left">Asset Carbon Risk Screening | Legacy Business Engineers Ltd | —</span>
        <span>&copy; 2026 Legacy Business Engineers Ltd | Private &amp; Confidential</span>
        <span>Page 2 of 5</span>
      </div>
    </div>'''
assert c.count(OLD) == 1, f"Page1 split: expected 1 match, got {c.count(OLD)}"
c = c.replace(OLD, NEW); changes.append('17. Page1 split — new page2 inserted')

# ═══════════════════════════════════════════════════════
# 18. STRUCTURAL — Split page3 at decision gate
#     Replace decision gate through end of page3 with:
#     page3-footer + close page3 + new page4 (decision gate + sign-off + page4-footer)
# ═══════════════════════════════════════════════════════
OLD = '''      <!-- Decision Gate — dynamic based on hold model -->
      <div class="next-step-box" id="nextStepBox">
        <h3 id="nextStepTitle">Recommended Next Step</h3>
        <p id="nextStepBody"></p>
        <div class="contact">Contact: info@legacybe.ie | legacybe.ie</div>
      </div>

      <!-- NOT CHECKED -->
      <div class="not-checked">
        <h4>NOT ASSESSED BY THIS SCREENING</h4>
        <ol>
          <li>Site-specific conditions not assessed (desktop screening only)</li>
          <li>Detailed MEP design, equipment specification, or tender documentation</li>
          <li>Uptime Institute certification assessment</li>
          <li>Environmental Impact Assessment or planning compliance</li>
          <li>Investment recommendation or financial advice</li>
        </ol>
      </div>

      <!-- Disclaimer -->
      <div class="disclaimer" id="disclaimerBlock">
        This Asset Carbon Risk Screening constitutes an independent desktop screening using published data and industry benchmarks. It is not a detailed design, Uptime Institute certification, Environmental Impact Assessment, planning application, or investment recommendation. All findings are indicative and subject to detailed design verification. Carbon intensity calculations use SEAI 2026 published grid emission factor (0.2241 kgCO&#8322;/kWh) and do not account for future grid decarbonisation. CRREM data centre pathway bands (200/300/400 kgCO&#8322;/MWh<sub>IT</sub>) are derived by LBE from the CRREM v2.01 commercial real estate methodology. CRREM has not published a sector-specific pathway for data centres. These bands are screening-level estimates (T3/T4) and should not be cited as CRREM-published values. CRREM misalignment year is a technical indicator &#8212; it does not predict financial impairment.
      </div>

      <!-- Sign-off -->
      <div class="signoff-grid">
        <div class="signoff-panel">
          <div class="signoff-title">Prepared by:</div>
          <div class="signoff-line"></div>
          <div style="font-size:8pt;color:#6b7280;margin-top:2px">Analyst</div>
          <div class="signoff-date">Date: ___________</div>
        </div>
        <div class="signoff-panel">
          <div class="signoff-title">Reviewed by:</div>
          <div class="signoff-line"></div>
          <div style="font-size:8pt;color:#6b7280;margin-top:2px">CEng MIEI</div>
          <div class="signoff-date">Date: ___________</div>
        </div>
        <div class="signoff-panel">
          <div class="signoff-title">Approved by:</div>
          <div class="signoff-line"></div>
          <div style="font-size:8pt;color:#6b7280;margin-top:2px">Director, CEng MIEI</div>
          <div class="signoff-date">Date: ___________</div>
        </div>
      </div>
      <div style="font-size:7.5pt;color:#9ca3af;text-align:center;margin-top:6px">
        Legacy Business Engineers Ltd &#8212; Professional Indemnity Insurance held &#8212; Intelligence layer only: this report identifies and quantifies, it does not design or deliver solutions.
      </div>

      <div class="page-footer">
        <span id="footer2Left">DC-RPT-001 v1.2.1 | Asset Carbon Risk Screening | —</span>
        <span>&copy; 2026 Legacy Business Engineers Ltd | Private &amp; Confidential</span>
      </div>
    </div>

  </div><!-- /report-wrap -->'''
NEW = '''      <div class="page-footer">
        <span id="footerP3Left">Asset Carbon Risk Screening | Legacy Business Engineers Ltd | —</span>
        <span>&copy; 2026 Legacy Business Engineers Ltd | Private &amp; Confidential</span>
        <span>Page 3 of 5</span>
      </div>
    </div>

    <!-- ══════════════ PAGE 4: Decision Gate + Sign-off ══════════════ -->
    <div class="a4-page page-break" id="page4">

      <div class="report-header">
        <div class="header-left">
          <img id="headerLogoP4" class="logo-circle header-logo-dynamic" alt="LBE Logo" onerror="this.style.display=\'none\'">
          <div class="header-titles">
            <h1>Asset Carbon Risk Screening</h1>
            <div class="subtitle">Investment Screening — Carbon, Regulatory &amp; Retrofit Economics</div>
          </div>
        </div>
        <div class="header-right">
          <strong id="rptFacilityName4">—</strong><br>
          <span id="rptDate4">—</span><br>
          <span id="rptRef4">—</span>
        </div>
      </div>

      <!-- Decision Gate — dynamic based on hold model -->
      <div class="next-step-box" id="nextStepBox">
        <h3 id="nextStepTitle">Recommended Next Step</h3>
        <p id="nextStepBody"></p>
        <div class="contact">Contact: info@legacybe.ie | legacybe.ie</div>
      </div>

      <!-- NOT CHECKED -->
      <div class="not-checked">
        <h4>NOT ASSESSED BY THIS SCREENING</h4>
        <ol>
          <li>Site-specific conditions not assessed (desktop screening only)</li>
          <li>Detailed MEP design, equipment specification, or tender documentation</li>
          <li>Uptime Institute certification assessment</li>
          <li>Environmental Impact Assessment or planning compliance</li>
          <li>Investment recommendation or financial advice</li>
        </ol>
      </div>

      <!-- Disclaimer -->
      <div class="disclaimer" id="disclaimerBlock">
        This Asset Carbon Risk Screening constitutes an independent desktop screening using published data and industry benchmarks. It is not a detailed design, Uptime Institute certification, Environmental Impact Assessment, planning application, or investment recommendation. All findings are indicative and subject to detailed design verification. Carbon intensity calculations use SEAI 2026 published grid emission factor (0.2241 kgCO&#8322;/kWh) and do not account for future grid decarbonisation. CRREM data centre pathway bands (200/300/400 kgCO&#8322;/MWh<sub>IT</sub>) are derived by LBE from the CRREM v2.01 commercial real estate methodology. CRREM has not published a sector-specific pathway for data centres. These bands are screening-level estimates (T3/T4) and should not be cited as CRREM-published values. CRREM misalignment year is a technical indicator &#8212; it does not predict financial impairment.
      </div>

      <!-- Sign-off — single block per spec RED 1 -->
      <div style="border:1px solid #d1d5db;border-radius:6px;padding:16px 20px;margin:14px 0;font-size:9.5pt">
        <div style="font-weight:600;color:#374151;margin-bottom:10px">Independent Technical Sign-off</div>
        <div style="margin-bottom:2px"><strong>Les Murphy CEng MIEI MBA</strong></div>
        <div style="color:#6b7280;margin-bottom:2px">Chartered Engineer | Independent Technical Advisor</div>
        <div style="color:#6b7280;margin-bottom:20px">Legacy Business Engineers Ltd</div>
        <div style="border-top:1px solid #1a1a1a;padding-top:4px;min-height:16px"></div>
        <div style="font-size:8pt;color:#6b7280;margin-top:4px">Date: ___________</div>
      </div>
      <div style="font-size:7.5pt;color:#9ca3af;text-align:center;margin-top:6px">
        Legacy Business Engineers Ltd &#8212; Professional Indemnity Insurance held &#8212; Intelligence layer only: this report identifies and quantifies, it does not design or deliver solutions.
      </div>

      <div class="page-footer">
        <span id="footerP4Left">Asset Carbon Risk Screening | Legacy Business Engineers Ltd | —</span>
        <span>&copy; 2026 Legacy Business Engineers Ltd | Private &amp; Confidential</span>
        <span>Page 4 of 5</span>
      </div>
    </div>

  </div><!-- /report-wrap -->'''
assert c.count(OLD) == 1, f"Page3 split: expected 1 match, got {c.count(OLD)}"
c = c.replace(OLD, NEW); changes.append('18. Page3 split — new page4 inserted')

# ═══════════════════════════════════════════════════════
# 19. Add page3 footer close tag to exposure+actions section
#     The page3 currently ends with the actions section then
#     immediately hits the page4 we just inserted above.
#     We need to add a footer for page3 between the actions
#     container close and the page4 start.
#     Actually: in change 18 we already added the footerP3Left
#     div at the start of the NEW string, before the page4 opening.
#     So page3's exposure/actions content is: from page3 open
#     through actionsContainer close, then the footerP3 div we
#     inserted appears BEFORE the decision gate. Perfect.
# ═══════════════════════════════════════════════════════
# No additional change needed — the footer is already inserted
# at the right place in change 18. The page3 div will close
# naturally after the footerP3Left div.
changes.append('19. Page3 footer placement confirmed (handled in 18)')

# ═══════════════════════════════════════════════════════
# Verify final structure
# ═══════════════════════════════════════════════════════
assert 'id="page0"' in c
assert 'id="page1"' in c
assert 'id="page2"' in c
assert 'id="page3"' in c
assert 'id="page4"' in c
assert 'footerP1Left' in c
assert 'footerP2Left' in c
assert 'footerP3Left' in c
assert 'footerP4Left' in c
assert 'Page 1 of 5' in c
assert 'Page 2 of 5' in c
assert 'Page 3 of 5' in c
assert 'Page 4 of 5' in c
assert 'Asset Carbon Risk Screening | Legacy Business Engineers Ltd' in c
assert 'LBE-SCR-2026-001' in c
assert "version: '1.2.1'" in c
assert 'Les Murphy CEng MIEI MBA' in c
assert 'Regulatory Exposure Summary' in c
assert 'Retrofit Options &amp; Economics' in c
assert 'phased retrofit programme' in c
assert '6\u20138 weeks from receipt of data pack' in c
assert '4\u20136 weeks' in c
assert 'Source+Sans+3' in c
assert 'Source+Serif+4' in c
# Negative checks
assert 'LBE-DC-CPS-2026-001' not in c
assert "version: '1.2.0'" not in c
assert 'Compliance Risk Register' not in c
assert 'Remediation Options' not in c
assert 'phased remediation programme' not in c
assert 'position: fixed' not in c  # removed from print CSS
assert 'footer1Left' not in c
assert 'footer2Left' not in c

with open(SRC, 'w', encoding='utf-8') as f:
    f.write(c)

print(f"SUCCESS — {len(changes)} changes applied:")
for ch in changes:
    print(f"  ✓ {ch}")
print(f"\nFile written: {SRC}")
print(f"Lines: {c.count(chr(10))}")
