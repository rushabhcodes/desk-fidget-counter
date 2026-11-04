# Desk fidget counter / USB scroll ring

A rechargeable desk knob with a **fixed 1.28-inch round colour screen**, a freely rotating grip ring, USB-C scrolling and a retained full-turn counter. The **left-side toggle** enables scrolling; counting continues in either position, including while running on battery. The screen shows turns, battery voltage, charge status and scroll mode.

Release **v2.0.0 / PCB Rev B**: [GitHub release](https://github.com/rushabhcodes/desk-fidget-counter/releases/tag/v2.0.0), [tscircuit project](https://tscircuit.com/rushabhcodes/desk-fidget-counter), [validation](validation/REPORT.md), [Gerber ZIP](manufacturing/desk-knob-revb-gerbers.zip), [complete project ZIP](release/desk-knob-v2.0.0.zip).

![Assembled design](mechanical/assembly.png)

**This is a software-checked prototype design.** Physical counting accuracy, optical contrast, USB behaviour, charging, runtime and printed fit remain to be measured using [BRINGUP.md](validation/BRINGUP.md). Fabrication files and compiled firmware do not establish a tested hardware build.

| Function | Implementation |
|---|---|
| Screen | Waveshare 19192, GC9A01, 240×240, visible Ø32.4 mm; fixed central cradle |
| Rotation | 48-slot opaque optical ring; Vishay TCUT1600X01_A dual sensor and Schmitt buffers; 192 edges/revolution |
| Count | Unsigned 64-bit completed turns; either direction adds one, reversal cancels unfinished progress |
| Scroll | USB HID wheel, 32 reports of one wheel unit per revolution; left toggle gates output |
| Controller | STM32F072CBT6, native crystal-less USB; hardware TIM3 quadrature, SPI2 display |
| Storage | MB85RC256V FRAM, two CRC-protected journal slots, immediate completed-turn commits |
| Power | Protected Adafruit 2750 350 mAh LiPo; BQ24074 power path and nominal 201 mA charging; pouch NTC |
| Connectors | USB-C; JST-PH2 battery, JST-PH6 SWD/BOOT0, JST-PH8 screen |
| Mechanics | Ø80×47 mm, Ø68 mm grip, Ø50 mm fixed bezel, 6806ZZ 30×42×7 mm bearing |

The ring has no mechanical detents. The optical skirt must be printed in material proven opaque at 950 nm; visible black colour alone is insufficient. The screen and cable stay stationary, so there are no slip rings or twisting wires.

## Use and initialization

Power the board over USB, program it through JST J4 as described in [firmware/README.md](firmware/README.md), and issue `RESET CONFIRM` once to initialize a new FRAM. The screen otherwise shows `RESET VIA USB` and counting waits for deliberate initialization. The internal three-second reset button is a service control under the removable rotor.

```sh
python scripts/count.py --list
python scripts/count.py --port /dev/ttyACM0 status
python scripts/count.py --port /dev/ttyACM0 reset --confirm
```

Turn the left toggle on for scrolling. USB detach, suspend or toggle-off clears queued wheel movement; battery-session turns are never replayed as scrolling on reconnection. Counting stops on invalid storage or persistent battery readings below 3.45 V. Battery voltage is displayed directly; it is not presented as a calibrated state-of-charge percentage. The screen and optical LED consume power continuously, so runtime needs measurement rather than a multi-day assumption.

## Files and rebuilding

- [Assembly guide](ASSEMBLY.md): hardware, seven printed parts, cable pinout and assembly sequence.
- [3D CAD](mechanical/README.md): [assembled GLB](mechanical/cad/assembled.glb), [exploded GLB](mechanical/cad/exploded.glb), printable STLs and parametric sources.
- [Manufacturing](manufacturing/README.md): source-derived KiCad board, checked Gerbers, BOM and placement data.
- [Firmware](firmware/README.md): included BIN/HEX, source, SWD wiring, USB console and behaviour.
- [Primary design references](reference/DATASHEETS.md): pin maps, optics, display and power calculations.

```sh
bun install --frozen-lockfile
bun run typecheck && bun run test
bun run check:netlist && bun run check:schematic && bun run check:placement
bun run build
bun validation/check-design.mjs && bun run check:shorts && bun run check:assembly
```

`assembly.circuit.tsx` is the published entrypoint and includes the full product's named 3D parts. `index.circuit.tsx` is the bare PCB. Immutable per-version CAD URLs bind the tscircuit viewer to this release. The [manifest](release-manifest.json) and [checksums](release/SHA256SUMS.txt) bind generated outputs to their source inputs. Earlier Rev A fabrication and firmware remain available under their existing GitHub release tags; Rev B mechanics and firmware belong with the Rev B board.

MIT-licensed project; vendor/package assets retain their upstream notices. USB firmware uses TinyUSB development identifiers; see the firmware guide for production use.

Concept references: [Ploopy Knob](https://ploopy.co/knob/) and [rushabhcodes/fidget-counter](https://tscircuit.com/rushabhcodes/fidget-counter).
