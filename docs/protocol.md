# FullCTRL Host ↔ MCU Protocol (Initial Draft)

This document defines the initial protocol between the Raspberry Pi host
and the SKR-mini-E3-V3.0 firmware. It is intentionally compact and focused
on enabling:

- Reliable configuration exchange.
- Streaming of motion blocks for printing.
- Real-time jog / velocity-mode control similar to Duet controllers.
- Periodic state updates for the web UI.

## Transport

- Physical link: USB CDC (virtual serial port).
- Encoding: binary frames.
- Endianness: little-endian for all multi-byte integer fields.

### Frame layout

Each frame has the following layout:

```text
Offset  Size  Field
0       2     Sync bytes (0xAA, 0x55)
2       1     Version (currently 0x01)
3       1     Message type (see below)
4       2     Sequence number (host-assigned, wraps around)
6       2     Payload length in bytes (N)
8       N     Payload
8 + N   2     CRC16-CCITT over bytes [2 .. 7 + N]
```

The MCU must validate:
- Sync bytes.
- Version (unknown versions may be rejected with an error).
- CRC16 before accepting a frame.

The host treats sequence numbers as best-effort; some message types may not
require acknowledgements.

## Message types

The `message_type_t` enum in firmware code mirrors the following values:

- `0x01` – `CONFIG_SET`
- `0x02` – `CONFIG_GET`
- `0x03` – `MOVE_BLOCK`
- `0x04` – `SET_HEATER`
- `0x05` – `SET_FAN`
- `0x06` – `SET_PIN`
- `0x07` – `QUERY_STATE`
- `0x08` – `STATE_UPDATE`
- `0x09` – `ERROR`
- `0x0A` – `RT_SET_VELOCITY`
- `0x0B` – `RT_STOP_MOTION`

The host and MCU share a simple rule:
- Messages with type `RT_*` are treated as **high priority** and should be
  executed as soon as possible, even if normal motion blocks are queued.

## Selected payload formats

All payloads are binary and packed without padding; field sizes are fixed.

### CONFIG_SET (0x01)

Configuration is sent from the host as small, self-contained records so that
updating a single axis or heater does not require resending everything.

```text
u8  config_group   # 0 = axis, 1 = heater, 2 = endstop, 3 = fan
u8  index          # axis index (0=X,1=Y,2=Z,3=E0), heater index, etc.
u8  field_id       # meaning depends on group
u8  reserved
u32 value_u32      # interpretation depends on field_id
```

For example, an axis steps/mm field could be encoded as fixed-point Q16.16
in `value_u32`.

The first implementation only needs a small subset of fields (e.g. steps/mm,
max feedrate, pin assignments), and more can be added as needed.

### MOVE_BLOCK (0x03)

Move blocks represent short segments of motion planned by the host. For the
initial draft, a move block can be described by per-axis deltas and a target
feedrate:

```text
u16 block_id       # host-chosen, for diagnostics
u16 flags          # bit0: relative/absolute, others reserved
i32 dx_steps
i32 dy_steps
i32 dz_steps
i32 de_steps
u32 feedrate_mm_min_q16_16
u32 nominal_accel_mm_s2_q16_16
```

The MCU converts step deltas and feedrate into timer periods and schedules
the stepper ISRs accordingly. Multiple blocks may be queued, but the host
should keep the queue shallow to allow interruption.

### RT_SET_VELOCITY (0x0A)

Real-time velocity mode for jogging and responsive manual control. The host
emits frequent `RT_SET_VELOCITY` frames while the user holds a jog button.
If frames stop arriving, the MCU times out and stops motion.

```text
u16 rt_source_id   # identifies the controlling client/source
u16 timeout_ms     # if no update in this time, stop motion
i32 vx_mm_s_q16_16
i32 vy_mm_s_q16_16
i32 vz_mm_s_q16_16
i32 ve_mm_s_q16_16
u32 max_accel_mm_s2_q16_16
```

The MCU ramps towards the requested velocity vector subject to acceleration
limits. When the host or UI stops sending commands (button released), the
MCU will see the timeout expire and automatically bring velocity to zero.

### RT_STOP_MOTION (0x0B)

Explicit “stop” command for a real-time source:

```text
u16 rt_source_id
u16 reserved
```

On receipt, the MCU smoothly decelerates all axes to a stop as quickly as
allowed by configured acceleration limits.

### STATE_UPDATE (0x08)

Periodic updates from MCU to host:

```text
u8  status         # enum: 0=idle,1=printing,2=paused,3=error
u8  reserved0
u16 reserved1
i32 x_pos_mm_q16_16
i32 y_pos_mm_q16_16
i32 z_pos_mm_q16_16
i32 e_pos_mm_q16_16
u16 hotend_temp_c_x100
u16 bed_temp_c_x100
u16 hotend_target_c_x100
u16 bed_target_c_x100
u32 error_flags
```

The host uses these to update `PrinterStateManager` and forward telemetry to
web clients via WebSocket.

## Error handling

If the MCU encounters invalid frames, CRC mismatches, or unsupported message
types, it should:

- Discard the offending frame.
- Optionally emit an `ERROR` message with:

```text
u8  error_code
u8  reserved0
u16 reserved1
u32 detail
```

The host logs these and may surface more descriptive messages in the web UI.

