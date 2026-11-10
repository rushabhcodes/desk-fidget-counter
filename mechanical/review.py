#!/usr/bin/env python3
"""SPDX-License-Identifier: MIT. Compare actual display-collar CAD and sections.

Run with --before /path/to/E13/assembled.glb using the CAD Python environment.
No purchased geometry or camera scale is changed between the two views.
"""
from pathlib import Path
import argparse, hashlib, json, os
os.environ.setdefault('PYOPENGL_PLATFORM', 'egl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.path import Path as PlotPath
from matplotlib.patches import PathPatch
import manifold3d as md
import numpy as np
import pyrender
import trimesh
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--before', type=Path, required=True)
args = parser.parse_args()
OUT = ROOT / 'review'
OUT.mkdir(exist_ok=True)
P = json.loads((ROOT / 'parameters.json').read_text())
paths = [args.before, ROOT / 'cad/assembled.glb']
scenes = [trimesh.load(p, force='scene') for p in paths]
to_cad = np.array([[1000, 0, 0, 0], [0, 0, -1000, 0],
                   [0, 1000, 0, 0], [0, 0, 0, 1.]])
colors = {'knob': '#e9bd65', 'screen-carrier': '#95a5ad',
          'screen-bezel': '#95a5ad', 'screen-module': '#3d7260'}

def camera_pose(eye, target):
    z = np.array(eye) - np.array(target)
    z /= np.linalg.norm(z)
    x = np.cross([0, 1, 0], z)
    x /= np.linalg.norm(x)
    pose = np.eye(4)
    pose[:3, :3] = np.column_stack((x, np.cross(z, x), z))
    pose[:3, 3] = eye
    return pose

def render(source, carrier_detail=False):
    scene = pyrender.Scene(bg_color=[.965, .974, .98, 1], ambient_light=[.35]*3)
    for node in source.graph.nodes_geometry:
        if carrier_detail and node not in ['screen-carrier','screen-bezel']:
            continue
        transform, key = source.graph[node]
        scene.add(pyrender.Mesh.from_trimesh(source.geometry[key], smooth=False), pose=transform)
    target = [0, .0175 if not carrier_detail else .0155, 0]
    pose = camera_pose([.018, .037, .15] if not carrier_detail else [.025,.045,.13], target)
    scene.add(pyrender.OrthographicCamera(xmag=.031, ymag=.0163, znear=.001, zfar=2), pose=pose)
    scene.add(pyrender.DirectionalLight(color=np.ones(3), intensity=2.2), pose=pose)
    scene.add(pyrender.DirectionalLight(color=np.ones(3), intensity=.7),
              pose=camera_pose([-.08, .08, -.08], target))
    renderer = pyrender.OffscreenRenderer(1200, 630)
    try:
        image, _ = renderer.render(scene)
    finally:
        renderer.delete()
    return Image.fromarray(image)

def solid(source, name):
    transform, key = source.graph[name]
    mesh = source.geometry[key].copy()
    mesh.apply_transform(to_cad @ transform)
    mesh.merge_vertices()
    shape = md.Manifold(md.Mesh64(np.asarray(mesh.vertices, dtype=np.float64),
                                 np.asarray(mesh.faces, dtype=np.uint64)))
    assert str(shape.status()).endswith('NoError'), name
    return shape

coverage = []
for source in scenes:
    carrier = solid(source, 'screen-carrier')
    blocked = 0
    for z in [14.8, 16.0, 17.7]:
        for angle in np.linspace(0, 2*np.pi, 48, endpoint=False):
            direction = np.array([np.cos(angle), np.sin(angle), 0])
            blocked += bool(carrier.ray_cast(direction*24.3+[0, 0, z],
                                             direction*22.2+[0, 0, z]))
    coverage.append(blocked)
assert coverage[1] == 144

# Verify the rigid insertion path with the bezel removed and the PH8 plug
# already mated. Flexible wire dressing still needs a physical first assembly.
insertion_heights = [0, 1, 2, 3, 5, 7, 9, 12, 16]
current_carrier = solid(scenes[1], 'screen-carrier')
for name in ['screen-module', 'lcd-cable-screen-plug']:
    module = solid(scenes[1], name)
    for lift in insertion_heights:
        assert (current_carrier ^ module.translate((0, 0, lift))).volume() < .001, (name, lift, 'screen insertion collision')

labels = ['E13 — open underneath the bezel', 'E14 — continuous fixed collar']
comparison = Image.new('RGB', (2400, 1440), '#f6f9fb')
draw = ImageDraw.Draw(comparison)
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 30)
for i, source in enumerate(scenes):
    comparison.paste(render(source), (i*1200, 70))
    draw.text((i*1200+30, 20), labels[i], fill='#263c48', font=font)
    comparison.paste(render(source, carrier_detail=True), (i*1200, 790))
    draw.text((i*1200+30, 740), 'Grip and screen hidden — fixed carrier and bezel', fill='#263c48', font=font)
comparison.save(OUT / 'display-gap-comparison.png')

fig, axes = plt.subplots(1, 2, figsize=(13, 5.2), sharex=True, sharey=True)
for ax, source, title in zip(axes, scenes, labels):
    for name in ['knob', 'screen-module', 'screen-carrier', 'screen-bezel']:
        # Rotate CAD Y onto the slicing normal. Plot its actual X/Z section.
        polygons = solid(source, name).rotate((90, 0, 0)).slice(0).to_polygons()
        loops = []
        for polygon in polygons:
            points = np.asarray(polygon) * [1, -1]
            points = np.vstack([points, points[0]])
            loops.append(PlotPath(points, [PlotPath.MOVETO] +
                                  [PlotPath.LINETO]*(len(points)-2) + [PlotPath.CLOSEPOLY]))
        if loops:
            ax.add_patch(PathPatch(PlotPath.make_compound_path(*loops),
                                   facecolor=colors[name], edgecolor='#344752', lw=.7))
    ax.annotate('', xy=(24, 20), xytext=(24.8, 20),
                arrowprops={'arrowstyle': '<->', 'color': '#344752'})
    ax.text(24.4, 20.25, '0.8 mm rotating seam', ha='center', fontsize=9)
    ax.set(title=title, xlim=(15, 28), ylim=(12.5, 21), xlabel='Radius / mm')
    ax.set_aspect('equal')
    ax.grid(alpha=.15)
axes[0].set_ylabel('Height above desk / mm')
axes[0].annotate('Open cavity', xy=(23.2, 16.5), xytext=(18, 16.6),
                 arrowprops={'arrowstyle': '->'}, fontsize=10)
axes[1].annotate('Fixed carrier wall\n1.0 mm thick', xy=(23.3, 16.5), xytext=(17.5, 16.6),
                 arrowprops={'arrowstyle': '->'}, fontsize=10)
fig.suptitle('Actual mesh sections through the centre — unchanged screen, rotor and body height')
fig.tight_layout()
fig.savefig(OUT / 'display-gap-section.png', dpi=170)
plt.close(fig)

sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
report = {'revision': P['mechanical_revision'], 'baseline_revision': 'E13',
          'source_models_sha256': [sha(p) for p in paths],
          'source_parameters_sha256': sha(ROOT/'parameters.json'),
          'blocked_radial_sight_lines': {'before': coverage[0], 'after': coverage[1], 'total': 144},
          'preconnected_screen_insertion': {'status': 'pass', 'lift_samples_mm': insertion_heights,
              'rigid_parts': ['screen-module', 'lcd-cable-screen-plug'],
              'scope': 'Carrier aperture with bezel removed; flexible cable dressing and physical mating remain prototype checks.'},
          'rotation_clearance_mm': P['display']['rotor_radial_clearance_mm'],
          'body_diameter_mm': P['base_diameter'], 'height_mm': P['display']['bezel_top_z'],
          'scope': 'Actual assembled meshes at identical camera scale. This is a visual/geometry review, not physical qualification.',
          'images': {p.name: sha(p) for p in OUT.glob('*.png')}}
(OUT/'report.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report, indent=2))
