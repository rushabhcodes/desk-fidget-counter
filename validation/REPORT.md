# Readiness — v5.11.0 / PCB E6 / enclosure E12

Reviewed 9 November 2026. PCB E6 remains **two layers, 1.6mm, 39 fitted components, all top**. Mechanics E12 remains **Ø84.8×19.5mm**, six PLA prints and four screws. J6 remains **JST SM08B-SRSS-TB(LF)(SN)/C160407**, a keyed 8-pin side-entry SMT socket with two grounded anchors.

The display connects through **one separately ordered crimped H1 SH8-to-PH8 harness**. The supplied jumper lead is unused. H1 specifies genuine housings, contacts and 30AWG wire, with 44±1mm free insulation between housing exits. No inline joints. The CAD shows both plugs, eight wires and eight separate continuous conductor/contact assemblies. Cable seating, contact detail and installed bends remain nominal engineering approximations requiring prototype fit. [Harness drawing](../manufacturing/WIRING.md).

| Check | Result |
|---|---|
| TypeScript, netlist, schematic, placement | Pass; zero placement warnings |
| Supplier footprints |39 references /179 copper pads, shapes and drills match exact imports |
| Validated E6 native routing, preserved |124 traces /150 vias; zero native errors; 13 angle-style advisories |
| Shorts from plotted copper |None on either layer |
| Independent KiCad 10.0.7 DRC |Zero violations, zero unconnected items, no per-violation exclusions |
| Fabrication export |All 179 pad envelopes/drills match; native routed copper geometry and every via unchanged |
| BOM/CPL |23 fitted MPN lines;39 complete /38 SMT placements;179 physical pin coordinates |
| Fresh public JLCPCB catalogue check |23 exact MPN/code lines purchasable; public quantities cover two nominal boards; unreserved |
| Assembly |25 mechanical groups,39 fitted package models, six connected watertight prints |
| CAD audit |210 solid pairs, zero unexpected intersections;14 views and six STL/GLB round trips |
| Harness clearance |Ø0.8mm wire envelopes at 43/44/45mm free lengths; screen rear electronics, PCB, packages, prints and swept rotor checked |

## E12 button improvement

The side button is now a **14×6.6 mm rounded paddle** with a shallow thumb dish at Z6.4 mm and a lower apron covering the exposed PCB tab. Twin 2 mm-wide rails, broad retaining ears and separate rigid inward/outward stops guide it. Travel stays 0.6 mm. Two stacked PORON return pads maintain return bias through the nominal 0.2 mm switch gap; four 2×1.6 mm pieces come from the already specified 1.57 mm foam, with 0.05 mm 467MP between layers and against the fixed backing. No extra SKU or fastener is required. Print the cap front face down and support its outboard ears locally.

Fresh geometry checks cover 13 cap/foam stroke poses and 24 small mid-stroke skew probes. A nominal 12 mm spherical fingertip clears the desk by 0.4 mm, or 0.14 mm at the tested lower height limit. The stationary roof stays 0.4 mm below the bearing. The return-stack budget includes foam, cavity and adhesive tolerances: 0.056 mm minimum rest precompression, 44.1% maximum calculated compression. Actual force, friction, electrical closure, safe switch overtravel and cycle life remain prototype checks. [Fit and calibration](../mechanical/FIT.md#captive-front-button).

The E6 board source, bare circuit JSON and fabrication rules are unchanged. All **1,133 PCB records** in the rebuilt assembly match the validated bare board exactly. A fresh source-derived KiCad export now passes independent DRC again, and a separate Gerber/Excellon parser verifies the plotted copper/drills and both closed board contours. All 179 pad envelopes and every native trace/via are preserved. [PCB preservation evidence](e12-pcb-preservation.json). The six current product STLs and their GLB round trips pass the updated independent CAD audit. Build, footprint, shorts, placement and assembly checks pass locally. [E12 build](logs/e12-native-build.log), [geometry](logs/e12-geometry.log), [CAD audit](logs/e12-cad-audit.log).

## Preserved PCB fabrication baseline

The whole board starts empty in one native beta_pipeline9 routing pass at 2× effort. All signal and power nets request 0.15mm tracks. All connections are routed together without preserved earlier-phase copper. Router targets are 0.20mm trace/pad,0.30mm via/pad,0.35mm hole clearance and 0.60mm board edge; final factory edge minimum remains 0.30mm. Minimum actual track is **0.150000000mm**; the four explicitly requested MCU bypass branches remain≥0.15mm. No manual copper, saved paths, patched solvers or supplier copper/drill edits. Overlapping capacitor body ink is omitted while preserving its lands. Any retained angle-style advisories recommend 45-degree geometry; they are not copper-clearance or manufacturing errors. Native warnings remain visible. Independent fabrication DRC and shorts checks must still pass. The full board was regenerated from empty after the final placements. MCU HF budgets are 4mm except C10 at 5mm; the separate C18 bulk-reservoir links use 10mm budgets. These are project engineering constraints, not manufacturer-certified lengths. See [budget rationale](../reference/DATASHEETS.md#e6-bypass-routing-budgets). A bottom-layer guard prevents through-via drilling in the USB ESD signal land; the window guard retains 0.35mm beyond the physical cutout. [Accepted routing log](logs/e11-native-build.txt).

Independent checks retain normal two-layer 1oz rules:≥0.10mm track/gap,≥0.15mm component-pad gaps,0.30/0.60mm vias and≥0.30mm copper-to-edge. USB slots remain0.60×1.50/1.60mm. No microvias or small-drill upgrade. Ground refill removed 0 isolated zones and changed no routed copper geometry. At KiCad’s 1nm resolution, only duplicate zero-length export segments already covered by an equal/wider same-net endpoint may be omitted; each is recorded in the fabrication report. Native circuit JSON is unchanged. [Rules](../reference/fabrication-rules.json).

J6 has ten unmodified SMT lands and no through-holes. Its original supplier STEP/OBJ are retained; the derivative applies only a rigid datum transform. J4 is now the only through-hole header. H1 socket and cable fit without increasing enclosure height. The official screen STEP and four supported rear bosses remain; both shared screws have open Ø2.2mm bores and 4mm driver access. A 2mm rear-component allowance covers electronics omitted from the supplier screen model. [CAD audit and limits](../mechanical/AUDIT.md).

## Fresh assembly and fabrication review

The current [fabrication/assembly package](../release/desk-knob-e6-e12-fabrication.zip) binds the source to one matching set of Gerbers/drills, both BOM/CPL modes, the physical pin map, assembly drawings, KiCad source and checked firmware. It includes a separate **Gerbers-E6.zip** for upload. The outer archive and every package file were checked against their SHA256 manifests. [Upload guide](../manufacturing/current/README.md) · [Machine-readable review](assembly-fabrication-review.json).

Fresh checks: independent KiCad 10.0.7 DRC has zero violations and zero unconnected items, with no per-violation exclusions; 179 supplier pad shapes/centres/drills match; all 166 drill/slot features and both closed contours parse correctly; all native traces/vias remain unchanged. Component plated annuli are approximately 0.200 mm at USB and 0.300 mm at J4; routing via annuli are 0.150 mm. BOM/CPL populations, coordinates and rotations agree for 39 complete or 38 SMT placements. The design uses two layers and **1 oz copper** under the [checked JLCPCB limits](https://jlcpcb.com/capabilities/pcb-capabilities/).

The schematic review covers MCU supplies/bypassing, USB orientation/CC/ESD, the LDO and peripheral power switch, FRAM/I2C, optical sensor/Schmitt outputs, J4 programming, J6 display/H1 mapping and PA0 button bias. Primary datasheet links and limits of that review are recorded in the machine-readable review. Firmware/companion tests and the linked 61,344-byte image check pass; the image requests 100 mA USB power. The image checker used the available GNU `nm` through its documented `--nm nm` option.

All 23 exact MPN/code lines were rechecked on the public JLCPCB catalogue. Their published quantities cover two nominal boards and all show purchasable status. These quantities do not establish allocation, feeder approval, attrition allowances, minimum purchasing quantities or a final quote. [Current public sourcing snapshot](../manufacturing/current/checks/public-sourcing.json).

**Current authenticated JLCPCB part/feeder/rotation and engineering DFM preview remain unverified.** Review the freshly exported matching files before paying. Electrical operation, crimped cable fit, printed strength/friction, bearing retention, button action and optical opacity remain first-prototype checks. Firmware/signals are unchanged; existing binary and software-test evidence is retained. [Bring-up](BRINGUP.md) · [Fit](../mechanical/FIT.md).

The source, current fabrication/assembly package and verification record are the deliverable. No supplier upload or order was performed during fabrication review. GitHub and TSCircuit publication are separate from final factory approval. [Fingerprints](readiness.json), [routing](native-routing.json), [independent DRC](kicad-drc.json), [fabrication geometry](fabrication-check.json), [BOM/CPL](bom-cpl-check.json), [Gerber/drills](manufacturing-inspection.json), [mechanics](../mechanical/geometry-check.json). The preserved E6 design is linked to E12 by byte and geometry identity, with fresh electrical/fabrication and E12 mechanical evidence above.
