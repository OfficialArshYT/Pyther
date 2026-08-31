[org 0x7c00]
BITS 16

; Where we want to temporarily load our Python engine code in RAM
KERNEL_OFFSET equ 0x1000

mov [BOOT_DRIVE], dl        ; BIOS stores boot drive number in DL register on startup

; Setup Stack Space
mov bp, 0x9000
mov sp, bp

call load_pyther_kernel     ; Jump to our Diskloader routine
call switch_to_32bit        ; Turn on 32-bit mode

jmp $

%include "disk.asm"         ; Separate file we will make for disk operations

BITS 16
switch_to_32bit:
    cli
    lgdt [gdt_descriptor]
    mov eax, cr0
    or eax, 0x1
    mov cr0, eax
    jmp CODE_SEG:init_32bit

; ------ GDT Settings ------
gdt_start: dd 0x0, 0x0
gdt_code:  dw 0xffff, 0x0, 0x9a00, 0xcf
gdt_data:  dw 0xffff, 0x0, 0x9200, 0xcf
gdt_end:
gdt_descriptor:
    dw gdt_end - gdt_start - 1
    dd gdt_start
CODE_SEG equ gdt_code - gdt_start
DATA_SEG equ gdt_data - gdt_start

BITS 32
init_32bit:
    mov ax, DATA_SEG
    mov ds, ax
    mov ss, ax
    mov es, ax
    mov fs, ax
    mov gs, ax
    
    ; Jump straight into our loaded Python execution code space!
    jmp KERNEL_OFFSET

; Variables
BOOT_DRIVE db 0

times 510-($-$$) db 0
dw 0xaa55