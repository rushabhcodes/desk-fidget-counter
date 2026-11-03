// SPDX-License-Identifier: MIT
#include "counter.h"
#include <assert.h>
#include <stdio.h>
#include <string.h>
static unsigned ms;
static void move(Counter *c, int steps, int delta, bool scroll) {
  for (int i = 0; i < steps; i++) {
    uint16_t a = (uint16_t)((c->previous + delta + 4096) % 4096);
    counter_sample(c, a, true, ++ms, scroll);
  }
}
int main(void) {
  assert(!charger_temperature_ok(0));
  assert(!charger_temperature_ok(449));
  assert(charger_temperature_ok(450));
  assert(charger_temperature_ok(750));
  assert(charger_temperature_ok(1300));
  assert(!charger_temperature_ok(1301));
  assert(!charger_temperature_ok(5000));
  Counter c;
  counter_init(&c, 0);
  counter_sample(&c, 4000, true, ++ms, false);
  move(&c, 32, 128, false);
  assert(c.turns == 1 && c.progress == 0);
  move(&c, 32, -128, false);
  assert(c.turns == 2);
  move(&c, 16, 128, false);
  move(&c, 16, -128, false);
  assert(c.turns == 2 && c.progress == 0);
  move(&c, 16, 128, false);
  move(&c, 48, -128, false);
  assert(c.turns == 3 && c.progress == 0);
  move(&c, 8, 128, true);
  assert(counter_report(&c) == 8);
  move(&c, 4, 128, true);
  move(&c, 1, 128, false);
  assert(counter_report(&c) == 0);
  move(&c, 19, 128, false);
  assert(c.turns == 4);
  move(&c, 1, 128, true);
  assert(counter_report(&c) == 1);
  counter_sample(&c, 1234, false, ++ms, true);
  assert(!c.baseline && c.progress == 0 && counter_report(&c) == 0);
  counter_sample(&c, 4000, true, ++ms, true);
  counter_sample(&c, 100, true, ++ms, true);
  assert(c.progress == 196);
  counter_sample(&c, 1000, true, ms += 21, true);
  assert(c.progress == 0);
  counter_sample(&c, 2500, true, ++ms, true);
  assert(!c.baseline);
  counter_init(&c, UINT64_MAX);
  counter_sample(&c, 0, true, ++ms, false);
  move(&c, 32, 128, false);
  assert(c.turns == UINT64_MAX);
  counter_init(&c, 0);
  counter_sample(&c, 0, true, ++ms, false);
  move(&c, 4096, 1, false);
  assert(c.turns == 1);
  move(&c, 1000, 1, false);
  move(&c, 1000, -1, false);
  assert(c.turns == 1 && c.progress == 0);
  uint8_t a[32], b[32];
  uint32_t seq;
  uint64_t turns;
  record_encode(a, 42, 0x123456789abcdef0ULL);
  assert(record_decode(a, &seq, &turns) && seq == 42 &&
         turns == 0x123456789abcdef0ULL);
  for (unsigned i = 0; i < 32; i++) {
    memcpy(b, a, 32);
    b[i] ^= 1;
    assert(!record_decode(b, &seq, &turns));
  }
  // Every interrupted prefix of the next journal record must leave the previous
  // slot usable.
  record_encode(b, 43, 11);
  for (unsigned n = 0; n < 32; n++) {
    uint8_t partial[32] = {0};
    memcpy(partial, b, n);
    assert(!record_decode(partial, &seq, &turns));
    assert(record_decode(a, &seq, &turns) && seq == 42);
  }
  char decimal[21];
  counter_format_total(0, decimal);
  assert(strcmp(decimal, "0") == 0);
  counter_format_total(4294967296ULL, decimal);
  assert(strcmp(decimal, "4294967296") == 0);
  counter_format_total(UINT64_MAX, decimal);
  assert(strcmp(decimal, "18446744073709551615") == 0);
  puts("counter tests: CW, CCW, wraps, reversals, slow motion, gates, "
       "stale/invalid/jump samples, saturation, CRC, 32 torn writes and "
       "64-bit decimal console formatting passed");
}
