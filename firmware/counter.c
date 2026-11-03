// SPDX-License-Identifier: MIT
#include "counter.h"
#include <limits.h>
#include <string.h>
void counter_init(Counter *c, uint64_t saved) {
  memset(c, 0, sizeof(*c));
  c->turns = saved;
}
bool counter_sample(Counter *c, uint16_t raw, bool valid, uint32_t ms,
                    bool enabled) {
  if (enabled != c->scrolling) {
    c->pending = 0;
    c->scroll_fraction = 0;
    c->scrolling = enabled;
  }
  if (!valid || raw >= 4096) {
    c->baseline = false;
    c->progress = 0;
    c->pending = 0;
    c->scroll_fraction = 0;
    c->rejected++;
    return false;
  }
  if (!c->baseline || (uint32_t)(ms - c->previous_ms) > 20) {
    c->previous = raw;
    c->previous_ms = ms;
    c->baseline = true;
    c->progress = 0;
    c->pending = 0;
    c->scroll_fraction = 0;
    return false;
  }
  int d = (int)raw - c->previous;
  c->previous = raw;
  c->previous_ms = ms;
  if (d > 2048)
    d -= 4096;
  else if (d < -2048)
    d += 4096;
  if (d > 1024 || d < -1024) {
    c->baseline = false;
    c->progress = 0;
    c->pending = 0;
    c->scroll_fraction = 0;
    c->rejected++;
    return false;
  }
  c->progress += d;
  bool changed = false;
  if (c->progress >= 4096 || c->progress <= -4096) {
    if (c->turns < UINT64_MAX)
      c->turns++;
    c->progress += (c->progress > 0 ? -4096 : 4096);
    changed = true;
  }
  if (enabled) {
    c->scroll_fraction += d;
    int ticks = c->scroll_fraction / 128;
    c->scroll_fraction -= ticks * 128;
    c->pending += ticks;
    if (c->pending > 127)
      c->pending = 127;
    if (c->pending < -127)
      c->pending = -127;
  }
  return changed;
}
int8_t counter_report(Counter *c) {
  int8_t n = (int8_t)c->pending;
  c->pending = 0;
  return n;
}
uint32_t record_crc(const uint8_t *p, unsigned n) {
  uint32_t c = ~0u;
  while (n--) {
    c ^= *p++;
    for (int k = 0; k < 8; k++)
      c = (c >> 1) ^ ((0u - (c & 1u)) & 0xedb88320u);
  }
  return ~c;
}
static void put32(uint8_t *p, uint32_t n) {
  for (int i = 0; i < 4; i++)
    p[i] = (uint8_t)(n >> (8 * i));
}
static uint32_t get32(const uint8_t *p) {
  return (uint32_t)p[0] | (uint32_t)p[1] << 8 | (uint32_t)p[2] << 16 |
         (uint32_t)p[3] << 24;
}
void record_encode(uint8_t p[32], uint32_t seq, uint64_t turns) {
  memset(p, 0, 32);
  memcpy(p, "DKA1", 4);
  put32(p + 4, seq);
  put32(p + 8, (uint32_t)turns);
  put32(p + 12, (uint32_t)(turns >> 32));
  put32(p + 24, record_crc(p, 24));
  put32(p + 28, 0xa55a3cc3u);
}
bool record_decode(const uint8_t p[32], uint32_t *s, uint64_t *t) {
  if (memcmp(p, "DKA1", 4) || get32(p + 28) != 0xa55a3cc3u ||
      record_crc(p, 24) != get32(p + 24))
    return false;
  *s = get32(p + 4);
  *t = get32(p + 8) | (uint64_t)get32(p + 12) << 32;
  return true;
}

bool charger_temperature_ok(uint16_t mv) { return mv >= 450 && mv <= 1300; }
