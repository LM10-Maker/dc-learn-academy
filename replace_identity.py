with open("/home/user/dc-learn-academy/DC-AI-001_v3_0_0.html", encoding='utf-8') as f:
    h = f.read()

def rep(old, new, label=""):
    count = h.count(old)
    if count == 0:
        print(f"WARN: not found: {repr(old[:60])}")
    else:
        print(f"  {label or 'OK'}: {count}x {repr(old[:50])}")
    return h.replace(old, new)

# 1. Title / meta
h = rep('<title>DC-LEARN-002 v5.13.7 | Data Centre Cooling Chain | Legacy Business Engineers</title>',
        '<title>DC-AI-001 v3.0.0 | Data Centre Power Density | Legacy Business Engineers</title>', 'title')
h = rep('/* --- DC-LEARN-002 v5.13.7 - Data Centre Cooling Chain ---',
        '/* --- DC-AI-001 v3.0.0 - Data Centre Power Density ---', 'comment')

# 2. Core constants
h = rep("var MODULE_TITLE = 'Cooling Chain';", "var MODULE_TITLE = 'Power Density';", 'MODULE_TITLE')
h = rep('const TOOL_ID = "DC-LEARN-002";', 'const TOOL_ID = "DC-AI-001";', 'TOOL_ID')
h = rep('const TOOL_VERSION = "5.13.7";', 'const TOOL_VERSION = "3.0.0";', 'TOOL_VERSION')

# 3. Storage keys (dc002_ → dc_ai_001_)
h = rep("'dc002_progress'", "'dc_ai_001_progress'", 'dc002_progress')
h = rep("'dc002_persona'",  "'dc_ai_001_persona'",  'dc002_persona')
h = rep("'dc002_tabTimes'", "'dc_ai_001_tabTimes'", 'dc002_tabTimes')
h = rep("'dc002_assess'",   "'dc_ai_001_assess'",   'dc002_assess')
h = rep('"dc002_assess"',   '"dc_ai_001_assess"',   'dc002_assess_dq')
h = rep("'dc002_cert_name'","'dc_ai_001_cert_name'","dc002_cert")
h = rep('"dc002_engage"',   '"dc_ai_001_engage"',   'dc002_engage')
h = rep("const DC_TIMING_KEY = 'dc002_timing';", "const DC_TIMING_KEY = 'dc_ai_001_timing';", 'DC_TIMING_KEY')

# 4. Personas constant and keys
h = rep('const PERSONAS = {declan:"Declan (Ops Manager)",ann:"Ann (Fund Manager)",mark:"Mark (MEP Engineer)",sarah:"Sarah (ESG Analyst)",tom:"Tom (QS / Cost Manager)"};',
        'const PERSONAS = {conor:"Conor (Asset Manager)",helena:"Helena (Chief Technology Officer)",eoin:"Eoin (MEP Retrofit Engineer)",rachel:"Rachel (ESG & Regulatory Director)",padraig:"Padraig (Project QS / Cost Manager)"};', 'PERSONAS')
h = rep('const PERSONA_KEYS = ["declan","ann","mark","sarah","tom"];',
        'const PERSONA_KEYS = ["conor","helena","eoin","rachel","padraig"];', 'PERSONA_KEYS')

# 5. PERSONA_MAP (two occurrences — both same string)
old_pm = "const PERSONA_MAP = {ann:{label:'Fund Manager',icon:'\U0001f4bc',stage:'rhetoric',preview:true},mark:{label:'MEP Engineer',icon:'\U0001f527',stage:'grammar',preview:false},declan:{label:'Ops Manager',icon:'\U0001f477',stage:'logic',preview:true},sarah:{label:'ESG Analyst',icon:'\U0001f331',stage:'rhetoric',preview:true},tom:{label:'QS / Cost Manager',icon:'\U0001f4ca',stage:'logic',preview:true}};"
new_pm = "const PERSONA_MAP = {conor:{label:'Asset Manager',icon:'\U0001f4bc',stage:'rhetoric',preview:true},helena:{label:'Chief Technology Officer',icon:'\U0001f5a5',stage:'grammar',preview:false},eoin:{label:'MEP Retrofit Engineer',icon:'\U0001f527',stage:'grammar',preview:false},rachel:{label:'ESG & Regulatory Director',icon:'\U0001f331',stage:'rhetoric',preview:true},padraig:{label:'Project QS / Cost Manager',icon:'\U0001f4ca',stage:'logic',preview:true}};"
h = rep(old_pm, new_pm, 'PERSONA_MAP')

# 6. Hero heading and sub-text in App render
h = rep('<h1>Data Centre Cooling Chain</h1>',
        '<h1>Data Centre Power Density</h1>', 'hero h1')
h = rep('Fictional reference facility — 9 levels from ambient air to precision cooling',
        'Fictional reference facility (Clonshaugh DC) — 9 levels of power density from server to infrastructure', 'hero sub')
h = rep('React.createElement(\'p\',null,\'DC-LEARN-002 v5.13.7 \xb7 Data Centre Cooling Chain\')',
        'React.createElement(\'p\',null,\'DC-AI-001 v3.0.0 \xb7 Data Centre Power Density\')', 'createElement p')

# 7. Tab labels
h = rep("{id:'chain',label:'Cooling Chain'}", "{id:'chain',label:'Power Density'}", 'tab chain')
h = rep("chain:'Cooling Chain'", "chain:'Power Density'", 'tabLabels chain')

# 8. Series nav
h = rep('<a href="./dc-learn-001.html">\u2190 DC-LEARN-001: Power Distribution</a>',
        '<span style={{color:\'var(--text-muted)\'}}>← No previous module</span>', 'nav prev')
h = rep("Module 2 of 16 \xb7 Series Spec v1.4",
        "Module 1 of 8 \xb7 DC-AI Series v1.0", 'nav pos')
h = rep('<a href="./dc-learn-003.html">DC-LEARN-003: Redundancy &amp; Topology \u2192</a>',
        '<a href="./dc-ai-002.html">DC-AI-002: Power Distribution \u2192</a>', 'nav next')

# 9. Inline mentions of old tool
h = rep('DC-LEARN-002 v5.13.7 \xb7 Data Centre Cooling Chain',
        'DC-AI-001 v3.0.0 \xb7 Data Centre Power Density', 'inline mention')

with open("/home/user/dc-learn-academy/DC-AI-001_v3_0_0.html", 'w', encoding='utf-8') as f:
    f.write(h)
print("\nScript 3 complete.")
