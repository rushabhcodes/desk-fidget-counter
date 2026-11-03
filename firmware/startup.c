// SPDX-License-Identifier: MIT
#include <stdint.h>
extern uint32_t _estack, _sidata, _sdata, _edata, _sbss, _ebss;
extern int main(void);
void Reset_Handler(void) {
  uint32_t *s = &_sidata, *d = &_sdata;
  while (d < &_edata)
    *d++ = *s++;
  for (d = &_sbss; d < &_ebss;)
    *d++ = 0;
  (void)main();
  while (1) {
  }
}
void Default_Handler(void) {
  while (1) {
  }
}
void SysTick_Handler(void);
void USB_IRQHandler(void);
__attribute__((section(".isr_vector"),
               used)) void (*const vectors[48])(void) = {
    [0] = (void (*)(void))&_estack, [1] = Reset_Handler,
    [2] = Default_Handler,          [3] = Default_Handler,
    [11] = Default_Handler,         [14] = Default_Handler,
    [15] = SysTick_Handler,         [16 ... 46] = Default_Handler,
    [47] = USB_IRQHandler};
