# Native autorouting

v5.1.0 retains two copper layers and top-side component assembly. The whole-board native build, decoupling-length checks, Gerber-derived shorts check and independent KiCad fabrication DRC pass.

`index.circuit.tsx` uses tscircuit’s built-in Pipeline 9 autorouter (`auto_local`, `beta_pipeline9`, effort `2x`) for the whole two-layer board in a single native phase. VBAT is tied directly to the USB-derived 3.3 V rail with C7 as its local bypass. Every connection, including the USB data pair, power, ground and MCU decoupling branches, goes through that autorouter. There is no custom routing function, saved route import, prescribed PCB path, manual routing via or external routing engine.

The source contains component placement, logical connections and manufacturing constraints. A new build derives every routed trace and via from those inputs. The previous routing generator, coordinate repair script and route replay files have been removed.

The manufactured minimum copper clearance is 0.15 mm and the board-edge clearance is 0.30 mm. The single unindexed `autoroutingphase` requests 0.16 mm trace/pad and via/pad clearance to leave margin through the router’s width adjustment and repair stages. A two-layer keepout reserves 0.4 mm outside the display window’s bounding box. Two circular copper keepouts follow the actual USB connector’s locating holes. `allowPlacements` permits connector housings above these spaces; copper routing remains blocked.

Power and ground request a nominal 0.19 mm width; the native router may narrow sections to the board’s 0.10 mm minimum. Explicit MCU branches request 0.10–0.15 mm, and the 4 mm maximum decoupling length remains checked. Vias have 0.60 mm pads and 0.20 mm drills, with a 0.55 mm minimum drill-edge spacing. No copper DRC check is disabled.

Pinned toolchain: tscircuit 0.0.3077, core 0.0.2267 and capacity-autorouter 0.0.1038. The project allows 20 minutes per build worker. Native CLI caches and diagnostic files are ignored by Git and are not imported as source routing.

Inspect the native inputs, outputs and cumulative PCB with:

```sh
bunx tsci build index.circuit.tsx --autorouter-debug --autorouter-dump-srj all
```

Run connectivity, schematic placement, PCB placement, the complete build, Gerber-derived shorts and independent fabrication DRC checks before accepting a result. The fabrication finalizer checks that every native trace and via is unchanged after KiCad finalization.
