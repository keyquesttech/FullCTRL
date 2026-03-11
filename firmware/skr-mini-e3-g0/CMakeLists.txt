cmake_minimum_required(VERSION 3.16)
project(fullctrl_skr_mini_e3_g0 C CXX ASM)

set(CMAKE_C_STANDARD 11)

# Basic CMake skeleton for STM32G0B1-based SKR-mini-E3-V3.0 firmware.
# You still need to provide:
# - A toolchain file that selects arm-none-eabi-gcc.
# - A startup file and linker script appropriate for STM32G0B1.

add_executable(fullctrl_skr_mini_e3_g0
    src/main.c
    src/board.c
)

target_include_directories(fullctrl_skr_mini_e3_g0 PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)


