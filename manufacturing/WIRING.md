# PCB E6 / Mechanics E11 physical wiring

All fitted board components mount from the top. Coordinates use +X right, +Y toward USB; PCB top is Z4.2 mm above the enclosure floor. Pin numbers refer to the physical board pads. Match pin 1 and the screen's printed signal labels, then check continuity before power.

## Keyed display harness H1

J6 is **JST SM08B-SRSS-TB(LF)(SN), JLCPCB C160407**, an 8-pin, 1 mm-pitch, side-entry SMT socket. It faces +X into the PCB window from (-21.3,-2) mm at 90°. Its two metal hold-down pads (9 and 10) are grounded. The exact JLC import retains all ten SMT lands; there are no J6 through-holes. [JST SH drawing](https://www.jst-mfg.com/product/pdf/eng/eSH.pdf) · [JLCPCB part](https://jlcpcb.com/partdetail/JST-SM08B_SRSS_TB_LF_SN/C160407).

The same connector is used for `J_SPI_DISPLAY` in [TSCircuit rv1106g2](https://github.com/tscircuit/rv1106g2/blob/86799ce9bc2b1b3b7edbfe334420a9dbedc33e9b/README.md). That project's pinout is different; use **this board's mapping below**. A bare-panel FPC connector is unsuitable for the Waveshare module's PH2.0 port.

Order **one finished, crimped H1 harness** to the schedule below. It is a made-to-drawing lead, not an identified stocked cable SKU. The original Waveshare kit cable ends in eight independent jumper sockets and is unused. Both H1 ends are keyed; SH uses friction retention, without a separate latch lever. Disconnect before lifting the screen.

| Harness part | Qty | Specification |
|---|---|---|
| Board-end housing | 1 | JST **SHR-08V-S-B**, 1 mm pitch, eight circuits, grip protrusions; overall 11×5×2.8 mm |
| Board contacts | 8 | JST **SSH-003T-P0.2-H**, qualified crimp for 32–28 AWG, insulation Ø0.4–0.8 mm |
| Display-end housing | 1 | JST **PHR-8**, 2 mm pitch; nominal 17.8×6.85×4.5 mm; check actual Waveshare socket fit |
| Display contacts | 8 | JST **SPH-004T-P0.5S**, qualified crimp for 32–28 AWG, insulation Ø0.5–0.9 mm |
| Wire | 8 lengths | **TE/Raychem 55A0111-30-9**, 30 AWG stranded ETFE, nominal Ø0.61 mm; number both ends. Colour in CAD is illustrative. |

**Free insulation length: 44±1 mm per conductor, measured along the wire between the rear housing exit faces. This is not raw cut length.** The cable maker must add the qualified terminal engagement, crimp and strip allowances. Request continuity/isolation testing and proper contact retention. No inline solder joints or heat-shrink sleeves are needed. [TE wire specification](https://www.te.com/en/product-216337-000.html) · [JST PH drawing](https://www.jst-mfg.com/product/pdf/eng/ePH.pdf) · [CSV termination schedule](LCD-harness.csv).

| J6 circuit / nominal pad XY mm | Signal | PHR-8 display circuit |
|---|---|---|
| 1 / (-23.35001, -5.50000) | BL | 1 / BL |
| 2 / (-23.35001, -4.50000) | RST | 2 / RST |
| 3 / (-23.35001, -3.50000) | DC | 3 / DC |
| 4 / (-23.35001, -2.50000) | CS | 4 / CS |
| 5 / (-23.35001, -1.50000) | CLK | 5 / CLK |
| 6 / (-23.35001, -0.50000) | DIN | 6 / DIN |
| 7 / (-23.35001, 0.50000) | GND | 7 / GND |
| 8 / (-23.35001, 1.50000) | VCC | 8 / VCC |

Match connector **circuit numbers and the display's printed signals**, not apparent left/right when looking into opposite connector faces. Pin8 is switched **3.3 V**, never USB 5 V. Check all eight connections and power-to-ground isolation before powering the display. BL is backlight control; there is no SPI MISO return from this display.

The CAD uses the original unscaled JLC header STEP and dimensioned nominal cable housings. Plug engagement datums, stepped noses and internal contact shapes are engineering approximations; they are not manufacturer mating CAD. Wires are rendered at Ø0.61 mm and clearance-checked at Ø0.8 mm with 43/44/45 mm free lengths. The display U bend has a nominal 3.3 mm centreline radius. That installed bend has not been qualified by the wire manufacturer: trial-dress the actual crimped cable, check plug engagement, no pinching and no strain before final closure. There is no long service loop.

## Removable programming harness H2

J4 is JST B6B-PH-K-S(LF)(SN), top entry. Mate with PHR-6 and SPH-004T-P0.5S contacts on wire qualified by the JST PH drawing (32–28 AWG, 0.5–0.9 mm insulation OD for this contact). A service harness of about 150 mm is external and removed after programming. It is not routed beneath the assembled screen.

| J4 pin / physical XY mm | Signal | Genuine ST-LINK/V2 20-pin SWD connector |
|---|---|---|
| 1 / (-5,20.8) | Target 3.3V reference | Pin 1 VAPP / VTref, probe input |
| 2 / (-3,20.8) | SWDIO | Pin 7 SWDIO |
| 3 / (-1,20.8) | SWCLK | Pin 9 SWCLK |
| 4 / (1,20.8) | NRST | Pin 15 NRST |
| 5 / (3,20.8) | GND | Pin 4 GND |
| 6 / (5,20.8) | BOOT0 | Leave empty for SWD; optional service jumper to pin 1 for ROM boot |

Power the target through USB-C while programming. VTref senses target voltage; do not connect a probe's power-output pin to it. Pin numbering on 10-pin SWD probes and low-cost ST-Link clones differs: use the probe manufacturer's documented SWDIO/SWCLK/NRST/GND/VTref signals, not this 20-pin number column. Main firmware is written by SWD; BOOT0 normally stays low through R10.

## USB cable and mechanical fit

The XUNPU C2909598 USB-C face is at Y42.1865 mm, 0.0135 mm inside the stationary side-wall radius and 0.2135 mm inside the outer floor edge; it remains accessible through the rear opening. Its 22 mm opening and the continuous 13.4×6.9 mm approach gauge include the specified [L-com drawing](https://www.l-com.cn/Images/Downloadables/2D/CAU4CC-40M-1M_2D.pdf)'s nominal 12.9×6.4 mm body plus general ±0.5 mm tolerance. The axis is Z=5.78 mm and the nominal rotor clearance is 0.77 mm (0.31 mm with the estimated axial allowance). The 35 mm gauge length is a checking volume, not a claimed cable dimension. Verify actual full insertion and strain relief.

There is **no internal battery, cell connector, thermistor, charging circuit or flexible battery wiring** in Rev E6.
