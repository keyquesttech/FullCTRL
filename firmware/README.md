## Firmware – SKR-mini-E3-V3.0

This directory contains the firmware for the SKR-mini-E3-V3.0 (STM32G0B1)
controller board. The firmware is designed to work as a thin, real-time
executor for commands sent by the Raspberry Pi host.

### High-level structure

- `skr-mini-e3-g0/`
  - `src/` – application source files (C)
  - `include/` – public headers
  - `CMakeLists.txt` – build configuration for the firmware

The firmware is responsible for:

- Initialising clocks, timers, GPIO, USB CDC.
- Receiving framed packets from the host and dispatching them to:
  - Motion engine (step/dir outputs for steppers).
  - Heater and temperature control loops.
  - IO (endstops, fans, general-purpose pins).
- Periodically sending state updates back to the host.

