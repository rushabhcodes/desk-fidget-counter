# Rev E3 mechanical CAD

The case body remains **Ø84.8×22.3 mm**, with the fixed 1.28-inch display and side USB. The original B3U-3000P switch moves to a supported front PCB tab and is pressed directly through the case aperture. There is no printed plunger, guide or keeper. Its nominal 1.7×1.0 mm actuator projects 0.65 mm beyond the wall; at maximum specified pretravel it still projects 0.25 mm. The body plus actuator has a front-to-back envelope of about 85.25 mm.

The custom PH-to-PH harness is removed. Use the display's included PH2.0-to-jumper lead, shorten it, and solder its PCB ends at J6. The original display plug stays removable. The optional 2.54 mm header is DNP and absent from the compact assembly. See [wiring](../manufacturing/WIRING.md) for actual pad coordinates, signal mapping and cutting/continuity checks.

Eight product prints and the fit coupon are in `stl/`. `cad/assembled.glb` and `cad/exploded.glb` contain the actual source PCB, 38 populated package models, fixed screen and eight wires. OBJ assets use PCB-centred mm/+Z-up; glTF uses metres/+Y-up. Purchased parts are not rescaled.

The window is 34.6×40.6 mm with R2 corners. PCB underside/top remain Z=2.6/4.2 mm; screen carrier underside/top are Z=17.3/18.3, front Z=20.9, bezel top Z=22.3. The 60×75×7 mm bearing remains at Z=12…19. The official Waveshare STEP is rigidly transformed, unscaled. The rear socket remains flush at Y42.35003, axis Z5.85. Its continuous 13.4×6.9 mm plug approach gauge includes the source drawing's nominal dimensions and general tolerance.

`parameters.json`, `generate.py`, `harness.py` and `generate-assembly.py` define the geometry and checks. The button check uses a 12 mm fingertip sphere at the maximum depressed actuator position and permits contact only with the original switch actuator. A 0.25 mm PCB-nose relief clears the FR-4 while retaining the shell wall; the base supports the tab and two lid pads restrain it from above. All package, wire, screen and swept-rotor checks remain enabled.

**Cable limits:** Waveshare publishes its included cable type and 20 cm package length, but no wire OD, free-wire length, bend radius or sleeve dimensions. The drawings use explicit nominal PH and Ø1 mm wire fit envelopes. The 2 mm dressing bend is provisional, not manufacturer-qualified. Actual supplied cable dimensions, dressed bends, termination strength and fit must be measured before fabrication/assembly signoff; CAD does not establish these facts.

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

The renderer uses pyrender 0.1.45, PyOpenGL 3.1.10, Pillow and Mesa EGL. Versioned model URLs resolve to the immutable release tag. The local exporter uses those same checked-in bytes before publication. Prototype the bearing fit, direct-button access, stock cable dressing, printed tolerances, 950 nm opacity and optical response before production.

The comparison renders use actual immutable predecessor assemblies at identical camera scale: [v5.1.0](https://github.com/rushabhcodes/desk-fidget-counter/releases/download/v5.1.0/assembled.glb) for the old plunger and [v5.0.0](https://github.com/rushabhcodes/desk-fidget-counter/releases/download/v5.0.0/assembled.glb) for the old USB recess. `render.py --button-before … --usb-before …` accepts these downloaded GLBs.
