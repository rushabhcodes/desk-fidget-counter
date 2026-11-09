// SPDX-License-Identifier: MIT
import fs from 'node:fs'
import assert from 'node:assert/strict'
import { createHash } from 'node:crypto'
import { loadOBJ, COORDINATE_TRANSFORMS } from 'circuit-json-to-gltf'
const read = path => JSON.parse(fs.readFileSync(path, 'utf8'))
const board = read('dist/index/circuit.json')
const assembled = read('dist/assembly/circuit.json')
const parts = read('mechanical/cad/parts.json')
for (const name of ['button-return-pads','button-return-adhesive']) {
  assert(parts.some(p=>p.name===name),`Missing button return material ${name}`)
}
assert.deepEqual(parts.filter(p=>p.name==='bearing'||p.name.startsWith('bearing-')).map(p=>p.name),['bearing'],'The complete bearing must have one visibility control')
for(const removed of ['button-plunger','lcd-cable-board-plug','outer-retainer','inner-retainer','bearing-clamp','encoder-skirt','encoder-adhesive'])assert(!parts.some(p=>p.name===removed),`${removed} must not appear in the current assembly`)
assert.equal(read('tscircuit.config.json').mainEntrypoint, 'assembly.circuit.tsx')
assert.equal(assembled.filter(c => c.type.endsWith('_error')).length, 0)
// Adding mechanical parts must not perturb a single manufactured PCB record.
const copper = cj => cj.filter(c => c.type.startsWith('pcb_'))
assert.deepEqual(copper(assembled), copper(board), 'Assembly must preserve bare-board copper and placement')
const sources = new Map(assembled.filter(c => c.type === 'source_component').map(c => [c.name, c]))
const cad = assembled.filter(c => c.type === 'cad_component')
assert(cad.some(c=>c.source_component_id===sources.get('J6').source_component_id),'J6 must have its fitted right-angle header model')
for (const name of ['lcd-cable-board-sh-plug']) assert(parts.some(p=>p.name===name),`Missing removable-cable detail ${name}`)
for (const part of parts) {
  const source = sources.get(part.name)
  assert(source, `Missing assembly part ${part.name}`)
  assert.equal(source.ftype, part.printed ? 'printedpart' : 'subassembly')
  if (part.printed) assert.equal(source.material, 'pla', `${part.name} must use the requested PLA material`)
  const model = cad.find(c => c.source_component_id === source.source_component_id)
  assert(model, `Missing CAD for ${part.name}`)
  assert.equal(model.model_obj_url, `./mechanical/cad/${part.asset}`, 'Assembly assets must travel with the repository')
  assert.deepEqual(model.position, { x: 0, y: 0, z: 0 })
  assert.deepEqual(model.model_origin_position, { x: 0, y: 0, z: 0 })
  assert.equal(model.model_unit_to_mm_scale_factor, 1)
  const bytes = fs.readFileSync(`mechanical/cad/${part.asset}`)
  const mesh = await loadOBJ({ url: `data:text/plain;base64,${bytes.toString('base64')}`, transform: COORDINATE_TRANSFORMS.OBJ_Z_UP_TO_Y_UP })
  const expected = part.bounds_pcb_mm
  for (const [axis, index] of [['x', 0], ['y', 2], ['z', 1]]) {
    assert(Math.abs(mesh.boundingBox.min[axis] - expected[0][index]) < 1e-4, `${part.name} min ${axis}`)
    assert(Math.abs(mesh.boundingBox.max[axis] - expected[1][index]) < 1e-4, `${part.name} max ${axis}`)
  }
}
const geometry = read('mechanical/cad/assembly-check.json')
assert.equal(geometry.fastener_count,4)
assert.equal(geometry.product_print_count,6)
assert.deepEqual(parts.filter(p=>p.printed).map(p=>p.name).sort(),['base','button-cap','knob','lid','screen-bezel','screen-carrier'])
assert.equal(geometry.source_parameters_sha256, createHash('sha256').update(fs.readFileSync('mechanical/parameters.json')).digest('hex'))
assert.equal(geometry.source_board_tsx_sha256, createHash('sha256').update(fs.readFileSync('index.circuit.tsx')).digest('hex'))
for (const [name, artifact] of Object.entries(geometry.cad_files)) {
  assert.equal(createHash('sha256').update(fs.readFileSync(`mechanical/cad/${name}`)).digest('hex'), artifact.sha256)
}
const audit = read('mechanical/audit/report.json')
assert.equal(audit.model_sha256, geometry.cad_files['assembled.glb'].sha256, 'Rerun the CAD audit after changing assembly geometry')
assert.deepEqual(audit.unexpected_intersections, [], 'No unplanned mechanical interference may remain')
assert.equal(audit.carrier_through_bores, 2, 'Both shared screen screws need open clearance bores')
for (const [name, check] of Object.entries(audit.print_checks)) {
  assert.equal(createHash('sha256').update(fs.readFileSync(`mechanical/stl/${name}.stl`)).digest('hex'), check.stl_sha256, `${name} print changed after its CAD audit`)
}
console.log(`Assembly passed: ${parts.length} named mechanical parts, correct OBJ axes/scale, assembled poses, GLB hashes and identical PCB geometry.`)
