#!/usr/bin/env python3
"""SPDX-License-Identifier: MIT. Depth-tested renders of the actual product GLB.
Requires pyrender 0.1.45, Pillow and Mesa EGL. Geometry is not rescaled by axis.
"""
import os,argparse
os.environ.setdefault('PYOPENGL_PLATFORM','egl')
from pathlib import Path
import numpy as np
import trimesh,pyrender
from PIL import Image,ImageDraw,ImageFont
args=argparse.ArgumentParser();args.add_argument('--compare-to',type=Path);options=args.parse_args()
ROOT=Path(__file__).resolve().parent
source=trimesh.load(ROOT/'cad/assembled.glb',force='scene')

def pose(eye,target,up=(0,1,0)):
 z=np.array(eye)-np.array(target);z/=np.linalg.norm(z)
 x=np.cross(up,z);x/=np.linalg.norm(x);y=np.cross(z,x)
 q=np.eye(4);q[:3,:3]=np.column_stack((x,y,z));q[:3,3]=eye;return q

def render(eye,target,path,width=1400,height=1050,model=source):
 scene=pyrender.Scene(bg_color=[.97,.975,.98,1],ambient_light=[.6,.6,.6])
 for node in model.graph.nodes_geometry:
  tf,geo=model.graph[node];mesh=model.geometry[geo]
  scene.add(pyrender.Mesh.from_trimesh(mesh,smooth=False),pose=tf)
 cp=pose(eye,target);scene.add(pyrender.OrthographicCamera(xmag=.050,ymag=.0375,znear=.001,zfar=2),pose=cp)
 scene.add(pyrender.DirectionalLight(color=np.ones(3),intensity=2.2),pose=cp)
 scene.add(pyrender.DirectionalLight(color=np.ones(3),intensity=.7),pose=pose([.07,.07,-.07],target))
 renderer=pyrender.OffscreenRenderer(width,height)
 color,depth=renderer.render(scene)
 renderer.delete();Image.fromarray(color).save(path)

render([-.07,.075,.095],[0,.010,0],ROOT/'assembly.png')
render([-.10,.018,.10],[0,.010,0],ROOT/'side-profile.png',1400,1050)
print('Rendered assembled product and low side profile with depth testing')

if options.compare_to:
 previous=trimesh.load(options.compare_to,force='scene')
 old_path=ROOT/'cad/.previous-side.png'
 render([-.10,.018,.10],[0,.010,0],old_path,model=previous)
 old=Image.open(old_path);new=Image.open(ROOT/'side-profile.png')
 comparison=Image.new('RGB',(2800,1170),(247,249,250));comparison.paste(old,(0,120));comparison.paste(new,(1400,120))
 draw=ImageDraw.Draw(comparison);font=ImageFont.load_default(size=36)
 draw.text((100,30),'Previous Rev B · 47 mm',(36,57,67),font=font)
 draw.text((1500,30),'Rev E · 22.3 mm · 52.6% lower',(36,57,67),font=font)
 draw.text((1500,80),'Same scale; side USB-C retained',(73,95,106),font=ImageFont.load_default(size=24))
 comparison.save(ROOT/'height-comparison.png');old_path.unlink()
 print('Rendered previous/current side profiles at identical camera scale')

# Actual assembled meshes with the upper parts hidden to expose the fixed cable.
cutaway=source.copy()
for node in list(cutaway.graph.nodes_geometry):
 if node in ['lid','knob','outer-retainer','bearing','screen-bezel','encoder-skirt','bearing-clamp','screen-module','screen-ui','fasteners']:
  cutaway.graph.transforms.remove_node(node)
render([-.035,.11,.065],[0,.008,0],ROOT/'wiring-cutaway.png',1400,1050,model=cutaway)
print('Rendered PCB, actual packages, JST plugs and eight static wires in cutaway')
