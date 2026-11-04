// SPDX-License-Identifier: MIT
#pragma once
#include <stdbool.h>
#include <stdint.h>
#define COUNTER_EDGES_PER_TURN 192
#define COUNTER_EDGES_PER_SCROLL 6
typedef struct {
  uint64_t turns;
  int32_t progress, scroll_fraction, pending;
  uint32_t previous_ms, rejected;
  uint16_t previous;
  bool baseline, scrolling;
} Counter;
void counter_init(Counter *c, uint64_t saved);
// Returns true when a completed turn changes the retained count.
bool counter_sample(Counter *c, uint16_t raw, bool encoder_ok, uint32_t ms,
                    bool scroll_enabled);
int8_t counter_report(Counter *c);
// Decimal representation without depending on libc's optional 64-bit printf.
void counter_format_total(uint64_t turns, char out[21]);
uint32_t record_crc(const uint8_t *data, unsigned len);
void record_encode(uint8_t out[32], uint32_t sequence, uint64_t turns);
bool record_decode(const uint8_t in[32], uint32_t *sequence, uint64_t *turns);
