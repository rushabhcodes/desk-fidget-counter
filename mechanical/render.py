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
args=argparse.ArgumentParser();args.add_argument('--compare-to',type=Path);args.add_argument('--usb-before',type=Path);args.add_argument('--button-before',type=Path);options=args.parse_args()
ROOT=Path(__file__).resolve().parent
source=trimesh.load(ROOT/'cad/assembled.glb',force='scene')

def pose(eye,target,up=(0,1,0)):
 z=np.array(eye)-np.array(target);z/=np.linalg.norm(z)
 x=np.cross(up,z);x/=np.linalg.norm(x);y=np.cross(z,x)
 q=np.eye(4);q[:3,:3]=np.column_stack((x,y,z));q[:3,3]=eye;return q

def render(eye,target,path,width=1400,height=1050,model=source,xmag=.050,ymag=.0375,metal=False):
 scene=pyrender.Scene(bg_color=[.97,.975,.98,1],ambient_light=([.04,.04,.04] if metal else [.6,.6,.6]))
 for node in model.graph.nodes_geometry:
  tf,geo=model.graph[node];mesh=model.geometry[geo]
  scene.add(pyrender.Mesh.from_trimesh(mesh,smooth=False),pose=tf)
 cp=pose(eye,target);scene.add(pyrender.OrthographicCamera(xmag=xmag,ymag=ymag,znear=.001,zfar=2),pose=cp)
 scene.add(pyrender.DirectionalLight(color=np.ones(3),intensity=2.2),pose=cp)
 scene.add(pyrender.DirectionalLight(color=np.ones(3),intensity=.7),pose=pose([.07,.07,-.07],target))
 if metal:
  scene.add(pyrender.DirectionalLight(color=np.ones(3),intensity=2.5),pose=pose([-.065,.065,-.080],target))
 renderer=pyrender.OffscreenRenderer(width,height)
 color,depth=renderer.render(scene)
 renderer.delete();Image.fromarray(color).save(path)

render([-.07,.075,.095],[0,.010,0],ROOT/'assembly.png')
render([-.10,.018,.10],[0,.010,0],ROOT/'side-profile.png',1400,1050)
print('Rendered assembled product and low side profile with depth testing')

# Show the real catalogue envelope and its improved steel material on its own.
# No race/shield dimensions are implied by this material preview.
steel=source.copy()
for node in list(steel.graph.nodes_geometry):
 if node!='bearing':steel.graph.transforms.remove_node(node)
render([.065,.065,.080],[0,.0155,0],ROOT/'bearing-envelope.png',1400,1050,model=steel,metal=True)
preview=Image.open(ROOT/'bearing-envelope.png').convert('RGB');draw=ImageDraw.Draw(preview)
draw.text((45,30),'6712ZZ - 60 x 75 x 7 mm catalogue envelope',(36,57,67),font=ImageFont.load_default(size=30))
draw.text((45,980),'Steel material preview; race/shield dimensions are not modelled',(73,95,106),font=ImageFont.load_default(size=24))
preview.save(ROOT/'bearing-envelope.png')

if options.compare_to:
 previous=trimesh.load(options.compare_to,force='scene')
 old_path=ROOT/'cad/.previous-side.png'
 render([-.10,.018,.10],[0,.010,0],old_path,model=previous)
 old=Image.open(old_path);new=Image.open(ROOT/'side-profile.png')
 comparison=Image.new('RGB',(2800,1170),(247,249,250));comparison.paste(old,(0,120));comparison.paste(new,(1400,120))
 draw=ImageDraw.Draw(comparison);font=ImageFont.load_default(size=36)
 draw.text((100,30),'Previous Rev B · 47 mm',(36,57,67),font=font)
 draw.text((1500,30),'Rev E3 · 22.3 mm · 52.6% lower',(36,57,67),font=font)
 draw.text((1500,80),'Same scale; side USB-C retained',(73,95,106),font=ImageFont.load_default(size=24))
 comparison.save(ROOT/'height-comparison.png');old_path.unlink()
 print('Rendered previous/current side profiles at identical camera scale')

# Actual assembled meshes with the upper parts hidden to expose the fixed cable.
cutaway=source.copy()
for node in list(cutaway.graph.nodes_geometry):
 if node in ['lid','knob','outer-retainer','bearing','screen-bezel','encoder-skirt','bearing-clamp','screen-module','screen-ui','fasteners']:
  cutaway.graph.transforms.remove_node(node)
render([-.035,.11,.065],[0,.008,0],ROOT/'wiring-cutaway.png',1400,1050,model=cutaway)
print('Rendered PCB, actual packages, original display plug and eight supplied wires in cutaway')

# Rear USB close-up uses the actual assembled meshes and a common camera.
usb_eye=[.004,.014,-.13];usb_target=[0,.007,-.039]
render(usb_eye,usb_target,ROOT/'usb-access.png',1400,700,xmag=.025,ymag=.0125)
if options.usb_before:
 before=trimesh.load(options.usb_before,force='scene')
 temp=ROOT/'cad/.usb-before.png'
 render(usb_eye,usb_target,temp,1400,700,model=before,xmag=.025,ymag=.0125)
 a=Image.open(temp).convert('RGB');b=Image.open(ROOT/'usb-access.png').convert('RGB')
 out=Image.new('RGB',(2800,810),(247,249,250));out.paste(a,(0,110));out.paste(b,(1400,110))
 d=ImageDraw.Draw(out);font=ImageFont.load_default(size=32)
 d.text((45,25),'Before: USB mouth recessed 9.65 mm',(36,57,67),font=font)
 d.text((1445,25),'Rev E3: USB mouth at the side wall',(36,57,67),font=font)
 d.text((1445,70),'Shell diameter 86 -> 84.8 mm; height stays 22.3 mm',(73,95,106),font=ImageFont.load_default(size=24))
 out.save(ROOT/'usb-access-comparison.png');temp.unlink()
print('Rendered USB side access from the actual CAD')

# Real front actuator/PCB extension compared at the same camera scale.
front_eye=[.006,.013,.13];front_target=[0,.005,.039]
render(front_eye,front_target,ROOT/'button-access.png',1400,700,xmag=.018,ymag=.009)
if options.button_before:
 previous=trimesh.load(options.button_before,force='scene');temp=ROOT/'cad/.button-before.png'
 render(front_eye,front_target,temp,1400,700,model=previous,xmag=.018,ymag=.009)
 out=Image.new('RGB',(2800,810),(247,249,250));out.paste(Image.open(temp).convert('RGB'),(0,110));out.paste(Image.open(ROOT/'button-access.png').convert('RGB'),(1400,110))
 d=ImageDraw.Draw(out);font=ImageFont.load_default(size=32)
 d.text((45,25),'Before: separate printed button plunger',(36,57,67),font=font)
 d.text((1445,25),'E3: original switch, directly accessible',(36,57,67),font=font)
 d.text((1445,70),'Supported PCB tab; no added button cap or plunger',(73,95,106),font=ImageFont.load_default(size=24))
 out.save(ROOT/'button-access-comparison.png');temp.unlink()
 print('Rendered direct button before/after from real CAD')
