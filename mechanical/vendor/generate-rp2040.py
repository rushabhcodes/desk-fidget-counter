#!/usr/bin/env python3
"""SPDX-License-Identifier: MIT. Tessellate the retained supplier STEP solids."""
from pathlib import Path
import hashlib,json,subprocess,sys,tempfile
import trimesh
root=Path(__file__).resolve().parents[2]
path=root/'mechanical/vendor/models.json'
models=json.loads(path.read_text())
with tempfile.TemporaryDirectory(prefix='desk-rp-models-') as temp:
 for name,translation in [('rp2040',[0,0,.02]),('abm8',[0,0,0])]:
  record=models[name];obj=Path(temp)/f'{name}.obj'
  subprocess.run([sys.executable,str(root/'mechanical/step-mesh.py'),str(root/record['step']),str(obj)],check=True)
  mesh=trimesh.load(obj,force='mesh');mesh.apply_translation(translation)
  assert mesh.is_watertight and mesh.volume>0
  mesh.visual.vertex_colors=[62,65,68,255] if name=='rp2040' else [160,165,168,255]
  mesh.export(root/record['obj']);mesh.export(root/f'mechanical/vendor/solid/{name}.ply')
  record.update(bounds=mesh.bounds.tolist(),size=dict(zip('xyz',mesh.extents.tolist())),
   source_step_sha256=hashlib.sha256((root/record['step']).read_bytes()).hexdigest(),
   model_origin_translation_mm=translation,derivative_generator='mechanical/vendor/generate-rp2040.py')
path.write_text(json.dumps(models,indent=2)+'\n')
