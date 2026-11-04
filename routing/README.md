# Reviewed routing / Rev C

`routes.json` contains prescribed copper and `routing.ts` checks the terminal contract before applying it. A pad or placement change requires regenerating this data and repeating native placement/routing checks, copper shorts checks and independent KiCad DRC. The terminal contract alone does not prove clearance.

Rev C has a routed central window and a clipped circular outline. The routing input records every source pad, hole and fixed local escape. Its original 35×41 mm window is a conservative envelope around the final 34.6×40.6 mm routed window. Conservative route generation may merge the cutout's narrow scan-line obstacles into one enclosing 35×41 mm rectangle; this excludes slightly more corner material and does not permit copper inside the real window. Run `node routing/generate.mjs` with Node 26.12.1 to write a candidate. Generated copper is frozen only after verification against the actual source geometry.

`repair.py` uses clearance-aware two-layer A* with the actual outer polygon and internal-cutout obstacles. It treats other nets, holes, static escapes and existing vias as obstacles. Its routes still require a complete rebuild and independent DRC. No reported violation may be suppressed to make a route pass.

The released firmware uses the same electrical pin map as Rev B. Placement, connector orientation and copper are new and must be checked as Rev C artifacts.

The released copper includes local vertex/via clearance corrections and a 0.10 mm minimum trace width. Its 158 saved branches produce 171 native PCB trace records and 222 manufactured vias. The source build, shorts check and independent fabrication DRC validate the final geometry.
