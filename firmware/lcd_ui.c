// SPDX-License-Identifier: MIT
#include "counter.h"
#include "lcd.h"
#include <string.h>
// Original compact 5x7 bitmap alphabet, rows packed as five bits.
static const struct {
  char c;
  uint8_t rows[7];
} font[] = {
    {'0', {14, 17, 19, 21, 25, 17, 14}}, {'1', {4, 12, 4, 4, 4, 4, 14}},
    {'2', {14, 17, 1, 2, 4, 8, 31}},     {'3', {30, 1, 1, 14, 1, 1, 30}},
    {'4', {2, 6, 10, 18, 31, 2, 2}},     {'5', {31, 16, 16, 30, 1, 1, 30}},
    {'6', {14, 16, 16, 30, 17, 17, 14}}, {'7', {31, 1, 2, 4, 8, 8, 8}},
    {'8', {14, 17, 17, 14, 17, 17, 14}}, {'9', {14, 17, 17, 15, 1, 1, 14}},
    {'A', {14, 17, 17, 31, 17, 17, 17}}, {'B', {30, 17, 17, 30, 17, 17, 30}},
    {'C', {14, 17, 16, 16, 16, 17, 14}}, {'D', {30, 17, 17, 17, 17, 17, 30}},
    {'E', {31, 16, 16, 30, 16, 16, 31}}, {'F', {31, 16, 16, 30, 16, 16, 16}},
    {'G', {14, 17, 16, 23, 17, 17, 14}}, {'H', {17, 17, 17, 31, 17, 17, 17}},
    {'I', {14, 4, 4, 4, 4, 4, 14}},      {'K', {17, 18, 20, 24, 20, 18, 17}},
    {'W', {17, 17, 17, 21, 21, 21, 10}}, {'L', {16, 16, 16, 16, 16, 16, 31}},
    {'M', {17, 27, 21, 21, 17, 17, 17}}, {'N', {17, 25, 21, 19, 17, 17, 17}},
    {'O', {14, 17, 17, 17, 17, 17, 14}}, {'P', {30, 17, 17, 30, 16, 16, 16}},
    {'R', {30, 17, 17, 30, 20, 18, 17}}, {'S', {15, 16, 16, 14, 1, 1, 30}},
    {'T', {31, 4, 4, 4, 4, 4, 4}},       {'U', {17, 17, 17, 17, 17, 17, 14}},
    {'V', {17, 17, 17, 17, 17, 10, 4}},  {'Y', {17, 17, 10, 4, 4, 4, 4}},
    {'.', {0, 0, 0, 0, 0, 6, 6}},        {'-', {0, 0, 0, 31, 0, 0, 0}}};
static void text(uint16_t row[240], unsigned y, const char *s, unsigned top,
                 unsigned scale, uint16_t color) {
  if (y < top || y >= top + 7 * scale)
    return;
  int left = (240 - (int)strlen(s) * 6 * (int)scale + (int)scale) / 2;
  unsigned line = (y - top) / scale;
  for (unsigned i = 0; s[i]; i++) {
    uint8_t bits = 0;
    for (unsigned k = 0; k < sizeof(font) / sizeof(font[0]); k++)
      if (font[k].c == s[i]) {
        bits = font[k].rows[line];
        break;
      }
    for (unsigned col = 0; col < 5; col++)
      if (bits & (16u >> col))
        for (unsigned dx = 0; dx < scale; dx++) {
          int x = left + (int)(i * 6 * scale + col * scale + dx);
          if (x >= 0 && x < 240)
            row[x] = color;
        }
  }
}
void lcd_render_row(const LcdView *v, unsigned y, uint16_t row[240]) {
  const uint16_t bg = 0x0863, white = 0xe71c, gold = 0xfdea, mint = 0x6f39,
                 red = 0xfa88;
  for (unsigned x = 0; x < 240; x++)
    row[x] = bg;
  if (y >= 240)
    return;
  text(row, y, "DESK KNOB", 37, 2, mint);
  text(row, y, "TURNS", 66, 2, white);
  char count[21];
  counter_format_total(v->turns, count);
  unsigned n = strlen(count);
  if (n <= 10)
    text(row, y, count, 91, n <= 7 ? 5 : 3, gold);
  else {
    char a[11];
    memcpy(a, count, n - 10);
    a[n - 10] = 0;
    text(row, y, a, 87, 3, gold);
    text(row, y, count + n - 10, 114, 3, gold);
  }
  text(row, y, v->scroll_on ? "SCROLL ON" : "SCROLL OFF", 150, 2,
       v->scroll_on ? mint : white);
  text(row, y, v->usb_ready ? "USB READY" : "COUNT ONLY", 172, 1, white);
  char volts[] = "0.00 V";
  volts[0] = (char)('0' + v->battery_mv / 1000 % 10);
  volts[2] = (char)('0' + v->battery_mv / 100 % 10);
  volts[3] = (char)('0' + v->battery_mv / 10 % 10);
  text(row, y, volts, 190, 2, v->low_battery ? red : white);
  text(row, y,
       !v->storage_ok   ? "RESET VIA USB"
       : v->low_battery ? "LOW BATTERY"
       : v->charging    ? "CHARGING"
                        : "",
       216, 1, !v->storage_ok || v->low_battery ? red : mint);
}
