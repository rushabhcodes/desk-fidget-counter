# Firmware 1.0.1 / PCB Rev A

Flash images: `build/desk-knob.bin` and `build/desk-knob.hex`; `build/desk-knob.elf` includes symbols. Target is **STM32F072CBT6**, 128 KiB Flash / 16 KiB RAM. Application starts at **0x08000000**. These images do not target RP2040, XIAO, or the earlier nRF52810 counter.

## Rebuild

Install GNU Arm Embedded GCC (tested with xPack GCC 15.2.1-1.1), GNU make, Python 3 and Git:

```sh
bash firmware/bootstrap.sh
```

Override `TOOLCHAIN=/absolute/path/arm-none-eabi-` if needed. The bootstrap checks TinyUSB 0.21.0 and both CMSIS commit hashes. No Arduino environment or ST HAL is required. Application code uses CMSIS register definitions, TinyUSB and C standard-library formatting. Licenses are in `../licenses`.

Host tests compile the exact `counter.c` used in the embedded binary:

```sh
bash scripts/test-firmware.sh
```

## Flash

J4 is an **unpopulated** 5-pad programming row, in pin order: 3V3 target reference, SWDIO (PA13), SWCLK (PA14), NRST, GND. Use a pogo adapter or temporarily fitted header with the enclosure removed. Power the target from USB; connect probe voltage reference, never a competing supply. Battery may be disconnected for initial bring-up.

With OpenOCD and an ST-Link:

```sh
openocd -f interface/stlink.cfg -f target/stm32f0x.cfg \
  -c "program firmware/build/desk-knob.elf verify reset exit"
```

STM32CubeProgrammer can also load the HEX file through SWD. To use the STM32 ROM USB DFU bootloader, bridge J5's BOOT0/3V3 pads, pull J4 NRST low briefly, release reset, then use CubeProgrammer USB DFU to load the application at 0x08000000. Remove the J5 bridge and reset afterward. ROM DFU is a recovery path; SWD is the primary documented programming interface.

## Behavior

- The external I2C bus uses PB6 SCL / PB7 SDA. AS5600 is 0x36; FRAM is 0x50. The AS5600 status and RAW_ANGLE are read together. Normal power and 2x slow filter are selected in volatile configuration; no OTP is written.
- Signed, modulo-4096 angle differences unwrap across zero. A complete ±4096 displacement increments the unsigned 64-bit count. Reversal cancels partial progress algebraically. Slow one-count movements remain observable; no cumulative deadband erases them.
- An invalid magnet flag, I2C error, sample gap over 20 ms, or jump over 1024 counts invalidates partial progress. Recovering starts with a new baseline. This favors avoiding phantom turns over guessing movement during faults. The physical speed envelope must be measured.
- PA0 reads the slide switch with 20 ms debounce. Scroll data is generated only while the switch is enabled, USB is present, the device is configured, and USB is awake. Disabling, detaching or suspending clears pending wheel motion; it never replays battery-session rotations on reconnection.
- PA1 held for three seconds writes a reset record before clearing RAM state. There is no short-press reset.
- Completed turns trigger an immediate FRAM commit. Two 32-byte records at addresses 0 and 64 contain sequence, count, CRC32 and a marker written last. The old slot remains valid until the replacement is committed. Each save is read back. If neither slot is valid at boot, explicit initialization is required rather than silently erasing an unknown history.
- A power failure during the brief commit can lose the last **unacknowledged** turn; it cannot convert a partial record into a large valid count. Validate this window physically. Unfinished fractional progress is intentionally not retained.
- USB100 is the reset state of EN1/EN2. TinyUSB configuration requests up to 500 mA before selecting USB500. Suspend selects both EN inputs high, isolating USB input current while the battery can continue counting. PGOOD controls attach/detach promptly.
- PB1 monitors the NTC through the 100k/100k divider. PB2 drives active-low charger CE. It starts high; only the defined temperature window permits charging. Open/short NTC disables it. Below 3.45 V on battery for three 100 ms measurements, motion acceptance stops and the fault LED flashes. Completed records remain available after recharge.

## Console protocol

ASCII commands, one at a time, newline terminated. Baud rate is a CDC line-coding convention, not a physical UART clock.

| Command | Response |
|---|---|
| `STATUS` or `COUNT` | JSON containing turns, progress, storage_ok, magnet_ok, scroll_on, battery_mv, low_battery, rejected and charger_mode |
| `RESET CONFIRM` | `OK RESET` after the new zero count has been saved and verified; otherwise `ERROR STORAGE` |
| `VERSION` | Board/firmware/TinyUSB version |
| `HELP` | Command list |

The HID report is the standard mouse descriptor with X/Y/buttons always zero and only the wheel field used. No keypresses are generated. Development VID/PID **CAFE:4011** follow TinyUSB's example namespace; obtain an authorized unique VID/PID before commercial distribution. Each board's USB serial is its STM32 unique ID.
