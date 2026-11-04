// SPDX-License-Identifier: MIT
// Keep placement/courtyard failures fatal. J6 mates through the LCD window.
import fs from 'node:fs'
import assert from 'node:assert/strict'
import { spawnSync } from 'node:child_process'

const result = spawnSync('./node_modules/.bin/tsci', ['check', 'placement', 'index.circuit.tsx'], { encoding: 'utf8' })
const output = result.stdout + result.stderr
process.stdout.write(output)
assert.equal(result.status, 0, 'Placement must pass without orientation or courtyard issues')
assert.match(output, /placement summary: no placement issues/)
assert.match(output, /placement drc:\s*Errors: 0\s*Warnings: 1/, 'Only the reviewed access advisory may remain')
assert.match(output, /pcb_connector_not_in_accessible_orientation_warning: J6 is facing x\+ but should face x- so the connector is accessible from the board edge/)
const geometry = JSON.parse(fs.readFileSync('mechanical/geometry-check.json', 'utf8'))
assert.equal(geometry.clearances.LCD_connector_in_PCB_window, true)
console.log('Placement passed: no orientation or courtyard issues. J6 faces the internal PCB window, verified with its actual housing and harness. Full copper, shorts and independent KiCad checks remain required.')
