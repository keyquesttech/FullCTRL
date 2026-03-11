## Firmware – SKR-mini-E3-V3.0

This directory contains the firmware for the SKR-mini-E3-V3.0 (STM32G0B1)
controller board. The firmware is designed to work as a thin, real-time
executor for commands sent by the Raspberry Pi host.

### Flashing via SD card

1. **Build** (on the Pi or your dev machine):
   ```bash
   cd ~/FullCTRL
   ./scripts/build_firmware.sh
   ```
2. Copy **`firmware/skr-mini-e3-g0/build/firmware.bin`** to the **root** of a FAT32-formatted SD card (the same card the printer uses, or any SD card the SKR can read).
3. **Power off** the SKR, insert the SD card, then **power on**. The board’s built-in bootloader will detect `firmware.bin`, flash the MCU, and then reboot. The SD card can be removed after a successful flash.

No USB DFU or `dfu-util` is required when using this method.

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

