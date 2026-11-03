#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
TASK_TEST_BINARY="$(mktemp /tmp/desk-knob-tests.XXXXXX)"
trap 'rm -f "$TASK_TEST_BINARY"' EXIT
cc -std=c11 -Wall -Wextra -Werror -Ifirmware tests/test_counter.c firmware/counter.c -o "$TASK_TEST_BINARY"
"$TASK_TEST_BINARY"
