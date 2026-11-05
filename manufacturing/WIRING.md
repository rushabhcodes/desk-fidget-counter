# Rev E3 physical wiring and connector views

All board components mount from the top. The PCB frame is +X right/+Y toward USB, with the PCB top at Z=4.2 mm above the enclosure floor. Pin numbers below refer to the **board header pads**, not an arbitrary view of the mating plug. Match the moulded pin-1 mark and the LCD's printed signal labels, then check continuity before applying power.

## Included display lead H1 — no separate harness purchase

Waveshare SKU 19192 includes a **PH2.0 8-pin, 20 cm cable**, with the PH plug at the display end and eight individual female jumper sockets at the board end. See the [manufacturer package list](https://www.waveshare.com/product/1.28inch-lcd-module.htm) and its [actual cable photograph](https://www.waveshare.com/img/devkit/accessories/PH2.0-wire-20cm-8PIN.jpg). The former JST-PH board header did **not** accept those jumper sockets.

The compact E3 build keeps the original display plug, shortens the supplied wires, and solders their stripped board ends into J6. **Do not populate J6's optional 61300811021 male header. No extra PH housings, crimp contacts, replacement wire or adapter cable is needed.** J6 has eight Ø1.2 mm plated holes at 2.54 mm pitch, inserted/soldered from the top. The same row can take the optional right-angle male header if the cable is kept intact, but storage of all 20 cm is not modelled or fit-qualified in this low enclosure.

| J6 pin / pad XY mm | Signal | Original display connector pin |
|---|---|---|
| 1 / (−21.5,4.39) | Switched 3.3V | 8 / VCC |
| 2 / (−21.5,1.85) | GND | 7 / GND |
| 3 / (−21.5,−0.69) | DIN | 6 / DIN |
| 4 / (−21.5,−3.23) | CLK | 5 / CLK |
| 5 / (−21.5,−5.77) | CS | 4 / CS |
| 6 / (−21.5,−8.31) | DC | 3 / DC |
| 7 / (−21.5,−10.85) | RST | 2 / RST |
| 8 / (−21.5,−13.39) | BL | 1 / BL |

Route and trial-fit before cutting. The CAD's insulated spans are about 35.5 mm from the PH housing back to the board dressing bend; leave a further 3.4 mm for the stripped solder end and trim each wire to its actual path. Preserve the factory PH termination. Strip/tin the board ends, insert from above, solder without loose strands, and trim tails to ≤0.8 mm below the board. Verify **every signal by continuity and the display's printed labels**, never by colour alone: factory colours may vary. Check VCC/GND and all eight channels before powering.

The supplied wire OD, conductor size, minimum bend radius, exact free-wire length and jumper-sleeve dimensions are **not published by Waveshare**. The model uses a stated Ø1 mm wire envelope and nominal PH plug; the 2 mm dressing bend is a layout allowance, not a manufacturer-qualified bend radius. Actual cable dressing, mechanical support and physical fit remain to be measured. Handle the PH housing when unplugging, support the soldered ends during assembly, and unplug at the display before lifting the screen. There is no long service loop.

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

The rear USB-C face is 0.15 mm beyond the side wall. Its 22 mm opening and the continuous 13.4×6.9 mm approach gauge include the specified [L-com drawing](https://www.l-com.cn/Images/Downloadables/2D/CAU4CC-40M-1M_2D.pdf)'s nominal 12.9×6.4 mm body plus general ±0.5 mm tolerance. The axis is Z=5.85 mm and the rotor clearance is 1.50 mm. The 35 mm gauge length is a checking volume, not a claimed cable dimension. Verify actual full insertion and strain relief.

There is **no internal battery, cell connector, thermistor, charging circuit or flexible battery wiring** in Rev E3.
