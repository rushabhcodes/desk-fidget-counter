# E6 low-profile architecture

The body remains **Ø84.8×22.3 mm** before optional feet. Its hollow 60×75×7 mm bearing surrounds the stationary 1.28-inch screen assembly, so the screen, cable and bearing occupy overlapping height ranges. No purchased part is scaled to fit.

The **34.6×40.6 mm R2 PCB window** admits the LCD's rear connector, fixed cable and two braced screen-support walls. J4 remains at (0,+20.5) mm; the braced walls fit around it. The PCB remains two-layer and all fitted electronics are on top. There is no battery or toggle; USB-C stays on the rear and the original side-actuated switch is operated by a captive printed cap at the front.

## Fewer parts and screws

[Ploopy's assembly](https://ploopyco.github.io/knob/assembly-instructions/) uses two PCB screws and hand-presses the bearing/top assembly together. E6 follows that assembly approach without copying its CAD. Our fixed display requires additional support: two M2×6 chassis screws and two M2×10 screws shared by the carrier and bezel, **four screws total**.

The six product prints are `base`, `lid`, `knob`, `screen-carrier`, `screen-bezel` and `button-cap`. The optical track is integral to the grip. Separate bearing retainers, bearing clamp, skirt adhesive and underside driver windows have been removed. The bearing uses calibrated hand-push fits; the [fit coupons and physical retention checks](FIT.md) are required before the full print. Friction and printer accuracy are not established by nominal CAD contact.

## Height budget

| Feature | Assembly Z / mm |
|---|---:|
| Base floor | 0–2.0 |
| PCB underside / top | 2.6 / 4.2 |
| Original USB-C axis | 5.85 |
| Optical beam | 8.7 |
| Lid annular plate | 9.2–10.4 |
| Outer grip lower edge | 10.8 |
| 6712ZZ bearing | 12.0–19.0 |
| Screen carrier support | 17.3 |
| Rotating upper web | 20.7–22.1 |
| LCD front / fixed bezel top | 20.9 / 22.3 |

The side cable needs a stationary opening below the rotating grip. The checked plug-approach gauge is **13.4×6.9 mm**, centred on the original socket axis; actual mating/strain-relief details still need a physical insertion test. Moving the rotating sleeve to desk level would obstruct this side connection.

The [printing guide](README.md), [assembly sequence](../ASSEMBLY.md), [fit budget](fit-budget.json) and [first-build checks](../validation/BRINGUP.md) cover support removal, bearing fit, wire dressing, optical opacity and screw engagement. The lid needs supports beneath its annular plate; the supplied orientations keep the other product parts flat. Optional feet add 1 mm. Physical prototype validation remains pending.

E6 uses PLA, with two 23×4 mm braced end walls, 7 mm-wide feet and short locating pins at the real screen-boss positions. The included PH plug enters along the display PCB plane. These changes retain the height, six prints and four enclosure screws. See [screen-fit.json](screen-fit.json) for the source-derived hole pattern and estimated cable seating.
