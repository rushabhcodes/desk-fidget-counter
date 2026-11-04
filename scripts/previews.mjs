// SPDX-License-Identifier: MIT
import fs from 'node:fs'
import {convertCircuitJsonToPcbSvg,convertCircuitJsonToSchematicSvg} from 'circuit-to-svg'
import {Resvg} from '@resvg/resvg-js'
const cj=JSON.parse(fs.readFileSync('dist/index/circuit.json','utf8'))
const cleanSvg=svg=>svg.replace(/^[\t ]+$/gm,'').trimEnd()+'\n'
fs.mkdirSync('previews',{recursive:true})
for(const p of fs.readdirSync('previews').filter(p=>/^schematic-\d+-.*\.(svg|png)$/.test(p))) fs.unlinkSync('previews/'+p)
for(const sheet of cj.filter(x=>x.type==='schematic_sheet')){
 const svg=convertCircuitJsonToSchematicSvg(cj,{schematicSheetId:sheet.schematic_sheet_id,width:1800,height:1250})
 const name=`previews/schematic-${sheet.sheet_index+1}-${sheet.display_name.toLowerCase().replace(/[^a-z0-9]+/g,"-")}`
 fs.writeFileSync(name+'.svg',cleanSvg(svg));fs.writeFileSync(name+'.png',new Resvg(svg).render().asPng())
}
for(const layer of ['top','bottom']){
 const svg=convertCircuitJsonToPcbSvg(cj,{layer,width:1500,height:1500})
 fs.writeFileSync(`previews/pcb-${layer}.svg`,cleanSvg(svg))
 fs.writeFileSync(`previews/pcb-${layer}.png`,new Resvg(svg).render().asPng())
}
// Run bom-and-assembly.py before this script to refresh its pin-1 diagrams.
if(fs.existsSync('previews/wiring.svg')) fs.writeFileSync('previews/wiring.png',new Resvg(fs.readFileSync('previews/wiring.svg','utf8')).render().asPng())
for (const side of ['top','bottom']) {
 const path=`previews/assembly-${side}`
 if(fs.existsSync(path+'.svg')) fs.writeFileSync(path+'.png',new Resvg(fs.readFileSync(path+'.svg','utf8')).render().asPng())
}
