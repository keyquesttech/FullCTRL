#!/usr/bin/env bash
set -euo pipefail

# Simple helper to configure and build the SKR-mini-E3-V3.0 firmware using cmake.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FW_DIR="${ROOT_DIR}/firmware/skr-mini-e3-g0"
BUILD_DIR="${FW_DIR}/build"

mkdir -p "${BUILD_DIR}"
cmake -S "${FW_DIR}" -B "${BUILD_DIR}" -DCMAKE_TOOLCHAIN_FILE="${FW_DIR}/toolchain-arm-none-eabi.cmake"
cmake --build "${BUILD_DIR}"

echo "Firmware build complete. Output is in: ${BUILD_DIR}"

