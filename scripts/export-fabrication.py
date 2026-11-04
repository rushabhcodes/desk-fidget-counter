#!/usr/bin/env python3
"""SPDX-License-Identifier: MIT. Finalize a source-derived KiCad export with declared fab rules.
Requires KiCad 10 Python (pcbnew) and kicad-cli. No DRC exclusions are set.
"""
from pathlib import Path
import csv, json, subprocess, sys
import pcbnew
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'manufacturing'
OUT.mkdir(exist_ok=True)
raw=Path(sys.argv[1])
boardpath=OUT/'desk-knob-revd.kicad_pcb'
b=pcbnew.LoadBoard(str(raw))
# Keep boards alive while pcbnew's footprint/zone proxy objects are in scope.
loaded_boards=[b]
source=json.loads((ROOT/'dist/index/circuit.json').read_text())
expected={c['name'] for c in source if c['type']=='source_component'}
assert {f.GetReference() for f in b.GetFootprints() if f.GetReference()}==expected, 'Raw KiCad export is stale; export the current circuit JSON first'
# All coordinates and nets come from tscircuit; refill removes floating copper islands.
for priority,z in enumerate(b.Zones(),1):
    assert z.GetNetname()=='GND', 'Only the declared ground pours are expected'
    # Native pour fragments can touch/overlap on tessellated boundaries. Distinct
    # priorities let KiCad refill their common ground without ambiguous overlaps.
    z.SetAssignedPriority(priority)
    z.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_ALWAYS)
    z.SetLocalClearance(pcbnew.FromMM(.25))
# Keep the QFP corner marks clear of solder-mask openings. The library's
# 0.6mm corner strokes reach the pad-mask margins; shorten their inward ends.
for fp in b.GetFootprints():
    if fp.GetReference()=='U1':
        center=fp.GetPosition()
        for g in fp.GraphicalItems():
            if g.GetLayer()!=pcbnew.F_SilkS or g.GetShape()!=pcbnew.SHAPE_T_SEGMENT:continue
            a,z=g.GetStart(),g.GetEnd()
            length=((a.x-z.x)**2+(a.y-z.y)**2)**.5
            if length < pcbnew.FromMM(.5):continue
            da=(a.x-center.x)**2+(a.y-center.y)**2
            dz=(z.x-center.x)**2+(z.y-center.y)**2
            f=pcbnew.FromMM(.25)/length
            if da<dz:g.SetStart(pcbnew.VECTOR2I(round(a.x+f*(z.x-a.x)),round(a.y+f*(z.y-a.y))))
            else:g.SetEnd(pcbnew.VECTOR2I(round(z.x+f*(a.x-z.x)),round(z.y+f*(a.y-z.y))))
# Export the actual standalone footprints so library comparison is meaningful.
lib=OUT/'tscircuit.pretty'
lib.mkdir(exist_ok=True)
for old in lib.glob('*.kicad_mod'):old.unlink()
for fp in b.GetFootprints():
    item=fp.GetFPID()
    item.SetLibItemName(pcbnew.UTF8(str(item.GetLibItemName())+'__'+fp.GetReference()))
    fp.SetFPID(item)
    pcbnew.PCB_IO_MGR.FindPlugin(pcbnew.PCB_IO_MGR.KICAD_SEXP).FootprintSave(str(lib),fp)
(OUT/'fp-lib-table').write_text('(fp_lib_table (lib (name "tscircuit")(type "KiCad")(uri "${KIPRJMOD}/tscircuit.pretty")(options "")(descr "Generated from the tscircuit source")))\n')
project={
 'board':{'design_settings':{'rules':{
  'min_clearance':.15,'min_track_width':.1,'min_via_diameter':.6,
  'min_through_hole_diameter':.3,'min_hole_clearance':.25,'min_hole_to_hole':.5,
  'min_copper_edge_clearance':.3,'min_text_height':.8,'min_text_thickness':.12,'min_silk_clearance':.1}}},
 'net_settings':{'classes':[{'name':'Default','clearance':.15,'track_width':.15,
  'via_diameter':.6,'via_drill':.3,'microvia_diameter':.3,'microvia_drill':.1,
  'diff_pair_width':.15,'diff_pair_gap':.15,'diff_pair_via_gap':.15,'bus_width':12,
  'line_style':0,'pcb_color':'rgba(0, 0, 0, 0.000)','schematic_color':'rgba(0, 0, 0, 0.000)','wire_width':6}]}}
pcbnew.SaveBoard(str(boardpath),b)
boardpath.with_suffix('.kicad_pro').write_text(json.dumps(project,indent=2)+'\n')
# Remove only entire GND zones that KiCad identifies as electrically isolated.
# Native pour fragments can be isolated zones rather than islands of one zone;
# normal island removal alone does not eliminate these zone objects.
removed=[]
for attempt in range(3):
 boardpath.with_suffix('.kicad_pro').write_text(json.dumps(project,indent=2)+'\n')
 result=subprocess.run(['kicad-cli','pcb','drc',str(boardpath),'--refill-zones','--save-board',
  '--format','json','--output',str(ROOT/'validation/kicad-drc.json'),'--exit-code-violations'])
 r=json.loads((ROOT/'validation/kicad-drc.json').read_text())
 isolated={item['uuid'] for v in r['violations'] if v['type']=='isolated_copper' for item in v['items']}
 if not isolated:break
 b=pcbnew.LoadBoard(str(boardpath));loaded_boards.append(b);count=0
 for zone in list(b.Zones()):
  if zone.m_Uuid.AsString() in isolated:
   assert zone.GetNetname()=='GND','Only isolated ground fragments may be removed'
   removed.append({'zone_uuid':zone.m_Uuid.AsString(),'net':'GND','reason':'KiCad isolated_copper'})
   zone.thisown=False
   b.Remove(zone);count+=1
 assert count==len(isolated),'Cannot identify an isolated pour fragment'
 pcbnew.SaveBoard(str(boardpath),b)
(ROOT/'validation/pour-cleanup.json').write_text(json.dumps({'removed_isolated_ground_zones':removed},indent=2)+'\n')
assert not r['violations'] and not r['unconnected_items'], 'DRC is not clean'
gerbers=OUT/'gerbers';gerbers.mkdir(exist_ok=True)
for old in gerbers.glob('desk-knob-*'):old.unlink()
subprocess.run(['kicad-cli','pcb','export','gerbers',str(boardpath),'--output',str(gerbers)+'/',
 '--layers','F.Cu,B.Cu,F.Mask,B.Mask,F.Paste,B.Paste,F.Silkscreen,B.Silkscreen,Edge.Cuts',
 '--subtract-soldermask','--check-zones'],check=True)
subprocess.run(['kicad-cli','pcb','export','drill',str(boardpath),'--output',str(gerbers)+'/',
 '--format','excellon','--excellon-separate-th','--excellon-oval-format','route','--generate-map','--map-format','svg'],check=True)
subprocess.run(['kicad-cli','pcb','export','pos',str(boardpath),'--output',str(OUT/'pick-and-place.csv'),
 '--format','csv','--units','mm','--side','both','--exclude-dnp'],check=True)

# Mechanical pad-only footprints have no reference and must not become placements.
position_file=OUT/'pick-and-place.csv'
with position_file.open(newline='') as f:
    rows=list(csv.DictReader(f))
fields=list(rows[0]); rows=[r for r in rows if r['Ref']]
with position_file.open('w',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(rows)
assert {r['Ref'] for r in rows}==expected, 'Placement population differs from the source BOM'

# Normalize generator whitespace without changing plotted geometry.
for svg in gerbers.glob('*.svg'):
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')
