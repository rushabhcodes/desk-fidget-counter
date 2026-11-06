// SPDX-License-Identifier: MIT
import models from "./mechanical/vendor/models.json"
// Resolve included assets through the local server or the publishing platform.
const base="./"
export function packageCad(name: keyof typeof models) {
  const m=models[name]
  return {objUrl:base+m.obj,modelOriginPosition:{x:0,y:0,z:0},
    modelUnitToMmScale:1,size:m.size,
    modelBounds:{min:{x:m.bounds[0][0],y:m.bounds[0][1],z:m.bounds[0][2]},
      max:{x:m.bounds[1][0],y:m.bounds[1][1],z:m.bounds[1][2]}}}
}
