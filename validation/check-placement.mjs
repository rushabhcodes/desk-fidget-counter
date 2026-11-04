// SPDX-License-Identifier: MIT
// Keep real placement/courtyard failures fatal. These centroid suggestions and
// J6's internal-window access were reviewed against routed Rev D and its CAD.
import fs from 'node:fs'
import assert from 'node:assert/strict'
import { spawnSync } from 'node:child_process'

const result = spawnSync('./node_modules/.bin/tsci', ['check', 'placement', 'index.circuit.tsx'], { encoding: 'utf8' })
const output = result.stdout + result.stderr
process.stdout.write(output)
if (result.status === 0) process.exit(0)
assert.equal(result.status, 1, 'Placement command failed unexpectedly')
assert.match(output, /placement drc:\s*Errors: 0\s*Warnings: 1/, 'Only the reviewed access advisory may remain')
assert.match(output, /pcb_connector_not_in_accessible_orientation_warning: J6 is facing x\+ but should face x- so the connector is accessible from the board edge/)
assert.match(output, /placement summary: 4 suboptimal orientations\s*\n/, 'New placement issues need review')
const suggestions = [...new Set([...output.matchAll(/^\s*- (R\d+) connections cross the routing path between its pads\./gm)].map(m => m[1]))].sort()
assert.deepEqual(suggestions, ['R15', 'R16', 'R27', 'R28'].sort(), 'Only the reviewed centroid hints may remain')
const circuit = JSON.parse(fs.readFileSync('dist/index/circuit.json', 'utf8'))
assert.equal(circuit.filter(c => c.type.endsWith('_error')).length, 0, 'A full routed build must pass first')
assert(circuit.filter(c => c.type === 'pcb_trace').length >= 117, 'Routed copper is required to review these hints')
const geometry = JSON.parse(fs.readFileSync('mechanical/geometry-check.json', 'utf8'))
assert.equal(geometry.clearances.LCD_connector_in_PCB_window, true)
console.log('Placement reviewed: zero placement/courtyard errors; four centroid hints and the J6 access advisory. J6 faces the internal PCB window, verified with its actual housing and harness. Full copper, shorts and independent KiCad checks remain required.')
