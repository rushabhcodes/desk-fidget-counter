// SPDX-License-Identifier: MIT
import fs from 'node:fs'
import { convertCircuitJsonToGltf } from 'circuit-json-to-gltf'
const circuit = JSON.parse(fs.readFileSync('dist/index/circuit.json', 'utf8'))
// Resolve the included model bytes locally for an offline CAD export.
for (const part of circuit.filter(c=>c.type==='cad_component')) {
  const url=part.model_obj_url
  if(url?.includes('/mechanical/vendor/obj/') || url?.includes('/easyeda_models/assets/')) {
    const local='mechanical/vendor/obj/'+url.split('/').pop().split('?')[0]
    part.model_obj_url='data:text/plain;base64,'+fs.readFileSync(local).toString('base64')
  }
}
const glb = await convertCircuitJsonToGltf(circuit, {
  format: 'glb', boardTextureResolution: 512, includeModels: true,
})
fs.mkdirSync('mechanical/cad', { recursive: true })
fs.writeFileSync('mechanical/cad/pcb-source.glb', Buffer.from(glb))
console.log('Exported source PCB CAD, with component models and board textures.')
