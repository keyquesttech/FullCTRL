/**
 * Minimal syscall stubs to satisfy newlib for bare-metal builds.
 *
 * These implementations are intentionally trivial and should be replaced
 * with proper semihosting or device-specific behaviour if needed. For the
 * firmware here, we avoid using stdio/heap, so these should never be
 * called in normal operation.
 */

#include <sys/stat.h>
#include <unistd.h>

int _close(int file) {
    (void)file;
    return -1;
}

int _fstat(int file, struct stat *st) {
    (void)file;
    if (st) {
        st->st_mode = S_IFCHR;
    }
    return 0;
}

int _isatty(int file) {
    (void)file;
    return 1;
}

int _lseek(int file, int ptr, int dir) {
    (void)file;
    (void)ptr;
    (void)dir;
    return 0;
}

int _read(int file, char *ptr, int len) {
    (void)file;
    (void)ptr;
    (void)len;
    return 0;
}

int _write(int file, char *ptr, int len) {
    (void)file;
    (void)ptr;
    return len;
}

void *_sbrk(ptrdiff_t incr) {
    (void)incr;
    return (void *)-1;
}

void _exit(int status) {
    (void)status;
    while (1) {
    }
}

int _kill(int pid, int sig) {
    (void)pid;
    (void)sig;
    return -1;
}

int _getpid(void) {
    return 1;
}

