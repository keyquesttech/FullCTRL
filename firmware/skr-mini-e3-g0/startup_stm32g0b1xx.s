    .syntax unified
    .cpu cortex-m0plus
    .thumb

    .global Reset_Handler
    .extern main

    .section .isr_vector, "a", %progbits
    .word   _estack
    .word   Reset_Handler

    .text
    .thumb_func
Reset_Handler:
    /* Simple C runtime init for .data/.bss could be added here. For now we
     * just jump straight to main(), which is sufficient for early bring-up.
     */
    bl      main

1:  b       1b

