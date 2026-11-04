# Purchased-part CAD provenance

The project uses actual catalogue parts and package dimensions. CAD describes **nominal geometry**, with the explicit detail limits below. Printed clearances need a physical fit check before ordering an assembled production run.

| Model | Source and dimensions | Detail |
|---|---|---|
| Waveshare 19192 | [Official 3D archive](https://files.waveshare.com/upload/4/49/1.28inch_LCD_Module_3D_Drawing.zip), `0508.stp`, 2021-05-08; [product](https://www.waveshare.com/product/1.28inch-lcd-module.htm) | Original STEP retained as `step/Waveshare-19192.stp`. Unscaled tessellation: 40.453106×37.5×9.2 mm. Supplier's simplified solid includes PCB, front, rear connector and four mounting bosses. Fine connector/contact details are absent from the supplier file. Colours are ours. |
| JST B6B-PH / S8B-PH | KiCad `Connector_JST.3dshapes`; [official JST PH drawing](https://www.jst-mfg.com/product/pdf/eng/ePH.pdf) | Pitch 2 mm; PH6 width 13.9 mm/top-entry height 6 mm; PH8 width 17.9 mm/side-entry height 4.85 mm in the STEP. Through-hole tails in the derivative OBJ are trimmed to 0.8 mm below a 1.6 mm PCB. Original untrimmed STEP retained. |
| ICs and passive packages | KiCad package STEP files in `step/`; per-file URLs in `models.json` | LQFP48, narrow SOIC8, SOT23-5/6, SC70-6, SOD323, 0603/0805. Lead geometry and package sizes come from those STEP files; material colours are ours. These are package-level models, not serial-number-specific manufacturer solids. |
| HRO USB-C and XUNPU tactile | Exact imported EasyEDA models from the original component packages in `imports/` | Retain supplier footprint/model orientation and offsets. Original public OBJ and STEP copies are included (C165948 / C720477); watertight STEP tessellations in `solid/` support collision checks because the display OBJ exports contain open material seams. Their coordinate bounds agree. |
| TCUT1600X01_A | [Vishay drawing p.6](https://www.vishay.com/docs/84174/tcut1600x01.pdf) | Datasheet-derived nominal 5.5×4×5.7 mm, 3 mm optical gap, 4.5 mm beam height. Fine moulding, optical lenses and lead-form details omitted. |
| NKK G12AH | [NKK Series G drawing](https://www.nkkswitches.com/pdf/Gtoggles.pdf) | Datasheet-derived nominal body, bushing, 3.8 mm lever and 2.54/5.08 mm pin grid. Lever shown tilted; moulding, internal contacts and detailed actuator joint omitted. Check both switch positions physically. |
| LCD harness | JST PH drawing above; [Alpha 2840/7 wire](https://www.alphawire.com/products/wire/hook-up-wire/premium/2840_7) | Two PHR-8 housings (17.8×4.5×6.85 mm), SPH-004T-P0.5S contacts (nominal 5.7 mm), individual wire paths at worst-case 0.6096 mm OD; minimum modelled bend radius 6.2 mm, above 10×OD. Spring/crimp microgeometry simplified. See `../harness.json` and `../../manufacturing/WIRING.md`. |
| Bearing | 6712ZZ catalogue 60×75×7 mm | Envelope retained; race internals/shields are simplified. Printed race fits require the coupon and an actual bearing. |
| Screws | DIN 965 / ISO 7046-1 M2, 3.8 mm head diameter, 1.2 mm head height | Nominal screw bodies, threads/drive detail omitted. The printed 4.2 mm countersinks leave clearance. |

The screen is rigidly transformed by `diag(-1,+1,-1)` then translated to Z=17.75 mm: its tab points -X, PCB underside is Z=17.3 mm, front is Z=20.9 mm and rear connector reaches Z=11.7 mm. No axis has been rescaled. This orientation allows a short cable to J6 and requires the matching Rev D bezel support pattern and MADCTL setting.

## Rebuilding

`generate-models.py` imports the listed KiCad STEP files from `/usr/share/kicad/3dmodels` and tessellates at 0.03 mm chordal deflection through `../step-mesh.py`; `custom-models.py` generates the two documented nominal models. Runtime: Python 3.12, `cadquery-ocp==8.0.1.1.0`, `trimesh==5.2.0`, `numpy`, `manifold3d==3.5.4`. The checked-in source STEP/OBJ files permit inspection without a KiCad installation. `models.json` records local paths, upstream URLs and measured bounds.

The supplier screen OBJ is an unchanged geometry tessellation of the original STEP; only vertex colours were added. Regenerate it with `step-mesh.py` and retain its source frame; the assembly generator applies the rigid transform.

## Rights

Original Waveshare CAD remains Waveshare material, supplied in its public module resources; it is not relicensed as project MIT code. The KiCad STEP headers retain their authors, CC-BY-SA-4.0 licence and ECAD design exception. Those notices also apply to derivative package meshes; the exception permits generated electronic designs without imposing the library's share-alike licence on this project. Other supplier/EasyEDA assets retain their existing rights. Our parametric geometry and scripts are MIT. See the original STEP headers and [KiCad licence](https://gitlab.com/kicad/libraries/kicad-packages3D/-/blob/master/LICENSE.md).
