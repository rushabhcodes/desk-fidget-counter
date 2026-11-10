// SPDX-License-Identifier: MIT
#include "counter.h"
#include "button.h"
#include "lcd.h"
#include "board.h"
#include "tusb.h"
#include <stdio.h>
#include <string.h>
static uint32_t ticks;
static Counter counter;
static bool stored = false, encoder_ok = true, peripherals_on = false;
static Dashboard dashboard;
static uint32_t cleared_at;
static bool clear_notice;
static unsigned active_slot = 0;
static uint32_t sequence = 0;
uint32_t tusb_time_millis_api(void) { return board_millis(); }
static void delay_ms(uint32_t n) { board_delay_ms(n); ticks = board_millis(); }
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
static bool transfer(unsigned addr, const uint8_t *w, unsigned wn, uint8_t *r, unsigned rn) {
  return board_i2c_transfer((uint8_t)addr, w, wn, r, rn);
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
      "{\"device\":\"desk-fidget-counter\",\"protocol\":1,\"firmware\":\"6.0.0\","
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
        reply("Desk Knob RP2040 F1 / firmware 6.0.0 / TinyUSB 0.21.0\r\n");
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
  board_init();
  delay_ms(50);
  restore();
  tusb_rhport_init_t cfg = {.role = TUSB_ROLE_DEVICE, .speed = TUSB_SPEED_FULL};
  tusb_init(0, &cfg);
  uint32_t sample_at = ticks;
  bool scroll_mode = false; // Safe power-on default: count without host scrolling.
  ButtonState mode_button = {0};
  while (1) {
    tud_task_ext(0, false); // Cooperative loop: never wait for another USB packet.
    ticks = board_millis();
    uint32_t now = ticks;
    bool awake = tud_mounted() && !tud_suspended();
    if (awake != peripherals_on) {
      clear_motion();
      counter.progress=0; // Cannot infer turns made while the optical LED is off.
      if (awake) {
        board_peripherals(true);
        ticks = board_millis();
        lcd_power(true,ticks);
      } else {
        lcd_power(false,now); // All LCD signal pins low before removing its rail
        board_peripherals(false);
      }
      peripherals_on=awake;
    }
    ButtonEvent event = button_update(&mode_button, board_button_pressed(), awake, now);
    if (event == BUTTON_SHORT) {
      scroll_mode = !scroll_mode;
      counter.pending = 0;
      counter.scroll_fraction = 0; // Preserve partial-turn counting across mode changes.
    } else if (event == BUTTON_LONG) {
      reset_count();
    }
    if ((uint32_t)(now - sample_at) >= 2) {
      sample_at = now;
      uint16_t raw = board_encoder_count();
      encoder_ok = board_encoder_ok();
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
    ticks=board_millis();
    now=ticks; // FRAM/console work can advance time before the UI snapshot.
    if (clear_notice && (uint32_t)(now-cleared_at)>=2000) clear_notice=false;
    LcdView view = {.turns=counter.turns,.host=dashboard,.now=now,
                    .storage_ok=stored,.scroll_on=scroll_mode,.usb_ready=awake,
                    .encoder_ok=encoder_ok,.hold_ms=button_hold_ms(&mode_button,now),
                    .count_cleared=clear_notice && (uint32_t)(now-cleared_at)<2000};
    if (peripherals_on) lcd_task(now,&view);
    board_idle(awake);
  }
}
