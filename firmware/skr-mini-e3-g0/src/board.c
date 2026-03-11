/**
 * Board support implementation for SKR-mini-E3-V3.0 (STM32G0B1).
 *
 * This file currently provides very small stubs for board initialisation and
 * logical pin control. The actual STM32 register-level code needs to be
 * filled in once the reference manual and board schematic are at hand.
 */

#include "board.h"
#include "board_pins.h"

void board_init(void) {
    /* TODO: configure system clock, GPIO modes, USB, timers, etc. */
}

void board_pin_set(uint32_t logical_pin) {
    (void)logical_pin;
    /* TODO: map logical_pin to GPIO port/pin and drive high. */
}

void board_pin_clear(uint32_t logical_pin) {
    (void)logical_pin;
    /* TODO: map logical_pin to GPIO port/pin and drive low. */
}

void board_pin_write(uint32_t logical_pin, int value) {
    if (value) {
        board_pin_set(logical_pin);
    } else {
        board_pin_clear(logical_pin);
    }
}

