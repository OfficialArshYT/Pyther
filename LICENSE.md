# Pyther Engine v1.0.8

An bare-metal 64-bit operating system framework and transpiler pipeline. Pyther Engine allows developers to write high-performance x86_64 system interfaces, desktop suites, and graphical games entirely in imperative Python logic by parsing scripts through an Abstract Syntax Tree (AST) compiler.

## Core Features
* **Bare-Metal Python Execution:** Write regular Python logic inside `kernel.py` and transpile it directly into standalone, natively compilable 64-bit C code.
* **Master Workspace Desktop OS:** Includes a fully functional operational desktop interface featuring built-in user utilities (Calculator, Notepad), system diagnostics (Memory Scan, System Information), graphics suite tests, and an integrated grid-based game (*Apple Collector*).
* **Proportional Vector Typography:** Custom high-definition 1:2 Golden Ratio mathematical font engine maps the full US/UK keyboard symbol layout natively to raw screen coordinates.
* **Dynamic Hardware Alignment:** Viewport kerning calculations dynamically query the motherboard's active Graphics Output Protocol (GOP) screen resolution values for absolute dead-center text alignment.
* **AST-Optimized Game Engine Logic:** Designed for strict imperative execution with dedicated key-value processing, dynamic digit extraction, and boundary collision handling without fallthrough logic.
* **Stable Assembly Shims:** Hand-written 16-byte aligned assembly landing shims prevent stack alignment exceptions across virtual hypervisors and real hardware.

## Prerequisite Toolchain
Ensure the following packages are globally installed and accessible via your local MSYS2 / UCRT64 shell workspace path environment variables:
* **Python 3.8+** (for parsing abstract semantic syntax blocks)
* **NASM** (Netwide Assembler for handling entry shims)
* **x86_64-w64-mingw32-gcc** (GNU Cross-compiler toolchain)
* **mtools** (`mformat`, `mmd`, `mcopy` for FAT32 disk volume construction)

## Usage Instruction Row
To compile your custom workspace code directly into a bootable partition drive image, execute the master builder script from your terminal:
```bash
python build.py
```

To test and execute your finished `pyther_fat.img` sector file within the QEMU hypervisor suite, launch the boot wrapper:
```bash
qemu-system-x86_64 \
  -# Note: Update path to edk2-x86_64-code.fd based on your local MSYS2/QEMU installation
qemu-system-x86_64 \
  -drive "if=pflash,format=raw,readonly=on,file=/path/to/edk2-x86_64-code.fd" \
  -drive "file=pyther_fat.img,format=raw" \
  -vga std
```

## Author & Credits
* **Developer:** Arsh
* **GitHub:** [@OfficialArshYT](https://github.com/OfficialArshYT)
* **YouTube:** [@OfficialArsh.](https://www.youtube.com/@OfficialArsh.)

## License & Copyright

**Copyright (c) 2026 Arsh**  
YouTube: [@OfficialArsh.](https://www.youtube.com/@OfficialArsh.)  
GitHub: [@OfficialArshYT](https://github.com/OfficialArshYT)  

### Custom License Terms

1. **ALL RIGHTS RESERVED (CORE ENGINE & DRIVERS)**  
   All source code, assembly modules, C drivers, headers, font binaries, build configs, and underlying engine logic outside of `kernel.py` and `build.py` are **All Rights Reserved**. You MAY NOT modify, reverse-engineer, redistribute, re-license, or claim ownership over any part of the core engine.

2. **PERMITTED MODIFICATIONS (`kernel.py` & `build.py`)**  
   You are permitted to view, edit, and modify `kernel.py` and `build.py` strictly for writing applications, games, and UI components to run on top of the Pyther Engine platform.

3. **COMMERCIAL USE RESTRICTIONS**  
   Commercial use, monetization, sublicensing, or paid distribution of Pyther Engine or any project built using Pyther Engine is strictly prohibited without explicit written permission and a signed agreement from Arsh.

4. **MANDATORY ATTRIBUTION & DISTRIBUTION**  
   Any public showcase, fork, or distribution featuring projects built with Pyther Engine MUST:
   - Include prominent credit to **Arsh** as the original framework creator.
   - Include links to YouTube (`@OfficialArsh.`) and GitHub (`@OfficialArshYT`).
   - Retain this exact license and copyright notice in full without alteration.
