// SPDX-License-Identifier: MIT
// Check the built board against the unchanged supplier imports, independently
// of the project's placement adapters and electrical aliases.
import fs from "node:fs"
import crypto from "node:crypto"
import assert from "node:assert/strict"
import { jlcParts } from "../jlc-parts"

const cj = JSON.parse(fs.readFileSync(process.argv[2] ?? "dist/index/circuit.json", "utf8"))
const audit = JSON.parse(fs.readFileSync("reference/jlcpcb-footprints.json", "utf8"))
const sourcePorts = new Map(cj.filter((x:any)=>x.type==="source_port").map((x:any)=>[x.source_port_id,x]))
const pcbPorts = new Map(cj.filter((x:any)=>x.type==="pcb_port").map((x:any)=>[x.pcb_port_id,x]))
const sources = cj.filter((x:any)=>x.type==="source_component")
const mm = (v:any) => v === undefined ? 0 : parseFloat(String(v))
const close = (a:number,b:number,label:string) => assert(Math.abs(a-b)<0.0002, `${label}: ${a} != ${b}`)
function children(element:any):any[] {
  if (!element) return []
  if (Array.isArray(element)) return element.flatMap(children)
  if (typeof element !== "object") return []
  return [element, ...children(element.props?.children)]
}
let checkedPads = 0
for (const source of sources) {
  const entry = audit.parts[source.manufacturer_part_number]
  assert(entry, `${source.name} needs an exact supplier import`)
  assert.equal(crypto.createHash("sha256").update(fs.readFileSync(entry.path)).digest("hex"), entry.sha256,
    `${entry.path} changed after import`)
  assert(source.supplier_part_numbers?.jlcpcb?.includes(entry.code), `${source.name} supplier identity`)
  const imported = jlcParts[source.manufacturer_part_number]({name:"REFERENCE"})
  const pads = children(imported.props.footprint).filter(x=>["smtpad","platedhole"].includes(x.type))
  const component = cj.find((x:any)=>x.type==="pcb_component" && x.source_component_id===source.source_component_id)
  const actual = cj.filter((x:any)=>["pcb_smtpad","pcb_plated_hole"].includes(x.type) && x.pcb_component_id===component.pcb_component_id)
  assert.equal(actual.length,pads.length,`${source.name} imported pad count`)
  const origin = component.footprint_origin ?? component.center
  const a = component.rotation*Math.PI/180
  for (const pad of pads) {
    const p = pad.props
    const number = Number(p.portHints.find((v:string)=>/^pin\d+$/.test(v)).slice(3))
    const target = actual.filter((q:any)=>{
      const port:any = pcbPorts.get(q.pcb_port_id)
      const sp:any = sourcePorts.get(port?.source_port_id)
      return sp?.pin_number===number
    })
    assert.equal(target.length,1,`${source.name}.${number} has one physical pad`)
    let x=mm(p.pcbX), y=mm(p.pcbY)
    if (p.points) {
      const xs=p.points.map((v:any)=>mm(v.x)), ys=p.points.map((v:any)=>mm(v.y))
      x=(Math.min(...xs)+Math.max(...xs))/2
      y=(Math.min(...ys)+Math.max(...ys))/2
    }
    const q = target[0]
    const ax = q.x ?? (Math.min(...q.points.map((v:any)=>v.x))+Math.max(...q.points.map((v:any)=>v.x)))/2
    const ay = q.y ?? (Math.min(...q.points.map((v:any)=>v.y))+Math.max(...q.points.map((v:any)=>v.y)))/2
    close(ax,origin.x+x*Math.cos(a)-y*Math.sin(a),`${source.name}.${number} X`)
    close(ay,origin.y+x*Math.sin(a)+y*Math.cos(a),`${source.name}.${number} Y`)
    const label=`${source.name}.${number}`
    if (p.shape === "polygon") {
      assert.equal(q.shape,"polygon",`${label} supplier polygon`)
      for(const v of p.points) {
        const vx=origin.x+mm(v.x)*Math.cos(a)-mm(v.y)*Math.sin(a)
        const vy=origin.y+mm(v.x)*Math.sin(a)+mm(v.y)*Math.cos(a)
        assert(q.points.some((u:any)=>Math.hypot(u.x-vx,u.y-vy)<.0002),`${label} polygon vertex preserved`)
      }
      assert.equal(q.points.length,p.points.length,`${label} polygon vertex count`)
    } else if (pad.type === "smtpad") {
      assert([p.shape,`rotated_${p.shape}`].includes(q.shape),`${label} supplier pad shape`)
      const expectedAngle=a+mm(p.pcbRotation)*Math.PI/180
      const actualAngle=mm(q.ccw_rotation)*Math.PI/180
      const bounds=(w:number,h:number,r:number)=>[
        Math.abs(Math.cos(r))*w+Math.abs(Math.sin(r))*h,
        Math.abs(Math.sin(r))*w+Math.abs(Math.cos(r))*h]
      const expected=bounds(mm(p.width),mm(p.height),expectedAngle)
      const actual=bounds(q.width,q.height,actualAngle)
      expected.forEach((v,i)=>close(actual[i],v,`${label} copper extent ${i}`))
      if(p.radius!==undefined)close(q.radius,mm(p.radius),`${label} corner radius`)
    } else {
      for(const [key,actual] of [
        ["holeDiameter",q.hole_diameter], ["outerDiameter",q.outer_diameter],
        ["holeWidth",q.hole_width], ["holeHeight",q.hole_height],
        ["outerWidth",q.outer_width], ["outerHeight",q.outer_height],
      ] as const)if(p[key]!==undefined)close(actual,mm(p[key]),`${label} ${key}`)
      if(p.rectPad)assert.equal(q.pad_shape,"rect",`${label} rectangular annulus`)
    }
    checkedPads++
  }
}
// RAMXEED DS501-00017-11v1-E p17: 6.00 +/-0.20mm lead span,
// 1.27mm pitch and 0.41 +/-0.10mm lead width. The old footprint put the
// lands under the body; require the new lands to cover both toe extremes.
const fram = sources.find((x:any)=>x.name==="U3")
const pc = cj.find((x:any)=>x.type==="pcb_component" && x.source_component_id===fram.source_component_id)
const origin = pc.footprint_origin ?? pc.center
const framPads = cj.filter((x:any)=>x.type==="pcb_smtpad" && x.pcb_component_id===pc.pcb_component_id)
assert.equal(framPads.length,8)
for (const pad of framPads) {
  const x = Math.abs(pad.x-origin.x)
  const a = (pad.ccw_rotation??0)*Math.PI/180
  const spanX = Math.abs(Math.cos(a))*pad.width+Math.abs(Math.sin(a))*pad.height
  const spanY = Math.abs(Math.sin(a))*pad.width+Math.abs(Math.cos(a))*pad.height
  assert(x-spanX/2 < 2.9 && x+spanX/2 > 3.1,"FRAM lands must cover the real lead toes")
  assert(spanY >= .51,"FRAM lands must cover maximum lead width")
}
console.log(`Exact JLCPCB imports verified: ${sources.length} references, ${checkedPads} copper pad centres/shapes/dimensions and plated drills; FRAM physical lead envelope covered.`)
