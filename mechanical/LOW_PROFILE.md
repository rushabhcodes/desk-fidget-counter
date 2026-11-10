# E14 low-profile architecture

E14 adds a fixed collar beneath the display bezel as part of the existing carrier. It conceals the open mounting cavity with no additional parts, screws or enclosure height. The 0.8 mm bezel/rotor running seam remains. [Visual review and actual sections](VISUAL-REVIEW.md).

The body is **Ø89.4×19.5 mm** before optional feet. E13 increases diameter by 4.6 mm to contain its R44.5 mm curved button, recessed 0.2 mm within the circular outline; the PCB outline and switch position are preserved by RP2040 revision F1. Its hollow 60×75×7 mm bearing surrounds the stationary 1.28-inch screen assembly, so the screen, cable and bearing occupy overlapping height ranges. No purchased part is scaled to fit.

The **34.6×40.6 mm R2 PCB window** admits the LCD's rear connector, fixed cable and two braced screen-support walls. J4 remains at (0,+20.5) mm; the braced walls fit around it. The PCB remains two-layer and all fitted electronics are on top. There is no battery or toggle; USB-C stays on the rear and the original side-actuated switch is operated by a captive printed cap at the front.

## Fewer parts and screws

[Ploopy's assembly](https://ploopyco.github.io/knob/assembly-instructions/) uses two PCB screws and hand-presses the bearing/top assembly together. E9 follows that assembly approach without copying its CAD. Our fixed display requires additional support: two M2×6 chassis screws and two M2×10 screws shared by the carrier and bezel, **four screws total**.

The six product prints are `base`, `lid`, `knob`, `screen-carrier`, `screen-bezel` and `button-cap`. The optical track is integral to the grip. Separate bearing retainers, bearing clamp, skirt adhesive and underside driver windows have been removed. The bearing uses calibrated hand-push fits; the [fit coupons and physical retention checks](FIT.md) are required before the full print. Friction and printer accuracy are not established by nominal CAD contact.

## Height budget

| Feature | Assembly Z / mm |
|---|---:|
| Base floor | 0–2.0 |
| PCB underside / top | 2.6 / 4.2 |
| USB-C axis (XUNPU C2909598) | 5.78 |
| Optical beam | 8.7 |
| Lid annular plate | 7.2–8.4 |
| Outer grip lower edge | 10.0 |
| 6712ZZ bearing | 9.2–16.2 |
| Screen rear-boss seats | 12.0 |
| Screen carrier support | 13.1 |
| Rotating upper web | 17.9–19.3 |
| LCD front / fixed bezel top | 18.1 / 19.5 |

The side cable needs a stationary opening below the rotating grip. The checked plug-approach gauge is **13.4×6.9 mm**, centred on the original socket axis; actual mating/strain-relief details still need a physical insertion test. Moving the rotating sleeve to desk level would obstruct this side connection.

The [printing guide](README.md), [assembly sequence](../ASSEMBLY.md), [fit budget](fit-budget.json) and [first-build checks](../validation/BRINGUP.md) cover support removal, bearing fit, wire dressing, optical opacity and screw engagement. The lid needs supports beneath its annular plate; the supplied orientations keep the other product parts flat. Optional feet add 1 mm. Physical prototype validation remains pending.

E9 uses PLA, with two 23×4 mm braced end walls, 7 mm-wide feet and short locating pins at the real screen-boss positions. The H1 PH plug enters along the display PCB plane. These changes retain six prints and four enclosure screws. See [screen-fit.json](screen-fit.json) for the source-derived hole pattern and estimated cable seating.

The side-entry cable permits a **19.5 mm** assembled height, **2.8 mm (12.6%) shorter** than E6. The lid plate is recessed to Z7.2–8.4 mm, with a stiffening rim up to Z9.2 mm and 4 mm driver access wells. The bearing is at Z9.2–16.2 mm; the grip starts at Z10.0 mm. The USB plug envelope reaches Z9.23 mm, leaving 0.77 mm nominal vertical clearance and 0.31 mm under the stated hardware tolerance budget. Sensor beam height and optical slot positions are unchanged. Purchased parts remain unscaled.

E9 additionally opens the carrier screw bores and clears the actual screen PCB outline for a 2 mm rear-component allowance. The [visual audit](AUDIT.md) records the corrections and inspection views.

E13 retains the compact keyed JST-SH8 socket on the left PCB annulus, facing into the window. A single SH8-to-PH8 crimped harness replaces the supplied jumper cable without raising the screen or enclosure. See the [physical wiring map](../manufacturing/WIRING.md).
