// SPDX-License-Identifier: MIT
#include "board.h"
#include "board-pins.h"
#include "hardware/clocks.h"
#include "hardware/gpio.h"
#include "hardware/i2c.h"
#include "hardware/pio.h"
#include "hardware/spi.h"
#include "hardware/sync.h"
#include "pico/stdlib.h"
#include "quadrature_encoder.pio.h"
#include "tusb.h"

static const uint lcd_pins[] = {PIN_LCD_RST, PIN_LCD_BL, PIN_LCD_CS, PIN_LCD_DC};
static struct repeating_timer wake_timer;
static bool timer_running, encoder_healthy = true;
static bool wake_tick(struct repeating_timer *timer) { (void)timer; return true; }

uint32_t board_millis(void) { return to_ms_since_boot(get_absolute_time()); }
void board_delay_ms(uint32_t ms) { sleep_ms(ms); }
bool board_button_pressed(void) { return !gpio_get(PIN_MODE_BTN); }

void board_init(void) {
  // Share the 48MHz USB PLL; keep the unused system PLL powered down.
  set_sys_clock_48mhz();
  gpio_init(PIN_PERIPH_EN);
  gpio_put(PIN_PERIPH_EN, false);
  gpio_set_dir(PIN_PERIPH_EN, GPIO_OUT);
  gpio_init(PIN_MODE_BTN);
  gpio_set_dir(PIN_MODE_BTN, GPIO_IN);
  gpio_pull_up(PIN_MODE_BTN);
  board_lcd_shutdown();
  i2c_init(i2c0, BOARD_I2C_HZ);
  gpio_set_function(PIN_SDA, GPIO_FUNC_I2C);
  gpio_set_function(PIN_SCL, GPIO_FUNC_I2C);
  // External pull-ups are fitted; no internal pull-ups to mask a wiring fault.
  gpio_disable_pulls(PIN_SDA);
  gpio_disable_pulls(PIN_SCL);
  uint offset = pio_add_program(pio0, &quadrature_encoder_program);
  hard_assert(offset == 0); // Computed jump table must occupy instruction zero.
  quadrature_encoder_program_init(pio0, 0, PIN_ENC_A, BOARD_ENCODER_MAX_STEP_RATE);
  gpio_disable_pulls(PIN_ENC_A);
  gpio_disable_pulls(PIN_ENC_B);
  gpio_set_input_hysteresis_enabled(PIN_ENC_A, true);
  gpio_set_input_hysteresis_enabled(PIN_ENC_B, true);
  pio_sm_set_enabled(pio0, 0, false);
}

void board_peripherals(bool enabled) {
  if (!enabled) pio_sm_set_enabled(pio0, 0, false);
  gpio_put(PIN_PERIPH_EN, enabled);
  if (enabled) {
    sleep_ms(5); // Settle the switched IR rail before acquiring a new baseline.
    pio_sm_clear_fifos(pio0, 0);
    encoder_healthy = true;
    pio_sm_set_enabled(pio0, 0, true);
  }
}
bool board_encoder_ok(void) {
  return encoder_healthy && (pio0->ctrl & 1u);
}
uint16_t board_encoder_count(void) {
  if (!board_encoder_ok()) return 0;
  // Drain old FIFO samples and get one fresh count. Bound the wait so a stopped
  // state machine reports a fault instead of hanging USB or persistence.
  unsigned n = pio_sm_get_rx_fifo_level(pio0, 0) + 1;
  uint32_t count = 0;
  uint64_t deadline = time_us_64() + 100;
  while (n) {
    if (!pio_sm_is_rx_fifo_empty(pio0, 0)) {
      count = pio_sm_get(pio0, 0);
      --n;
    } else if (time_us_64() >= deadline) {
      encoder_healthy = false;
      return 0;
    }
  }
  return (uint16_t)count;
}
bool board_i2c_transfer(uint8_t addr, const uint8_t *write, unsigned wn,
                        uint8_t *read, unsigned rn) {
  if (wn && i2c_write_timeout_us(i2c0, addr, write, wn, rn != 0, 3000) != (int)wn)
    return false;
  return !rn || i2c_read_timeout_us(i2c0, addr, read, rn, false, 3000) == (int)rn;
}
void board_idle(bool awake) {
  if (awake && !timer_running)
    timer_running = add_repeating_timer_ms(-1, wake_tick, NULL, &wake_timer);
  else if (!awake && timer_running) {
    cancel_repeating_timer(&wake_timer);
    timer_running = false;
  }
  // USB remains clocked and its IRQ wakes the CPU on resume. No timer ticks or
  // encoder PIO run during suspend; actual suspend current needs measurement.
  // Do not sleep over an event queued by the USB ISR just before WFI. With
  // interrupts masked, a newly pending IRQ wakes WFI and is serviced on restore.
  uint32_t interrupts = save_and_disable_interrupts();
  if (!tud_task_event_ready()) __wfi();
  restore_interrupts(interrupts);
}
void board_lcd_signal(LcdSignal signal, bool high) { gpio_put(lcd_pins[signal], high); }
void board_lcd_setup(void) {
  for (unsigned i = 0; i < 4; i++) {
    gpio_init(lcd_pins[i]);
    gpio_put(lcd_pins[i], i == LCD_SELECT);
    gpio_set_dir(lcd_pins[i], GPIO_OUT);
  }
  spi_init(spi0, BOARD_SPI_HZ);
  spi_set_format(spi0, 8, SPI_CPOL_0, SPI_CPHA_0, SPI_MSB_FIRST);
  gpio_set_function(PIN_SPI_SCK, GPIO_FUNC_SPI);
  gpio_set_function(PIN_SPI_MOSI, GPIO_FUNC_SPI);
}
void board_lcd_shutdown(void) {
  spi_deinit(spi0);
  const uint pins[] = {PIN_LCD_RST, PIN_LCD_BL, PIN_LCD_CS, PIN_LCD_DC,
                       PIN_SPI_SCK, PIN_SPI_MOSI};
  for (unsigned i = 0; i < sizeof pins / sizeof *pins; i++) {
    gpio_init(pins[i]);
    gpio_put(pins[i], false);
    gpio_set_dir(pins[i], GPIO_OUT);
  }
}
bool board_lcd_byte(uint8_t value) {
  uint64_t deadline = time_us_64() + 100;
  while (!spi_is_writable(spi0)) if (time_us_64() >= deadline) return false;
  spi_get_hw(spi0)->dr = value;
  while (spi_is_readable(spi0)) (void)spi_get_hw(spi0)->dr;
  return true;
}
bool board_lcd_finish(void) {
  uint64_t deadline = time_us_64() + 1000;
  while (spi_is_busy(spi0)) if (time_us_64() >= deadline) return false;
  while (spi_is_readable(spi0)) (void)spi_get_hw(spi0)->dr;
  spi_get_hw(spi0)->icr = 1; // Clear receive overrun: display is write-only.
  return true;
}
