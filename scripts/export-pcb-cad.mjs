// SPDX-License-Identifier: MIT
import fs from 'node:fs'
import { convertCircuitJsonToGltf } from 'circuit-json-to-gltf'
const circuit = JSON.parse(fs.readFileSync('dist/index/circuit.json', 'utf8'))
const glb = await convertCircuitJsonToGltf(circuit, {
  format: 'glb', boardTextureResolution: 512, includeModels: true,
})
fs.mkdirSync('mechanical/cad', { recursive: true })
fs.writeFileSync('mechanical/cad/pcb-source.glb', Buffer.from(glb))
console.log('Exported source PCB CAD, with component models and board textures.')
