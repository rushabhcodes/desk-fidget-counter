// SPDX-License-Identifier: MIT
#include "button.h"
#include <assert.h>
#include <stdio.h>

int main(void) {
  ButtonState b = {0};
  assert(button_update(&b,false,true,0)==BUTTON_NONE);
  // Contact chatter must produce one short action, on release.
  assert(button_update(&b,true,true,10)==BUTTON_NONE);
  assert(button_update(&b,false,true,14)==BUTTON_NONE);
  assert(button_update(&b,true,true,18)==BUTTON_NONE);
  assert(button_update(&b,true,true,42)==BUTTON_NONE);
  assert(button_update(&b,true,true,43)==BUTTON_NONE);
  assert(button_update(&b,false,true,120)==BUTTON_NONE);
  assert(button_update(&b,true,true,124)==BUTTON_NONE);
  assert(button_update(&b,false,true,128)==BUTTON_NONE);
  assert(button_update(&b,false,true,153)==BUTTON_SHORT);
  assert(button_update(&b,false,true,200)==BUTTON_NONE);
  // A long hold clears once and never also changes mode on release.
  button_update(&b,true,true,1000); button_update(&b,true,true,1025);
  assert(button_hold_ms(&b,2025)==1000);
  assert(button_update(&b,true,true,4024)==BUTTON_NONE);
  assert(button_update(&b,true,true,4025)==BUTTON_LONG);
  assert(button_update(&b,true,true,9000)==BUTTON_NONE);
  button_update(&b,false,true,9010);
  assert(button_update(&b,false,true,9035)==BUTTON_NONE);
  // A release immediately before the long threshold must not clear the count.
  button_update(&b,true,true,10000); button_update(&b,true,true,10025);
  assert(button_update(&b,false,true,13024)==BUTTON_NONE);
  assert(button_update(&b,false,true,13025)==BUTTON_NONE);
  assert(button_update(&b,false,true,13049)==BUTTON_SHORT);
  // Startup/resume with the button held cannot trigger any action.
  button_update(&b,false,false,14000);
  assert(button_update(&b,true,true,15000)==BUTTON_NONE);
  assert(button_update(&b,true,true,20000)==BUTTON_NONE);
  button_update(&b,false,true,20001);
  assert(button_update(&b,false,true,20026)==BUTTON_NONE);
  button_update(&b,true,true,21000); button_update(&b,true,true,21025);
  button_update(&b,false,true,21100);
  assert(button_update(&b,false,true,21125)==BUTTON_SHORT);
  // Millisecond rollover does not shorten or repeat a hold.
  b=(ButtonState){0}; button_update(&b,false,true,UINT32_MAX-100);
  button_update(&b,true,true,UINT32_MAX-90);
  button_update(&b,true,true,UINT32_MAX-65);
  assert(button_update(&b,true,true,2933)==BUTTON_NONE);
  assert(button_update(&b,true,true,2934)==BUTTON_LONG);
  puts("Button: debounced short press, single long press, release boundary, boot/resume hold and timer rollover passed");
}
