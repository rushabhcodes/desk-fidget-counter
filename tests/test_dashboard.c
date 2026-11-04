// SPDX-License-Identifier: MIT
#include "dashboard.h"
#include <assert.h>
#include <stdio.h>
#include <string.h>
int main(void) {
  Dashboard d={0};
  assert(!dashboard_fresh(&d,0));
  assert(dashboard_receive(&d,"DASH 23:59:59 2028-02-29 1000 0 87 1",UINT32_MAX-500));
  assert(dashboard_seconds(&d,499)==0); // midnight and millisecond wrap
  unsigned y,m,day; dashboard_date(&d,499,&y,&m,&day);
  assert(y==2028 && m==3 && day==1);
  assert(dashboard_fresh(&d,4498));
  assert(!dashboard_fresh(&d,4499));
  Dashboard before=d;
  const char *bad[]={"DASH 24:00:00 2026-01-01 0 0 0 0",
    "DASH 00:00:00 2026-02-29 0 0 0 0","DASH 00:00:00 2026-04-31 0 0 0 0",
    "DASH 00:00:00 2026-00-01 0 0 0 0","DASH 00:00:00 2026-01-01 1001 0 0 0",
    "DASH 00:00:00 2026-01-01 0 1001 0 0","DASH 00:00:00 2026-01-01 0 0 -2 0",
    "DASH 00:00:00 2026-01-01 0 0 101 0","DASH 00:00:00 2026-01-01 0 0 0 2",
    "DASH 00:00:00 2026-01-01 0 0 0 0 extra","DASH 00:00:00 2026-01-01 -0 0 0 0",
    "DASH 00:00:00 2026-01-01 42949672960 0 0 0","DASH",""};
  for(unsigned i=0;i<sizeof bad/sizeof bad[0];i++) {
    assert(!dashboard_receive(&d,bad[i],42));
    assert(!memcmp(&d,&before,sizeof d));
  }
  assert(dashboard_receive(&d,"DASH 00:00:00 2026-11-04 0 1000 -1 0",5000));
  assert(d.battery_percent==-1 && d.ram_tenths==1000);
  puts("Dashboard: bounds, invalid dates, atomic rejection, missing battery, midnight and uptime wrap passed");
}
