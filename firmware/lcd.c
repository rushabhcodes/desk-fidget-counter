// SPDX-License-Identifier: MIT
#include "lcd.h"
#include "board.h"
// Mode 0, SPI0 12MHz; one 480-byte scanline per task call. No full framebuffer.
static uint8_t phase, init_index;
static unsigned scanline;
static uint32_t deadline;
static bool healthy = true;
static LcdView frame;
static uint16_t row[240];
static const struct {
  uint8_t cmd, n, data[12];
} regs[] = {
#include "gc9a01-registers.inc"
};
static void pin(LcdSignal p, bool high) { board_lcd_signal(p, high); }
static bool byte(uint8_t b) { return board_lcd_byte(b); }
static bool finish(void) { return board_lcd_finish(); }
static bool command(uint8_t cmd, const uint8_t *data, unsigned n) {
  pin(LCD_SELECT, false);
  pin(LCD_DATA, false);
  bool ok = byte(cmd) && finish();
  pin(LCD_DATA, true);
  for (unsigned i = 0; ok && i < n; i++)
    ok = byte(data[i]);
  ok = ok && finish();
  pin(LCD_SELECT, true);
  return ok;
}
void lcd_init(void) {
  pin(LCD_RESET, false);
  pin(LCD_BACKLIGHT, false);
  pin(LCD_SELECT, true);
  pin(LCD_DATA, false);
  board_lcd_setup();
  phase = 0;
  init_index=0; scanline=0;
  healthy = true;
  deadline = 20;
}
void lcd_power(bool enabled, uint32_t now) {
  if (enabled) { lcd_init(); deadline=now+20; return; }
  pin(LCD_BACKLIGHT,false); pin(LCD_RESET,false); pin(LCD_SELECT,false); pin(LCD_DATA,false);
  board_lcd_shutdown();
}
bool lcd_ok(void) { return healthy; }
void lcd_task(uint32_t now, const LcdView *view) {
  if (!healthy || (int32_t)(now - deadline) < 0)
    return;
  bool ok = true;
  switch (phase) {
  case 0:
    pin(LCD_RESET, true);
    deadline = now + 120;
    phase = 1;
    break;
  case 1:
    if (init_index < sizeof(regs) / sizeof(regs[0])) {
      const unsigned i = init_index++;
      ok = command(regs[i].cmd, regs[i].data, regs[i].n);
    } else {
      ok = command(0x11, 0, 0);
      deadline = now + 120;
      phase = 2;
    }
    break;
  case 2:
    ok = command(0x29, 0, 0);
    deadline = now + 20;
    phase = 3;
    break;
  case 3:
    if (!scanline)
      frame = *view; // Coherent UI for the full refresh
    lcd_render_row(&frame, scanline, row);
    {
      uint8_t x[] = {0, 0, 0, 239},
              y[] = {0, (uint8_t)scanline, 0, (uint8_t)scanline};
      ok = command(0x2a, x, 4) && command(0x2b, y, 4) && command(0x2c, 0, 0);
      pin(LCD_SELECT, false);
      pin(LCD_DATA, true);
      for (unsigned i = 0; ok && i < 240; i++)
        ok = byte(row[i] >> 8) && byte(row[i] & 255);
      ok = ok && finish();
      pin(LCD_SELECT, true);
    }
    if (++scanline == 240) {
      scanline = 0;
      pin(LCD_BACKLIGHT, true);
      deadline = now + 100;
    }
    break;
  }
  if (!ok) {
    healthy = false;
    pin(LCD_BACKLIGHT, false);
    pin(LCD_SELECT, true);
  } // USB and counting continue
}
