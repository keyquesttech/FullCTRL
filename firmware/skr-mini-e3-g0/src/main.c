#include <stdint.h>

#include "board.h"
#include "board_pins.h"
#include "protocol.h"

/**
 * Entry point for the SKR-mini-E3-V3.0 firmware.
 *
 * For now this performs board initialisation and then enters a simple loop.
 * USB CDC handling and protocol parsing will be added as low-level drivers
 * are implemented.
 */
int main(void) {
    board_init();

    (void)PIN_X_STEP;
    (void)MSG_CONFIG_SET;

    while (1) {
        /* TODO: poll USB CDC, parse frames, execute commands, update timers. */
    }

    return 0;
}
