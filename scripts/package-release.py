#!/usr/bin/env python3
"""SPDX-License-Identifier: MIT. Package inspected artifacts and bind them to source hashes.
Run after all validation/export/preview steps, before committing/tagging v1.0.0.
"""
from pathlib import Path
import hashlib,json,zipfile,subprocess
ROOT=Path(__file__).resolve().parents[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
files=sorted(ROOT.glob('manufacturing/gerbers/*'))
fab=ROOT/'manufacturing/desk-knob-reva-gerbers.zip'
with zipfile.ZipFile(fab,'w',zipfile.ZIP_DEFLATED) as z:
 for p in files:
  if p.suffix!='.svg':z.write(p,p.name)
# Version tag resolves the exact committed source. Hashes are content-based,
# avoiding a self-referential commit hash embedded inside its own commit.
tracked=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard'],cwd=ROOT,text=True).splitlines()
inputs=[];outputs=[]
for name in sorted(set(tracked)):
 p=ROOT/name
 if not p.is_file() or name.startswith('release/') or name=='release-manifest.json':continue
 if name.startswith(('dist/','previews/','manufacturing/gerbers/','manufacturing/tscircuit.pretty/','mechanical/stl/','firmware/build/','validation/logs/')) or name.endswith(('.kicad_pcb','.kicad_pro','.zip')) or name in ['mechanical/assembly.png','mechanical/geometry-check.json','manufacturing/BOM.csv','manufacturing/pick-and-place.csv','validation/kicad-drc.json','validation/manufacturing-inspection.json','validation/firmware-image-check.json']:
  outputs.append({'path':name,'sha256':sha(p)})
 else:inputs.append({'path':name,'sha256':sha(p)})
manifest={'release':'v1.0.0','hardware':'Rev A / A1','repository':'https://github.com/rushabhcodes/desk-fidget-counter','tscircuit':'https://tscircuit.com/rushabhcodes/desk-fidget-counter','source_revision':'Git tag v1.0.0; resolve tag to its commit; source file hashes below','toolchain':{'Bun':'1.3.3','tscircuit':'0.0.3064','TypeScript':'5.9.3','KiCad':'10.0.7','ARM_GCC':'xPack 15.2.1-1.1','TinyUSB':'0.21.0 / dae3f9a366bfcddbf9dcf1b48d7500286a849539','CMSIS_5':'2b7495b8535bdcb306dac29b9ded4cfb679d7e5c','STM32_CMSIS_F0':'cbb5da5d48b4b5f2efacdc2f033be30f9d29889f'},'source_inputs':inputs,'artifacts':outputs,'physical_prototype_tests':'Unperformed; see validation/BRINGUP.md'}
(ROOT/'release-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
release=ROOT/'release';release.mkdir(exist_ok=True)
bundle=release/'desk-knob-v1.0.0.zip'
with zipfile.ZipFile(bundle,'w',zipfile.ZIP_DEFLATED) as z:
 for name in sorted(set(tracked)|{'release-manifest.json'}):
  p=ROOT/name
  if p.is_file() and not name.startswith('release/'):z.write(p,'desk-knob-v1.0.0/'+name)
checkfiles=[bundle,fab,ROOT/'firmware/build/desk-knob.bin',ROOT/'firmware/build/desk-knob.hex',ROOT/'release-manifest.json']
(release/'SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  {p.relative_to(ROOT)}\n' for p in checkfiles))
print(f'Packaged {len(inputs)} source inputs and {len(outputs)} artifacts; {bundle.stat().st_size} byte complete archive')
