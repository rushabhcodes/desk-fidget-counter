# Repository readiness / v5.8.1

Reviewed **9 November 2026**. **PCB E4 is locally checked for prototype fabrication.** J1 is now the standard XUNPU TYPEC-309-ACP16L65 / C2909598 receptacle, with an exact JLCPCB import, its real supplier CAD and a drawing-checked mounting pattern. The old short-slot connector is removed. The two-layer, 1.6 mm board has 39 references / 38 fitted components, all top; J6 remains DNP. The E9 PLA enclosure retains six prints, four screws, one complete bearing object and **Ø84.8×19.5 mm** dimensions.

The repository is the deliverable. Temporary exports were used to validate Gerbers, drill files and matching BOM/CPL sets; **no permanent fabrication kit or order is created**. Export/download a fresh consistent set yourself when ordering. The historical v5.4.0 files have an undersized FRAM footprint and outdated assembly angles; do not use them.

## CAD audit update

E9 fixes two screen-carrier issues found by a visual and solid-model audit: a 0.1 mm membrane across each shared screw bore, and insufficient allowance beneath rear electronics omitted by the supplier screen STEP. Both bores are now through holes. The carrier clears the actual screen PCB profile by 0.4 mm laterally, with a conservative 2 mm rear-component reservation. Twelve visual views, 153 solid-pair checks, independent screw/driver gauges and six STL/GLB pose comparisons pass. No unexpected interference remains under the stated geometry and fit assumptions. [Audit and images](../mechanical/AUDIT.md). Physical kit fit remains unmeasured.

The PCB source is unchanged and all **1,107 PCB records** in both new native builds are identical to validated v5.8.0. [E9 preservation evidence](e9-pcb-preservation.json) connects the current assembly to the existing E4 fabrication checks; circuit project metadata differs after the mechanical/documentation changes.

## Verified checks

| Check | Result |
|---|---|
| TypeScript, firmware/companion tests, netlist and schematic placement | Pass |
| Placement and orientation | Zero errors, zero warnings and no suboptimal orientation |
| Exact supplier footprints | 23 unchanged imports; all 39 references / **177 copper pads** verified |
| Native routing | **122 traces / 131 vias**, zero circuit error records |
| Gerber-derived shorts | No shorts on either layer |
| Independent KiCad 10.0.7 DRC | Zero violations and zero unconnected items; no per-violation exclusions |
| Export geometry | All pad centres, copper envelopes and plated drills match source; every native trace/via unchanged after finalization |
| Fresh BOM/CPL | 22 exact fitted MPN lines, 38 top placements; reference sets and source positions match, physical pin map included |
| Public JLCPCB catalogue | All 22 fitted lines purchasable with stock for at least two boards, checked 9 November |
| Assembly CAD | 22 named mechanical parts, 38 fitted package models, six watertight prints; bare/assembly PCB records identical |
| Mechanical checks | Full rotor sweep, stated tolerance probes, real screen/bosses, all package/wire clearances, USB approach and printed-button travel pass |

[Readiness fingerprints](readiness.json), [fresh native routing](native-routing.json), [independent DRC](kicad-drc.json), [export checks](fabrication-check.json), [BOM/CPL checks](bom-cpl-check.json), [drill/outline inspection](manufacturing-inspection.json) and [mechanical checks](../mechanical/geometry-check.json) contain the evidence. Older E3/E6/E7 preservation reports are historical and do not validate PCB E4.

## USB and manufacturing rules

The imported shield slots are **0.60×1.50 mm** (two) and **0.60×1.60 mm** (two): ratios **2.5:1 and 2.667:1**, above JLCPCB’s ≥2:1 guidance. The two Ø0.65 mm locating holes match the drawing’s 6 mm pitch and leave approximately 0.364 mm to adjacent copper. The supplier copper, drills and footprints were not resized. The [selection audit](../reference/usb-connector-selection.json) and [measured slot record](supplier-review.json) document the replacement.

All four VBUS contacts, four contact grounds and four shell stakes are connected. A6/B6 carry D+, A7/B7 carry D−; CC1 and CC2 retain separate 5.1 kΩ pull-downs; both SBU contacts are unconnected. The exact library pin numbers are preserved; USB A1 is marked in the top assembly view. Source origin is (0,37.55) mm, rotation 180°. The copper/drills remain supported by the short rear tab; total PCB extents are **68×83.5 mm**.

The supplier model is unscaled and rigidly aligned to its SMT lead seating plane, giving 3.161 mm above PCB against the drawing’s 3.16 mm body height. The mouth is at Y42.1865 mm and axis Z5.780 mm. A **13.4×6.9 mm** plug approach gauge clears the real PCB, packages, shell and rotating grip; nominal grip clearance is 0.77 mm. The product height remains 19.5 mm.

The [JLCPCB fabrication rules](../reference/fabrication-rules.json) use 1 oz / two-layer FR-4: track ≥0.10 mm, track/via gap ≥0.10 mm, component pad gap ≥0.15 mm, Ø0.30/0.60 mm routing via drill/pad, NPTH-to-copper ≥0.20 mm, component PTH-to-copper ≥0.28 mm, component drill spacing ≥0.45 mm and copper-to-edge ≥0.30 mm. No blind vias, microvias or small-drill upgrade is requested. ENIG and the specified outline/window remain part of the normal quote.

## Routing and reproduction

The built-in **auto_local Pipeline 7** runs two native phases at 2x effort: 14 local MCU bypass/bulk connections plus the two encoder-buffer bypass connections, then the rest of the board. Both accepted phases start with a fresh cache miss. C10 moved 0.25 mm, and the buffer bypass connections are routed in the local phase. Their individual 6 mm limits apply to the actual bypass branches; the MCU 4 mm limits remain. There is no custom solver, hand-routed copper, coordinate repair or saved-path import. Native debug messages offer path files, but the source does not import them.

Both phases request 0.15 mm tracks; the measured narrowest legal neck is **0.115710653 mm**. The four explicitly requested MCU bypass/return branches remain ≥0.15 mm, including VSSA→C8; their 4 mm decoupling-length constraint is retained. Native warnings: **0**. Any warning messages are recorded verbatim in [native-routing.json](native-routing.json); clearance, connectivity and manufacturing checks are independently enforced.

Run [the reproduction commands](../manufacturing/README.md). The independent exporter writes temporary evidence, checks all 177 copper pads against source, applies declared rules, refills GND and permits removal only of electrically isolated ground fragments. It removed **0** isolated zones. No native trace or via changed. Normal KiCad informational checks are listed in the DRC report; no electrical or drilling violation is excluded. Toolchain remains tscircuit 0.0.3077 / core 0.0.2267 / capacity-autorouter 0.0.1038, Bun 1.3.3, TypeScript 5.9.3 and KiCad 10.0.7.

## Supplier preview and first prototype

The [dated catalogue check](../reference/jlcpcb-sourcing-2026-11-09.json) confirms current exact identities and public overseas/catalogue quantities. J1 showed 1,105 units; U1 showed 42. These quantities are not reserved. Public initial unit prices sum to approximately $8.76 per fitted board before loss/minimum quantities, feeder/assembly/PCB charges, shipping and India taxes; this is not an order quote. The old $190.15 v5.4.0 quote and old signed-in 22/22 match are historical only.

The browser tool could not navigate JLCPCB to perform a new authenticated upload. **Current supplier BOM matching, feeder origins/rotations and final engineering DFM preview remain unverified.** Locally generated BOM/CPL sets and their physical pin coordinates are checked. Review those exact new files in JLCPCB before paying; normal supplier DFM and quotation are part of your order.

No physical prototype has been built yet. USB enumeration/suspend, optical counts and opacity, screen operation, current/temperature, actual button return/overtravel, PLA stiffness/creep and bearing retention require [bring-up](BRINGUP.md) and [fit tests](../mechanical/FIT.md). The official Waveshare screen STEP, four real rear-boss seats and two short locating pins are retained; the included PH lead enters sideways and its shortened ends solder at J6. Unpublished cable seating and bearing internals use the accepted approximations, with trial fit/slack required before trimming. Six prints and four screws remain; only the moving button face projects from the circular base.
