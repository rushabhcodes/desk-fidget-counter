#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
TASK_TEST_BINARY="$(mktemp /tmp/desk-knob-tests.XXXXXX)"
trap 'rm -f "$TASK_TEST_BINARY"' EXIT
cc -std=c11 -Wall -Wextra -Werror -Ifirmware tests/test_counter.c firmware/counter.c -o "$TASK_TEST_BINARY"
"$TASK_TEST_BINARY"
cc -std=c11 -Wall -Wextra -Werror -Ifirmware tests/test_lcd_ui.c firmware/lcd_ui.c firmware/counter.c firmware/dashboard.c -o "$TASK_TEST_BINARY"
"$TASK_TEST_BINARY"

cc -std=c11 -Wall -Wextra -Werror -Ifirmware tests/test_dashboard.c firmware/dashboard.c -o "$TASK_TEST_BINARY"
"$TASK_TEST_BINARY"
python3 -m unittest discover -s tests -p "test_companion.py"

cc -std=c11 -Wall -Wextra -Werror -Ifirmware tests/test_button.c firmware/button.c -o "$TASK_TEST_BINARY"
"$TASK_TEST_BINARY"
