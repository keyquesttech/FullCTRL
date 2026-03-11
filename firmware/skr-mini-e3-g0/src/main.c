#include <stdint.h>

#include "board_pins.h"
#include "protocol.h"

/**
 * Entry point for the SKR-mini-E3-V3.0 firmware.
 *
 * At this stage the file serves primarily as a placeholder illustrating the
 * intended structure. Hardware initialisation, USB CDC bring-up, and the
 * command dispatch loop will be added as the low-level work progresses.
 */
int main(void) {
    (void)PIN_X_STEP;
    (void)MSG_CONFIG_SET;

    while (1) {
        /* TODO: poll USB CDC, parse frames, execute commands, update timers. */
    }

    return 0;
}

