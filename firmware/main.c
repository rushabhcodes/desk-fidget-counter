// SPDX-License-Identifier: MIT
#include "counter.h"
#include "button.h"
#include "lcd.h"
#include "stm32f0xx.h"
#include "tusb.h"
#include <stdio.h>
#include <string.h>
uint32_t SystemCoreClock = 48000000;
static volatile uint32_t ticks;
static Counter counter;
static bool stored = false, encoder_ok = true, peripherals_on = false;
static Dashboard dashboard;
static uint32_t cleared_at;
static bool clear_notice;
static unsigned active_slot = 0;
static uint32_t sequence = 0;
void SysTick_Handler(void) { ticks++; }
uint32_t tusb_time_millis_api(void) { return ticks; }
void USB_IRQHandler(void) {
  EXTI->PR = 1u << 18; // USB wake-up shares this IRQ on STM32F072 (RM0091).
  tud_int_handler(0);
}
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
static void clear_motion(void) {
  counter.pending = 0;
  counter.scroll_fraction = 0;
  counter.baseline = false;
}
void tud_mount_cb(void) { clear_motion(); }
void tud_umount_cb(void) { clear_motion(); dashboard.received=false; }
void tud_suspend_cb(bool remote_wakeup_en) {
  (void)remote_wakeup_en;
  clear_motion(); dashboard.received=false;
}
void tud_resume_cb(void) { clear_motion(); }
static void clock_run(void) {
  FLASH->ACR = FLASH_ACR_PRFTBE | FLASH_ACR_LATENCY;
  RCC->CR2 |= RCC_CR2_HSI48ON;
  while (!(RCC->CR2 & RCC_CR2_HSI48RDY)) {
  }
  RCC->CFGR = (RCC->CFGR & ~RCC_CFGR_SW) | RCC_CFGR_SW_HSI48;
  while ((RCC->CFGR & RCC_CFGR_SWS) != RCC_CFGR_SWS_HSI48) {
  }
}
static void usb_sleep(void) {
  // RM0091 Stop-mode / USB suspend sections: USB's asynchronous resume wakes EXTI18.
  // Keep IRQs masked until 48MHz is restored; a newly pending IRQ wakes WFI.
  __disable_irq();
  if (!tud_suspended() || !(USB->CNTR & USB_CNTR_LPMODE) ||
      NVIC_GetPendingIRQ(USB_IRQn)) { __enable_irq(); return; }
  SysTick->CTRL = 0;
  SCB->ICSR = SCB_ICSR_PENDSTCLR_Msk;
  PWR->CR = (PWR->CR & ~PWR_CR_PDDS) | PWR_CR_LPDS;
  SCB->SCR |= SCB_SCR_SLEEPDEEP_Msk;
  __DSB(); __WFI(); __ISB();
  SCB->SCR &= ~SCB_SCR_SLEEPDEEP_Msk;
  clock_run(); // Stop exits on HSI8; restore USB/application HSI48 before IRQ.
  SysTick_Config(48000);
  __enable_irq();
}
static void init(void) {
  clock_run();
  RCC->AHBENR |= RCC_AHBENR_GPIOAEN | RCC_AHBENR_GPIOBEN | RCC_AHBENR_GPIOCEN | RCC_AHBENR_GPIOFEN;
  GPIOC->MODER = 0xffffffffu;
  GPIOF->MODER = 0xffffffffu;
  GPIOB->MODER =
      0xffffffffu; // Unused GPIOs analog, configured pins overridden below.
  RCC->APB1ENR |= RCC_APB1ENR_I2C1EN | RCC_APB1ENR_USBEN | RCC_APB1ENR_CRSEN |
                  RCC_APB1ENR_TIM3EN | RCC_APB1ENR_SPI2EN | RCC_APB1ENR_PWREN;
  EXTI->RTSR |= 1u << 18;
  EXTI->IMR |= 1u << 18;
  RCC->CFGR3 &= ~RCC_CFGR3_USBSW; // HSI48 is the USB clock.
  CRS->CFGR =
      47999u | (34u << 16) | (2u << 28); // 1kHz USB SOF, default error limit.
  CRS->CR = CRS_CR_AUTOTRIMEN | CRS_CR_CEN | (32u << 8);
  SysTick_Config(48000);
  // Single front-side momentary button, PA0 active low with internal pull-up.
  pinmode(GPIOA, 0, 0);
  GPIOA->PUPDR = (GPIOA->PUPDR & ~3u) | 1u;
  for (unsigned p=1;p<8;p++) pinmode(GPIOA,p,3);
  pinmode(GPIOA,8,1);out(8,false);
  pinmode(GPIOA,9,3);pinmode(GPIOA,10,3);pinmode(GPIOA,15,3);
  GPIOB->BSRR = 1u << (2+16); // peripherals remain off until configured
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
static void reply(const char *s) {
  if (tud_cdc_connected()) {
    tud_cdc_write_str(s);
    tud_cdc_write_flush();
  }
}
static void status(void) {
  char b[320], turns[21];
  counter_format_total(counter.turns, turns);
  snprintf(b,sizeof b,
      "{\"device\":\"desk-fidget-counter\",\"protocol\":1,\"firmware\":\"5.0.0\","
      "\"turns\":%s,\"progress\":%ld,\"storage_ok\":%s,"
      "\"encoder_timer_running\":%s,\"scroll_on\":%s,\"rejected\":%lu,"
      "\"lcd_transport_ok\":%s,\"host_data_fresh\":%s}\r\n",
      turns,(long)counter.progress,stored?"true":"false",
      encoder_ok?"true":"false",counter.scrolling?"true":"false",
      (unsigned long)counter.rejected,lcd_ok()?"true":"false",
      dashboard_fresh(&dashboard,ticks)?"true":"false");
  reply(b);
}

static void reset_count(void) {
  if (save(0)) {
    counter_init(&counter, 0);
    cleared_at = ticks; clear_notice = true;
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
  unsigned bytes=0;
  while (tud_cdc_available() && bytes++<64) {
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
        reply("COUNT | STATUS | RESET CONFIRM | VERSION | DASH <clock date cpu ram battery ac>\r\n");
      else if (!strcmp(line, "VERSION"))
        reply("Desk Knob Rev E / firmware 5.0.0 / TinyUSB 0.21.0\r\n");
      else if (!strncmp(line,"DASH ",5)) {
        if (!dashboard_receive(&dashboard,line,ticks)) reply("ERROR DASH\r\n");
      } else
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
  uint32_t sample_at = ticks;
  bool scroll_mode = false; // Safe power-on default: count without host scrolling.
  ButtonState mode_button = {0};
  while (1) {
    tud_task();
    uint32_t now = ticks;
    bool awake = tud_mounted() && !tud_suspended();
    if (awake != peripherals_on) {
      clear_motion();
      counter.progress=0; // Cannot infer turns made while the optical LED is off.
      if (awake) {
        GPIOB->BSRR=1u<<2;
        delay_ms(5); // TPS22919 controlled ramp before SPI is driven
        lcd_power(true,ticks);
      } else {
        lcd_power(false,now); // All LCD signal pins low before removing its rail
        GPIOB->BSRR=1u<<(2+16);
      }
      peripherals_on=awake;
    }
    ButtonEvent event = button_update(&mode_button, !(GPIOA->IDR & 1u), awake, now);
    if (event == BUTTON_SHORT) {
      scroll_mode = !scroll_mode;
      counter.pending = 0;
      counter.scroll_fraction = 0; // Preserve partial-turn counting across mode changes.
    } else if (event == BUTTON_LONG) {
      reset_count();
    }
    if ((uint32_t)(now - sample_at) >= 2) {
      sample_at = now;
      encoder_ok = (TIM3->CR1 & TIM_CR1_CEN) != 0;
      uint16_t raw = (uint16_t)TIM3->CNT;
      bool changed = counter_sample(
          &counter, raw, encoder_ok && stored && peripherals_on, now,
          scroll_mode && awake);
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
    now=ticks; // FRAM/console work can advance time before the UI snapshot.
    if (clear_notice && (uint32_t)(now-cleared_at)>=2000) clear_notice=false;
    LcdView view = {.turns=counter.turns,.host=dashboard,.now=now,
                    .storage_ok=stored,.scroll_on=scroll_mode,.usb_ready=awake,
                    .encoder_ok=encoder_ok,.hold_ms=button_hold_ms(&mode_button,now),
                    .count_cleared=clear_notice && (uint32_t)(now-cleared_at)<2000};
    if (peripherals_on) lcd_task(now,&view);
    if (tud_suspended() && !peripherals_on) usb_sleep();
    else __WFI();
  }
}
