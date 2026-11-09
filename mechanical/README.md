# E12 mechanics / E6 PCB

[Visual CAD audit](AUDIT.md): E9 opens both carrier screw bores through their full bosses and relieves the actual screen PCB profile to reserve 2 mm for rear electronics omitted by the supplier STEP. Fourteen inspection views, actual screw/part interference checks and print-to-GLB correspondence are recorded with the delivered model.

The enclosure uses **six product prints and four screws** while retaining the Ø84.8×19.5 mm body, fixed Waveshare 19192 display, rear USB-C and a guided front paddle with foam return. The optical track is integral to the grip. The complete bearing has one CAD visibility control; both races, shields, balls and cage are included in that object.

| Print | Orientation | Notes |
|---|---|---|
| `base` | Flat floor on bed | PCB locators, two braced screen-support walls and solder wells are integral. |
| `lid` | Supplied orientation | Support the underside annular plate above the six capture feet; avoid supports on bearing fit surfaces. |
| `knob` | Front face on bed | Integral 48-slot optical track; use material tested opaque at 950 nm. |
| `screen-carrier` | Flat annulus on bed | Short bosses share the bezel fasteners; no separate carrier screws. |
| `button-cap` | Front face down, supplied rotated pose | Rounded 14×6.6 mm paddle, 0.4 mm running clearance and separate foam return. Use local support beneath the outboard ears; keep guides free of support and burrs. No extra fasteners. |
| `screen-bezel` | Front face on bed | Use the supplied inverted pose; the glass relief faces upward during printing. |

Start with a 0.4 mm nozzle, 0.2 mm layers and six perimeters and 35–50% infill. Print the nominal fit coupon first with the actual bearing; the tight/loose alternatives help measure printer compensation. These settings are starting points, not a guarantee of fit. See [FIT.md](FIT.md).

Hardware is two DIN 965 M2×6 chassis screws and two M2×10 shared screen screws, one complete 6712ZZ bearing, six compliant PCB capture pads and two stacked foam button-return pads. There are no separate outer bearing retainer, bearing clamp, optical skirt or encoder adhesive ring. [Assembly sequence](../ASSEMBLY.md) and [off-board shopping table](../README.md#what-to-buy-outside-jlcpcb).

The PCB window is 34.6×40.6 mm, R2, for the fixed cable and the two braced support walls. PCB underside/top remain Z2.6/4.2 mm; carrier bottom Z13.1 mm, with the supplier PCB profile relieved to protect a 2 mm rear-component allowance, display front Z18.1 mm and bezel top Z19.5 mm. J4 remains at (0,+20.5) mm; disconnect its programming lead before closure. The USB keeps its rear position; the front switch has a 14×6.6 mm rounded printed paddle with a lower apron covering the PCB tab. The thumb dish is raised to Z6.4 mm to give a nominal 12 mm fingertip 0.4 mm desk clearance. The guide walls, travel stops and lid roof sit inside the circular shell; only the moving pusher projects. The circular body remains Ø84.8 mm; the cap brings overall depth to 86.6 mm. The screen is located by two short pins at its real mounting-boss centres (±9.3, ±13.35 mm), with all four rear bosses seated on the 4 mm-thick end walls. The separate enclosure screw axes remain outside those module holes. No purchased part is rescaled.

H1 is a separately purchased crimped JST-SH8-to-PH8 harness. Both keyed ends unplug; the supplied kit jumper lead is unused. Free insulation length is 44±1 mm between housing exits, not a raw cut length. The model uses Ø0.61 mm wire and checks Ø0.8 mm at 43/44/45 mm free lengths. Housing seating, contacts and static bends remain explicit engineering approximations requiring physical fit. [Harness parts and circuit map](../manufacturing/WIRING.md).

## Rebuild

With the pinned Bun dependencies and Python packages in [vendor provenance](vendor/README.md):

```sh
bun run build
python mechanical/generate.py
bun run cad:pcb
python mechanical/generate-assembly.py
python mechanical/audit.py --render
bun run build
bun run check:assembly
python mechanical/render.py
```

`parameters.json` and the source scripts define all nominal geometry. Prints are restored from their recorded bed poses to assembled positions. `cad/assembled.glb`, `cad/exploded.glb` and the per-part OBJs use the same parts; OBJ is PCB-centred millimetres/+Z-up, glTF is metres/+Y-up. Relative model paths use included files.

Checks retain the complete rotor sweep, actual screen/package models, larger wire envelope, USB/button access and race-specific bearing interfaces. All six product meshes must be connected, watertight solids. Push-fit retention is a physical test; geometry checks cannot certify friction or printer capability. [Detailed limits](vendor/README.md), [fit budget](fit-budget.json), [geometry checks](geometry-check.json) and [bring-up](../validation/BRINGUP.md).

![Braced PLA base, with support walls highlighted](screen-support.png)

The highlighted walls and webs are part of one base print. All four screen bosses seat at Z12.0 mm; the carrier clears the real PCB profile with a 0.4 mm lateral allowance and protects 2 mm below the screen PCB, so it does not compete with those seats. [Side-entry connector view](screen-connector.png) · [Source-derived screen audit](screen-fit.json). Physical PLA strength and exact kit mating remain prototype checks.

Full [assembled GLB](https://github.com/rushabhcodes/desk-fidget-counter/blob/main/mechanical/cad/assembled.glb) and [exploded GLB](https://github.com/rushabhcodes/desk-fidget-counter/blob/main/mechanical/cad/exploded.glb) downloads are retained on GitHub. These large offline exports are excluded from the TSCircuit package upload limit; its live 3D assembly uses the included OBJ models and circuit source. All six product STLs remain in both publications.
