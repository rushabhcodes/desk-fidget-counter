# Desk fidget counter

A rechargeable, continuously rotating desk knob with USB-C HID scrolling and a retained full-turn counter. The STM32F072 runs independently from a computer. A physical slide switch gates scrolling; counting continues in either position.

Release **v1.0.0 / PCB Rev A**: [GitHub release and downloads](https://github.com/rushabhcodes/desk-fidget-counter/releases/tag/v1.0.0), [tscircuit project](https://tscircuit.com/rushabhcodes/desk-fidget-counter), [validation results](validation/REPORT.md), [fabrication ZIP](manufacturing/desk-knob-reva-gerbers.zip), [complete project ZIP](release/desk-knob-v1.0.0.zip).

A complete clockwise or counterclockwise revolution adds one count. Backtracking subtracts unfinished progress: +180°, −180° adds zero; +180°, −540° adds one. Completed turns remain saved; unfinished progress restarts at power-up. Sensor faults or stale samples discard uncertain partial progress instead of inventing turns.

**Rev A is a software-validated fabrication design awaiting a physical prototype.** USB enumeration, magnetic alignment, counting speed, charging temperature, battery runtime, fit and feel require the bring-up tests in [validation/BRINGUP.md](validation/BRINGUP.md). No measured hardware performance is claimed.

![Mechanical assembly](mechanical/assembly.png)

| Function | Implementation |
|---|---|
| USB | Driver-free HID mouse wheel plus standard CDC serial count console |
| Controller | STM32F072CBT6, internal HSI48/CRS, SWD and ROM boot access |
| Rotation | AS5600 12-bit magnetic angle sensor, 500 Hz target sampling |
| Persistence | MB85RC256V FRAM, alternating CRC-protected commit records |
| Charging | BQ24074 real power path, ~201 mA charge, separate NTC and MCU thermal gate |
| Cell | Protected 350 mAh 1S LiPo, USB-C rechargeable |
| Controls | Scroll slide switch; 3-second count reset button; green status LED |
| Mechanics | Ø72 × 31 mm base/knob, 25 × 37 × 7 mm bearing, diametric magnet |

## Build and use

```sh
bun install --frozen-lockfile
bun run test
bun run typecheck
bun run check:netlist
bun run check:schematic
bun run check:placement
bun run build
bun run check:shorts
```

Use [firmware/README.md](firmware/README.md) to build or flash the included binary. Initial FRAM contents are deliberately treated as unknown: hold RESET for three seconds or issue `RESET CONFIRM` once to initialize it. A rapidly blinking LED indicates invalid storage, magnet, or low battery. A brief battery heartbeat indicates healthy standalone counting. With USB connected, a steady LED indicates scroll mode; count-only mode uses the heartbeat.

Read the count with a serial terminal at 115200 baud (`STATUS` followed by newline), or:

```sh
python -m pip install pyserial==3.5
python scripts/count.py --port /dev/ttyACM0
python scripts/count.py --port /dev/ttyACM0 --reset
```

Windows uses a COM port; macOS uses `/dev/cu.usbmodem...`. HID scrolling needs no count-console program. Standard integer mouse-wheel reports use 32 ticks per revolution; OS scrolling preferences control display smoothness and direction. Wireless is omitted.

## Fabricate and assemble

- [Manufacturing specification](manufacturing/README.md): stackup, fabrication rules, actual Gerber/drill bundle, BOM, placement file and export process.
- [Assembly and mechanical guide](ASSEMBLY.md): printable files, screws, bearing, magnet, cell retention and access.
- [Datasheet contracts](reference/DATASHEETS.md): verified pinouts, footprints, charging calculations and tradeoffs.
- [Validation and bring-up](validation/BRINGUP.md): software evidence and the required physical measurements.
- [License and attribution](licenses/ATTRIBUTION.md): original work plus TinyUSB/CMSIS and reference licenses.

`index.circuit.tsx` and `parts.tsx` are the authored circuit. `dist/index/circuit.json` records the released build. The manufacturing export refills source-derived ground zones in KiCad, removes unconnected copper islands, checks the declared rules, and plots the final fabrication files. All inputs and output hashes are recorded in the release manifest.

Inspired by the [Ploopy Knob](https://ploopy.co/knob/) and [rushabhcodes/fidget-counter](https://tscircuit.com/rushabhcodes/fidget-counter). No Ploopy CAD or firmware is copied. The existing fidget-counter project is preserved.
