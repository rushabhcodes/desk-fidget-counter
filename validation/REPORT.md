# Repository readiness / v5.9.0

Reviewed 9 November 2026. PCB E5 is locally checked for prototype fabrication: **two layers, 1.6mm, 39 fitted components, all top**. Mechanics E10 retains **Ø84.8×19.5mm**, six PLA prints, four screws and one complete bearing object. The display now unplugs from fitted **J6, Würth 61300821021/C5517754**, a right-angle 2×4 male header accepting the included individual female jumper ends.

Both factory cable ends remain. The 20 cm lead is shortened in its middle with eight individually heat-shrunk solder joints; the CAD shows the housings, wires, contacts and sleeves. Nominal housing dimensions and engagement are explicit approximations. Trial-dress the actual kit with slack before cutting. [Physical wiring](../manufacturing/WIRING.md) · [Assembly](../ASSEMBLY.md).

The repository is the deliverable. Temporary exports validate manufacture; no permanent fabrication kit or order was created. Download/export a consistent fresh set when ordering. Historical v5.4.0 files and older DNP-J6 pin maps must not be used.

| Check | Result |
|---|---|
| TypeScript, netlist, schematic placement | Pass; unchanged firmware test/binary evidence retained |
| Placement | Zero errors and warnings |
| Exact supplier footprints | All 39 references /177 copper pads, shapes and drills verified |
| Native routing | 122 traces /123 vias; zero native errors or warnings |
| Gerber-derived shorts | None on either layer |
| Independent KiCad 10.0.7 DRC | Zero violations and unconnected items; no per-violation exclusions |
| Fabrication export | All 177 pads and drills match source; every native trace/via unchanged |
| BOM/CPL | 23 fitted MPN lines, 39 complete /37 SMT top placements;177 physical pin coordinates |
| Current public JLCPCB catalogue | All 23 exact identities purchasable with catalogue stock; not reserved |
| Assembly CAD | 24 named mechanical parts, 39 fitted package models, six connected watertight product prints |
| Mechanical audit | 190 solid pairs; zero unexpected intersections;14 views and six STL/GLB round trips |

The native auto_local Pipeline 7 router starts empty in both phases at 2× effort. Fourteen local MCU and two encoder-bypass connections precede the remaining 31 connections. Phase pad/trace and via/pad targets are0.20/0.30mm; actual copper must meet the independent JLCPCB minimum checks. The minimum actual track is **0.115710653mm**; the four explicitly requested MCU branches remain≥0.15mm. No custom solver, manual trace/via changes or saved paths are used.

The initial connector-layout routes exposed sub0.10mm clearances and silkscreen issues in independent DRC. Labels use 1 mm text and a shorter row legend. The USB ESD device moved 0.5 mm left and 0.2mm down, and USB data nets use 0.15 mm nominal tracks, to change the native breakout. The full native route was regenerated. Only the accepted passing route is published. [Routing log](logs/e10-native-build.txt).

JLCPCB rules retain standard two-layer 1 oz FR-4, ≥0.10mm tracks/gaps, ≥0.15mm component-pad gaps, 0.30/0.60mm routing vias, ≥0.20mm NPTH-to-copper, ≥0.28mm component-drill-to-copper, ≥0.45mm component-drill spacing and≥0.30mm copper-to-edge. The exact XUNPU USB-C slots remain0.60×1.50/1.60mm, ratios2.5/2.667. No blind vias, microvias or small-drill upgrade. Independent finalization removed 0 electrically isolated GND zones and changed no native route. [Fabrication rules](../reference/fabrication-rules.json).

The new J6 footprint is retained byte-for-byte, includingØ1.1000232mm finished holes and approximatelyØ1.70mm annuli. The original unscaled supplier STEP/OBJ are retained; the assembly derivative changes only its datum and trims tails to≤0.8mm below the PCB. The body and mating posts are unscaled. Header model, female housings, wires and sleeve envelopes clear the stationary and swept moving parts. [Model provenance](../mechanical/vendor/README.md) · [Visual audit](../mechanical/AUDIT.md).

The E9 open carrier bores and 2mm screen rear-component reservation remain. Four real screen bosses have seats; both shared screws have open Ø2.2 mm clearance bores and 4mm driver access. The official screen STEP is unscaled. Its omitted electronics, exact kit mating, PLA strength/friction, bearing retention, button return/overtravel and optical opacity require physical prototype checks. USB plug clearance remains0.77mm nominal/0.31mm under the stated budget.

Public initial catalogue unit prices total about **$9.85 per fitted board**, before minimum/loss quantities, feeder/assembly/PCB charges, shipping and India taxes. This is not a quote. J6 showed 58 units and U1 showed 32 in the [dated catalogue check](../reference/jlcpcb-sourcing-2026-11-09.json). Quantities are not allocated.

**Current authenticated JLCPCB BOM match, feeder origins/rotations and engineering DFM preview remain unverified.** The browser tool could not perform a new authenticated upload. Review the exact exported files in JLCPCB before paying. No physical prototype is claimed. [Bring-up](BRINGUP.md) · [Fit checks](../mechanical/FIT.md).

[Readiness fingerprints](readiness.json),[native routing](native-routing.json),[independent DRC](kicad-drc.json),[fabrication geometry](fabrication-check.json),[BOM/CPL checks](bom-cpl-check.json),[Gerber/drill inspection](manufacturing-inspection.json) and[mechanical checks](../mechanical/geometry-check.json) record the evidence. Older PCB-preservation reports are historical and do not validate E5.
