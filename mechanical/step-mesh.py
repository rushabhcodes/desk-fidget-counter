#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Tessellate unchanged STEP geometry at 0.03mm deflection; OCP 8.0.1.
import sys,json
import numpy as np,trimesh
from OCP.STEPControl import STEPControl_Reader
from OCP.BRepBndLib import BRepBndLib
from OCP.Bnd import Bnd_Box
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_FACE,TopAbs_REVERSED
from OCP.TopoDS import TopoDS
from OCP.TopLoc import TopLoc_Location
from OCP.BRep import BRep_Tool
from OCP.BRepMesh import BRepMesh_IncrementalMesh
r=STEPControl_Reader();r.ReadFile(sys.argv[1]);r.TransferRoots();s=r.OneShape();BRepMesh_IncrementalMesh(s,.03,False,.15,True)
e=TopExp_Explorer(s,TopAbs_FACE);vs=[];fs=[];groups=[];fi=0
while e.More():
 face=TopoDS.Face(e.Current());loc=TopLoc_Location();tri=BRep_Tool.Triangulation_s(face,loc)
 if tri:
  start=len(vs);matrix=loc.Transformation()
  for i in range(1,tri.NbNodes()+1):
   p=tri.Node(i).Transformed(matrix);vs.append([p.X(),p.Y(),p.Z()])
  for i in range(1,tri.NbTriangles()+1):
   a,b,c=tri.Triangle(i).Get()
   if face.Orientation()==TopAbs_REVERSED:b,c=c,b
   fs.append([start+a-1,start+b-1,start+c-1]);groups.append(fi)
 fi+=1;e.Next()
m=trimesh.Trimesh(vs,fs,process=True);m.export(sys.argv[2]);np.savez(sys.argv[2]+'.faces.npz',vertices=np.array(vs),faces=np.array(fs),groups=np.array(groups))
print(json.dumps({'bounds_mm':m.bounds.tolist(),'faces':len(m.faces),'volume':m.volume,'watertight':m.is_watertight,'components':len(m.split())}))
