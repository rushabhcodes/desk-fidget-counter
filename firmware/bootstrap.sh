#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p .deps
if [[ ! -d .deps/tinyusb/.git ]]; then
  git clone --depth 1 --branch 0.21.0 https://github.com/hathach/tinyusb.git .deps/tinyusb
fi
test "$(git -C .deps/tinyusb rev-parse HEAD)" = dae3f9a366bfcddbf9dcf1b48d7500286a849539
python3 .deps/tinyusb/tools/get_deps.py stm32f0
# get_deps.py uses TinyUSB's pinned dependency revisions; verify the two used here.
test "$(git -C .deps/tinyusb/lib/CMSIS_5 rev-parse HEAD)" = 2b7495b8535bdcb306dac29b9ded4cfb679d7e5c
test "$(git -C .deps/tinyusb/hw/mcu/st/cmsis_device_f0 rev-parse HEAD)" = cbb5da5d48b4b5f2efacdc2f033be30f9d29889f
make "$@"
