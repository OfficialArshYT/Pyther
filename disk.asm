BITS 16

load_pyther_kernel:
    mov bx, KERNEL_OFFSET   ; Read data straight into our target memory address
    mov dh, 15              ; Number of sectors to read (plenty of room for Python text!)
    mov ah, 0x02            ; BIOS read sector function
    mov al, dh
    mov ch, 0x00            ; Cylinder 0
    mov dh, 0x00            ; Head 0
    mov cl, 0x02            ; Start reading from sector 2 (right after bootloader)
    mov dl, [BOOT_DRIVE]    ; Select our boot drive
    int 0x13                ; Trigger BIOS disk interrupt
    ret