// SPDX-License-Identifier: MIT
#include "stm32f0xx.h"
#include "tusb.h"
#include <string.h>
// TinyUSB's example VID/PID are development identifiers, not a purchased
// production VID.
#ifndef USB_VID
#define USB_VID 0xcafe
#endif
#ifndef USB_PID
#define USB_PID 0x4011
#endif
static const tusb_desc_device_t device = {.bLength = sizeof(tusb_desc_device_t),
                                          .bDescriptorType = TUSB_DESC_DEVICE,
                                          .bcdUSB = 0x0200,
                                          .bDeviceClass = TUSB_CLASS_MISC,
                                          .bDeviceSubClass =
                                              MISC_SUBCLASS_COMMON,
                                          .bDeviceProtocol = MISC_PROTOCOL_IAD,
                                          .bMaxPacketSize0 = 64,
                                          .idVendor = USB_VID,
                                          .idProduct = USB_PID,
                                          .bcdDevice = 0x0500,
                                          .iManufacturer = 1,
                                          .iProduct = 2,
                                          .iSerialNumber = 3,
                                          .bNumConfigurations = 1};
uint8_t const *tud_descriptor_device_cb(void) {
  return (uint8_t const *)&device;
}
static uint8_t const hid_report[] = {TUD_HID_REPORT_DESC_MOUSE()};
uint8_t const *tud_hid_descriptor_report_cb(uint8_t instance) {
  (void)instance;
  return hid_report;
}
#define CONFIG_LEN (TUD_CONFIG_DESC_LEN + TUD_CDC_DESC_LEN + TUD_HID_DESC_LEN)
static uint8_t const config[] = {
    TUD_CONFIG_DESCRIPTOR(1, 3, 0, CONFIG_LEN,
                          0, 100),
    TUD_CDC_DESCRIPTOR(0, 4, 0x81, 8, 0x02, 0x82, 64),
    TUD_HID_DESCRIPTOR(2, 5, HID_ITF_PROTOCOL_MOUSE, sizeof(hid_report), 0x83,
                       16, 1)};
uint8_t const *tud_descriptor_configuration_cb(uint8_t index) {
  (void)index;
  return config;
}
uint16_t const *tud_descriptor_string_cb(uint8_t index, uint16_t lang) {
  (void)lang;
  static uint16_t out[64];
  const char *s = "";
  static char serial[25];
  if (index == 0) {
    out[0] = (TUSB_DESC_STRING << 8) | 4;
    out[1] = 0x0409;
    return out;
  }
  if (index == 1)
    s = "rushabhcodes";
  else if (index == 2)
    s = "Desk Fidget Counter";
  else if (index == 4)
    s = "Dashboard and Count";
  else if (index == 5)
    s = "Scroll Wheel";
  else if (index == 3) {
    const uint8_t *uid = (const uint8_t *)UID_BASE;
    const char *h = "0123456789ABCDEF";
    for (int i = 0; i < 12; i++) {
      serial[i * 2] = h[uid[i] >> 4];
      serial[i * 2 + 1] = h[uid[i] & 15];
    }
    serial[24] = 0;
    s = serial;
  } else
    return NULL;
  unsigned n = strlen(s);
  if (n > 63)
    n = 63;
  for (unsigned i = 0; i < n; i++)
    out[i + 1] = (uint8_t)s[i];
  out[0] = (uint16_t)((TUSB_DESC_STRING << 8) | (2 * n + 2));
  return out;
}
uint16_t tud_hid_get_report_cb(uint8_t i, uint8_t id, hid_report_type_t t,
                               uint8_t *b, uint16_t n) {
  (void)i;
  (void)id;
  (void)t;
  (void)b;
  (void)n;
  return 0;
}
void tud_hid_set_report_cb(uint8_t i, uint8_t id, hid_report_type_t t,
                           uint8_t const *b, uint16_t n) {
  (void)i;
  (void)id;
  (void)t;
  (void)b;
  (void)n;
}
