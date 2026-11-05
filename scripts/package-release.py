#!/usr/bin/env python3
"""SPDX-License-Identifier: MIT. Package inspected artifacts and bind them to source hashes.
Run after all validation/export/preview steps, before committing/tagging the package.json version.
"""
from pathlib import Path
import hashlib,json,zipfile,subprocess
ROOT=Path(__file__).resolve().parents[1]
VERSION='v'+json.loads((ROOT/'package.json').read_text())['version']
native_versions={name:json.loads((ROOT/'node_modules'/package/'package.json').read_text())['version']
 for name,package in [('tscircuit','tscircuit'),('tscircuit_core','@tscircuit/core'),('capacity_autorouter','@tscircuit/capacity-autorouter')]}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
files=sorted(ROOT.glob('manufacturing/gerbers/*'))
fab=ROOT/'manufacturing/desk-knob-reve3-gerbers.zip'
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
 if name in {'mechanical/fit-coupons.json','mechanical/bearing-envelope.png'} or name.startswith(('dist/','previews/','manufacturing/gerbers/','manufacturing/tscircuit.pretty/','mechanical/stl/','mechanical/cad/','firmware/build/','validation/logs/')) or name.endswith(('.kicad_pcb','.kicad_pro','.zip')) or name in ['mechanical/assembly.png','mechanical/exploded.png','mechanical/side-profile.png','mechanical/height-comparison.png','mechanical/wiring-cutaway.png','mechanical/usb-access.png','mechanical/usb-access-comparison.png','mechanical/button-access.png','mechanical/button-access-comparison.png','mechanical/geometry-check.json','mechanical/harness.json','manufacturing/BOM.csv','manufacturing/LCD-harness.csv','manufacturing/pick-and-place.csv','validation/kicad-drc.json','validation/manufacturing-inspection.json','validation/firmware-image-check.json','validation/pour-cleanup.json','mechanical/print-poses.json']:
  outputs.append({'path':name,'sha256':sha(p)})
 else:inputs.append({'path':name,'sha256':sha(p)})
manifest={'release':VERSION,'hardware':'Rev E3 / E3','repository':'https://github.com/rushabhcodes/desk-fidget-counter','tscircuit':'https://tscircuit.com/rushabhcodes/desk-fidget-counter','source_revision':f'Git tag {VERSION}; resolve tag to its commit; source file hashes below','toolchain':{'Bun':'1.3.3',**native_versions,'TypeScript':'5.9.3','KiCad':'10.0.7','ARM_GCC':'xPack 15.2.1-1.1','TinyUSB':'0.21.0 / dae3f9a366bfcddbf9dcf1b48d7500286a849539','CMSIS_5':'2b7495b8535bdcb306dac29b9ded4cfb679d7e5c','STM32_CMSIS_F0':'cbb5da5d48b4b5f2efacdc2f033be30f9d29889f'},'source_inputs':inputs,'artifacts':outputs,'physical_prototype_tests':'Unperformed; bearing race faces, calibrated prints, PCB capture fit and supplied-cable OD/bends/termination need measurement before physical-fit signoff. See mechanical/FIT.md and validation/BRINGUP.md'}
(ROOT/'release-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
release=ROOT/'release';release.mkdir(exist_ok=True)
bundle=release/f'desk-knob-{VERSION}.zip'
with zipfile.ZipFile(bundle,'w',zipfile.ZIP_DEFLATED) as z:
 for name in sorted(set(tracked)|{'release-manifest.json'}):
  p=ROOT/name
  if p.is_file() and not name.startswith('release/'):z.write(p,f'desk-knob-{VERSION}/'+name)
checkfiles=[bundle,fab,ROOT/'firmware/build/desk-knob.bin',ROOT/'firmware/build/desk-knob.hex',ROOT/'mechanical/cad/assembled.glb',ROOT/'mechanical/cad/exploded.glb',ROOT/'release-manifest.json']
(release/'SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  {p.relative_to(ROOT)}\n' for p in checkfiles))
print(f'Packaged {len(inputs)} source inputs and {len(outputs)} artifacts; {bundle.stat().st_size} byte complete archive')
