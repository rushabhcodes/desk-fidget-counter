# Repository readiness / v5.10.1

Reviewed 9 November 2026. PCB E6 remains **two layers, 1.6mm, 39 fitted components, all top**. Mechanics E11 remains **Ø84.8×19.5mm**, six PLA prints and four screws. J6 is now **JST SM08B-SRSS-TB(LF)(SN)/C160407**, a keyed 8-pin side-entry SMT socket with two grounded anchors.

The display connects through **one separately ordered crimped H1 SH8-to-PH8 harness**. The supplied jumper lead is unused. H1 specifies genuine housings, contacts and 30AWG wire, with 44±1mm free insulation between housing exits. No inline joints. The CAD shows both plugs, eight wires and eight separate continuous conductor/contact assemblies. Cable seating, contact detail and installed bends remain nominal engineering approximations requiring prototype fit. [Harness drawing](../manufacturing/WIRING.md).

| Check | Result |
|---|---|
| TypeScript, netlist, schematic, placement | Pass; zero placement warnings |
| Supplier footprints |39 references /179 copper pads, shapes and drills match exact imports |
| Fresh native autorouting |124 traces /150 vias; zero native errors; 13 angle-style advisories |
| Shorts from plotted copper |None on either layer |
| Independent KiCad 10.0.7 DRC |Zero violations, zero unconnected items, no per-violation exclusions |
| Fabrication export |All 179 pad envelopes/drills match; native routed copper geometry and every via unchanged |
| BOM/CPL |23 fitted MPN lines;39 complete /38 SMT placements;179 physical pin coordinates |
| Public JLCPCB catalogue |All 23 exact MPN/code lines purchasable with stock; not reserved |
| Assembly |23 mechanical groups,39 fitted package models, six connected watertight prints |
| CAD audit |171 solid pairs, zero unexpected intersections;14 views and six STL/GLB round trips |
| Harness clearance |Ø0.8mm wire envelopes at 43/44/45mm free lengths; screen rear electronics, PCB, packages, prints and swept rotor checked |

The whole board starts empty in one native beta_pipeline9 routing pass at 2× effort. All signal and power nets request 0.15mm tracks. All connections are routed together without preserved earlier-phase copper. Router targets are 0.20mm trace/pad,0.30mm via/pad,0.35mm hole clearance and 0.60mm board edge; final factory edge minimum remains 0.30mm. Minimum actual track is **0.150000000mm**; the four explicitly requested MCU bypass branches remain≥0.15mm. No manual copper, saved paths, patched solvers or supplier copper/drill edits. Overlapping capacitor body ink is omitted while preserving its lands. Any retained angle-style advisories recommend 45-degree geometry; they are not copper-clearance or manufacturing errors. Native warnings remain visible. Independent fabrication DRC and shorts checks must still pass. The full board was regenerated from empty after the final placements. MCU HF budgets are 4mm except C10 at 5mm; the separate C18 bulk-reservoir links use 10mm budgets. These are project engineering constraints, not manufacturer-certified lengths. See [budget rationale](../reference/DATASHEETS.md#e6-bypass-routing-budgets). A bottom-layer guard prevents through-via drilling in the USB ESD signal land; the window guard retains 0.35mm beyond the physical cutout. [Accepted routing log](logs/e11-native-build.txt).

Independent checks retain normal two-layer 1oz rules:≥0.10mm track/gap,≥0.15mm component-pad gaps,0.30/0.60mm vias and≥0.30mm copper-to-edge. USB slots remain0.60×1.50/1.60mm. No microvias or small-drill upgrade. Ground refill removed 0 isolated zones and changed no routed copper geometry. At KiCad’s 1nm resolution, only duplicate zero-length export segments already covered by an equal/wider same-net endpoint may be omitted; each is recorded in the fabrication report. Native circuit JSON is unchanged. [Rules](../reference/fabrication-rules.json).

J6 has ten unmodified SMT lands and no through-holes. Its original supplier STEP/OBJ are retained; the derivative applies only a rigid datum transform. J4 is now the only through-hole header. H1 socket and cable fit without increasing enclosure height. The official screen STEP and four supported rear bosses remain; both shared screws have open Ø2.2mm bores and 4mm driver access. A 2mm rear-component allowance covers electronics omitted from the supplier screen model. [CAD audit and limits](../mechanical/AUDIT.md).

Displayed public catalogue unit prices sum to approximately **$9.08 per fitted board**, excluding minimum/loss quantities, feeder/assembly/PCB charges, the H1 cable, shipping and India taxes. J6 shows 174,827 units and U1 shows 32. This is not a quote or reservation. [Dated evidence](../reference/jlcpcb-sourcing-2026-11-09.json).

**Current authenticated JLCPCB part/feeder/rotation and engineering DFM preview remain unverified.** Review the freshly exported matching files before paying. Electrical operation, crimped cable fit, printed strength/friction, bearing retention, button action and optical opacity remain first-prototype checks. Firmware/signals are unchanged; existing binary and software-test evidence is retained. [Bring-up](BRINGUP.md) · [Fit](../mechanical/FIT.md).

The repository is the deliverable. Manufacturing exports were temporary validation only; no permanent fabrication kit or order was created. [Fingerprints](readiness.json), [routing](native-routing.json), [independent DRC](kicad-drc.json), [fabrication geometry](fabrication-check.json), [BOM/CPL](bom-cpl-check.json), [Gerber/drills](manufacturing-inspection.json), [mechanics](../mechanical/geometry-check.json). Historical reports do not validate this revision.
