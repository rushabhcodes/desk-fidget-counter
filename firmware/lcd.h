// SPDX-License-Identifier: MIT
#pragma once
#include <stdbool.h>
#include <stdint.h>
typedef struct {
  uint64_t turns;
  uint16_t battery_mv;
  bool storage_ok, low_battery, scroll_on, usb_ready, charging;
} LcdView;
void lcd_render_row(const LcdView *view, unsigned y, uint16_t row[240]);
void lcd_init(void);
void lcd_task(uint32_t now, const LcdView *view);
bool lcd_ok(void);
