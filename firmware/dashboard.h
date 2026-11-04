// SPDX-License-Identifier: MIT
#pragma once
#include <stdbool.h>
#include <stdint.h>
typedef struct {
  unsigned seconds, year, month, day, cpu_tenths, ram_tenths;
  int battery_percent; // -1 means host has no battery sensor
  bool ac, received;
  uint32_t received_at;
} Dashboard;
// Atomic update: malformed or out-of-range packets leave the last sample intact.
bool dashboard_receive(Dashboard *d, const char *line, uint32_t now);
bool dashboard_fresh(const Dashboard *d, uint32_t now);
unsigned dashboard_seconds(const Dashboard *d, uint32_t now);
void dashboard_date(const Dashboard *d, uint32_t now, unsigned *year, unsigned *month, unsigned *day);
