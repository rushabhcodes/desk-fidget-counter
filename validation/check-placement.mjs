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
assert.match(output, /placement drc:\s*Errors: 0\s*Warnings: 0/, 'No placement warnings may remain')
const source=fs.readFileSync('index.circuit.tsx','utf8');assert(source.includes('doNotPlace name="J6"'),'J6 is an unpopulated optional header; its holes terminate the supplied cable')
const geometry = JSON.parse(fs.readFileSync('mechanical/geometry-check.json', 'utf8'))
assert.equal(geometry.clearances.LCD_connector_in_PCB_window, true)
console.log('Placement passed: no orientation or courtyard issues. J6 is the labelled cable termination row; the optional header is DNP. Full copper, shorts and independent KiCad checks remain required.')
