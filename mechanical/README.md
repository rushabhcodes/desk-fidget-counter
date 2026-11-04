# Rev E mechanical CAD

Nominal envelope **Ø86×22.3 mm**, rotating grip Ø84.8 mm starting Z=10.8 mm, fixed screen bezel Ø48 mm. Side USB-C is retained; a guided horizontal front plunger reaches the Omron side button opposite USB. All 39 board components assemble from above.

- `cad/assembled.glb` and `cad/exploded.glb`: named product parts plus actual source-PCB geometry and package models, glTF metres/+Y-up.
- `stl/`: nine printable product parts and a bearing-fit coupon, in print orientation.
- `parameters.json`, `generate.py`: nominal millimetre geometry and clearance checks.
- `vendor/`: original Waveshare STEP, KiCad package STEP/OBJ models and provenance. No axis scaling of bought parts.
- `harness.py` / `harness.json`: individual H1 wire curves, pin mapping, housing dimensions and minimum bend radius.
- `cad/*.obj`: PCB-centred millimetres/+Z-up for the tscircuit assembly viewer.

The PCB underside/top are Z=2.6/4.2 mm. Screen carrier underside/top are Z=17.3/18.3, front Z=20.9, bezel top Z=22.3. The 6712ZZ bearing occupies Z=12…19 mm. The official screen source spans 40.453106×37.5×9.2 mm, rigidly rotated 180° about Y so the tab faces -X; the rear connector reaches Z=11.7. The cable uses a 24.209 mm nominal free path and 6.2 mm minimum bend radius, with 0.6096 mm maximum wire diameter.

The former battery tray and toggle opening are removed. The lid captures the front plunger above its open-top base guide; its thin nose clears the PCB edge. An exact swept solid checks every nominal pose through the complete 0.40 mm stroke and confirms contact with the real actuator. The longer guide and 0.6 mm nose keep at least 0.17 mm above the PCB in the conservative nominal downward-play calculation; FDM dimensional error remains unqualified. Actual switch pretravel and printed fit must be measured and the nose/stop adjusted before use. A 34.6×40.6 mm routed PCB window accommodates the rear connector and cable below the screen. The bearing, port and retained clearances continue to set overall height. [Stack/research](LOW_PROFILE.md), [assembly sequence](../ASSEMBLY.md), [wiring and cable dimensions](../manufacturing/WIRING.md), [supplier geometry and limitations](vendor/README.md).

## Generate

After installing the pinned project dependencies and the Python geometry packages listed in `vendor/README.md`:

```sh
bun run build
python mechanical/generate.py
bun run cad:pcb
python mechanical/generate-assembly.py
bun run build
bun run check:assembly
python mechanical/render.py
```

The CAD renderer additionally needs pyrender 0.1.45, PyOpenGL 3.1.10, Pillow and Mesa EGL. Run `render.py` last for depth-tested previews. Model URLs resolve to the immutable GitHub tag for the package version; the PCB CAD exporter uses the identical checked-in bytes locally before publication.

The checks establish nominal mesh integrity, swept moving-part clearances and source-derived placement. Print a coupon and prototype first: FDM tolerance, actual bearing race widths/drag, cable crimp/retention, screw seating, optical opacity and feel have not been physically measured.
