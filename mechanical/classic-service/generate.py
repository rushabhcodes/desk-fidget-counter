#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Build the serviceable Classic enclosure around the original F1 board."""

import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path
import shutil
import sys

import manifold3d as m
import numpy as np
from scipy.spatial import cKDTree
import trimesh

MECHANICAL = Path(__file__).resolve().parents[1]
ROOT = MECHANICAL.parent
sys.path.insert(0, str(MECHANICAL))

from button import return_budget, return_pad_solids
from harness import tube

P = json.loads((MECHANICAL / "parameters.json").read_text())
CLASSIC_POSES = json.loads((MECHANICAL / "print-poses.json").read_text())
PCB_BOTTOM = P["pcb_bottom_z"]
PCB_TOP = PCB_BOTTOM + P["pcb_thickness"]
BOARD_CENTER = (PCB_BOTTOM + PCB_TOP) / 2
RADIUS = P["base_diameter"] / 2
ERROR_VOLUME = 0.001
GEOMETRY_SEGMENTS = 192
CARRIER_SCREWS = P["chassis_screw_axes"]
DISPLAY_SCREWS = P["bezel_screw_axes"]
CARRIER_PILOT_BOTTOM = 5.48
CARRIER_PILOT_TOP = 8.70
DISPLAY_TOP = P["display"]["bezel_top_z"]
DISPLAY_BOTTOM = P["screen_support"]["carrier_bottom_z"]
SCREEN_LIFT = [0, .5, 1, 2, 3, 5, 7, 9, 12, 16, 20]
ROTOR_LIFT = [0, .25, .5, .75, 1, 1.5, 2, 3, 5, 8, 12, 16, 24]
BOARD_LIFT = [0, .25, .5, 1, 1.5, 2, 3, 5, 8, 12, 16, 20]
TO_CAD = np.array([[1000, 0, 0, 0], [0, 0, -1000, 0], [0, 1000, 0, 0], [0, 0, 0, 1.0]])
TO_GLTF = np.linalg.inv(TO_CAD)


def hash_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cylinder(radius, low, high, x=0, y=0, sides=GEOMETRY_SEGMENTS):
    return m.Manifold.cylinder(high - low, radius, radius, sides).translate((x, y, low))


def box(size, center):
    return m.Manifold.cube(size, True).translate(center)


def ring(outer, inner, low, high):
    return cylinder(outer, low, high) - cylinder(inner, low - .2, high + .2)


def combine(solids):
    return m.Manifold.batch_boolean(list(solids), m.OpType.Add)


def as_solid(mesh):
    vertices = np.ascontiguousarray(mesh.vertices, dtype=np.float64)
    faces = np.ascontiguousarray(mesh.faces, dtype=np.uint64)
    solid = m.Manifold(m.Mesh64(vertices, faces))
    assert solid.status() == m.Error.NoError, solid.status()
    return solid


def as_mesh(solid):
    mesh = solid.to_mesh64()
    return trimesh.Trimesh(np.asarray(mesh.vert_properties)[:, :3], np.asarray(mesh.tri_verts), process=False)


def polygon(points):
    return m.CrossSection([[(point["x"], point["y"]) for point in points]])


def print_to_assembly(name, mesh):
    pose = CLASSIC_POSES[name]
    if "rotation_deg" in pose:
        mesh.apply_translation(-np.array(pose["translation_mm"]))
        mesh.apply_transform(np.linalg.inv(trimesh.transformations.euler_matrix(*np.radians(pose["rotation_deg"]))))
    else:
        if pose["inverted"]:
            mesh.apply_transform(trimesh.transformations.rotation_matrix(math.pi, [1, 0, 0]))
        mesh.apply_translation([0, 0, pose["z"]])
    return mesh


def classic_print(name):
    path = MECHANICAL / "stl" / f"{name}.stl"
    return as_solid(print_to_assembly(name, trimesh.load_mesh(path)))


def source_cad():
    path = MECHANICAL / "cad/assembled.glb"
    record = json.loads((MECHANICAL / "cad/assembly-check.json").read_text())
    assert hash_file(path) == record["cad_files"][path.name]["sha256"]
    assert hash_file(ROOT / "index.circuit.tsx") == record["source_board_tsx_sha256"]
    assert hash_file(MECHANICAL / "parameters.json") == record["source_parameters_sha256"]
    scene = trimesh.load_scene(path)
    parts = {}
    for node in sorted(scene.graph.nodes_geometry):
        transform, geometry = scene.graph[node]
        mesh = scene.geometry[geometry].copy()
        mesh.apply_transform(TO_CAD @ transform)
        parts[node] = mesh
    pcb_faces = [part for name, part in parts.items() if name.startswith("pcb-Box0_")]
    assert sum(getattr(face.visual.material,"baseColorTexture",None) is not None for face in pcb_faces) == 2, (
        "The F1 top and bottom textures are required for the assembly CAD. "
        "Install Pillow in the CAD environment."
    )
    return parts, path


def board_solid(circuit):
    board = next(row for row in circuit if row["type"] == "pcb_board")
    material = polygon(board["outline"]) - polygon(next(row["points"] for row in circuit if row["type"] == "pcb_cutout"))
    solid = material.extrude(P["pcb_thickness"]).translate((0, 0, PCB_BOTTOM))
    return solid - combine(
        cylinder(hole["hole_diameter"]/2, PCB_BOTTOM-.1, PCB_TOP+.1, hole["x"], hole["y"])
        for hole in circuit if hole["type"] == "pcb_hole"
    )


def make_base(board):
    base = classic_print("base")
    for x, y in CARRIER_SCREWS:
        # The relieved inner side of each boss clears the F1 outline.
        foot = cylinder(3.3, 1.82, 7.2, x, y) - cylinder(36.60, 1.7, 7.3)
        base += foot
        base -= cylinder(2.35, 5.24, 7.35, x, y)
        base -= cylinder(1.22, -.18, 7.4, x, y)
        base -= cylinder(2.1, -.22, .18, x, y)
        base -= m.Manifold.cylinder(.90, 2.10, 1.20, GEOMETRY_SEGMENTS).translate((x, y, .18))
    # This channel opens only above the front tab. The nose support below
    # the board and the paddle's outboard stops remain in the base.
    approach = polygon(board["outline"]).offset(.28).extrude(5.9).translate((0,0,PCB_TOP))
    front = box((41,16,7.5),(0,-40.2,7.3))
    return base - (approach ^ front)


def make_display_mount(module, rear_reservation):
    old_bezel = classic_print("screen-bezel")
    shroud = ring(23.8, 22.8, DISPLAY_BOTTOM, 18.36)
    towers = combine(cylinder(2.2, DISPLAY_BOTTOM, 18.38, x, y) for x, y in DISPLAY_SCREWS)
    web = ring(23.73, 21.55, 17.36, 18.16)
    cavity = module.slice(P["display"]["pcb_bottom_z"]+.1).offset(.38).extrude(5.03)
    cavity = cavity.translate((0, 0, DISPLAY_BOTTOM-.1))
    mount = old_bezel + ((shroud + towers + web) ^ cylinder(24, DISPLAY_BOTTOM, 18.37))
    mount -= cavity + rear_reservation + module.translate((0, 0, .02))
    for x, y in DISPLAY_SCREWS:
        mount -= cylinder(1.1, DISPLAY_BOTTOM-.1, 19.7, x, y)
        mount -= m.Manifold.cylinder(.9, 1.1, 2.1, 64).translate((x, y, 18.3))
        mount -= cylinder(2.1, 19.15, 19.7, x, y)
    return mount


def make_rotor_carrier():
    carrier = classic_print("lid")
    cap = P["front_button"]["printed_cap"]
    stop_y = cap["ear_center_y_mm"] + cap["ear_depth_mm"]/2 + cap["nominal_max_travel_mm"]
    # Move the inward travel stops onto the removable carrier. Removing this
    # module clears the vertical path of the front PCB tab.
    for sign in [-1,1]:
        carrier += box((2.8,.8,.84),(sign*5.2,stop_y+.4,7.60))
    for x, y in CARRIER_SCREWS:
        carrier += cylinder(2.12, CARRIER_PILOT_BOTTOM, 9.08, x, y)
        carrier += cylinder(3.02, 7.205, 9.08, x, y)
        carrier -= cylinder(.82, CARRIER_PILOT_BOTTOM-.10, CARRIER_PILOT_TOP, x, y)
    return carrier


def component_solids(circuit):
    names = {item["source_component_id"]:item["name"] for item in circuit if item["type"] == "source_component"}
    result = {}
    for record in circuit:
        if record["type"] != "cad_component":
            continue
        name = names[record["source_component_id"]]
        model = record["model_obj_url"].split("?")[0].split("/")[-1]
        path = MECHANICAL / "vendor/solid" / model.replace(".obj", ".ply")
        mesh = trimesh.load_mesh(path if path.exists() else MECHANICAL / "vendor/obj" / model,
                                 process=model not in ("b3u3000.obj", "jst-sh8.obj"))
        origin = record.get("model_origin_position", {})
        coords = ("x", "y", "z")
        mesh.apply_translation([-origin.get(k, 0) for k in coords])
        mesh.apply_transform(trimesh.transformations.euler_matrix(
            *[math.radians(record.get("rotation", {}).get(k,0)) for k in coords]
        ))
        pose = record["position"]
        mesh.apply_translation([pose["x"],pose["y"],pose["z"]+BOARD_CENTER])
        components = mesh.split(only_watertight=False)
        result[name] = combine(as_solid(part) for part in components)
    assert len(result) == sum(row["type"] == "pcb_component" for row in circuit) == 52
    return result


def check_clear(name, a, b):
    aa, bb = np.array(a.bounding_box()).reshape(2,3), np.array(b.bounding_box()).reshape(2,3)
    if np.any(np.minimum(aa[1],bb[1])-np.maximum(aa[0],bb[0])<=1e-8):
        return
    overlap = (a ^ b).volume()
    assert overlap < ERROR_VOLUME, (name, round(overlap,6))


def rear_electronics(module):
    depth = P["display"]["rear_component_clearance_depth_mm"]
    bottom = P["display"]["pcb_bottom_z"]
    reserve = module.slice(bottom+.1).extrude(depth).translate((0,0,bottom-depth))
    for x,y in P["display"]["mounting_hole_centers_mm"]:
        reserve -= cylinder(2.05,bottom-depth-1,bottom+1,x,y)
    return reserve - box((10.6,20.6,depth+2), (10.2,0,bottom-depth/2))


def rotor_envelopes():
    bearing = P["bearing"]
    bearing_top = bearing["bottom_z"] + bearing["width"]
    lower = P["knob_bottom_z"]
    chamfer = P["knob_lower_chamfer"]
    encoder = P["encoder"]
    track = encoder["track_radius"]
    half_wall = encoder["track_thickness"]/2
    opening = P["display"]["bezel_diameter"]/2 + P["display"]["rotor_radial_clearance_mm"]
    shoulder = P["bearing_mount"]["outer_contact_id"]/2
    pocket = P["bearing_pocket_id"]/2

    def expanded(radius, dz):
        def annulus(outer, inner, low, high):
            return ring(outer+radius, inner-radius, low-dz, high+dz)

        grip = annulus(RADIUS, pocket, lower, bearing_top)
        h = chamfer["height_mm"]
        slope = m.Manifold.cylinder(h, RADIUS-chamfer["radial_mm"]+radius, RADIUS+radius,
                                    GEOMETRY_SEGMENTS).translate((0,0,lower-dz))
        grip -= cylinder(RADIUS+radius+.2,lower-dz,lower-dz+h)-slope
        grip += annulus(RADIUS,shoulder,bearing_top,bearing_top+1.7)
        grip += annulus(RADIUS,opening,bearing_top+1.7,P["knob_top_z"])
        skirt = annulus(track+half_wall,track-half_wall,encoder["skirt_bottom_z"],bearing_top+1.8)
        flange = annulus(encoder["bond_outer_radius"],track-half_wall,bearing_top+.44,bearing_top+1.84)
        return {"grip":grip,"skirt":skirt,"skirt flange":flange}

    budget = P["fit_budget"]
    return (
        expanded(budget["moving_xy_print_check"],budget["moving_z_print_check"]),
        expanded(budget["moving_xy_pcb_check"],budget["moving_z_hardware_check"]),
    )


def hardware_checks(prints, cad, packages, pcb, module, rear):
    base, carrier = prints["base"], prints["rotor-carrier"]
    lid, grip, cap = prints["display-mount"], prints["knob"], prints["button-cap"]
    static = {"base":base,"rotor-carrier":carrier,"display-mount":lid}
    expanded_print, expanded_hardware = rotor_envelopes()
    for name, part in static.items():
        check_clear(f"{name} / rear LCD allowance",part,rear)
        for feature, swept in expanded_print.items():
            check_clear(f"{name} / tolerance-expanded {feature}",part,swept)
    for name, part in {**packages,"PCB":pcb,"screen":module}.items():
        for feature, swept in expanded_hardware.items():
            check_clear(f"{name} / tolerance-expanded {feature}",part,swept)

    bearing_pieces = as_solid(cad["bearing"])
    for name, part in prints.items():
        check_clear(f"{name} / bearing",part,bearing_pieces)
    checks = []
    for inner, part in [(True,carrier),(False,grip)]:
        bearing = P["bearing"]
        low,high = bearing["bottom_z"],bearing["bottom_z"]+bearing["width"]
        race = ring(32 if inner else 37.5,30 if inner else 35.5,low,high)
        radial = 1.0004 if inner else .9998
        assert (race ^ part.scale((radial,radial,1))).volume() > .1
        assert (race ^ part.translate((0,0,.01 if inner else -.01))).volume() > .1
        checks += [f"{'inner' if inner else 'outer'} radial", f"{'inner' if inner else 'outer'} shoulder"]

    support = P["screen_support"]
    for x,y in P["display"]["mounting_hole_centers_mm"]:
        contact = cylinder(2,support["seat_z"]-.01,support["seat_z"]+.03,x,y)
        assert (base.translate((0,0,.01)) ^ module ^ contact).volume() > .01
    assert (module.translate((0,0,.5)) ^ lid).volume() > .01
    for z in [14.8,16.0,17.7]:
        for angle in np.linspace(0,math.tau,48,endpoint=False):
            c,s = math.cos(angle),math.sin(angle)
            assert lid.ray_cast((24.3*c,24.3*s,z),(22.35*c,22.35*s,z)),(z,angle)

    usb = P["usb_access"]
    plug_gauge = box((usb["plug_width_mm"],usb["plug_check_length_mm"],usb["plug_height_mm"]),
                     (0,usb["plug_shoulder_y"]+usb["plug_check_length_mm"]/2,usb["axis_z"]))
    for name, part in {**prints,**packages,"PCB":pcb}.items():
        check_clear(f"USB plug gauge / {name}",plug_gauge,part)
    for x,y in DISPLAY_SCREWS:
        shaft = cylinder(1.0,DISPLAY_BOTTOM-.2,DISPLAY_TOP-1,x,y)
        driver = cylinder(2,DISPLAY_TOP+.01,DISPLAY_TOP+14,x,y)
        check_clear("display fastener through bore",shaft,lid)
        for name, part in {**prints,"screen":module,"bearing":bearing_pieces}.items():
            check_clear(f"top screwdriver / {name}",driver,part)
    for x,y in CARRIER_SCREWS:
        driver = cylinder(2.03,-14,.17,x,y)
        shank = cylinder(1.03,.98,CARRIER_PILOT_BOTTOM,x,y)
        check_clear("underside screwdriver",driver,base)
        check_clear("underside shank / base",shank,base)
        assert 8.0-(CARRIER_PILOT_BOTTOM-0.0) >= 2.4

    button = P["front_button"]
    spec = button["printed_cap"]
    pretravel = np.linspace(0,spec["nominal_max_travel_mm"],13)
    actuator = box((2,1,1.4),(0,button["actuator_front_y"]+.19,button["axis_z"]))
    switch_body = packages["SW1"] - actuator
    for travel in pretravel:
        pressed = cap.translate((0,float(travel),0))
        for name, part in {**static,**packages,"SW1":switch_body,"PCB":pcb,"knob":grip}.items():
            check_clear(f"button at {travel:.2f} mm / {name}",pressed,part)
        foam,bonds = return_pad_solids(P,float(travel))
        for pad in [foam,bonds]:
            for name, part in {**static,"button":pressed,"PCB":pcb}.items():
                check_clear(f"button return at {travel:.2f} mm / {name}",pad,part)
    assert (cap.translate((0,spec["nominal_max_travel_mm"]+.05,0)) ^ (base+carrier)).volume() > .01
    assert (cap.translate((0,-.05,0)) ^ base).volume() > .01
    assert (cap.translate((0,0,.45)) ^ carrier).volume() > .01
    skew_poses = 0
    pivot = spec["ear_center_y_mm"]-1.7
    surroundings = {**static, **packages, "SW1":switch_body, "PCB":pcb}
    for travel, dx, dz, yaw in itertools.product([.1,.3,.5],[-.1,.1],[-.1,.1],[-.4,.4]):
        skewed = cap.translate((0,-pivot,0)).rotate((0,0,yaw)).translate((dx,pivot+travel,dz))
        for name, part in surroundings.items():
            check_clear(f"button off-centre at {travel:.2f} mm / {name}",skewed, part)
        skew_poses += 1
    return {
        "rotor_tolerance_envelopes":P["fit_budget"],
        "bearing_contacts_checked":checks,
        "display_boss_contacts":4,
        "display_collar_blocked_sightlines":144,
        "usb_plug_gauge_mm":[usb["plug_width_mm"],usb["plug_height_mm"]],
        "button_stroke_poses":len(pretravel),
        "button_off_centre_poses":skew_poses,
        "button_return_budget":return_budget(P),
    }


def service_checks(prints, cad, packages, pcb, module):
    base, carrier = prints["base"], prints["rotor-carrier"]
    grip = prints["knob"]
    bearing = as_solid(cad["bearing"])
    paddle = prints["button-cap"]
    board_assembly = {"PCB":pcb, **packages}
    ph_plug = as_solid(cad["lcd-cable-screen-plug"])
    sh_plug = as_solid(cad["lcd-cable-board-sh-plug"])
    harness = json.loads((MECHANICAL / "harness.json").read_text())
    cable_solids = {"board-end housing":sh_plug,"screen-end housing":ph_plug}
    wire_diameter = P["stock_display_cable"]["wire_od_check_mm"]
    for wire in harness["connections"]:
        cable_solids[f'{wire["signal"]} wire'] = as_solid(tube(np.array(wire["centerline_mm"]), wire_diameter/2))
    _, expanded_hardware = rotor_envelopes()
    for name, cable in cable_solids.items():
        for part in ("base","rotor-carrier","display-mount","knob"):
            check_clear(f"{name} / {part}",cable,prints[part])
        for feature, swept in expanded_hardware.items():
            check_clear(f"{name} / tolerance-expanded {feature}",cable,swept)

    for dz in SCREEN_LIFT:
        for name, moving in [("LCD",module),("PH8",ph_plug)]:
            lifted = moving.translate((0,0,dz))
            for other, part in {"base":base,"carrier":carrier,"grip":grip,"bearing":bearing}.items():
                check_clear(f"{name} lift {dz} / {other}",lifted,part)

    for dz in ROTOR_LIFT:
        for name, moving in [("carrier",carrier),("grip",grip),("bearing",bearing)]:
            raised = moving.translate((0,0,dz))
            for other, part in {"base":base, "paddle":paddle, **board_assembly}.items():
                check_clear(f"{name} lift {dz} / {other}",raised,part)

    for dz in BOARD_LIFT:
        for name, part in board_assembly.items():
            check_clear(f"{name} lift {dz} / base",part.translate((0,0,dz)),base)
    return {
        "screen_and_plug_vertical_lifts_mm":SCREEN_LIFT,
        "assembled_rotor_carrier_vertical_lifts_mm":ROTOR_LIFT,
        "pcb_vertical_lifts_mm":BOARD_LIFT,
        "harness_source_free_length_mm":harness["free_length_between_rear_housing_exits_mm"],
        "harness_wire_od_checked_mm":wire_diameter,
    }


def m2_flat_head(x, y, top, length, upside_down=False):
    # DIN 965 envelope used in the Classic. The cross recess is simplified.
    shell = combine([
        cylinder(1, 1.2, length),
        cylinder(1.9, 0, .3),
        m.Manifold.cylinder(.9, 1.9, 1, 64).translate((0,0,.3)),
    ])
    shell -= box((1.65,.43,.65),(0,0,.18)) + box((.43,1.65,.65),(0,0,.18))
    if not upside_down:
        shell = shell.rotate((180,0,0))
    return shell.translate((x,y,top))


def screws_checks(prints, pcb, packages, module):
    underside = combine(m2_flat_head(x,y,0,8,True) for x,y in CARRIER_SCREWS)
    display = combine(m2_flat_head(x,y,DISPLAY_TOP,10) for x,y in DISPLAY_SCREWS)
    for label, hardware, anchors, low, high, seat in [
        ("underside M2×8",underside,CARRIER_SCREWS,CARRIER_PILOT_BOTTOM,8.04,"rotor-carrier"),
        ("display M2×10",display,DISPLAY_SCREWS,DISPLAY_TOP-10.04,DISPLAY_BOTTOM,"base"),
    ]:
        threads = combine(cylinder(1.02,low,high,x,y) for x,y in anchors)
        for name, part in {**prints,**packages,"PCB":pcb,"LCD":module}.items():
            mask = threads if name == seat else m.Manifold()
            check_clear(f"{label} / {name}",hardware-mask,part)
        assert (hardware ^ prints[seat] ^ threads).volume() > .1,label
    return {"underside-screws":underside,"display-screws":display}


def export_assemblies(output, cad):
    offsets = {
        "underside-screws":-13,
        "rotor-carrier":81,"knob":81,"bearing":81,
        "screen-module":137,"screen-ui":137,"lcd-cable-screen-plug":137,
        "display-mount":175,"display-screws":186,
    }
    for name in cad:
        if name.startswith(("pcb-capture","pcb-pad-adhesive")):
            offsets[name] = 81
        elif name.startswith("pcb-") or name == "lcd-cable-board-sh-plug":
            offsets[name] = 39
    for exploded in [False,True]:
        scene = trimesh.Scene()
        for name, mesh in cad.items():
            if name == "lcd-cable-contacts" or (exploded and name.startswith("lcd-wire")):
                continue
            offset = offsets.get(name,0) if exploded else 0
            move = trimesh.transformations.translation_matrix([0,0,offset])
            scene.add_geometry(mesh,node_name=name,geom_name=name,transform=TO_GLTF @ move)
        scene.metadata.update({
            "product":"Classic F1 service enclosure",
            "units":"metres",
            "exploded":exploded,
            "print_count":5,
        })
        scene.export(output / ("exploded.glb" if exploded else "assembled.glb"))


def verify_assembly(output, cad, print_names):
    delivered = trimesh.load_scene(output / "assembled.glb")
    assert np.allclose(delivered.extents*1000, [2*RADIUS, DISPLAY_TOP, 2*RADIUS], atol=.01)
    deviations = {}
    for name in print_names:
        transform, geometry = delivered.graph[name]
        restored = trimesh.transform_points(delivered.geometry[geometry].vertices, TO_CAD @ transform)
        stl_vertices = cad[name].vertices
        deviation = max(
            cKDTree(restored).query(stl_vertices)[0].max(),
            cKDTree(stl_vertices).query(restored)[0].max(),
        )
        assert deviation < .00002,(name,deviation)
        deviations[name] = round(float(deviation),8)
    for name in cad:
        if name.startswith("pcb-Box0_"):
            material = cad[name].visual.material
            transform, geometry = delivered.graph[name]
            face = delivered.geometry[geometry]
            assert len(face.faces) == len(cad[name].faces),name
            assert np.allclose(trimesh.transform_points(face.vertices,TO_CAD @ transform),cad[name].vertices,atol=.00002),name
            original = material.baseColorTexture
            if original is not None:
                assert np.array_equal(np.asarray(face.visual.material.baseColorTexture),np.asarray(original)),name
    return deviations


def export_stl(output, name, solid):
    if name in ("knob", "button-cap"):
        path = output / f"{name}.stl"
        shutil.copyfile(MECHANICAL / "stl" / path.name, path)
        mesh = print_to_assembly(name,trimesh.load_mesh(path))
    else:
        mesh = as_mesh(solid.as_original().simplify(.0001))
        if name == "display-mount":
            mesh.apply_transform(trimesh.transformations.rotation_matrix(math.pi,[1,0,0]))
        z = -mesh.bounds[0,2]
        mesh.apply_translation([0,0,z])
        vertices = mesh.vertices.astype(np.float32)
        mesh = trimesh.Trimesh(vertices,mesh.faces,process=True)
        mesh.update_faces(mesh.nondegenerate_faces(height=1e-8))
        mesh.remove_unreferenced_vertices()
        assert mesh.is_watertight and mesh.is_winding_consistent and len(mesh.split()) == 1,name
        expected = mesh.copy()
        expected.apply_translation([0,0,-z])
        if name == "display-mount":
            expected.apply_transform(trimesh.transformations.rotation_matrix(-math.pi,[1,0,0]))
        file = output / f"{name}.stl"
        mesh.export(file)
        mesh = trimesh.load_mesh(file)
        assert mesh.is_watertight and mesh.is_winding_consistent and len(mesh.split()) == 1,name
        mesh.apply_translation([0,0,-z])
        if name == "display-mount":
            mesh.apply_transform(trimesh.transformations.rotation_matrix(-math.pi,[1,0,0]))
    assert mesh.is_watertight and mesh.volume > 0,name
    if name in ("knob","button-cap"):
        expected = as_mesh(solid)
    pose_error = max(cKDTree(mesh.vertices).query(expected.vertices)[0].max(),
                     cKDTree(expected.vertices).query(mesh.vertices)[0].max())
    assert pose_error < .0002,(name,pose_error)
    return mesh, float(pose_error)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=ROOT / "dist/classic-service")
    parser.add_argument("--circuit", type=Path, default=ROOT / "dist/index/circuit.json")
    args = parser.parse_args()
    circuit = json.loads(args.circuit.read_text())
    cad, source_path = source_cad()
    module = as_solid(cad["screen-module"])
    rear = rear_electronics(module)
    pcb = board_solid(circuit)
    packages = component_solids(circuit)

    board = next(row for row in circuit if row["type"] == "pcb_board")
    prints = {
        "base": make_base(board),
        "rotor-carrier": make_rotor_carrier(),
        "knob": classic_print("knob"),
        "display-mount": make_display_mount(module, rear),
        "button-cap": classic_print("button-cap"),
    }
    fixed = {**prints,"F1 PCB":pcb,"LCD module":module}
    for (a, sa), (b, sb) in itertools.combinations(fixed.items(),2):
        check_clear(f"{a} / {b}",sa,sb)
    for ref, part in packages.items():
        for name, solid in prints.items():
            check_clear(f"{name} / {ref}",solid,part)
    print("Nominal printed and electronic interfaces passed.",flush=True)
    checks = hardware_checks(prints,cad,packages,pcb,module,rear)
    checks.update(service_checks(prints,cad,packages,pcb,module))
    fasteners = screws_checks(prints,pcb,packages,module)

    args.out.mkdir(parents=True, exist_ok=True)
    stl_dir = args.out / "stl"
    stl_dir.mkdir(exist_ok=True)
    print_report = {}
    colors = {"base":"#344752","rotor-carrier":"#6b8797","knob":"#e9bd65",
              "display-mount":"#95a5ad","button-cap":"#26343d"}
    for name, solid in prints.items():
        cad[name], deviation = export_stl(stl_dir,name,solid)
        cad[name].visual.vertex_colors = trimesh.visual.color.hex_to_rgba(colors[name])
        print_report[name] = {
            "watertight_stl":True,
            "max_pose_vertex_error_mm":round(deviation,7),
            "solid_volume_mm3":round(float(cad[name].volume),2),
        }
    for old in ["lid","screen-carrier","screen-bezel","fasteners"]:
        del cad[old]
    for name, solid in fasteners.items():
        cad[name] = as_mesh(solid)
        cad[name].visual.vertex_colors = trimesh.visual.color.hex_to_rgba("#9facb2")
    export_assemblies(args.out,cad)
    for name,deviation in verify_assembly(args.out,cad,prints).items():
        print_report[name]["max_stl_to_glb_vertex_error_mm"] = deviation
    report = {
        "classic_assembly_sha256":hash_file(source_path),
        "pcb_source_sha256":hash_file(ROOT / "index.circuit.tsx"),
        "circuit_json_sha256":hash_file(args.circuit),
        "fitted_packages_checked":len(packages),
        "product_prints":print_report,
        **checks,
    }
    (args.out/"checks.json").write_text(json.dumps(report,indent=2)+"\n")
    print(f"Verified all five prints, assembly motion and the F1 PCB fit. Output in {args.out}",flush=True)


if __name__ == "__main__":
    main()
