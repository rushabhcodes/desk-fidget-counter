# SPDX-License-Identifier: MIT
TOOLCHAIN ?= arm-none-eabi-
TINYUSB ?= .deps/tinyusb
CC = $(TOOLCHAIN)gcc
OBJCOPY = $(TOOLCHAIN)objcopy
SIZE = $(TOOLCHAIN)size
CMSIS = $(TINYUSB)/lib/CMSIS_5/CMSIS/Core/Include
DEVICE = $(TINYUSB)/hw/mcu/st/cmsis_device_f0/Include
SOURCES = main.c counter.c lcd.c lcd_ui.c startup.c usb_descriptors.c syscalls.c \
 $(TINYUSB)/src/tusb.c $(TINYUSB)/src/common/tusb_fifo.c \
 $(TINYUSB)/src/device/usbd.c $(TINYUSB)/src/class/cdc/cdc_device.c \
 $(TINYUSB)/src/class/hid/hid_device.c \
 $(TINYUSB)/src/portable/st/stm32_fsdev/dcd_stm32_fsdev.c \
 $(TINYUSB)/src/portable/st/stm32_fsdev/fsdev_common.c
CFLAGS = -std=gnu11 -Os -g3 -mcpu=cortex-m0 -mthumb -ffunction-sections -fdata-sections \
 -Wall -Wextra -Wno-misleading-indentation -DSTM32F072xB -DCFG_TUSB_MCU=OPT_MCU_STM32F0 \
 -I. -I$(TINYUSB)/src -I$(CMSIS) -I$(DEVICE)
LDFLAGS = -Tstm32f072cb.ld -Wl,--gc-sections,-Map=build/desk-knob.map \
 -nostartfiles --specs=nosys.specs -Wl,--print-memory-usage
all: build/desk-knob.bin build/desk-knob.hex
build/desk-knob.elf: $(SOURCES) counter.h lcd.h tusb_config.h stm32f072cb.ld
	mkdir -p build
	$(CC) $(CFLAGS) $(SOURCES) $(LDFLAGS) -o $@
	$(SIZE) $@
build/desk-knob.bin: build/desk-knob.elf
	$(OBJCOPY) -O binary $< $@
build/desk-knob.hex: build/desk-knob.elf
	$(OBJCOPY) -O ihex $< $@
clean:
	rm -rf build
.PHONY: all clean
