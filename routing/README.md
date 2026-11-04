# Reviewed routing / Rev B

`routes.json` contains the prescribed two-layer copper. `routing.ts` verifies its terminal contract before applying it. Component/pad edits still require a complete rebuild, placement checks, shorts checks and independent KiCad DRC; the contract alone is not a clearance check.

`input.json` records the routing input used for the Rev B repairs. `repair.py` is a two-layer A* utility using NumPy and Shapely; it treats other nets, holes, fixed local traces and existing vias as obstacles. It preserves short reviewed escape sections where necessary. Frozen copper, rather than a new nondeterministic autorouter run, is the released result.

The charger EN1 pulldown was rotated for a straight local escape. LCD software CS uses spare PA8 to avoid congested SPI pin escapes. Two final KiCad margin corrections were a local 0.23 mm neck and 0.02 mm bend adjustment in a 3V3 branch, plus small via adjustments (0.02 mm and 0.0075 mm). A 0.005 mm offset at the CHG_EN1 via (9.8,−1.495) avoids a horizontal drill/trace arc degeneracy in the geometry checker; independent copper clearance and shorts checks still run normally.

To repair selected paths in an edited design, regenerate the input/terminal contract from that source, inspect which branches must move, run `python routing/repair.py <trace-id> ...`, and repeat every validation/export step. Review any retained escape or manual coordinate correction after rerouting. Do not publish a new path merely because the pathfinder found one.
