# PCB E5 / Mechanics E10 physical wiring

All fitted board components mount from the top. Coordinates use +X right, +Y toward USB; PCB top is Z4.2 mm above the enclosure floor. Pin numbers refer to the physical board pads. Match pin 1 and the screen's printed signal labels, then check continuity before power.

## Removable display lead H1

Waveshare SKU 19192 includes a **PH2.0 8-pin, 20 cm cable** with eight individual female jumper ends. [Package list](https://www.waveshare.com/product/1.28inch-lcd-module.htm) · [Manufacturer cable photograph](https://www.waveshare.com/img/devkit/accessories/PH2.0-wire-20cm-8PIN.jpg).

J6 is now a **fitted Würth 61300821021 / JLCPCB C5517754, 2×4 right-angle male header at 2.54 mm pitch**. It carries SPI plus reset, backlight, ground and switched 3.3 V. The individual supplied female ends fit the nominal 0.64 mm square pins; no replacement mating connector or crimp kit is needed. [Manufacturer drawing](https://www.we-online.com/components/products/datasheet/61300821021.pdf) · [JLCPCB part](https://jlcpcb.com/partdetail/WURTHELEKTRONIK-61300821021/C5517754).

The exact imported footprint retains eight Ø1.1000232 mm finished drills and approximately Ø1.70 mm annuli. The manufacturer's recommended Ø1.02±0.05 mm holes are slightly smaller; the imported holes are retained, giving clearance around the 0.64 mm square pins and approximately 0.30 mm annular rings. Do not modify the footprint or bend a straight header to substitute for this part. Trim its tails after soldering to ≤0.8 mm below the PCB and insulate the inspected wells.

| J6 physical pin / hole XY mm | Signal | Original display pin |
|---|---|---|
| 1 / (-19.08, -7.31) | BL | 1 / BL |
| 2 / (-21.62, -7.31) | RST | 2 / RST |
| 3 / (-19.08, -4.77) | DC | 3 / DC |
| 4 / (-21.62, -4.77) | CS | 4 / CS |
| 5 / (-19.08, -2.23) | CLK | 5 / CLK |
| 6 / (-21.62, -2.23) | DIN | 6 / DIN |
| 7 / (-19.08, 0.31) | GND | 7 / GND |
| 8 / (-21.62, 0.31) | VCC | 8 / VCC |

Viewed in the PCB XY frame, each Y row has an odd pin at X−19.08 mm and an even pin at X−21.62 mm. After bending, the mating pins face +X into the window: odd pins are the lower row at Z5.43 mm, even pins the upper row at Z7.97 mm. The silkscreen labels identify every signal. This is an unkeyed connection; verify by signal and continuity, never wire colour alone.

The compact cavity does not store the full 20 cm lead. **Retain both factory connector ends and shorten each wire in its middle.** Mate both ends, trial-dress with practical slack, then remove the excess. Stagger the joints as illustrated, solder by signal, and individually insulate all eight joints with heat-shrink. Do not leave bare conductors, rely on a shared sleeve, or heat the plastic housings while soldering. The model reserves a 6 mm long, Ø2 mm finished sleeve around each joint. Select tubing that fits the actual wire and stays within that envelope. No extra cable or contacts are required; heat-shrink is an assembly consumable.

Illustrated free paths are 25.6–27.9 mm between housing exits, **not cut lengths**. Allow stripping/joint overlap and assembly slack when trial dressing. The nominal housing envelopes are 14.5×2.54×2.54 mm per jumper end. Wire OD1.2 mm is rendered and OD1.5 mm is clearance-checked; the static centreline radius is at least 3.3 mm in the nominal route. Actual Waveshare housing dimensions, contact engagement and minimum bend radius are unpublished approximations. Test the actual kit and avoid repeated flexing. Unplug the display lead before lifting the screen; there is no long service loop.

## Removable programming harness H2

J4 is JST B6B-PH-K-S(LF)(SN), top entry. Mate with PHR-6 and SPH-004T-P0.5S contacts on wire qualified by the JST PH drawing (32–28 AWG, 0.5–0.9 mm insulation OD for this contact). A service harness of about 150 mm is external and removed after programming. It is not routed beneath the assembled screen.

| J4 pin / physical XY mm | Signal | Genuine ST-LINK/V2 20-pin SWD connector |
|---|---|---|
| 1 / (-5,20.5) | Target 3.3V reference | Pin 1 VAPP / VTref, probe input |
| 2 / (-3,20.5) | SWDIO | Pin 7 SWDIO |
| 3 / (-1,20.5) | SWCLK | Pin 9 SWCLK |
| 4 / (1,20.5) | NRST | Pin 15 NRST |
| 5 / (3,20.5) | GND | Pin 4 GND |
| 6 / (5,20.5) | BOOT0 | Leave empty for SWD; optional service jumper to pin 1 for ROM boot |

Power the target through USB-C while programming. VTref senses target voltage; do not connect a probe's power-output pin to it. Pin numbering on 10-pin SWD probes and low-cost ST-Link clones differs: use the probe manufacturer's documented SWDIO/SWCLK/NRST/GND/VTref signals, not this 20-pin number column. Main firmware is written by SWD; BOOT0 normally stays low through R10.

## USB cable and mechanical fit

The XUNPU C2909598 USB-C face is at Y42.1865 mm, 0.0135 mm inside the stationary side-wall radius and 0.2135 mm inside the outer floor edge; it remains accessible through the rear opening. Its 22 mm opening and the continuous 13.4×6.9 mm approach gauge include the specified [L-com drawing](https://www.l-com.cn/Images/Downloadables/2D/CAU4CC-40M-1M_2D.pdf)'s nominal 12.9×6.4 mm body plus general ±0.5 mm tolerance. The axis is Z=5.78 mm and the nominal rotor clearance is 0.77 mm (0.31 mm with the estimated axial allowance). The 35 mm gauge length is a checking volume, not a claimed cable dimension. Verify actual full insertion and strain relief.

There is **no internal battery, cell connector, thermistor, charging circuit or flexible battery wiring** in Rev E5.
