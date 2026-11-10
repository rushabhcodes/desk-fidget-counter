# SPDX-License-Identifier: MIT
CMAKE ?= cmake
PICO_TOOLCHAIN_PATH ?= $(CURDIR)/.deps/toolchain/bin
all:
	$(CMAKE) -S . -B build/cmake -G Ninja -DCMAKE_BUILD_TYPE=MinSizeRel -DPICO_TOOLCHAIN_PATH="$(PICO_TOOLCHAIN_PATH)"
	$(CMAKE) --build build/cmake
	cp build/cmake/desk-knob.elf build/cmake/desk-knob.bin build/cmake/desk-knob.hex build/cmake/desk-knob.uf2 build/
	python3 -c 'from pathlib import Path; p=Path("build/desk-knob.hex"); p.write_bytes(p.read_bytes().replace(b"\r\n", b"\n"))'
clean:
	rm -rf build/cmake
.PHONY: all clean
