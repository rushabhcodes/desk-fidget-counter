# Rev D prototype bring-up

**All physical checks below are pending.** Record board/firmware tag, instruments, measurements and photographs. Software, CAD, routing and image checks do not replace a first assembled prototype.

## Power and USB

- [ ] Inspect bare board and soldering against Gerbers, pin-1 drawing and BOM. Confirm VBUS / V3V3 / PERIPH_3V3 / GND isolation. U4 is the SC70 load switch, not a charger.
- [ ] Use a current-limited USB test setup. Confirm always-on 3.3V, low PB2/peripheral rail before configuration, no heating, and stable output under load.
- [ ] Verify VBUS inrush, steady operation below the declared 100mA, load-switch ramp, display/IR current and both USB-C orientations with the specified cable.
- [ ] Confirm USB HID+CDC enumeration on macOS, Windows and Linux. Test cold boot, warm reset, rapid hotplug and laptop sleep/wake.
- [ ] Suspend USB, disconnect the SWD probe, and measure total VBUS current against the applicable USB suspend limit. Confirm LCD/IR power off, no high LCD inputs/back-powering, Stop-mode entry and EXTI18 wake. Scope HSI48/USB resume timing and repeated suspend/reset cycles; no compliance is claimed before measurement.
- [ ] Turn the ring during suspension: no counts/scrolling should be guessed or replayed after resume. Existing committed count must survive.

## Programming, persistence and screen

- [ ] Meter J4's VTref/SWDIO/SWCLK/NRST/GND/BOOT0 mapping before connecting the probe. Program/verify Rev D firmware over SWD. Exercise ROM recovery separately.
- [ ] Initialize FRAM with RESET CONFIRM. Test power removal during every journal write stage; recover a valid prior/committed record, never a corrupted guessed value. Document the brief possible rollback of an in-flight completed-turn write.
- [ ] Build H1 to the physical signal-to-signal map in manufacturing/WIRING.md. Verify all eight continuities, no adjacent shorts, correct VCC/GND, PHR latch/retention and crimp pull strength. Verify the actual screen connector revision/position against the supplier STEP.
- [ ] Confirm GC9A01 startup/orientation with tab -X, MADCTL 0xA8, RGB order, backlight, and readability. Test count up to 20 digits and RESET VIA USB fault state. A write-only SPI transport-success flag cannot detect an unplugged screen.
- [ ] Run the companion on intended OSes. Compare local clock/date, total CPU%, RAM%, battery%/AC to host tools. Test no-battery desktop, companion close/reopen, multiple devices, port already in use and laptop disconnect/reconnect.
- [ ] Stop updates: after five seconds, replace clock/metrics with HOST OFFLINE while scrolling/counting continue on awake USB. Check midnight/date rollover, timezone changes and host clock adjustments.

## Optical counting and controls

- [ ] Verify U2 collector is on PERIPH_3V3, common cathode to GND, separate emitter pulldowns and nominal IR current. Scope both Schmitt inputs and PB4/PB5.
- [ ] Confirm 48 periods/channel and exactly 192 combined edges per full revolution, approximately quadrature phase, and high/low voltage margins.
- [ ] Test 950nm opacity of the printed skirt, slots, axial/radial alignment, dust, sunlight and room lighting. Black visible colour alone is insufficient.
- [ ] Compare 10/100/1000 measured turns both directions. Exercise slow edges, reversals, stopping on transitions and maximum intended speed while display and FRAM run. Measure a reliable speed envelope.
- [ ] Confirm wheel direction and 32 units per turn. Toggle off/on while rotating: count continues, no queued wheel motion replays, both switch positions fit and debounce.
- [ ] Test the service reset's three-second hold and intentional CDC reset. Unknown/corrupt FRAM must require initialization.

## Mechanics and fabrication

- [ ] Print the bearing-fit coupon first; measure actual inner/outer race contact faces, printed shrinkage and running torque. Clamp each race independently without shield preload.
- [ ] Inspect every through-hole tail: trimmed to ≤0.8mm below the PCB, deburred, clear of base and insulating film. Check each solder well and all top-side package heights.
- [ ] Check original screen carrier, bosses, tab, front and connector against the cradle/bezel. Tightening must not bow the PCB or load active glass.
- [ ] Confirm H1's short free span and smooth ≥6.1mm bends at actual wire OD. It must clear posts, PCB, every optical-skirt angle and all package bodies. Unplug before lifting the screen for service; there is no long service loop.
- [ ] Check DIN965 screw seating and engagement, access windows, both toggle positions, the specified USB plug's insertion shoulder/strain relief, 0.6mm bezel/grip gap, and the full rotating swept volume.
- [ ] Confirm no loose wire can enter the moving skirt. Rotate many complete turns before final closure. Check bearing retention, skirt adhesive and feet over time.
- [ ] Have the fabricator review the two-layer board rules and closed internal routing contour. Reflow/feeder rotations and solder-mask clearances must match pin-1 drawings before an assembly order.
