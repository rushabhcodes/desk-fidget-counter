// SPDX-License-Identifier: MIT
// Minimal newlib support. The application uses snprintf, not host file I/O.
#include <errno.h>
#include <stddef.h>
#include <stdint.h>
#include <sys/stat.h>
#include <sys/types.h>
extern char end, _estack;
void *_sbrk(ptrdiff_t increment) {
  static char *top;
  if (!top)
    top = &end;
  char *previous = top;
  if (increment < 0 ||
      (uintptr_t)top + (uintptr_t)increment > (uintptr_t)&_estack - 2048u) {
    errno = ENOMEM;
    return (void *)-1;
  }
  top += increment;
  return previous;
}
int _close(int fd) {
  (void)fd;
  errno = EBADF;
  return -1;
}
int _fstat(int fd, struct stat *st) {
  if (fd < 0 || fd > 2) {
    errno = EBADF;
    return -1;
  }
  st->st_mode = S_IFCHR;
  return 0;
}
int _isatty(int fd) { return fd >= 0 && fd <= 2; }
off_t _lseek(int fd, off_t offset, int whence) {
  (void)fd;
  (void)offset;
  (void)whence;
  errno = ESPIPE;
  return -1;
}
ssize_t _read(int fd, void *p, size_t n) {
  (void)fd;
  (void)p;
  (void)n;
  errno = ENOSYS;
  return -1;
}
ssize_t _write(int fd, const void *p, size_t n) {
  (void)fd;
  (void)p;
  (void)n;
  errno = ENOSYS;
  return -1;
}
int _getpid(void) { return 1; }
int _kill(int pid, int sig) {
  (void)pid;
  (void)sig;
  errno = EINVAL;
  return -1;
}
void _exit(int status) {
  (void)status;
  for (;;) {
  }
}
