// SPDX-License-Identifier: MIT
#pragma once
#include <stdbool.h>
#include <stdint.h>

typedef enum { LCD_RESET, LCD_BACKLIGHT, LCD_SELECT, LCD_DATA } LcdSignal;
void board_init(void);
uint32_t board_millis(void);
void board_delay_ms(uint32_t ms);
bool board_button_pressed(void);
void board_peripherals(bool enabled);
uint16_t board_encoder_count(void);
bool board_encoder_ok(void);
void board_idle(bool awake);
bool board_i2c_transfer(uint8_t addr, const uint8_t *write, unsigned wn,
                        uint8_t *read, unsigned rn);
void board_lcd_setup(void);
void board_lcd_shutdown(void);
void board_lcd_signal(LcdSignal signal, bool high);
bool board_lcd_byte(uint8_t value);
bool board_lcd_finish(void);
