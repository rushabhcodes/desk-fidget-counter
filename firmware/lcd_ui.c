// SPDX-License-Identifier: MIT
#include "counter.h"
#include "lcd.h"
#include <string.h>
#include <stdio.h>
// Original compact 5x7 bitmap alphabet, rows packed as five bits.
static const struct {
  char c;
  uint8_t rows[7];
} font[] = {
    {'0', {14, 17, 19, 21, 25, 17, 14}}, {'1', {4, 12, 4, 4, 4, 4, 14}},
    {'2', {14, 17, 1, 2, 4, 8, 31}},     {'3', {30, 1, 1, 14, 1, 1, 30}},
    {'4', {2, 6, 10, 18, 31, 2, 2}},     {'5', {31, 16, 16, 30, 1, 1, 30}},
    {'6', {14, 16, 16, 30, 17, 17, 14}}, {'7', {31, 1, 2, 4, 8, 8, 8}},
    {'8', {14, 17, 17, 14, 17, 17, 14}}, {'9', {14, 17, 17, 15, 1, 1, 14}},
    {'A', {14, 17, 17, 31, 17, 17, 17}}, {'B', {30, 17, 17, 30, 17, 17, 30}},
    {'C', {14, 17, 16, 16, 16, 17, 14}}, {'D', {30, 17, 17, 17, 17, 17, 30}},
    {'E', {31, 16, 16, 30, 16, 16, 31}}, {'F', {31, 16, 16, 30, 16, 16, 16}},
    {'G', {14, 17, 16, 23, 17, 17, 14}}, {'H', {17, 17, 17, 31, 17, 17, 17}},
    {'I', {14, 4, 4, 4, 4, 4, 14}},      {'K', {17, 18, 20, 24, 20, 18, 17}},
    {'W', {17, 17, 17, 21, 21, 21, 10}}, {'L', {16, 16, 16, 16, 16, 16, 31}},
    {'M', {17, 27, 21, 21, 17, 17, 17}}, {'N', {17, 25, 21, 19, 17, 17, 17}},
    {'O', {14, 17, 17, 17, 17, 17, 14}}, {'P', {30, 17, 17, 30, 16, 16, 16}},
    {'R', {30, 17, 17, 30, 20, 18, 17}}, {'S', {15, 16, 16, 14, 1, 1, 30}},
    {'T', {31, 4, 4, 4, 4, 4, 4}},       {'U', {17, 17, 17, 17, 17, 17, 14}},
    {'V', {17, 17, 17, 17, 17, 10, 4}},  {'Y', {17, 17, 10, 4, 4, 4, 4}},
    {':', {0, 6, 6, 0, 6, 6, 0}}, {'%', {17, 2, 4, 4, 8, 16, 17}},
    {'.', {0, 0, 0, 0, 0, 6, 6}},        {'-', {0, 0, 0, 31, 0, 0, 0}}};
static void text(uint16_t row[240], unsigned y, const char *s, unsigned top,
                 unsigned scale, uint16_t color) {
  if (y < top || y >= top + 7 * scale)
    return;
  int left = (240 - (int)strlen(s) * 6 * (int)scale + (int)scale) / 2;
  unsigned line = (y - top) / scale;
  for (unsigned i = 0; s[i]; i++) {
    uint8_t bits = 0;
    for (unsigned k = 0; k < sizeof(font) / sizeof(font[0]); k++)
      if (font[k].c == s[i]) {
        bits = font[k].rows[line];
        break;
      }
    for (unsigned col = 0; col < 5; col++)
      if (bits & (16u >> col))
        for (unsigned dx = 0; dx < scale; dx++) {
          int x = left + (int)(i * 6 * scale + col * scale + dx);
          if (x >= 0 && x < 240)
            row[x] = color;
        }
  }
}
void lcd_render_row(const LcdView *v, unsigned y, uint16_t row[240]) {
  const uint16_t bg=0x0863, white=0xe71c, gold=0xfdea, mint=0x6f39, red=0xfa88;
  for (unsigned x=0;x<240;x++) row[x]=bg;
  if (y>=240) return;
  bool live=dashboard_fresh(&v->host,v->now);
  char b[40];
  if (live) {
    unsigned yr,mo,day; dashboard_date(&v->host,v->now,&yr,&mo,&day);
    snprintf(b,sizeof b,"%04u-%02u-%02u",yr,mo,day);
  } else strcpy(b,"LAPTOP DASHBOARD");
  text(row,y,b,24,1,mint);
  if (live) {
    unsigned s=dashboard_seconds(&v->host,v->now);
    snprintf(b,sizeof b,"%02u:%02u:%02u",s/3600,s/60%60,s%60);
  } else strcpy(b,"--:--:--");
  text(row,y,b,42,3,gold);
  for (unsigned i=0;i<2;i++) {
    unsigned value=i?v->host.ram_tenths:v->host.cpu_tenths, top=83+i*29;
    if (live) snprintf(b,sizeof b,"%s %3u.%u%%",i?"RAM":"CPU",value/10,value%10);
    else snprintf(b,sizeof b,"%s  --.-%%",i?"RAM":"CPU");
    text(row,y,b,top,2,white);
    if (y>=top+17 && y<top+20)
      for (unsigned x=54;x<186;x++) row[x]=live && x-54<value*132/1000?mint:0x2188;
  }
  if (!live) strcpy(b,"HOST OFFLINE");
  else if (v->host.battery_percent<0) strcpy(b,"NO HOST BATTERY");
  else snprintf(b,sizeof b,"HOST %d%% %s",v->host.battery_percent,v->host.ac?"AC":"BAT");
  text(row,y,b,147,live && v->host.battery_percent<0?1:2,
       live && v->host.battery_percent>=0 && v->host.battery_percent<15 && !v->host.ac?red:white);
  text(row,y,"TURNS",175,1,mint);
  counter_format_total(v->turns,b);
  text(row,y,b,186,strlen(b)<=10?2:1,gold);
  text(row,y,!v->storage_ok?"RESET VIA USB":v->scroll_on?"SCROLL ON":"SCROLL OFF",
       210,1,!v->storage_ok?red:mint);
}
