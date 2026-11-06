# Rev C low-profile architecture

> Current mechanics E4 / PCB E3: USB-only, Ø84.8×22.3 mm, original side switch without plunger, included display lead soldered at J6 and 38 populated PCB parts. E4 adds accepted approximate bearing internals, independent self-seating race retainers, soft PCB capture pads and full swept tolerance checks. Use [ASSEMBLY.md](../ASSEMBLY.md) and [FIT.md](FIT.md). Rev C measurements below are historical context, including the removed battery and toggle.


Rev C is **Ø86 ×22.3 mm** before feet, compared with Ø80×47 mm for Rev B. The grip starts at **z10.8 mm**, previously z22 mm. Width increases by 6 mm to accommodate a 60×75×7 mm hollow bearing and useful printed bearing-retainer walls. The dimensions are nominal CAD results; no prototype has been measured.

## Research and design choice

- [Grayhill ring-encoder design guide](https://grayhill.com/wp-content/uploads/media/ring-encoder-knob-design-guide-1.pdf) uses a hollow optical ring with a fixed central function. This supports separating the stationary screen from the outer grip.
- [SmartKnob](https://github.com/scottbez1/smartknob) routes a fixed round display through a hollow motor shaft. Its motor, haptics, screen PCB and mechanics are different; no CAD or circuit files were copied.
- [Ploopy Knob hardware](https://ploopyco.github.io/knob/appendices/hardware/) uses a thin-section bearing. Its 6705ZZ is too small to surround our screen, connectors and protected cell.
- [JST's PH drawing](https://www.jst-mfg.com/product/pdf/eng/ePH.pdf) gives a 4.8 mm side-entry height. S2B/S8B battery/display headers replace the tall or bottom-mounted arrangement; the six-way programming header remains top-entry. All components are installed from the top.
- The [6712 bearing family](https://www.zotybearing.com/bearings/6700-Series-Ball-Bearings/Factory-direct-selling-thin-wall-ball-bearing-6712-6712RS-6712-2RSsize-60x75x7mm-bearing) provides the 60 mm bore needed to nest the screen assembly inside the bearing.

The custom board has four flat sides on a Ø72 mm circular envelope and a **34.6×40.6 mm rounded rectangular internal window**. The protected battery sits on the insulated base floor through that window; the LCD's rear PH connector descends through its right-hand part. This removes the old battery → PCB → bearing → cable → screen tower. Three independent screen posts rise through the same window, so the stationary screen support never crosses the rotating encoder skirt.

## Height budget

| Feature | Assembly Z / mm |
|---|---:|
| Base floor | 0–2.0 |
| Battery envelope | 2.2–8.0 |
| PCB | 2.6–4.2 |
| Side USB-C axis | 5.95 |
| Accepted USB plug overmould | max 8 mm high, top z9.95 |
| Optical beam | 8.7 |
| Moving grip's lower retainer | 10.8–12.0 |
| 6712ZZ bearing | 12.0–19.0 |
| Stationary inner-race clamp | 19.0–20.2 |
| Rotating top web | 20.7–22.1 |
| LCD carrier PCB | 17.3–18.3 |
| LCD front / fixed bezel top | 20.9 / 22.3 |

The side USB-C requirement limits the grip's lower edge. An 8 mm-high plug has **0.85 mm** nominal vertical clearance below the rotating retainer. A larger cable overmould may not fit. The left toggle remains in a fixed recess below the rotor. The lower edge cannot be taken to the desk without obstructing those side controls or changing the USB arrangement.

## Retention and service

The bearing's outer race is captured by the gold grip and a separate lower retainer. Its inner race is captured by the stationary post and a screwed clamp. The optical skirt attaches to the underside of the grip's central web using a thin transfer-adhesive annulus, rather than crossing the stationary bearing post with a moving radial plate. Allow 0.05–0.06 mm adhesive thickness; use a suitable transfer adhesive such as [3M 467MP](https://www.3m.com/3M/en_US/p/dc/v000185218/), prepare flat mating surfaces and verify adhesion to the actual printed material before use. This bond carries only the lightweight optical skirt; bearing retention uses screws.

Three Ø5.2 mm driver windows in the base and chassis align with the outer-race retainer screws when the rotor is parked. They allow the retainer to be fastened after the bearing clamp and grip are installed. Thin removable feet may cover these underside service windows.

The board is captured between base locating pegs and chassis pads at its four NPTHs; no tall PCB standoffs are required. All through-hole tails must be trimmed and deburred to **≤0.8 mm**. Individual solder wells preserve a nominal 1.2 mm insulating base floor below those tails. The PCB window keeps soldered metal away from the pouch; use a thin insulating barrier and inspect actual lead lengths.

The 22.3 mm envelope is the checked compact design with the selected protected battery, stock 1.28-inch module, side USB-C, toggle and printed race retention. It is not a claim that every alternative screen, connector, bearing or manufacturing process has the same minimum. Physical module fit, cable bends, bearing race widths, adhesive bond, optical opacity and printed tolerances still need prototype checks.
