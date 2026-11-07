// SPDX-License-Identifier: MIT
// Publish the same native assembly output that is checked locally.
import fs from 'node:fs'
import assert from 'node:assert/strict'
const circuit = fs.readFileSync('dist/assembly/circuit.json')
assert(!JSON.parse(circuit).some(c=>c.type.endsWith('_error')), 'Build must pass before publishing')
fs.writeFileSync('dist/circuit.json', circuit)
console.log('Staged the validated full assembly at dist/circuit.json.')
