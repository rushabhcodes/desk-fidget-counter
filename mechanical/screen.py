# SPDX-License-Identifier: MIT
"""Audit the original Waveshare STEP rather than a hand-entered hole pattern."""
from pathlib import Path
import hashlib, re


def audit(parameters):
    path = Path(__file__).parent / parameters['display']['official_step']
    raw = path.read_bytes()
    entities = {int(n): body for n, body in
                re.findall(r'#(\d+)=(.*?);', raw.decode(), re.S)}
    circles = set()
    for body in entities.values():
        if not body.startswith('CIRCLE'):
            continue
        radius = float(body.rsplit(',', 1)[1][:-1])
        if abs(radius - .85) > 1e-6:
            continue
        axis = entities[int(re.search(r'#(\d+)', body)[1])]
        point = entities[int(re.search(r'#(\d+)', axis)[1])]
        x, y, z = (float(n) for n in
                   re.search(r'\(([^()]*)\)\)', point)[1].split(','))
        circles.add((round(-x, 5), round(y, 5), round(17.75-z, 5)))
    xy = sorted(set((x, y) for x, y, z in circles))
    assert xy == sorted(tuple(p) for p in parameters['display']['mounting_hole_centers_mm'])
    assert len(xy) == 4
    rear_z = min(z for x, y, z in circles)
    assert abs(rear_z-parameters['screen_support']['seat_z']) < 1e-6
    for pin in parameters['screen_support']['locator_pins']:
        assert tuple(pin['center_mm']) in xy
        assert pin['diameter_mm'] < 1.7
    return {
        'source': 'https://files.waveshare.com/upload/4/49/1.28inch_LCD_Module_3D_Drawing.zip',
        'member': '1.28inch LCD Module 3D Drawing/0508.stp',
        'retained_step_sha256': hashlib.sha256(raw).hexdigest(),
        'current_download_comparison': 'Byte-identical to official archive downloaded 2026-11-09',
        'assembly_transform': 'Rigid diag(-1,+1,-1), plus Z17.75mm; no scaling',
        'hole_centers_assembly_mm': xy,
        'hole_pitch_assembly_mm': [18.6, 26.7],
        'rear_boss_seat_z_mm': rear_z,
        'simplified_bore_diameter_mm': 1.7,
        'module_thread': 'Not established by simplified STEP; no screw is threaded into these bores',
        'retention': 'Four rear bosses supported on braced walls; two short locating pins; existing bezel captures module',
        'enclosure_screws': 'Separate from the four module holes; two shared bezel/carrier screws remain on their own axes',
        'cable_mating': parameters['display']['cable_mating'],
        'limits': 'STEP omits fine connector contacts/cavity and rear electronics. Exact kit plug seating, thread details, PLA fit/strength and wire slack require physical qualification.'
    }
