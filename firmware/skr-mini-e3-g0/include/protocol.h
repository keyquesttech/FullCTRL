/**
 * Host ↔ MCU protocol definitions (high level).
 *
 * The concrete framing and message layout is specified in docs/protocol.md.
 * This header provides enums and simple structs that mirror that document
 * so firmware code can work with strongly-typed message kinds.
 */

#pragma once

#include <stdint.h>

typedef enum {
    MSG_CONFIG_SET = 1,
    MSG_CONFIG_GET = 2,
    MSG_MOVE_BLOCK = 3,
    MSG_SET_HEATER = 4,
    MSG_SET_FAN = 5,
    MSG_SET_PIN = 6,
    MSG_QUERY_STATE = 7,
    MSG_STATE_UPDATE = 8,
    MSG_ERROR = 9,
    MSG_RT_SET_VELOCITY = 10,
    MSG_RT_STOP_MOTION = 11,
} message_type_t;

typedef struct {
    uint16_t length;
    uint8_t type;      /* message_type_t */
    uint8_t reserved;  /* padding / future use */
} message_header_t;

