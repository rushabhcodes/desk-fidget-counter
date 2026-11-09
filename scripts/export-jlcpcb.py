#!/usr/bin/env python3
"""SPDX-License-Identifier: MIT. Export JLCPCB upload files without moving copper."""
from pathlib import Path
import argparse, csv, hashlib, json, tempfile

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('input_dir', type=Path, help='Fresh source-derived KiCad export directory containing BOM.csv and pick-and-place.csv')
parser.add_argument('--output', type=Path, help='Upload CSV destination; defaults to a temporary directory')
args = parser.parse_args()
OUT = args.output or Path(tempfile.mkdtemp(prefix='desk-jlc-check-'))
OUT.mkdir(exist_ok=True)
read_csv = lambda path: list(csv.DictReader(path.open(newline='')))
bom = [r for r in read_csv(args.input_dir / 'BOM.csv') if r['Populate'] == 'YES']
placements = read_csv(args.input_dir / 'pick-and-place.csv')
catalogue = json.loads((ROOT / 'reference/jlcpcb-parts.json').read_text())['parts']
cj = json.loads((ROOT / 'dist/index/circuit.json').read_text())
sources = {x['name']: x for x in cj if x['type'] == 'source_component'}
components = {x['source_component_id']: x for x in cj if x['type'] == 'pcb_component'}
source_ports = {x['source_port_id']: x for x in cj if x['type'] == 'source_port'}
pcb_ports = [x for x in cj if x['type'] == 'pcb_port']
refs = {r['Reference'] for r in bom}
assert refs == {r['Ref'] for r in placements} and len(refs) == 39
assert {'J4','J6'} <= refs and all(r['Side'] == 'top' for r in placements)
assert all(sources[r['Reference']]['manufacturer_part_number'] == r['MPN'] for r in bom)

def write_csv(name, fields, rows):
    with (OUT / name).open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

for mode, excluded in [('complete', set()), ('smt', {'J4'})]:
    selected = [r for r in bom if r['Reference'] not in excluded]
    groups = {}
    for r in selected:
        p = catalogue[r['MPN']]
        key = r['MPN']
        if key not in groups:
            groups[key] = {'Comment': key + ' / ' + p['description'], 'Designator': [],
                           'Footprint': p['footprint'], 'LCSC Part #': p['lcsc'],
                           'Manufacturer': r['Manufacturer'], 'MPN': key}
        groups[key]['Designator'].append(r['Reference'])
    rows = [{**r, 'Designator': ','.join(r['Designator'])} for r in groups.values()]
    write_csv('BOM-' + mode + '.csv', ['Comment', 'Designator', 'Footprint', 'LCSC Part #', 'Manufacturer', 'MPN'], rows)
    chosen = {r['Reference'] for r in selected}
    cpl = []
    for p in placements:
        if p['Ref'] not in chosen:
            continue
        pc = components[sources[p['Ref']]['source_component_id']]
        origin = pc.get('footprint_origin', pc['center'])
        # KiCad's export and Gerbers share this origin and +Y-up convention.
        # Preserve negative Y; applying abs() would mirror/misalign the board.
        assert abs(float(p['PosX']) - (100 + origin['x'])) < 1e-5
        assert abs(float(p['PosY']) - (origin['y'] - 100)) < 1e-5
        angle_error = (float(p['Rot']) - pc['rotation'] + 180) % 360 - 180
        assert abs(angle_error) < 1e-5, f"{p['Ref']} CPL rotation differs from the imported footprint frame"
        cpl.append({'Designator': p['Ref'], 'Mid X': p['PosX'], 'Mid Y': p['PosY'],
                    'Layer': 'Top', 'Rotation': f"{float(p['Rot']) % 360:.6f}"})
    assert chosen == {r['Designator'] for r in cpl}
    write_csv('CPL-' + mode + '.csv', ['Designator', 'Mid X', 'Mid Y', 'Layer', 'Rotation'], cpl)

# Physical pin positions let the assembler check asymmetric packages and feeder
# zero angles against copper instead of relying on a generic component icon.
pins = []
for p in pcb_ports:
    sp = source_ports.get(p.get('source_port_id'))
    if not sp or sp.get('pin_number') is None:
        continue
    name = next((n for n, s in sources.items() if s['source_component_id'] == sp['source_component_id']), None)
    if name not in refs:
        continue
    pins.append({'Designator': name, 'Physical pin': sp['pin_number'],
                 'Gerber X mm': f"{100 + p['x']:.6f}", 'Gerber Y mm': f"{p['y'] - 100:.6f}",
                 'Pin names': '/'.join(sp.get('port_hints', []))})
assert {p['Designator'] for p in pins} == refs
write_csv('physical-pin-map.csv', ['Designator', 'Physical pin', 'Gerber X mm', 'Gerber Y mm', 'Pin names'], pins)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
report = {
    'release': json.loads((ROOT / 'package.json').read_text())['version'],
    'pcb_revision': 'E6', 'mechanical_revision': json.loads((ROOT / 'mechanical/parameters.json').read_text())['mechanical_revision'],
    'complete_placements': 39, 'smt_only_placements': 38, 'DNP': [],
    'physical_pins': len(pins), 'all_components_top': True,
    'bom_cpl_reference_sets_match': True, 'native_placement_coordinates_preserved': True,
    'native_placement_rotations_preserved': True,
    'rotation_convention': 'KiCad placement degrees normalized to [0,360); positive CCW. Feeder zero/origin must be checked in JLCPCB preview against the physical-pin map.',
    'sourcing_attention': [r['Reference'] for r in bom if not catalogue[r['MPN']]['lcsc']],
    'stock': 'Not reserved or checkout-verified; match exact manufacturer and MPN before payment.',
    'input_hashes': {'temporary/BOM.csv': sha(args.input_dir / 'BOM.csv'),
                     'temporary/pick-and-place.csv': sha(args.input_dir / 'pick-and-place.csv'),
                     **{path: sha(ROOT / path) for path in ['dist/index/circuit.json', 'reference/jlcpcb-parts.json']}},
    'output_hashes': {p.name: sha(p) for p in sorted(OUT.glob('*.csv'))},
    'supplier_upload': 'No upload claimed for this revision. Final JLCPCB part matching, feeder origin and rotation preview must correspond to these exact current files.'
}
(OUT / 'checks.json').write_text(json.dumps(report, indent=2) + '\n')
print(f'JLCPCB CSV check passed: 39 complete / 38 SMT placements, matching BOM/CPL sets, native coordinates and physical pin map. Temporary files: {OUT}')
