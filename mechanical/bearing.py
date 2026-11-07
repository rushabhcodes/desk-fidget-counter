# SPDX-License-Identifier: MIT
"""6712ZZ model: verified boundary size, explicitly estimated internals.

This represents a purchased bearing, never a print or a bearing manufacture
specification. The component interfaces use separate inner/outer race solids.
"""
import math
import numpy as np
import trimesh
import manifold3d as m

def mesh(s):
    q=s.to_mesh64()
    return trimesh.Trimesh(np.asarray(q.vert_properties)[:,:3],np.asarray(q.tri_verts),process=True)

def ring(ro,ri,h,z):
    return m.Manifold.cylinder(h,ro,ro,192).translate((0,0,z))-m.Manifold.cylinder(h+.2,ri,ri,192).translate((0,0,z-.1))

def chamfered_ring(ro,ri,h,z,c):
    profile=[(ri+c,0),(ro-c,0),(ro,c),(ro,h-c),(ro-c,h),(ri+c,h),(ri,h-c),(ri,c)]
    return m.CrossSection([profile]).revolve(192).translate((0,0,z))

def build(parameters):
    b=parameters['bearing'];a=b['approximation'];z=b['bottom_z'];h=b['width']
    pitch=a['pitch_diameter']/2;groove=a['groove_radius'];count=a['ball_count']
    circle=[(pitch+groove*math.cos(t),h/2+groove*math.sin(t)) for t in np.linspace(0,2*math.pi,96,endpoint=False)]
    raceway=m.CrossSection([circle]).revolve(192).translate((0,0,z))
    inner=chamfered_ring(a['inner_race_od']/2,b['id']/2,h,z,a['edge_chamfer'])-raceway
    outer=chamfered_ring(b['od']/2,a['outer_race_id']/2,h,z,a['edge_chamfer'])-raceway
    shields=[]
    for level in [z+a['shield_recess'],z+h-a['shield_recess']-a['shield_thickness']]:
        # A shallow seat holds the outer shield rim; the inner rim has clearance.
        outer-=ring(a['shield_outer_diameter']/2+.05,a['outer_race_id']/2-.1,a['shield_thickness']+.06,level-.03)
        shields.append(ring(a['shield_outer_diameter']/2,a['shield_inner_diameter']/2,a['shield_thickness'],level))
    balls=[];bars=[]
    cage=ring(pitch+.35,pitch-.35,.2,z+1.25)+ring(pitch+.35,pitch-.35,.2,z+h-1.45)
    for i in range(count):
        theta=2*math.pi*i/count
        balls.append(m.Manifold.sphere(a['ball_diameter']/2,32).translate((pitch*math.cos(theta),pitch*math.sin(theta),z+h/2)))
        theta+=math.pi/count
        bars.append(m.Manifold.cube((.7,.35,h-2.5),True).rotate((0,0,math.degrees(theta))).translate((pitch*math.cos(theta),pitch*math.sin(theta),z+h/2)))
    cage+=m.Manifold.batch_boolean(bars,m.OpType.Add)
    solids={'bearing-inner-race':inner,'bearing-outer-race':outer,'bearing-shield-bottom':shields[0],'bearing-shield-top':shields[1],'bearing-balls':m.Manifold.batch_boolean(balls,m.OpType.Add),'bearing-cage':cage}
    # A visual approximation must still be mechanically self-consistent.
    for name,solid in solids.items():
        assert solid.volume()>0 and str(solid.status()).endswith('NoError'),name
    for i,(name,s) in enumerate(solids.items()):
        for other,t in list(solids.items())[i+1:]:
            assert (s^t).volume()<1e-4,(name,other,'bearing internal collision',(s^t).volume())
    report={'purchased_part':'Maysme 6712ZZ','verified_boundary_mm':{'id':b['id'],'od':b['od'],'width':h},'approximation':a,'assembly_object_count':1,'assembly_object_name':'bearing','internal_solid_count':len(solids),'internal_intersections':0,'status':'User-authorized best approximation. Race/shield geometry and ball/cage internals are not manufacturer CAD. All internals are combined into one bearing object in the product assembly.'}
    return {name:mesh(s) for name,s in solids.items()},solids,report
