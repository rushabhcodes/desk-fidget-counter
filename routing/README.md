# Reviewed routing / Rev D

`routes.json` contains prescribed copper and `routing.ts` checks the terminal contract before applying it. A pad or placement change requires regenerating this data and repeating native placement/routing checks, copper shorts checks and independent KiCad DRC. The terminal contract alone does not prove clearance.

Rev D has a routed central window and a clipped circular outline. The routing input records every source pad, hole and fixed local escape. Its original 35×41 mm window is a conservative envelope around the final 34.6×40.6 mm routed window. Conservative route generation may merge the cutout's narrow scan-line obstacles into one enclosing 35×41 mm rectangle; this excludes slightly more corner material and does not permit copper inside the real window. Run `node routing/generate.mjs` with Node 26.12.1 to write a candidate. Generated copper is frozen only after verification against the actual source geometry.

`repair.py` uses clearance-aware two-layer A* with the actual outer polygon and internal-cutout obstacles. It treats other nets, holes, static escapes and existing vias as obstacles. Its routes still require a complete rebuild and independent DRC. No reported violation may be suppressed to make a route pass.

The released firmware uses Rev D's USB-only pin map, including PB2 peripheral-power enable. Placement, connector orientation and copper are checked as Rev D artifacts.

The released copper includes local vertex/via clearance corrections and a 0.10 mm minimum trace width. Its 117 saved branches produce 127 native PCB trace records and 178 manufactured vias. Routed vias have Ø0.6 mm pads and Ø0.3 mm drills; three ground stitching vias use Ø0.7 mm pads. The source build, shorts check and independent fabrication DRC validate the final geometry.

Rev D removes the cell and charging network. SW1 is 2mm further left to clear the optical skirt; its body/lever courtyard may overhang the PCB edge (`allowOffBoard`), while its copper lands and drills remain subject to all board-edge/fabrication rules. J6 correctly points into the internal window; the CLI outer-edge connector-access heuristic does not understand this internal mating space. Actual body, mated harness and swept-ring checks validate that access.
