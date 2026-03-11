cmake_minimum_required(VERSION 3.16)
project(fullctrl_skr_mini_e3_g0 C CXX ASM)

set(CMAKE_C_STANDARD 11)

# Placeholder CMake file for the STM32G0B1-based SKR-mini-E3-V3.0 firmware.
# Toolchain configuration, startup files, linker scripts, and HAL sources
# will be added as the low-level bring-up progresses.

add_executable(fullctrl_skr_mini_e3_g0
    src/main.c
)

target_include_directories(fullctrl_skr_mini_e3_g0 PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)

