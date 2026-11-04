// SPDX-License-Identifier: MIT
#include "dashboard.h"
#include <string.h>
static unsigned days(unsigned y, unsigned m) {
  static const unsigned n[] = {31,28,31,30,31,30,31,31,30,31,30,31};
  return n[m-1] + (m == 2 && y % 4 == 0 && (y % 100 != 0 || y % 400 == 0));
}
static bool number(const char **p, unsigned *out, unsigned digits, char sep) {
  unsigned v=0,n=0;
  while (**p>='0' && **p<='9' && n<digits) { v=v*10+(unsigned)(*(*p)++-'0'); n++; }
  if (!n || **p!=sep) return false;
  *out=v; if(sep) (*p)++; return true;
}
bool dashboard_receive(Dashboard *d, const char *line, uint32_t now) {
  if (strlen(line)>60 || strncmp(line,"DASH ",5)) return false;
  const char *p=line+5; unsigned h,m,s,y,mo,day,cpu,ram,battery,ac;
  if (!number(&p,&h,2,':') || !number(&p,&m,2,':') || !number(&p,&s,2,' ') ||
      !number(&p,&y,4,'-') || !number(&p,&mo,2,'-') || !number(&p,&day,2,' ') ||
      !number(&p,&cpu,4,' ') || !number(&p,&ram,4,' ')) return false;
  bool missing=!strncmp(p,"-1 ",3);
  if (missing) { battery=0; p+=3; }
  else if (!number(&p,&battery,3,' ')) return false;
  if (!number(&p,&ac,1,0) || h>23 || m>59 || s>59 || y<2020 || y>9999 ||
      mo<1 || mo>12 || day<1 || day>days(y,mo) || cpu>1000 || ram>1000 ||
      battery>100 || ac>1) return false;
  *d=(Dashboard){.seconds=h*3600+m*60+s,.year=y,.month=mo,.day=day,
      .cpu_tenths=cpu,.ram_tenths=ram,.battery_percent=missing?-1:(int)battery,.ac=ac,
      .received=true,.received_at=now};
  return true;
}
bool dashboard_fresh(const Dashboard *d, uint32_t now) {
  return d->received && (uint32_t)(now-d->received_at)<5000;
}
unsigned dashboard_seconds(const Dashboard *d, uint32_t now) {
  return (d->seconds+(uint32_t)(now-d->received_at)/1000)%86400;
}
void dashboard_date(const Dashboard *d, uint32_t now, unsigned *year, unsigned *month, unsigned *day) {
  *year=d->year; *month=d->month; *day=d->day;
  // Called only on fresh samples; at most one midnight has elapsed.
  if (dashboard_fresh(d,now) && dashboard_seconds(d,now)<d->seconds) {
    if (++*day>days(*year,*month)) {
      *day=1;
      if (++*month>12) { *month=1; ++*year; }
    }
  }
}
