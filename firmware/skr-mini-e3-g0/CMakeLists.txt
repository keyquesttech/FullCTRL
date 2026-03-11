cmake_minimum_required(VERSION 3.16)
project(fullctrl_skr_mini_e3_g0 C CXX ASM)

set(CMAKE_C_STANDARD 11)

# Basic CMake skeleton for STM32G0B1-based SKR-mini-E3-V3.0 firmware.

add_executable(fullctrl_skr_mini_e3_g0
    startup_stm32g0b1xx.s
    src/main.c
    src/board.c
    src/syscalls.c
)

target_include_directories(fullctrl_skr_mini_e3_g0 PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)

target_compile_options(fullctrl_skr_mini_e3_g0 PRIVATE
    -mcpu=cortex-m0plus
    -mthumb
    -ffunction-sections
    -fdata-sections
)

target_link_options(fullctrl_skr_mini_e3_g0 PRIVATE
    -T${CMAKE_CURRENT_SOURCE_DIR}/stm32g0b1xx.ld
    -nostartfiles
    -Wl,--gc-sections
    -Wl,-Map=fullctrl_skr_mini_e3_g0.map
    -specs=nosys.specs
)

