# Pyther Engine v1.1.5

An open-source, bare-metal 64-bit operating system framework and transpiler pipeline. Pyther Engine allows developers to write high-performance x86_64 system interfaces, desktop suites, and graphical games entirely in imperative Python logic by parsing scripts through an Abstract Syntax Tree (AST) compiler.

## Core Features
* **Bare-Metal Python Execution:** Write regular Python logic inside `kernel.py` and transpile it directly into standalone, natively compilable 64-bit C code.
* **Master Workspace Desktop OS:** Includes a fully functional operational desktop interface featuring built-in user utilities (Calculator, Notepad), system diagnostics (Memory Scan, System Information), graphics suite tests, and an integrated grid-based game (*Apple Collector*).
* **Proportional Vector Typography:** Custom high-definition 1:2 Golden Ratio mathematical font engine maps the full US/UK keyboard symbol layout natively to raw screen coordinates.
* **Dynamic Hardware Alignment:** Viewport kerning calculations dynamically query the motherboard's active Graphics Output Protocol (GOP) screen resolution values for absolute dead-center text alignment.
* **AST-Optimized Game Engine Logic:** Designed for strict imperative execution with dedicated key-value processing, dynamic digit extraction, and boundary collision handling without fallthrough logic.
* **Stable Assembly Shims:** Hand-written 16-byte aligned assembly landing shims prevent stack alignment exceptions across virtual hypervisors and real hardware.

## Project Structure
```text
1.1.5/
├── fonts/               # Local typographic asset binaries
├── system/              # Temporary generated C and intermediate link targets
├── build.py             # Main AST node translation compiler script
├── entry.asm            # 16-bit stack aligner assembly landing frame
├── kernel_entry.c       # Unified global UEFI context header template
└── kernel.py            # Active Python developer workspace loop script (Desktop OS & Applications)
```

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
  -drive "if=pflash,format=raw,readonly=on,file=C:/msys64/ucrt64/share/qemu/edk2-x86_64-code.fd" \
  -drive "file=pyther_fat.img,format=raw" \
  -vga std
```

## Author & Credits
* **Developer:** Arsh
* **GitHub:** [@OfficialArshYT](https://github.com/OfficialArshYT)
* **YouTube:** [@OfficialArsh.](https://www.youtube.com/@OfficialArsh.)

## License
MIT License

Copyright (c) 2026 Arsh
GitHub: https://github.com/OfficialArshYT
YouTube: https://www.youtube.com/@OfficialArsh.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
