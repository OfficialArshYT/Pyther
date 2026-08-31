[bits 32]
[extern _pyther_start]

global _start
_start:
    call _pyther_start
    cli
    hlt
    jmp $