#!/usr/bin/env python3
"""SPDX-License-Identifier: MIT. Audit the delivered GLB and printable meshes.

Run with the documented CAD Python environment. --render creates orthographic
and internal inspection sheets from the actual mesh, without changing geometry.
"""
from pathlib import Path
import os, json, itertools, hashlib, argparse
os.environ.setdefault('PYOPENGL_PLATFORM','egl')
import numpy as np, trimesh, manifold3d as md, pyrender
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'mechanical/audit'
OUT.mkdir(exist_ok=True)
parser=argparse.ArgumentParser();parser.add_argument('--render',action='store_true')
parser.add_argument('--compare-carrier',type=Path,help='Optional earlier carrier STL for a true-scale screw-bore section')
options=parser.parse_args()
P=json.loads((ROOT/'mechanical/parameters.json').read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source=trimesh.load(ROOT/'mechanical/cad/assembled.glb',force='scene')
printed=['base','lid','knob','screen-carrier','screen-bezel','button-cap']
meshes={}
for node in source.graph.nodes_geometry:
    transform,key=source.graph[node]
    mesh=source.geometry[key].copy();mesh.apply_transform(transform)
    meshes[node]=mesh

def solid(mesh):
    mesh=mesh.copy();mesh.apply_transform(np.array([[1000,0,0,0],[0,0,-1000,0],[0,1000,0,0],[0,0,0,1.]]))
    mesh.merge_vertices()
    return md.Manifold(md.Mesh64(np.ascontiguousarray(mesh.vertices,dtype=np.float64),np.ascontiguousarray(mesh.faces,dtype=np.uint64)))

closed={n:solid(m) for n,m in meshes.items() if n in printed+['fasteners','bearing','screen-module','lcd-cable-screen-plug','lcd-cable-board-sh-plug'] or n.startswith('lcd-wire-')}
assert all(str(s.status()).endswith('NoError') for s in closed.values())
box=lambda size,center:md.Manifold.cube(size,True).translate(center)
# Explicit geometric masks allow only the designed self-tapped pilot engagement
# and the simplified vendor socket's filled mating volume. No blanket skips.
thread_mask=md.Manifold()
for axes,lo,hi in [(P['chassis_screw_axes'],P['lid_top_z']-6,P['lid_bottom_z']),
                    (P['bezel_screw_axes'],P['display']['bezel_top_z']-10,P['screen_support']['carrier_bottom_z'])]:
    for x,y in axes:thread_mask+=md.Manifold.cylinder(hi-lo+.02,1.01,1.01,96).translate((x,y,lo-.01))
mating_mask=box((6,20,5.6),(8.2,0,P['display']['cable_mating']['axis_z_mm']))
hits=[];unexpected=[];pair_count=0
for (a,sa),(b,sb) in itertools.combinations(closed.items(),2):
    pair_count+=1
    ma,mb=meshes[a],meshes[b]
    if np.any(np.minimum(ma.bounds[1],mb.bounds[1])-np.maximum(ma.bounds[0],mb.bounds[0])<=1e-8):continue
    overlap=sa^sb;volume=overlap.volume()
    if volume<=.001:continue
    mask=None;reason=None
    if {a,b}=={'fasteners','base'}:mask=thread_mask;reason='M2 shanks engage the 1.6mm printed pilot bores; tap before assembly'
    if {a,b}=={'lcd-cable-screen-plug','screen-module'}:mask=mating_mask;reason='Estimated plug mates inside the supplier STEP solid socket envelope'
    residual=(overlap-mask).volume() if mask is not None else volume
    record={'parts':[a,b],'intersection_mm3':round(volume,5),'allowed_contact':reason,'outside_allowed_mask_mm3':round(residual,6)}
    hits.append(record)
    if residual>.001:unexpected.append(record)

# Independently restore each delivered STL's print pose and compare it with the
# actual GLB vertices. Rendering and manufacturing must use the same solid.
from scipy.spatial import cKDTree
poses=json.loads((ROOT/'mechanical/print-poses.json').read_text());print_checks={}
glb_to_cad=np.array([[1000,0,0,0],[0,0,-1000,0],[0,1000,0,0],[0,0,0,1.]])
for n in printed:
    stl=trimesh.load(ROOT/'mechanical/stl'/f'{n}.stl',force='mesh',process=True)
    assert stl.is_watertight and stl.is_winding_consistent and len(stl.split())==1,n
    pose=poses[n]
    if pose['inverted']:stl.apply_transform(trimesh.transformations.rotation_matrix(np.pi,[1,0,0]))
    stl.apply_translation([0,0,pose['z']])
    actual=meshes[n].copy();actual.apply_transform(glb_to_cad)
    deviation=max(cKDTree(stl.vertices).query(actual.vertices)[0].max(),cKDTree(actual.vertices).query(stl.vertices)[0].max())
    assert deviation<.00002,(n,deviation)
    print_checks[n]={'connected_watertight':True,'stl_sha256':sha(ROOT/'mechanical/stl'/f'{n}.stl'),'STL_to_GLB_max_vertex_error_mm':round(float(deviation),9)}

# Validate driver access, engagement and an open carrier bore using independent
# gauges at the installed screw locations, not a duplicated hole-depth formula.
carrier_top=P['display']['front_z'];carrier_bottom=P['screen_support']['carrier_bottom_z']
for x,y in P['bezel_screw_axes']:
    shaft=md.Manifold.cylinder(carrier_top-carrier_bottom+.4,1.0,1.0,96).translate((x,y,carrier_bottom-.2))
    assert (closed['screen-carrier']^shaft).volume()<.001,'Carrier must have a completely open M2 clearance bore'
    driver=md.Manifold.cylinder(20,2,2,96).translate((x,y,P['display']['bezel_top_z']+.01))
    for n in ['knob','screen-carrier','screen-module','bearing']:
        assert (closed[n]^driver).volume()<.001,(n,'bezel driver access')

geometry=json.loads((ROOT/'mechanical/geometry-check.json').read_text())
report={'revision':P['mechanical_revision'],'model_sha256':sha(ROOT/'mechanical/cad/assembled.glb'),
        'source_parameters_sha256':sha(ROOT/'mechanical/parameters.json'),'tested_solid_pair_count':pair_count,
        'intentional_contacts':hits,'unexpected_intersections':unexpected,'print_checks':print_checks,
        'carrier_through_bores':2,'bezel_driver_diameter_mm':4,
        'screen_rear_reservation':geometry['screen_fit']['rear_component_reservation'],
        'enclosure_size_mm':[84.8,84.8,19.5],
        'scope':'Nominal delivered geometry plus stated fit-budget envelopes. Rear electronics reservation is an engineering allowance; exact kit plug fit, PLA strength/friction and bearing retention are physically untested.'}
(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
assert not unexpected,unexpected
print('CAD audit passed:',pair_count,'solid pairs; six print/GLB round trips; two open M2 bores; driver access.',flush=True)
if not options.render:raise SystemExit(0)

def camera_pose(eye,target,up=(0,1,0)):
    z=np.array(eye,dtype=float)-target;z/=np.linalg.norm(z)
    x=np.cross(up,z);x/=np.linalg.norm(x);y=np.cross(z,x)
    p=np.eye(4);p[:3,:3]=np.column_stack((x,y,z));p[:3,3]=eye;return p

def draw(names,eye,target,up=(0,1,0),xmag=.049,width=1050,height=800):
    scene=pyrender.Scene(bg_color=[.965,.974,.98,1],ambient_light=[.4,.4,.4])
    for n in names:
        scene.add(pyrender.Mesh.from_trimesh(meshes[n],smooth=False))
    pose=camera_pose(eye,np.array(target),up)
    scene.add(pyrender.OrthographicCamera(xmag=xmag,ymag=xmag*height/width,znear=.001,zfar=2),pose=pose)
    for e,intensity in [(eye,2.2),([-.08,.09,-.09],1.0),([.08,.04,.06],.6)]:
        scene.add(pyrender.DirectionalLight(color=np.ones(3),intensity=intensity),pose=camera_pose(e,np.array(target)))
    renderer=pyrender.OffscreenRenderer(width,height)
    try:color,_=renderer.render(scene)
    finally:renderer.delete()
    return Image.fromarray(color)

all_names=list(meshes)
views=[('Top / screen and bezel',[0,.15,.0001],[0,.01,0],(0,0,-1)),
       ('Front / captive mode button',[0,.020,.15],[0,.008,0],(0,1,0)),
       ('Rear / USB-C',[0,.020,-.15],[0,.008,0],(0,1,0)),
       ('Left side',[-.15,.020,0],[0,.008,0],(0,1,0)),
       ('Right side',[.15,.020,0],[0,.008,0],(0,1,0)),
       ('Bottom / floor',[0,-.15,.0001],[0,.01,0],(0,0,1))]
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',26)
sheet=Image.new('RGB',(2100,2550),'#f6f9fb')
for i,(name,eye,target,up) in enumerate(views):
    im=draw(all_names,eye,target,up,xmag=.060 if i in [0,5] else .049)
    x=(i%2)*1050;y=(i//2)*850
    sheet.paste(im,(x,y+50));ImageDraw.Draw(sheet).text((x+25,y+12),name,font=font,fill='#263c48')
    print('Rendered',name,flush=True)
sheet.save(OUT/'exterior-contact-sheet.png')

internals=[('PCB, support walls and button', [n for n in all_names if n.startswith('pcb-') or n in ['base','button-cap']],[-.08,.11,.09],[0,.007,0]),
           ('Stationary bearing / fixed cable cavity', [n for n in all_names if n not in ['knob','screen-module','screen-ui','screen-bezel','screen-carrier']],[-.08,.11,.09],[0,.009,0]),
           ('Fixed cable, carrier and posts',[n for n in all_names if n not in ['knob','lid','bearing','screen-bezel','screen-module','screen-ui','fasteners']],[-.08,.11,.09],[0,.009,0]),
           ('Screen underside / side-entry PH8 plug',[n for n in all_names if n=='screen-module' or n.startswith('lcd-')],[.055,-.07,.07],[0,.012,0]),
           ('Rotor underside / integral 48-slot track',['knob'],[.07,-.08,.07],[0,.012,0]),
           ('Encoder fork / rotating track close-up',['knob','pcb-U2'],[-.055,-.030,.055],[-.023,.0087,-.010])]
inside=Image.new('RGB',(2100,2550),'#f6f9fb')
for i,(name,names,eye,target) in enumerate(internals):
    im=draw(names,eye,target,xmag=.032 if i==3 else .015 if i==5 else .049)
    x=(i%2)*1050;y=(i//2)*850;inside.paste(im,(x,y+50));ImageDraw.Draw(inside).text((x+20,y+12),name,font=font,fill='#263c48')
    print('Rendered',name,flush=True)
inside.save(OUT/'internal-contact-sheet.png')
# Two close views expose the installed JST-SH8 socket and replacement H1,
# with a single keyed plug at either end and eight crimped wires.
lead_names=[n for n in all_names if n.startswith('lcd-') or n in ['pcb-J6','screen-module']]
lead_sheet=Image.new('RGB',(2100,850),'#f6f9fb')
for i,(label,eye,target) in enumerate([
    ('Screen hidden / keyed J6 and crimped H1 harness',[-.055,.065,.055],[-.004,.008,0]),
    ('Underside / JST-SH8 to JST-PH8 replacement cable',[.045,-.060,.065],[.001,.009,0])]):
    im=draw([n for n in lead_names if i or n!='screen-module'],eye,target,xmag=.030)
    lead_sheet.paste(im,(1050*i,50));ImageDraw.Draw(lead_sheet).text((1050*i+20,12),label,font=font,fill='#263c48')
lead_sheet.save(OUT/'display-harness.png')


report['rendered_exterior_views']=6;report['rendered_internal_views']=6;report['rendered_harness_views']=2
report['images']={n:sha(OUT/n) for n in ['exterior-contact-sheet.png','internal-contact-sheet.png','display-harness.png']}
if options.compare_carrier:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.path import Path as PlotPath
    from matplotlib.patches import PathPatch
    old=trimesh.load(options.compare_carrier,force='mesh',process=True)
    old.apply_translation([0,0,carrier_bottom])
    previous=md.Manifold(md.Mesh64(np.asarray(old.vertices),np.asarray(old.faces,dtype=np.uint64)))
    x,y=P['bezel_screw_axes'][0]
    fig,axes=plt.subplots(1,2,figsize=(10,7),sharex=True,sharey=True)
    for ax,shape,title in zip(axes,[previous,closed['screen-carrier']],['E8 / obstructed bore','E9 / open through bore']):
        polygons=shape.rotate((0,90,0)).slice(-x).to_polygons()
        paths=[]
        for polygon in polygons:
            coords=np.asarray(polygon);coords=np.column_stack((coords[:,1]-y,coords[:,0]));coords=np.vstack((coords,coords[0]))
            paths.append(PlotPath(coords,[PlotPath.MOVETO]+[PlotPath.LINETO]*(len(coords)-2)+[PlotPath.CLOSEPOLY]))
        ax.add_patch(PathPatch(PlotPath.make_compound_path(*paths),facecolor='#9eafb8',edgecolor='#344752',lw=.8))
        # M2 shaft outline; the screw head is omitted from this bore detail.
        ax.fill([-1,1,1,-1],[12.8,12.8,18.3,18.3],color='#edbb65',alpha=.65,label='M2 screw shaft')
        ax.set(xlim=(-2.7,2.7),ylim=(13.0,18.5),xlabel='Distance from screw axis / mm',title=title)
        ax.set_aspect('equal');ax.grid(alpha=.2);ax.legend(loc='lower left',fontsize=8)
    axes[0].set_ylabel('Assembly height Z / mm')
    axes[0].annotate('0.1 mm plastic membrane',xy=(.5,18.05),xytext=(-2.4,18.35),fontsize=9,arrowprops={'arrowstyle':'->','color':'#a82727'},color='#a82727')
    axes[1].annotate('Ø2.2 mm clearance bore',xy=(1.1,17.9),xytext=(-2.4,18.35),fontsize=9,arrowprops={'arrowstyle':'->','color':'#23744a'},color='#23744a')
    fig.suptitle('Section through the actual delivered carrier meshes — identical scale')
    fig.tight_layout();fig.savefig(OUT/'bore-section.png',dpi=180);plt.close(fig)
    report['carrier_comparison_source_sha256']=sha(options.compare_carrier)
    report['images']['bore-section.png']=sha(OUT/'bore-section.png')
(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
