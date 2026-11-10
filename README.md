# Desk fidget counter

A USB-powered scroll ring with a fixed **1.28-inch round display**. It counts complete turns, retains the count in FRAM, and shows your computer’s clock, CPU/RAM usage and battery through a USB companion app.

Short-press the front button to switch between scrolling and counting only. Hold for three seconds to clear the count. The screen and cable stay fixed while the outer grip rotates.

![Desk knob assembly](mechanical/assembly.png)

## Board and enclosure

- **Two-layer, 1.6 mm PCB**, with all 52 fitted components on top. USB-C is on the rear; a 14×7 mm curved button with guided travel and foam return operates the front Omron switch.
- **Six product prints and four screws**, in an approximately **Ø89.4 × 19.5 mm** body, with the button inside its circular outline. The optical skirt is integral to the grip; the screen carrier and bezel share two screws.
- **One complete 6712ZZ bearing object** in the CAD viewer, including its races, shields, balls and cage. Calibrate the printed bearing fits with the coupons before printing the enclosure.
- The source defines connectivity, supplier footprints, placement and fabrication rules. F1 uses independently checked external routing through TSCircuit’s documented custom-router interface; the stored copper is guarded against changes to its input. See [routing](routing/README.md).

**Current electronics: RP2040 PCB F1 / firmware 6.0.0.** The STM32 has been replaced with an RP2040, 2 MB Winbond boot flash, a 12 MHz Abracon crystal, local supply bypassing and 27 Ω USB termination. The PCB outline and connector, sensor and switch datums remain compatible with the Ø89.4 mm E14 enclosure and its recessed circular button. Local circuit, fabrication and assembly checks pass for a first prototype. The older E6 archive targets STM32; use the matching [F1 fabrication kit](release/desk-knob-f1-e14-fabrication.zip). See [readiness](validation/readiness.json) and the [firmware/programming guide](firmware/README.md).

[Visual CAD audit](mechanical/AUDIT.md): fourteen inspection views, corrected carrier screw bores and reserved space for screen rear electronics; enclosure height remains 19.5 mm.

[E14 visual review](mechanical/VISUAL-REVIEW.md): a continuous fixed collar covers the open underside of the screen bezel. It belongs to the existing carrier and retains the 0.8 mm rotating seam, body dimensions, six prints and four screws.

## What to buy outside JLCPCB

Quantities below are for **one complete device**. A complete JLCPCB **assembly** order supplies the PCB and its 52 fitted electronic components, including the MCU, optical sensor, FRAM, USB connector, front button, J4 programming header and J6 removable display header. A bare-PCB order supplies the board only.

| Qty | Buy or supply separately | Specification and purpose |
|---|---|---|
| 1 kit | [Waveshare 19192 display](https://www.waveshare.com/product/1.28inch-lcd-module.htm) | Non-touch, 1.28-inch, 240×240 GC9A01 module. The supplied PH-to-jumper lead is unused. Connect using replacement H1 below. |
| 1 | [Complete 6712ZZ bearing](https://maysmeprecision.com/Show/?Cid=677) | **60 mm bore × 75 mm OD × 7 mm**, double metal shields. Buy the assembled bearing; its internal balls/races are not separate purchases. |
| 6 | [E14 printed enclosure parts](mechanical/stl) | `base`, `lid`, `knob`, `screen-carrier`, `screen-bezel`, `button-cap`. PLA; the grip’s integral optical track must be **opaque at 950 nm**. Black colour alone does not establish this. Print the fit coupons first. |
| 2 | Countersunk **DIN 965 M2×6** screws | Attach the base and lid. Nominal head Ø3.8 mm; check the actual purchased head/drive against the model. |
| 2 | Countersunk **DIN 965 M2×10** screws | One shared pair retains the screen bezel and carrier on the braced screw supports. |
| 1 small piece | [PORON 4701-30-20062-04 foam](https://www.rogerscorp.com/elastomeric-material-solutions/poron-industrial-polyurethanes/poron-4701-30) | **1.57 mm** nominal, 320 kg/m³. Cut four Ø4 mm and two Ø2.6 mm PCB capture pads, plus four 2×1.6 mm pieces for two stacked button-return pads; a 20×20 mm sample is sufficient. |
| 1 small piece | [3M 467MP transfer adhesive](https://www.3m.com/3M/en_US/p/dc/v000185218/) | **0.05 mm** adhesive for the six PCB pads and the two stacked button-return pads. The integral optical skirt needs no separate adhesive joint. |
| As needed | [3M 5413 polyimide tape](https://www.3m.co.uk/3M/en_GB/p/d/v000091659/) | **0.069 mm** insulation over inspected underside solder wells. Trim through-hole tails/joints to the documented ≤0.8 mm allowance first. |
| 1 assembled lead | **H1 keyed display harness** | Order a crimped **JST SHR-08V-S-B to PHR-8**, eight wires, straight circuit mapping 1→1 through 8→8, **44±1 mm free insulation between rear housing exits**. [Parts and drawing](manufacturing/WIRING.md). This custom lead is separate from both the display kit and JLCPCB assembly. |
| 1, reuse if suitable | USB data cable | USB-C at the device; ordinary USB 2.0 data is sufficient. Check the plug against the enclosure’s documented 13.4×6.9 mm approach gauge. |
| Optional: 3 | Adhesive silicone feet | Approximately Ø5×1 mm. These add 1 mm to the nominal body height. |

**H1 is a replacement crimped cable, purchased separately. J6’s keyed JST-SH socket is fitted by JLCPCB, including in the SMT-only option.** The display, bearing, printed parts and final wiring/mechanical assembly are not supplied as part of PCB assembly.

### Programming equipment and tools

These items are reusable and removed before closing the enclosure:

| Qty | Item | Requirement |
|---|---|---|
| 1 | SWD programmer | CMSIS-DAP / Raspberry Pi Debug Probe supporting RP2040. USB powers the board; VTref is a sense connection. |
| 1 | J4 programming lead | JST **PHR-6**, 2.0 mm PH series, with the correct probe-end termination. A precrimped lead can be used. If making it, use six **SPH-004T-P0.5S** contacts plus spares and qualified 32–28 AWG wire, insulation Ø0.5–0.9 mm. See the [physical pin map](https://github.com/rushabhcodes/desk-fidget-counter/blob/main/manufacturing/WIRING.md). |
| 1, only for SMT-only PCBA | J4 board header | The **51-placement SMT-only** option includes J6 and leaves only **JST B6B-PH-K-S(LF)(SN), C131342** for local through-hole soldering. Complete assembly has 52 placements. |

Have solder/flux and a soldering setup, wire stripper, flush cutters, multimeter, caliper, an M2×0.4 tap and a screwdriver matching your screws. Follow the [printing and fit guide](mechanical/FIT.md); the supplied print orientations and support notes matter.

## Software and controls

Flash firmware 6.0.0 through J4 SWD or the RP2040 USB UF2 bootloader, then initialize a fresh FRAM with a three-second button hold or the explicit console command in the [firmware guide](https://github.com/rushabhcodes/desk-fidget-counter/blob/main/firmware/README.md).

For laptop information:

```sh
python -m pip install -r companion/requirements.txt
python companion/dashboard.py
```

The [companion guide](https://github.com/rushabhcodes/desk-fidget-counter/blob/main/companion/README.md) covers macOS, Windows and Linux. Counting and scrolling work without the companion while USB is awake. USB suspend switches the display and encoder off; turns during suspend are not measured.

## Build and validation

```sh
bun install --frozen-lockfile
bun run typecheck && bun run test
bun run check:netlist && bun run check:schematic
bun run build
bun run check:placement && bun validation/check-design.mjs
bun run check:footprints && bun run check:shorts && bun run check:assembly
```

The lockfile pins a compatible released `@tscircuit/circuit-json-util` for the CLI’s KiCad exporter; no router or library source is patched.

`assembly.circuit.tsx` is the complete product; `index.circuit.tsx` is the bare PCB. The build stages the checked full assembly at `dist/circuit.json` for publication. Source, package CAD, prints and wiring are included in the repository. The [F1/E14 fabrication kit](release/desk-knob-f1-e14-fabrication.zip) includes matching Gerbers, BOM/CPL, physical pin maps, independent checks and RP2040 firmware. Follow the [upload guide](manufacturing/current/README.md). Final factory preview and physical prototype bring-up remain; no supplier upload or order has been made.

- [Assembly steps](https://github.com/rushabhcodes/desk-fidget-counter/blob/main/ASSEMBLY.md) · [Wiring and programming connections](https://github.com/rushabhcodes/desk-fidget-counter/blob/main/manufacturing/WIRING.md)
- [Mechanical source and CAD](https://github.com/rushabhcodes/desk-fidget-counter/blob/main/mechanical/README.md) · [Model provenance and limitations](https://github.com/rushabhcodes/desk-fidget-counter/blob/main/mechanical/vendor/README.md)
- [Manufacturing requirements](https://github.com/rushabhcodes/desk-fidget-counter/blob/main/manufacturing/README.md) · [Validation results](https://github.com/rushabhcodes/desk-fidget-counter/blob/main/validation/REPORT.md) · [First-prototype bring-up](https://github.com/rushabhcodes/desk-fidget-counter/blob/main/validation/BRINGUP.md)

Inspired by the [Ploopy Knob](https://ploopy.co/knob/) and [original fidget counter](https://tscircuit.com/rushabhcodes/fidget-counter). Project code and original geometry are MIT; purchased-part assets retain their upstream rights.
