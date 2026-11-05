# Firmware 5.0.0 / PCB Rev E / E2 / E3

The included `build/desk-knob.bin` and `.hex` target STM32F072CBT6 at **0x08000000**. This firmware controls the USB-only Rev E, E2 and E3 optical boards, switched LCD/IR rail and Waveshare 19192. Rev D toggle boards require firmware 4.0.0; earlier charging boards also need their matching tagged firmware; PA2–PA5/PA7/PB0/PB1 no longer serve battery functions.

## Build and program

```sh
bash scripts/test-firmware.sh
bash firmware/bootstrap.sh
python3 validation/check-firmware-image.py
```

The bootstrap pins TinyUSB 0.21.0 and CMSIS commits. Install ARM GCC/newlib and Make; alternatively use `make -C firmware TOOLCHAIN=/path/to/arm-none-eabi- TINYUSB=/path/to/tinyusb`.

J4 is the top-entry JST PH6 programming connector. Pins 1–6 are **VTref 3.3V, SWDIO, SWCLK, NRST, GND, BOOT0**. Power the target from USB; VTref is probe sense, not a supply input. Leave BOOT0 unconnected for ordinary SWD. [Exact connector views and ST-LINK/V2 mapping](../manufacturing/WIRING.md).

```sh
openocd -f interface/stlink.cfg -f target/stm32f0x.cfg \
  -c 'program firmware/build/desk-knob.hex verify reset exit'
```

STM32CubeProgrammer also programs the HEX over SWD. For the MCU's ROM recovery, bridge J4 BOOT0 to VTref, pulse NRST, use the supported ROM USB DFU interface, then remove the bridge/reset. Verify this recovery mode on the first board. J4 is a service connector beneath the removable fixed screen; remove the programming harness before final assembly.

## Behaviour

PB4/PB5 AF1 feed TIM3 encoder mode 3 with approximately 3.3µs filters. Hardware collects quadrature edges during display/FRAM transfers. The 48-slot ring gives **192 edges/revolution** and six edges per HID wheel unit (**32 units/turn**). Completed displacement ±192 increments the unsigned 64-bit total; reversal cancels unfinished progress. Sampling targets 2ms. An invalid journal, sample gap above 20ms or jump above 48 edges discards uncertain progress. Measure the actual usable speed envelope.

The side-actuated PA0 front button uses the MCU's internal pull-up and 25ms debounce. Boot starts in Count-only mode. A short press changes Scroll / Count-only on release, clearing queued wheel motion while counting continues. A three-second hold clears/initializes FRAM once and does not change mode on release; the display shows progress and confirmation. A button held at boot or resume must be released before any action. PA1 and PA6 are unused analog inputs; there is no separate reset button or LED. Detach/suspend clears motion queues; the powered-down optical sensor cannot measure turns while suspended. A new baseline is taken on resume.

FRAM uses I2C1 PB6/PB7 at approximately 300kHz, address 0x50. Completed turns update alternating 32-byte records at 0/64: sequence, 64-bit count, CRC32 and a commit marker written last, followed by read-back. Unknown FRAM requires `RESET CONFIRM` or a deliberate three-second button hold. Previously committed records remain compatible. An unplug during a write may restore the previous committed turn count; no battery or reserve supply completes in-flight transactions.

The display uses SPI2 mode 0, 12MHz, PB13 SCK/PB15 MOSI, PB10 reset, PB11 backlight, PA8 CS and PB14 DC. One 480-byte RGB565 row is sent per task; there is no full framebuffer. Each refresh uses a coherent snapshot. The **module tab faces -X**, with **MADCTL 0xA8** for this mounting. Verify orientation and colours physically. A bounded transport fault blanks the screen while counting/USB continue. No MISO is present: a transport-success flag cannot prove the screen is connected or displaying correctly.

Laptop clock/date, CPU/RAM percentages and laptop battery/AC come from the local [companion](../companion/README.md). Samples expire after five seconds, then placeholders and `HOST OFFLINE` appear. Desktop/no-sensor machines show `NO HOST BATTERY`. The clock/calendar advances between samples and handles midnight/leap-year rollover. Turn count and scroll state remain visible. Invalid storage shows `HOLD 3S TO INIT`; holding displays progress, and successful clear shows `COUNT CLEARED`. A timer fault shows `TIMER ERROR`.

## USB power

The USB descriptor is **bus-powered, 100mA**, HID mouse wheel + CDC. PB2 enables U4 TPS22919 only when USB is configured and awake. Before cutting the peripheral supply, firmware drives all LCD signals low to prevent back-powering. Resume ramps the rail, resets the scanline/init state and initializes the display again. LCD and IR are off before configuration and during suspend; the FRAM and MCU retain the always-on 3.3V rail.

USB suspend current, VBUS inrush and wake timing require physical measurement. After switching peripherals off, firmware enters STM32 Stop mode with SysTick disabled and USB EXTI18 wake-up enabled. HSI48 and SysTick are restored before unmasking interrupts after wake (ST RM0091 Stop-mode and USB suspend sections). Measure current with the SWD probe disconnected; no measured USB compliance is claimed. No remote wake-up is advertised. A USB charger without a data host will not configure the device and will not enable its display/encoder.

## CDC console

Newline-terminated ASCII, maximum 63 bytes per command, DTR asserted. `scripts/count.py` verifies application identity before reset or status operations. Close the dashboard companion before opening another program on the same serial port.

| Command | Result |
|---|---|
| `STATUS` / `COUNT` | JSON with device/protocol/firmware identity, turns, progress, storage_ok, encoder_timer_running, scroll_on, rejected, lcd_transport_ok, host_data_fresh |
| `RESET CONFIRM` | Commit zero or report storage failure |
| `VERSION` | Rev E / firmware 5.0.0 / TinyUSB 0.21.0 |
| `DASH …` | Validated clock/date/metrics; full field contract in companion guide |
| `HELP` | Command list |

The count formatter handles UINT64_MAX without libc 64-bit formatting. Native tests cover counter wraps/reversals/faults, torn FRAM records, malformed metric packets, stale data, calendar rollover and scanline buffer bounds. ARM image checks inspect actual descriptors and vectors. Those checks do not establish physical optical response or host interoperability.

USB **CAFE:4011** is TinyUSB's development VID/PID, shared by other projects. Use authorized identifiers before commercial distribution. Native HID scrolling needs no companion; CDC dashboard telemetry needs the companion running.

Hardware release v5.2.0 exposes the original side switch and changes the display cable termination without changing any signal or MCU pin. The included firmware remains 5.0.0; the same verified BIN/HEX supports Rev E, E2 and E3.
