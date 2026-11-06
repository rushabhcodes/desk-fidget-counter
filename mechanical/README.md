# Mechanics E4 / PCB E3

The case body remains **Ø84.8×22.3 mm**, with the fixed 1.28-inch display and side USB. The original B3U-3000P switch moves to a supported front PCB tab and is pressed directly through the case aperture. There is no printed plunger, guide or keeper. Its nominal 1.7×1.0 mm actuator projects 0.65 mm beyond the wall; at maximum specified pretravel it still projects 0.25 mm. The body plus actuator has a front-to-back envelope of about 85.25 mm.

The custom PH-to-PH harness is removed. Use the display's included PH2.0-to-jumper lead, shorten it, and solder its PCB ends at J6. The original display plug stays removable. The optional 2.54 mm header is DNP and absent from the compact assembly. See [wiring](../manufacturing/WIRING.md) for actual pad coordinates, signal mapping and cutting/continuity checks.

Eight product prints and three bearing-fit coupon variants are in `stl/`. See [fit measurements and tolerance sensitivity](FIT.md) before printing the product. `cad/assembled.glb` and `cad/exploded.glb` contain the actual source PCB, 38 populated package models, fixed screen and eight wires. OBJ assets use PCB-centred mm/+Z-up; glTF uses metres/+Y-up. Purchased parts are not rescaled. The bearing has separate races, shields, balls and cage: verified boundary size, user-authorized approximate internals. [Detailed bearing render](bearing-detail.png). Six compliant PCB pads and adhesive layers are also modelled.

The window is 34.6×40.6 mm with R2 corners. PCB underside/top remain Z=2.6/4.2 mm; screen carrier underside/top are Z=17.3/18.3, front Z=20.9, bezel top Z=22.3. The 60×75×7 mm bearing remains at Z=12…19. The official Waveshare STEP is rigidly transformed, unscaled. The rear socket remains flush at Y42.35003, axis Z5.85. Its continuous 13.4×6.9 mm plug approach gauge includes the source drawing's nominal dimensions and general tolerance.

`parameters.json`, `generate.py`, `harness.py` and `generate-assembly.py` define the geometry and checks. The button check uses a 12 mm fingertip sphere at the maximum depressed actuator position and permits contact only with the original switch actuator. A 0.25 mm PCB-nose relief clears the FR-4 while retaining the shell wall; the base supports the tab and two lid pads restrain it from above. All package, wire, screen and swept-rotor checks remain enabled.

**Accepted cable approximation:** the original supplied lead is drawn with Ø1.2 mm wires and checked at Ø1.5 mm. Static dressing uses a 3 mm XZ bend and a smooth fan; actual 3D minimum radii and per-wire lengths are in `harness.json`. These values are estimates, not supplier limits. Approximately 37 mm insulated spans plus 2.55 mm stripped PCB ends fit the checked layout; trial-route before trimming. No email or supplier response is required for this approximation-based release.

## Generate

With the pinned Bun dependencies and Python geometry packages from [vendor provenance](vendor/README.md):

```sh
bun run build
python mechanical/generate.py
bun run cad:pcb
python mechanical/generate-assembly.py
bun run build
bun run check:assembly
python mechanical/render.py
```

The renderer uses pyrender 0.1.45, PyOpenGL 3.1.10, Pillow and Mesa EGL. Model URLs are relative to the repository and resolve to the included OBJ files. The local exporter uses those same checked-in bytes; a new remote release tag is not required to view or rebuild them. The complete rotation check uses tolerance-expanded circular envelopes and verifies four independent race contacts. Calibrate bearing fits to ±0.10 mm diameter and relative mating heights to ±0.10 mm; hardware bring-up remains a first-prototype step.

The comparison renders use actual immutable predecessor assemblies at identical camera scale: [v5.1.0](https://github.com/rushabhcodes/desk-fidget-counter/releases/download/v5.1.0/assembled.glb) for the old plunger and [v5.0.0](https://github.com/rushabhcodes/desk-fidget-counter/releases/download/v5.0.0/assembled.glb) for the old USB recess. `render.py --button-before … --usb-before …` accepts these downloaded GLBs.

E4 keeps the nominal 84.8×22.3 mm body and the original E3 PCB. Use the full E4 print set: shortened bearing post/housing hard stops, 0.8 mm bezel gap, 0.8 mm optical wall, 0.4 mm glass relief and six soft capture pads. The part source scripts, `fit-budget.json`, `bearing-model.json` and `geometry-check.json` define and document the estimates.
