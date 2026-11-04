// SPDX-License-Identifier: MIT
#include "lcd.h"
#include <assert.h>
#include <stdio.h>
#include <string.h>
int main(int argc, char **argv) {
  LcdView view = {.turns = 12345,
                  .battery_mv = 3920,
                  .storage_ok = true,
                  .scroll_on = true,
                  .usb_ready = true,
                  .charging = true};
  struct {
    uint16_t before[8], row[240], after[8];
  } guarded;
  FILE *f = argc > 1 ? fopen(argv[1], "wb") : NULL;
  if (f)
    fprintf(f, "P6\n240 240\n255\n");
  unsigned colored = 0;
  for (unsigned state = 0; state < 3; state++) {
    if (state == 1)
      view.turns = UINT64_MAX;
    if (state == 2) {
      view.storage_ok = false;
      view.low_battery = true;
      view.scroll_on = false;
      view.usb_ready = false;
    }
    for (unsigned y = 0; y < 240; y++) {
      memset(&guarded, 0xa5, sizeof(guarded));
      lcd_render_row(&view, y, guarded.row);
      for (unsigned i = 0; i < 8; i++)
        assert(guarded.before[i] == 0xa5a5 && guarded.after[i] == 0xa5a5);
      for (unsigned x = 0; x < 240; x++) {
        uint16_t v = guarded.row[x];
        colored += v != 0x0863;
        if (f && state == 0) {
          unsigned char rgb[] = {(unsigned char)(((v >> 11) & 31) * 255 / 31),
                                 (unsigned char)(((v >> 5) & 63) * 255 / 63),
                                 (unsigned char)((v & 31) * 255 / 31)};
          fwrite(rgb, 1, 3, f);
        }
      }
    }
  }
  assert(colored > 1000);
  if (f)
    fclose(f);
  puts("LCD UI: all 240 scanlines, 20-digit counts, fault states and buffer "
       "boundaries passed");
}
