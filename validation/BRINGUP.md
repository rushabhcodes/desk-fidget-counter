# Rev E3 prototype bring-up

**All physical checks below are pending.** Record board/firmware tag, instruments, measurements and photographs. Software, CAD, routing and image checks do not replace a first assembled prototype.

## Power and USB

- [ ] Inspect bare board and soldering against Gerbers, pin-1 drawing and BOM. Confirm VBUS / V3V3 / PERIPH_3V3 / GND isolation. U4 is the SC70 load switch, not a charger.
- [ ] Use a current-limited USB test setup. Confirm always-on 3.3V, low PB2/peripheral rail before configuration, no heating, and stable output under load.
- [ ] Verify VBUS inrush, steady operation below the declared 100mA, load-switch ramp, display/IR current and both USB-C orientations with the specified cable.
- [ ] Confirm USB HID+CDC enumeration on macOS, Windows and Linux. Test cold boot, warm reset, rapid hotplug and laptop sleep/wake.
- [ ] Suspend USB, disconnect the SWD probe, and measure total VBUS current against the applicable USB suspend limit. Confirm LCD/IR power off, no high LCD inputs/back-powering, Stop-mode entry and EXTI18 wake. Scope HSI48/USB resume timing and repeated suspend/reset cycles; no compliance is claimed before measurement.
- [ ] Turn the ring during suspension: no counts/scrolling should be guessed or replayed after resume. Existing committed count must survive.

## Programming, persistence and screen

- [ ] Meter J4's VTref/SWDIO/SWCLK/NRST/GND/BOOT0 mapping before connecting the probe. Program/verify firmware 5.0.0 over SWD. Exercise ROM recovery separately.
- [ ] Initialize FRAM with RESET CONFIRM. Test power removal during every journal write stage; recover a valid prior/committed record, never a corrupted guessed value. Document the brief possible rollback of an in-flight completed-turn write.
- [ ] Shorten the supplied H1 according to the physical signal-to-signal map in manufacturing/WIRING.md. Verify all eight continuities, no adjacent shorts, correct VCC/GND, retained factory PH latch and termination strength. Verify the actual screen connector revision/position against the supplier STEP.
- [ ] Confirm GC9A01 startup/orientation with tab -X, MADCTL 0xA8, RGB order, backlight, and readability. Test count up to 20 digits and HOLD 3S TO INIT and TIMER ERROR fault states. A write-only SPI transport-success flag cannot detect an unplugged screen.
- [ ] Run the companion on intended OSes. Compare local clock/date, total CPU%, RAM%, battery%/AC to host tools. Test no-battery desktop, companion close/reopen, multiple devices, port already in use and laptop disconnect/reconnect.
- [ ] Stop updates: after five seconds, replace clock/metrics with HOST OFFLINE while scrolling/counting continue on awake USB. Check midnight/date rollover, timezone changes and host clock adjustments.

## Optical counting and controls

- [ ] Verify U2 collector is on PERIPH_3V3, common cathode to GND, separate emitter pulldowns and nominal IR current. Scope both Schmitt inputs and PB4/PB5.
- [ ] Confirm 48 periods/channel and exactly 192 combined edges per full revolution, approximately quadrature phase, and high/low voltage margins.
- [ ] Test 950nm opacity of the printed skirt, slots, axial/radial alignment, dust, sunlight and room lighting. Black visible colour alone is insufficient.
- [ ] Compare 10/100/1000 measured turns both directions. Exercise slow edges, reversals, stopping on transitions and maximum intended speed while display and FRAM run. Measure a reliable speed envelope.
- [ ] Confirm wheel direction and 32 units per turn. Short-press while rotating: switch Scroll / Count-only, counting continues, and no queued wheel motion replays. Confirm Count-only at boot.
- [ ] Test the front button’s three-second hold and intentional CDC reset. Confirm hold progress and COUNT CLEARED, one clear per hold, no mode change on long release, and no action if held at boot/resume. Unknown/corrupt FRAM must require initialization.

## Mechanics and fabrication

- [ ] Print the bearing-fit coupon variants first; record actual inner/outer race contact faces, printed diameters/shrinkage, full-seat taper, axial capture and running torque in [FIT.md](../mechanical/FIT.md). Clamp each race independently without shield preload.
- [ ] Inspect every through-hole tail: trimmed to ≤0.8mm below the PCB, deburred, clear of base and insulating film. Check each solder well and all top-side package heights.
- [ ] Check original screen carrier, bosses, tab, front and connector against the cradle/bezel. Tightening must not bow the PCB or load active glass.
- [ ] Confirm H1's shortened stock cable and its actual dressed bends/OD, whose manufacturer limits are unpublished. It must clear posts, PCB, every optical-skirt angle and all package bodies. Unplug before lifting the screen for service; there is no long service loop.
- [ ] Check DIN965 screw seating and engagement, access windows, direct switch actuation, return, side-load protection and PCB-tab support, the now-exposed USB socket, specified plug's full insertion/withdrawal and shoulder/strain relief, 0.8mm bezel/grip gap, and the full rotating swept volume.
- [ ] Confirm no loose wire can enter the moving skirt. Rotate many complete turns before final closure. Check bearing retention, skirt adhesive and feet over time.
- [ ] Have the fabricator review the two-layer board rules and closed internal routing contour. Reflow/feeder rotations and solder-mask clearances must match pin-1 drawings before an assembly order.

- [ ] Measure original Omron actuator position and pretravel; check direct fingertip access through the front aperture. Verify return without shell interference, excessive travel or PCB flex. There is no printed plunger, guide or stop to tune. Check the base/lid support pads on the new tab.

- [ ] Verify the E3 USB tab seats in the wider rear aperture, its four shield solder joints remain supported, and both plug orientations fully latch without the plastic body touching PCB or shell. Compare the actual cable with the 13.4×6.9 mm tolerance-expanded body gauge. Check the Ø4.4 mm driver windows pass the actual M2 heads and driver.

- [ ] Confirm the exact Waveshare 19192 package includes the PH2.0 8PIN 20cm lead shown by the manufacturer. Trial-route before cutting; retain its PH display plug, shorten the board end and solder into J6. Leave the optional header DNP. Meter all eight signals by label, not colour. The E4 model uses the requested best approximation; check actual wire OD, stripped-core fit, plug revision, bending and termination strength during first-prototype assembly. Do not substitute a newly purchased custom harness.

- [ ] Fit all six PORON discs under the E4 lid, inspect compression and PCB restraint, and confirm that each race retainer seats on the bearing before reaching a printed hard stop. Check the 0.8 mm optical wall and opaque filament/coating. The accepted digital fit budget does not replace these first-build observations.
