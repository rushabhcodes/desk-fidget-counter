// SPDX-License-Identifier: MIT
#pragma once
#include <stdbool.h>
#include <stdint.h>
#include "dashboard.h"
typedef struct {
  uint64_t turns;
  Dashboard host;
  uint32_t now;
  bool storage_ok, scroll_on, usb_ready;
} LcdView;
void lcd_render_row(const LcdView *view, unsigned y, uint16_t row[240]);
void lcd_init(void);
void lcd_power(bool enabled, uint32_t now);
void lcd_task(uint32_t now, const LcdView *view);
bool lcd_ok(void);
