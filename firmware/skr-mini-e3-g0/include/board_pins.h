/**
 * Logical-to-physical pin mapping for SKR-mini-E3-V3.0 (STM32G0B1).
 *
 * This header defines named constants for all critical peripherals:
 * steppers, heaters, thermistors, endstops, and fans.
 *
 * The values here are *logical* identifiers. The mapping from these values
 * to concrete STM32 GPIO ports/pins is implemented in board.c, allowing
 * host-side configuration or future variants without changing the rest of
 * the firmware.
 */

#pragma once

#include <stdint.h>

/* Logical pin identifiers. These are arbitrary 32-bit values; board.c is
 * responsible for turning them into concrete GPIO config. */

enum {
    /* Stepper drivers */
    PIN_X_STEP = 1,
    PIN_X_DIR,
    PIN_X_ENABLE,

    PIN_Y_STEP,
    PIN_Y_DIR,
    PIN_Y_ENABLE,

    PIN_Z_STEP,
    PIN_Z_DIR,
    PIN_Z_ENABLE,

    PIN_E0_STEP,
    PIN_E0_DIR,
    PIN_E0_ENABLE,

    /* Heaters and thermistors */
    PIN_HEATER_HOTEND,
    PIN_HEATER_BED,

    PIN_THERM_HOTEND,
    PIN_THERM_BED,

    /* Endstops */
    PIN_X_MIN,
    PIN_Y_MIN,
    PIN_Z_MIN,

    /* Fans */
    PIN_FAN_PART,
    PIN_FAN_CONTROLLER,
};


