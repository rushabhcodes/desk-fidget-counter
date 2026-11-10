#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p .deps downloads
if [[ ! -d .deps/pico-sdk/.git ]]; then
  git clone --depth 1 --branch 2.2.0 https://github.com/raspberrypi/pico-sdk.git .deps/pico-sdk
fi
test "$(git -C .deps/pico-sdk rev-parse HEAD)" = a1438dff1d38bd9c65dbd693f0e5db4b9ae91779
if [[ ! -d .deps/tinyusb/.git ]]; then
  git clone --depth 1 --branch 0.21.0 https://github.com/hathach/tinyusb.git .deps/tinyusb
fi
test "$(git -C .deps/tinyusb rev-parse HEAD)" = dae3f9a366bfcddbf9dcf1b48d7500286a849539
if [[ ! -x .deps/toolchain/bin/arm-none-eabi-gcc ]]; then
  # Pinned Linux x86_64 compiler. Other hosts can set make PICO_TOOLCHAIN_PATH.
  test "$(uname -s)" = Linux && test "$(uname -m)" = x86_64
  archive=downloads/arm-gnu-toolchain-14.3.rel1-x86_64-arm-none-eabi.tar.xz
  curl --fail --location --retry 3 -o "$archive" https://developer.arm.com/-/media/Files/downloads/gnu/14.3.rel1/binrel/arm-gnu-toolchain-14.3.rel1-x86_64-arm-none-eabi.tar.xz
  printf '%s  %s\n' 8f6903f8ceb084d9227b9ef991490413014d991874a1e34074443c2a72b14dbd "$archive" | sha256sum --check -
  mkdir -p .deps/toolchain
  tar -xJf "$archive" --strip-components=1 -C .deps/toolchain
fi
python3 ../scripts/generate-board-pins.py --check
make "$@"
