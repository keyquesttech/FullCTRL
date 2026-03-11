#!/usr/bin/env bash
set -euo pipefail

# Flash the built firmware to the SKR-mini-E3-V3.0 via DFU, similar to how
# Marlin/Klipper flows work.
#
# Usage:
#   1. Build firmware:
#        ./scripts/build_firmware.sh
#   2. Put the SKR into DFU mode (BOOT0+RESET, or via dedicated buttons).
#   3. Flash:
#        ./scripts/flash_firmware.sh
#
# This assumes dfu-util is installed (install.sh takes care of that).

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FW_BUILD_DIR="${ROOT_DIR}/firmware/skr-mini-e3-g0/build"
BIN="${FW_BUILD_DIR}/fullctrl_skr_mini_e3_g0.bin"

if [ ! -f "${BIN}" ]; then
  echo "Firmware binary not found at ${BIN}"
  echo "Run ./scripts/build_firmware.sh first."
  exit 1
fi

echo "Flashing firmware to STM32 at 0x08000000..."
sudo dfu-util -a 0 -s 0x08000000:leave -D "${BIN}"

echo "Flash complete. Power-cycle or reset the SKR to run the new firmware."

