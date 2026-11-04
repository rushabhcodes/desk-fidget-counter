# Rev E2 physical wiring and connector views

All board components mount from the top. The PCB frame is +X right/+Y toward USB, with the PCB top at Z=4.2 mm above the enclosure floor. Pin numbers below refer to the **board header pads**, not an arbitrary view of the mating plug. Match the moulded pin-1 mark and the LCD's printed signal labels, then check continuity before applying power.

## Permanent LCD harness H1

| Board J6 pin / physical pad XY mm | Wire colour | Signal | Waveshare 19192 connector pin |
|---|---|---|---|
| 1 / (-19.5,-10.5) | White | BL | 1 / BL |
| 2 / (-19.5,-8.5) | Violet | RST | 2 / RST |
| 3 / (-19.5,-6.5) | Orange | DC | 3 / DC |
| 4 / (-19.5,-4.5) | Yellow | CS | 4 / CS |
| 5 / (-19.5,-2.5) | Blue | CLK | 5 / CLK |
| 6 / (-19.5,-0.5) | Green | DIN | 6 / DIN |
| 7 / (-19.5,1.5) | Black | GND | 7 / GND |
| 8 / (-19.5,3.5) | Red | Switched 3.3V | 8 / VCC |

H1 uses **2×JST PHR-8 housings, 16×SPH-004T-P0.5S contacts and 8×Alpha Wire 2840/7 32AWG stranded PTFE wires**. The free insulated wire span is **24.5±0.5 mm between the two housing backs**; the model's centreline span is 24.209 mm. The wire supplier must add its actual terminal/crimp insertion allowance when determining cut length. This is a custom short pin-for-pin harness, not the included 200 mm PH-to-Dupont lead. Specify continuity by signal at both ends; do not order by ambiguous “same-side”/“opposite-side” wire-colour descriptions.

The PH8 board header is JST S8B-PH-K-S(LF)(SN), top-mounted with side entry into the PCB window. The display's header is on its underside. The module tab faces -X; its BL end is at Y=-7 mm in the assembly model. Mated plug backs are at (-11.25,Y,6.6) on the board and (8.2,Y,9.3) on the display. The eight individual paths, maximum insulation diameter and exact pin-to-pin correspondence are in `mechanical/harness.json`. They remain stationary inside the optical skirt. Do not tie them to the rotor or force a sharp bend at the crimp.

Use the correct JST crimp process/tooling for SPH-004T and 32AWG wire, inspect terminal retention and crimp pull strength, and prototype the short harness before ordering multiples. Unplug H1 before lifting the display far from the cradle; this short harness is not a service loop.

## Removable programming harness H2

J4 is JST B6B-PH-K-S(LF)(SN), top entry. Mate with PHR-6 and SPH-004T-P0.5S contacts on the same specified wire (or a compatible wire/contact combination from the JST drawing). A service harness of about 150 mm is external and removed after programming. It is not routed beneath the assembled screen.

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

Use **L-com CAU4CC-40M-1M**, a real 1 m USB-C-to-C data cable with a published 12.9×6.4 mm metal-plug cross-section ([manufacturer drawing](https://www.l-com.cn/Images/Downloadables/2D/CAU4CC-40M-1M_2D.pdf)). The board uses USB 2.0 data/5V only; the cable's higher ratings are not required or negotiated. The side opening is 14×8.8 mm around a Z=5.95 mm connector axis, leaving 1.65 mm vertically to the rotating retainer at the specified plug height. The CAD clearance tool models an 18 mm axial plug keep-out, not an invented complete supplier cable model. Verify insertion shoulder/strain relief and drawing tolerances with the actual cable; substitute only after checking its plug envelope.

There is **no internal battery, cell connector, thermistor, charging circuit or flexible battery wiring** in Rev E2.
