// SPDX-License-Identifier: MIT
#include "button.h"

ButtonEvent button_update(ButtonState *b, bool pressed, bool enabled, uint32_t now) {
  if (!enabled) {
    *b = (ButtonState){0};
    return BUTTON_NONE;
  }
  if (!b->initialized) {
    *b = (ButtonState){.initialized=true, .candidate=pressed, .pressed=pressed,
                       .armed=!pressed, .changed_at=now, .pressed_at=now};
    return BUTTON_NONE;
  }
  if (pressed != b->candidate) {
    b->candidate = pressed;
    b->changed_at = now;
  }
  if (b->pressed != b->candidate && (uint32_t)(now-b->changed_at) >= 25) {
    b->pressed = b->candidate;
    if (b->pressed) {
      b->pressed_at = now;
      b->long_done = false;
    } else if (!b->armed) {
      b->armed = true;
    } else if (!b->long_done) {
      return BUTTON_SHORT;
    }
  }
  if (b->armed && b->pressed && b->candidate && !b->long_done &&
      (uint32_t)(now-b->pressed_at) >= 3000) {
    b->long_done = true;
    return BUTTON_LONG;
  }
  return BUTTON_NONE;
}

uint16_t button_hold_ms(const ButtonState *b, uint32_t now) {
  if (!b->initialized || !b->armed || !b->pressed || b->long_done) return 0;
  uint32_t elapsed = now-b->pressed_at;
  return elapsed > 3000 ? 3000 : (uint16_t)elapsed;
}
