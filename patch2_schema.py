"""
Patch 2: Replace INPUT_SCHEMA with 17 cooling chain fields.
         Demo = Example Facility, Dublin (no Clonshaugh).
"""
import sys

DST = 'tools/DC-TOOL-002_v2_0_0.html'
with open(DST, encoding='utf-8') as f:
    h = f.read()

OLD = """/* ================================================================
   INPUT_SCHEMA — Same as v1.0 (DC-Screen aligned)
   ================================================================ */
const INPUT_SCHEMA = [
  { id:'facility_name',    label:'Facility Name',           type:'text',   required:true,  demo:'Example Facility',  hint:'Internal reference name', unit:null },
  { id:'location',         label:'Location',                type:'text',   required:false, demo:'Dublin',            hint:'City or area',            unit:null },
  { id:'build_year',       label:'Year Built',              type:'number', required:true,  demo:2013,                hint:'Original commissioning',  unit:null, min:1990, max:2026 },
  { id:'it_load_mw',       label:'IT Load',                 type:'number', required:true,  demo:2.4,                 hint:'Total IT load', unit:'MW', min:0, max:200, step:0.1 },
  { id:'rack_count',       label:'Rack Count',              type:'number', required:true,  demo:400,                 hint:'Total populated racks',   unit:'racks', min:1, max:10000 },
  { id:'rack_density_kw',  label:'Average Rack Density',    type:'number', required:false, demo:6,                   hint:'Average kW per rack',     unit:'kW/rack', min:1, max:100, step:0.5 },
  { id:'pue',              label:'Current PUE',             type:'number', required:true,  demo:1.50,                hint:'Annualised PUE from metering', unit:null, min:1.0, max:3.0, step:0.01 },
  { id:'mic_kva',          label:'MIC',                     type:'number', required:false, demo:5000,                hint:'Maximum Import Capacity', unit:'kVA', min:0, max:200000, step:100 },
  { id:'voltage_kv',       label:'Supply Voltage',          type:'select', required:false, demo:'10',                hint:'ESB Networks supply',  unit:'kV', options:['10','20','38','110'] },
  { id:'cooling_type',     label:'Primary Cooling',         type:'select', required:true,  demo:'air_crac',          hint:'Main cooling technology', unit:null, options:[
    {value:'air_crac',label:'DX CRAC'},{value:'air_free',label:'Air-side Free Cooling'},{value:'chilled_water',label:'Chilled Water'},{value:'evaporative',label:'Evaporative/Adiabatic'},{value:'hybrid_dlc',label:'Hybrid DLC'},{value:'full_dlc',label:'Full DLC'},{value:'immersion',label:'Immersion'}
  ]},
  { id:'redundancy_level', label:'Power Redundancy',        type:'select', required:true,  demo:'n_plus_1',          hint:'UPS/generator topology',  unit:null, options:[
    {value:'n',label:'N'},{value:'n_plus_1',label:'N+1'},{value:'two_n',label:'2N'},{value:'two_n_plus_1',label:'2N+1'}
  ]},
  { id:'generator_fuel',   label:'Generator Fuel',          type:'select', required:false, demo:'diesel',            hint:'Backup fuel type', unit:null, options:[
    {value:'diesel',label:'Diesel'},{value:'gas',label:'Natural Gas'},{value:'hvo',label:'HVO'}
  ]},
  { id:'generator_hours',  label:'Generator Run Hours',     type:'number', required:false, demo:200,                 hint:'Annual run hours', unit:'hrs/yr', min:0, max:8760, step:10 },
  { id:'ppa_pct',          label:'Renewable Energy',        type:'number', required:false, demo:45,                  hint:'% from all renewable sources', unit:'%', min:0, max:100 },
  { id:'hall_config',      label:'Hall Configuration',      type:'text',   required:false, demo:'Hall A, Hall B',    hint:'Hall names/layout',       unit:null },
  { id:'total_floor_m2',   label:'Whitespace Area',         type:'number', required:false, demo:1800,                hint:'Total raised floor area', unit:'m²', min:0, max:100000 }
];"""

NEW = """/* ================================================================
   INPUT_SCHEMA — 17 fields (DC_TOOL_002_CALC_ENGINE_v2_0.md)
   ================================================================ */
const INPUT_SCHEMA = [
  { id:'facility_name',         label:'Facility Name',              type:'text',   required:true,  demo:'Example Facility, Dublin', hint:'Internal reference name',             unit:null },
  { id:'location',              label:'Location',                   type:'text',   required:true,  demo:'Dublin, Ireland',          hint:'City or country',                     unit:null },
  { id:'build_year',            label:'Year Built',                 type:'number', required:true,  demo:2013,    hint:'Original commissioning year',   unit:null,     min:1990, max:2026 },
  { id:'it_load_mw',            label:'IT Load',                    type:'number', required:true,  demo:2.4,     hint:'Total IT load',                  unit:'MW',     min:0.1, max:200, step:0.1 },
  { id:'pue',                   label:'Current PUE',                type:'number', required:true,  demo:1.50,    hint:'Annualised PUE from metering',   unit:null,     min:1.0, max:3.0, step:0.01 },
  { id:'cooling_type',          label:'Primary Cooling Technology', type:'select', required:true,  demo:'air_crac', hint:'Main cooling technology in use', unit:null, options:[
    {value:'air_crac',label:'DX CRAC / CRAH'},{value:'air_free',label:'Air-side Free Cooling'},{value:'chilled_water',label:'Chilled Water CRAH'},{value:'evaporative',label:'Evaporative / Adiabatic'},{value:'hybrid_dlc',label:'Hybrid DLC'},{value:'full_dlc',label:'Full Direct Liquid Cooling'},{value:'immersion',label:'Immersion Cooling'}
  ]},
  { id:'has_free_cooling',      label:'Free Cooling / Economiser',  type:'select', required:true,  demo:'no',    hint:'Air-side or fluid economiser installed', unit:null, options:[
    {value:'yes',label:'Yes — full economiser in service'},{value:'partial',label:'Partial — some capacity only'},{value:'no',label:'No — no economiser'}
  ]},
  { id:'has_containment',       label:'Aisle Containment',          type:'select', required:true,  demo:'no',    hint:'Hot-aisle or cold-aisle containment',    unit:null, options:[
    {value:'yes',label:'Yes — full containment'},{value:'partial',label:'Partial — some aisles only'},{value:'no',label:'No — open floor plan'}
  ]},
  { id:'supply_temp_c',         label:'Supply Air Temperature',     type:'number', required:false, demo:18,      hint:'CRAC/CRAH supply air setpoint',  unit:'°C',     min:10, max:35, step:0.5 },
  { id:'chiller_count',         label:'Chiller Count',              type:'number', required:false, demo:3,       hint:'Number of chillers installed',   unit:null,     min:0, max:20 },
  { id:'chiller_kw_each',       label:'Chiller Capacity (each)',    type:'number', required:false, demo:500,     hint:'Cooling capacity per chiller',   unit:'kW',     min:0, max:10000 },
  { id:'chiller_type',          label:'Chiller Type',               type:'select', required:false, demo:'air_cooled', hint:'Heat rejection method',     unit:null, options:[
    {value:'air_cooled',label:'Air-Cooled Chiller'},{value:'water_cooled',label:'Water-Cooled + Cooling Tower'},{value:'dry_cooler',label:'Dry Cooler'},{value:'adiabatic',label:'Adiabatic Cooler'}
  ]},
  { id:'refrigerant_type',      label:'Primary Refrigerant',        type:'select', required:false, demo:'r410a', hint:'Main refrigerant across cooling units', unit:null, options:[
    {value:'r410a',label:'R410A (GWP 2,088)'},{value:'r407c',label:'R407C (GWP 1,774)'},{value:'r134a',label:'R134a (GWP 1,430)'},{value:'r32',label:'R32 (GWP 675)'},{value:'r1234ze',label:'R1234ze (GWP 7)'},{value:'none',label:'No refrigerant (water/DLC)'}
  ]},
  { id:'refrigerant_charge_kg', label:'Total Refrigerant Charge',   type:'number', required:false, demo:192,     hint:'Total charge across all cooling units', unit:'kg', min:0, max:10000 },
  { id:'has_water_meter',       label:'Cooling Water Metered?',     type:'select', required:false, demo:'no',    hint:'Sub-meter on cooling water supply',     unit:null, options:[
    {value:'yes',label:'Yes — sub-metered'},{value:'no',label:'No — unmetered'},{value:'na',label:'N/A — no water-cooled equipment'}
  ]},
  { id:'ppa_pct',               label:'Renewable Energy',           type:'number', required:false, demo:45,      hint:'% from renewable sources (PPA/GOs)',   unit:'%',  min:0, max:100 },
  { id:'total_floor_m2',        label:'Whitespace Area',            type:'number', required:false, demo:1800,    hint:'Total raised floor / whitespace area',  unit:'m²', min:0, max:100000 }
];"""

if OLD not in h:
    print("ERROR: INPUT_SCHEMA old block not found!")
    # Show what we have around that area
    idx = h.find('INPUT_SCHEMA — ')
    if idx != -1:
        print(repr(h[idx-5:idx+200]))
    import sys; sys.exit(1)

h = h.replace(OLD, NEW, 1)
print(f"Patch 2 (INPUT_SCHEMA) done. Lines: {h.count(chr(10))+1}")

with open(DST, 'w', encoding='utf-8') as f:
    f.write(h)
