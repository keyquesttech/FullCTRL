/**
 * High-level board initialisation and peripheral control APIs.
 *
 * This header provides a small abstraction layer over the STM32G0B1 MCU so
 * other modules (motion engine, heaters, fans) can be written without
 * depending directly on register-level details.
 *
 * Hardware-specific implementation will be provided in board.c.
 */

#pragma once

#include <stdint.h>

void board_init(void);

/* Basic GPIO control helpers for logical pins as defined in board_pins.h. */
void board_pin_set(uint32_t logical_pin);
void board_pin_clear(uint32_t logical_pin);
void board_pin_write(uint32_t logical_pin, int value);

