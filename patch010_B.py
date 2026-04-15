"""
Patch B for DC-TOOL-010 v2.0.0
Replace INPUT_SCHEMA array with 14-field facility audit schema.
"""
import sys

DST = 'tools/DC-TOOL-010_v2_0_0.html'
with open(DST, encoding='utf-8') as f:
    h = f.read()

OLD_SCHEMA_START = """/* ================================================================
   INPUT_SCHEMA — Same as v1.0 (DC-Screen aligned)
   ================================================================ */
const INPUT_SCHEMA = ["""

OLD_SCHEMA_END = """];

const DEMO_DATA = {};"""

NEW_SCHEMA = """/* ================================================================
   INPUT_SCHEMA — 14 fields (DC-TOOL-010 v2.0 Facility Audit Checklist)
   Source: DC_TOOL_010_CALC_ENGINE_v2_0.md
   ================================================================ */
const INPUT_SCHEMA = [
  { id:'facility_name',       label:'Facility Name',              type:'text',   required:true,  demo:'Example Facility',    hint:'Internal reference name', unit:null },
  { id:'location',            label:'Location',                   type:'text',   required:true,  demo:'Dublin, Ireland',     hint:'City or area', unit:null },
  { id:'build_year',          label:'Year Built',                 type:'number', required:true,  demo:2013,                  hint:'Original commissioning year', unit:null, min:1990, max:2026 },
  { id:'it_load_mw',          label:'IT Load',                    type:'number', required:true,  demo:2.4,                   hint:'Total IT load', unit:'MW', min:0.1, max:100, step:0.1 },
  { id:'pue',                 label:'Current PUE',                type:'number', required:true,  demo:1.50,                  hint:'Annualised PUE from metering', unit:null, min:1.0, max:3.0, step:0.01 },
  { id:'racks',               label:'Number of Racks',            type:'number', required:true,  demo:400,                   hint:'Total populated racks', unit:'racks', min:10, max:10000 },
  { id:'kw_per_rack',         label:'Average kW per Rack',        type:'number', required:true,  demo:6,                     hint:'Current average kW per rack', unit:'kW/rack', min:1, max:100, step:0.5 },
  { id:'target_kw_rack',      label:'Target kW per Rack',         type:'number', required:true,  demo:20,                    hint:'Planned upgrade density', unit:'kW/rack', min:1, max:100, step:0.5 },
  { id:'mic_mva',             label:'MIC',                        type:'number', required:true,  demo:5,                     hint:'Maximum Import Capacity', unit:'MVA', min:0.1, max:200, step:0.1 },
  { id:'ppa_pct',             label:'Renewable Energy Coverage',  type:'number', required:true,  demo:0,                     hint:'% from PPA or GOs', unit:'%', min:0, max:100 },
  { id:'cooling_type',        label:'Primary Cooling',            type:'select', required:true,  demo:'chiller_only',        hint:'Main cooling technology', unit:null, options:[
    {value:'chiller_only', label:'Chiller only (no free cooling)'},
    {value:'chiller_fc',   label:'Chiller + free cooling'},
    {value:'dx',           label:'Direct expansion (DX)'},
    {value:'evaporative',  label:'Evaporative / adiabatic'}
  ]},
  { id:'cooling_capacity_mw', label:'Cooling Capacity',           type:'number', required:true,  demo:3,                     hint:'Total installed cooling plant capacity', unit:'MW', min:0.1, max:50, step:0.1 },
  { id:'bms_points',          label:'BMS Points (approx)',         type:'number', required:false, demo:500,                   hint:'Approximate number of BMS monitoring points', unit:'pts', min:0, max:50000, step:100 },
  { id:'grid_feed',           label:'Grid Feed Type',             type:'select', required:true,  demo:'single_mv',           hint:'ESB Networks supply configuration', unit:null, options:[
    {value:'single_mv',    label:'Single MV (10 kV)'},
    {value:'dual_mv',      label:'Dual MV (10 kV)'},
    {value:'hv',           label:'HV (38 kV)'},
    {value:'transmission', label:'Transmission (110 kV)'}
  ]}
];

const DEMO_DATA = {};"""

idx_start = h.find(OLD_SCHEMA_START)
if idx_start == -1:
    print("ERROR: INPUT_SCHEMA start not found!")
    sys.exit(1)
idx_end = h.find(OLD_SCHEMA_END, idx_start)
if idx_end == -1:
    print("ERROR: DEMO_DATA separator not found!")
    sys.exit(1)

old_block = h[idx_start : idx_end + len(OLD_SCHEMA_END)]
h = h[:idx_start] + NEW_SCHEMA + h[idx_start + len(old_block):]
print(f"Patch B (INPUT_SCHEMA) done: replaced {len(old_block)} chars with {len(NEW_SCHEMA)} chars")

with open(DST, 'w', encoding='utf-8') as f:
    f.write(h)
print(f"Saved. Lines: {h.count(chr(10)) + 1}")
