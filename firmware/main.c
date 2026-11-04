// SPDX-License-Identifier: MIT
#include "counter.h"
#include "lcd.h"
#include "stm32f0xx.h"
#include "tusb.h"
#include <stdio.h>
#include <string.h>
uint32_t SystemCoreClock = 48000000;
static volatile uint32_t ticks;
static Counter counter;
static bool stored = false, encoder_ok = true, low_battery = false,
            usb_present = false;
static unsigned active_slot = 0;
static uint32_t sequence = 0;
static uint16_t battery_mv = 0;
static uint16_t ntc_mv = 0;
static uint8_t charger_mode = 0;
void SysTick_Handler(void) { ticks++; }
uint32_t tusb_time_millis_api(void) { return ticks; }
void USB_IRQHandler(void) { tud_int_handler(0); }
static void pinmode(GPIO_TypeDef *g, unsigned p, unsigned mode) {
  g->MODER = (g->MODER & ~(3u << (2 * p))) | (mode << (2 * p));
}
static void out(unsigned p, bool on) {
  GPIOA->BSRR = 1u << (p + (on ? 0 : 16));
}
static void delay_ms(uint32_t n) {
  uint32_t t = ticks;
  while ((uint32_t)(ticks - t) < n) {
  }
}
static void
charge(unsigned mode) { // EN2,EN1 = 00 USB100, 01 USB500, 11 USB suspend.
  charger_mode = (uint8_t)mode;
  out(2, mode != 0);
  out(3, mode == 2);
}
void tud_mount_cb(void) { charge(1); }
void tud_umount_cb(void) {
  charge(0);
  counter.pending = 0;
  counter.scroll_fraction = 0;
}
void tud_suspend_cb(bool remote_wakeup_en) {
  (void)remote_wakeup_en;
  charge(2);
  counter.pending = 0;
  counter.scroll_fraction = 0;
}
void tud_resume_cb(void) { charge(tud_mounted() ? 1 : 0); }
static void init(void) {
  FLASH->ACR = FLASH_ACR_PRFTBE | FLASH_ACR_LATENCY;
  RCC->CR2 |= RCC_CR2_HSI48ON;
  while (!(RCC->CR2 & RCC_CR2_HSI48RDY)) {
  }
  RCC->CFGR = (RCC->CFGR & ~RCC_CFGR_SW) | RCC_CFGR_SW_HSI48;
  while ((RCC->CFGR & RCC_CFGR_SWS) != RCC_CFGR_SWS_HSI48) {
  }
  RCC->AHBENR |= RCC_AHBENR_GPIOAEN | RCC_AHBENR_GPIOBEN;
  GPIOB->MODER =
      0xffffffffu; // Unused GPIOs analog, configured pins overridden below.
  RCC->APB1ENR |= RCC_APB1ENR_I2C1EN | RCC_APB1ENR_USBEN | RCC_APB1ENR_CRSEN |
                  RCC_APB1ENR_TIM3EN | RCC_APB1ENR_SPI2EN;
  RCC->APB2ENR |= RCC_APB2ENR_ADCEN;
  RCC->CFGR3 &= ~RCC_CFGR3_USBSW; // HSI48 is the USB clock.
  CRS->CFGR =
      47999u | (34u << 16) | (2u << 28); // 1kHz USB SOF, default error limit.
  CRS->CR = CRS_CR_AUTOTRIMEN | CRS_CR_CEN | (32u << 8);
  SysTick_Config(48000);
  // GPIO0 scroll, GPIO1 reset: external 10k pull-ups; GPIO4/5 open-drain
  // charger status.
  for (unsigned p = 0; p < 6; p++)
    pinmode(GPIOA, p, (p == 2 || p == 3) ? 1 : 0);
  pinmode(GPIOA, 6, 1);
  out(6, false);
  charge(0);
  pinmode(GPIOA, 7, 3);
  pinmode(GPIOB, 0, 3);
  pinmode(GPIOB, 1, 3);
  GPIOB->BSRR = (1u << 2); // CE high before enabling its GPIO output.
  pinmode(GPIOB, 2, 1);
  pinmode(GPIOB, 6, 2);
  pinmode(GPIOB, 7, 2);
  GPIOB->OTYPER |= (1u << 6) | (1u << 7);
  GPIOB->AFR[0] =
      (GPIOB->AFR[0] & ~(0xffu << 24)) | (0x11u << 24); // PB6/7 AF1 I2C1.
  pinmode(GPIOA, 11, 2);
  pinmode(GPIOA, 12, 2); // AF0 USB; PA13/14 remain SWD.
  // Conservative ~300kHz bus: low 1.67us, high 1.33us plus
  // synchronizer/filter/rise time.
  I2C1->TIMINGR = 0x30b00f13; // PRESC3=83.3ns, SCLDEL11, SDADEL0, H15, L19.
  I2C1->CR1 = I2C_CR1_PE;
  // Dual Schmitt outputs -> PB4/PB5 AF1 TIM3_CH1/CH2. Hardware keeps
  // counting edges while a display row or FRAM transfer is in progress.
  pinmode(GPIOB, 4, 2);
  pinmode(GPIOB, 5, 2);
  GPIOB->AFR[0] = (GPIOB->AFR[0] & ~(0xffu << 16)) | (0x11u << 16);
  TIM3->ARR = 65535;
  TIM3->CCMR1 = 1u | (13u << 4) | (1u << 8) | (13u << 12); // ~3.3us filters
  TIM3->CCER = TIM_CCER_CC1E | TIM_CCER_CC2E;
  TIM3->SMCR = 3; // encoder mode 3, count both edges of both channels
  TIM3->EGR = TIM_EGR_UG;
  TIM3->CNT = 0;
  TIM3->CR1 = TIM_CR1_CEN;
  lcd_init();
  ADC1->CR |= ADC_CR_ADCAL;
  while (ADC1->CR & ADC_CR_ADCAL) {
  }
  ADC1->CFGR2 = ADC_CFGR2_CKMODE_0;
  ADC1->SMPR = 7;
  ADC->CCR |= ADC_CCR_VREFEN;
  ADC1->ISR = ADC_ISR_ADRDY;
  ADC1->CR |= ADC_CR_ADEN;
  while (!(ADC1->ISR & ADC_ISR_ADRDY)) {
  }
}
static void i2c_abort(void) {
  I2C1->CR2 |= I2C_CR2_STOP;
  I2C1->CR1 = 0;
  I2C1->ICR = 0x3f38;
  I2C1->CR1 = I2C_CR1_PE;
}
static bool wait_flag(uint32_t flag) {
  uint32_t start = ticks;
  while (!(I2C1->ISR & flag)) {
    if ((I2C1->ISR & (I2C_ISR_NACKF | I2C_ISR_BERR | I2C_ISR_ARLO)) ||
        (uint32_t)(ticks - start) > 3) {
      i2c_abort();
      return false;
    }
  }
  return true;
}
static bool transfer(uint8_t addr, const uint8_t *w, unsigned wn, uint8_t *r,
                     unsigned rn) {
  if (I2C1->ISR & I2C_ISR_BUSY) {
    i2c_abort();
    return false;
  }
  I2C1->ICR = 0x3f38;
  if (wn) {
    I2C1->CR2 =
        (addr << 1) | (wn << 16) | I2C_CR2_START | (rn ? 0 : I2C_CR2_AUTOEND);
    for (unsigned i = 0; i < wn; i++) {
      if (!wait_flag(I2C_ISR_TXIS))
        return false;
      I2C1->TXDR = w[i];
    }
    if (!wait_flag(rn ? I2C_ISR_TC : I2C_ISR_STOPF))
      return false;
  }
  if (rn) {
    I2C1->CR2 = (addr << 1) | (rn << 16) | I2C_CR2_RD_WRN | I2C_CR2_START |
                I2C_CR2_AUTOEND;
    for (unsigned i = 0; i < rn; i++) {
      if (!wait_flag(I2C_ISR_RXNE))
        return false;
      r[i] = (uint8_t)I2C1->RXDR;
    }
    if (!wait_flag(I2C_ISR_STOPF))
      return false;
  }
  I2C1->ICR = I2C_ICR_STOPCF;
  return true;
}
static bool fram_read(unsigned a, uint8_t *p, unsigned n) {
  uint8_t w[2] = {(uint8_t)(a >> 8), (uint8_t)a};
  return transfer(0x50, w, 2, p, n);
}
static bool fram_write(unsigned a, const uint8_t *p, unsigned n) {
  uint8_t w[34];
  if (n > 32)
    return false;
  w[0] = (uint8_t)(a >> 8);
  w[1] = (uint8_t)a;
  memcpy(w + 2, p, n);
  return transfer(0x50, w, n + 2, NULL, 0);
}
static bool save(uint64_t turns) {
  unsigned slot = active_slot ^ 1u, addr = slot * 64;
  uint8_t p[32], verify[32], zero[4] = {0};
  uint32_t seq;
  uint64_t count;
  record_encode(p, sequence + 1, turns);
  if (!fram_write(addr + 28, zero, 4) || !fram_write(addr, p, 28) ||
      !fram_write(addr + 28, p + 28, 4) || !fram_read(addr, verify, 32) ||
      !record_decode(verify, &seq, &count) || count != turns ||
      seq != sequence + 1)
    return false;
  active_slot = slot;
  sequence = seq;
  stored = true;
  return true;
}
static void restore(void) {
  uint8_t a[32], b[32];
  uint32_t sa = 0, sb = 0;
  uint64_t ca = 0, cb = 0;
  bool va = fram_read(0, a, 32) && record_decode(a, &sa, &ca),
       vb = fram_read(64, b, 32) && record_decode(b, &sb, &cb);
  if (va && (!vb || (int32_t)(sa - sb) > 0)) {
    active_slot = 0;
    sequence = sa;
    counter_init(&counter, ca);
    stored = true;
  } else if (vb) {
    active_slot = 1;
    sequence = sb;
    counter_init(&counter, cb);
    stored = true;
  } else
    counter_init(&counter, 0); // Require deliberate RESET CONFIRM / 3s button
                               // to initialize unknown FRAM.
}
static uint16_t adc(unsigned ch) {
  ADC1->CHSELR = 1u << ch;
  ADC1->CR |= ADC_CR_ADSTART;
  uint32_t t = ticks;
  while (!(ADC1->ISR & ADC_ISR_EOC)) {
    if ((uint32_t)(ticks - t) > 2)
      return 0;
  }
  return (uint16_t)ADC1->DR;
}
static void power_poll(void) {
  uint16_t vref = adc(17);
  if (!vref)
    return;
  uint32_t vdda = 3300u * (*(const uint16_t *)0x1ffff7ba) / vref;
  battery_mv = (uint16_t)(adc(7) * vdda * 2u / 4095u);
  ntc_mv = (uint16_t)(adc(9) * vdda * 2u / 4095u);
  // 103AT-2, 75uA nominal TS bias, 200k parallel divider load. This
  // conservative voltage window stays within the cell's 0..45C charging range
  // including bias tolerance.
  bool thermal_ok = charger_temperature_ok(ntc_mv);
  GPIOB->BSRR = thermal_ok ? (1u << (2 + 16)) : (1u << 2);
  uint32_t vbus = adc(8) * vdda * 147u / (4095u * 47u);
  bool present = !(GPIOA->IDR & (1u << 4));
  (void)vbus;
  if (present != usb_present) {
    usb_present = present;
    counter.pending = 0;
    counter.scroll_fraction = 0;
    if (present)
      tud_connect();
    else {
      tud_disconnect();
      charge(0);
    }
  }
  static unsigned low_samples = 0;
  if (!usb_present && battery_mv < 3450) {
    if (low_samples < 3)
      low_samples++;
  } else
    low_samples = 0;
  low_battery = low_samples >= 3;
}
static void reply(const char *s) {
  if (tud_cdc_connected()) {
    tud_cdc_write_str(s);
    tud_cdc_write_flush();
  }
}
static void status(void) {
  char b[320];
  char turns[21];
  counter_format_total(counter.turns, turns);
  snprintf(
      b, sizeof(b),
      "{\"turns\":%s"
      ",\"progress\":%ld,\"storage_ok\":%s,\"encoder_timer_running\":%s,\"scroll_on\":"
      "%s,\"battery_mv\":%u,\"low_battery\":%s,\"rejected\":%lu,\"lcd_transport_ok\":%s,"
      "\"charger_"
      "mode\":%u}\r\n",
      turns, (long)counter.progress, stored ? "true" : "false",
      encoder_ok ? "true" : "false", counter.scrolling ? "true" : "false",
      battery_mv, low_battery ? "true" : "false",
      (unsigned long)counter.rejected, lcd_ok() ? "true" : "false",
      charger_mode);
  reply(b);
}
static void reset_count(void) {
  if (save(0)) {
    counter_init(&counter, 0);
    reply("OK RESET\r\n");
  } else {
    stored = false;
    reply("ERROR STORAGE\r\n");
  }
}
static void console(void) {
  static char line[64];
  static unsigned n = 0;
  static bool overflow = false;
  while (tud_cdc_available()) {
    char c = (char)tud_cdc_read_char();
    if (c == '\r')
      continue;
    if (c == '\n') {
      line[n] = 0;
      if (overflow)
        reply("ERROR LINE TOO LONG\r\n");
      else if (!strcmp(line, "COUNT") || !strcmp(line, "STATUS"))
        status();
      else if (!strcmp(line, "RESET CONFIRM"))
        reset_count();
      else if (!strcmp(line, "HELP"))
        reply("COUNT | STATUS | RESET CONFIRM | VERSION\r\n");
      else if (!strcmp(line, "VERSION"))
        reply("Desk Knob Rev C / firmware 3.0.0 / TinyUSB 0.21.0\r\n");
      else
        reply("ERROR COMMAND\r\n");
      n = 0;
      overflow = false;
    } else if (n < sizeof(line) - 1)
      line[n++] = c;
    else
      overflow = true;
  }
}
int main(void) {
  init();
  delay_ms(50);
  restore();
  tusb_rhport_init_t cfg = {.role = TUSB_ROLE_DEVICE, .speed = TUSB_SPEED_FULL};
  tusb_init(0, &cfg);
  tud_disconnect();
  uint32_t sample_at = ticks, power_at = ticks, button_since = 0,
           sw_since = ticks;
  bool held = false, reset_done = false, sw = false, sw_candidate = false;
  while (1) {
    tud_task();
    uint32_t now = ticks;
    bool present = !(GPIOA->IDR & (1u << 4));
    if (present != usb_present) {
      usb_present = present;
      counter.pending = 0;
      counter.scroll_fraction = 0;
      if (present)
        tud_connect();
      else {
        tud_disconnect();
        charge(0);
      }
    }
    if ((uint32_t)(now - power_at) >= 100) {
      power_at = now;
      power_poll();
    }
    bool raw_sw = !(GPIOA->IDR & 1u);
    if (raw_sw != sw_candidate) {
      sw_candidate = raw_sw;
      sw_since = now;
    }
    if ((uint32_t)(now - sw_since) >= 20)
      sw = sw_candidate;
    bool button = !(GPIOA->IDR & (1u << 1));
    if (button && !held) {
      held = true;
      button_since = now;
      reset_done = false;
    } else if (!button) {
      held = false;
    }
    if (held && !reset_done && (uint32_t)(now - button_since) >= 3000) {
      reset_count();
      reset_done = true;
    }
    if ((uint32_t)(now - sample_at) >= 2) {
      sample_at = now;
      encoder_ok = (TIM3->CR1 & TIM_CR1_CEN) != 0;
      uint16_t raw = (uint16_t)TIM3->CNT;
      bool changed = counter_sample(
          &counter, raw, encoder_ok && stored && !low_battery, now,
          sw && usb_present && tud_mounted() && !tud_suspended());
      if (changed && !save(counter.turns)) {
        stored = false;
        counter.baseline = false;
      }
    }
    if (tud_hid_ready() && counter.pending) {
      int8_t wheel = counter_report(&counter);
      tud_hid_mouse_report(0, 0, 0, 0, wheel, 0);
    }
    console();
    LcdView view = {.turns = counter.turns,
                    .battery_mv = battery_mv,
                    .storage_ok = stored,
                    .low_battery = low_battery,
                    .scroll_on = sw,
                    .usb_ready =
                        usb_present && tud_mounted() && !tud_suspended(),
                    .charging = usb_present && !(GPIOA->IDR & (1u << 5))};
    lcd_task(now, &view);
    // 4Hz fault; slow battery heartbeat; steady scroll-mode indicator on USB.
    out(6, (!stored || !encoder_ok || low_battery) ? ((now / 125) & 1u)
           : usb_present                           ? (sw || now % 2000 < 30)
                                                   : now % 2000 < 15);
  }
}
