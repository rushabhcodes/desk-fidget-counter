// SPDX-License-Identifier: MIT
#pragma once
#include <stdbool.h>
#include <stdint.h>

typedef enum { BUTTON_NONE, BUTTON_SHORT, BUTTON_LONG } ButtonEvent;
typedef struct {
  bool initialized, candidate, pressed, armed, long_done;
  uint32_t changed_at, pressed_at;
} ButtonState;

// A held button at boot/resume must be released before it can act.
ButtonEvent button_update(ButtonState *b, bool pressed, bool enabled, uint32_t now);
uint16_t button_hold_ms(const ButtonState *b, uint32_t now);
