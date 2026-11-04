// SPDX-License-Identifier: MIT
#include "lcd.h"
#include "stm32f0xx.h"
// Mode 0, SPI2 12MHz; one 480-byte scanline per task call. No full framebuffer.
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
static void pin(unsigned p, bool high) {
  if (p == 12)
    GPIOA->BSRR = 1u << (8 + (high ? 0 : 16));
  else
    GPIOB->BSRR = 1u << (p + (high ? 0 : 16));
}
static bool byte(uint8_t b) {
  unsigned budget = 4800;
  while (!(SPI2->SR & SPI_SR_TXE))
    if (!--budget)
      return false;
  *(volatile uint8_t *)&SPI2->DR = b;
  return true;
}
static bool finish(void) {
  unsigned budget = 48000;
  while (SPI2->SR & SPI_SR_BSY)
    if (!--budget)
      return false;
  return true;
}
static bool command(uint8_t cmd, const uint8_t *data, unsigned n) {
  pin(12, false);
  pin(14, false);
  bool ok = byte(cmd) && finish();
  pin(14, true);
  for (unsigned i = 0; ok && i < n; i++)
    ok = byte(data[i]);
  ok = ok && finish();
  pin(12, true);
  return ok;
}
void lcd_init(void) {
  pin(10, false);
  pin(11, false);
  pin(12, true);
  pin(14, false);
  GPIOA->MODER = (GPIOA->MODER & ~(3u << 16)) | (1u << 16); // PA8 CS
  for (unsigned p = 10; p <= 15; p++) {
    if (p == 12)
      continue; // PB12 unused; software CS is PA8
    unsigned mode = (p == 13 || p == 15) ? 2 : 1;
    GPIOB->MODER = (GPIOB->MODER & ~(3u << (p * 2))) | (mode << (p * 2));
    GPIOB->OSPEEDR |= 3u << (p * 2);
  }
  GPIOB->AFR[1] &= ~((15u << 20) | (15u << 28)); // AF0 SPI2 PB13/PB15
  SPI2->CR2 = (7u << 8) | SPI_CR2_FRXTH;
  SPI2->CR1 = SPI_CR1_MSTR | SPI_CR1_SSM | SPI_CR1_SSI | SPI_CR1_BR_0 |
              SPI_CR1_BIDIMODE | SPI_CR1_BIDIOE | SPI_CR1_SPE;
  phase = 0;
  healthy = true;
  deadline = 20;
}
bool lcd_ok(void) { return healthy; }
void lcd_task(uint32_t now, const LcdView *view) {
  if (!healthy || (int32_t)(now - deadline) < 0)
    return;
  bool ok = true;
  switch (phase) {
  case 0:
    pin(10, true);
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
      pin(12, false);
      pin(14, true);
      for (unsigned i = 0; ok && i < 240; i++)
        ok = byte(row[i] >> 8) && byte(row[i] & 255);
      ok = ok && finish();
      pin(12, true);
    }
    if (++scanline == 240) {
      scanline = 0;
      pin(11, true);
      deadline = now + 100;
    }
    break;
  }
  if (!ok) {
    healthy = false;
    pin(11, false);
    pin(12, true);
  } // USB and counting continue
}
