// SPDX-License-Identifier: MIT
// Keep the CLI's real placement/courtyard failures fatal. These eight centroid
// orientation suggestions were reviewed against the completely routed Rev C PCB.
import fs from 'node:fs'
import assert from 'node:assert/strict'
import { spawnSync } from 'node:child_process'

const result = spawnSync('./node_modules/.bin/tsci', ['check', 'placement', 'index.circuit.tsx'], { encoding: 'utf8' })
const output = result.stdout + result.stderr
process.stdout.write(output)
if (result.status === 0) process.exit(0)
assert.equal(result.status, 1, 'Placement command failed unexpectedly')
assert.match(output, /placement drc:\s*Errors: 0\s*Warnings: 0/, 'Placement DRC must pass')
assert.match(output, /placement summary: 8 suboptimal orientations\s*\n/, 'New placement issues need review')
const suggestions = [...new Set([...output.matchAll(/^\s*- (R\d+) connections cross the routing path between its pads\./gm)].map(m => m[1]))].sort()
assert.deepEqual(suggestions, ['R15', 'R16', 'R17', 'R22', 'R27', 'R28', 'R5', 'R8'].sort(), 'Only the reviewed centroid hints may remain')
const circuit = JSON.parse(fs.readFileSync('dist/index/circuit.json', 'utf8'))
assert.equal(circuit.filter(c => c.type.endsWith('_error')).length, 0, 'A full routed build must pass first')
assert(circuit.filter(c => c.type === 'pcb_trace').length >= 158, 'Routed copper is required to review these hints')
console.log('Placement passed: zero placement/courtyard DRC violations; eight reviewed centroid orientation suggestions. Full copper, shorts and independent KiCad checks remain required.')
