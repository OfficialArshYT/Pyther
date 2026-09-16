# Pyther 1.0.8

A hobby x86 operating system framework powered by a custom Python AST-to-C transpiler engine and bare-metal drivers.

## What is this?
Pyther lets you write kernel logic in Python (`kernel.py`). The build engine (`build.py`) parses your Python AST, emits bare-metal C drivers combined with your translated code, and builds a bootable 32-bit OS image.

## Features
- Transpiles a subset of Python syntax into freestanding C.
- Bare-metal VGA text-mode graphics and PS/2 keyboard scancode drivers.
- Built-in API helpers: `os_clear`, `os_print`, `os_print_int`, `os_draw_box`, `os_backspace`, `os_read_char`, `os_read_int`.
- Demo suite included: Extended Calculator, Text Notepad, VGA Palette Demo, and In-OS Developer Guide.

## Quick Start

### Prerequisites
Install GCC (32-bit support), NASM, Python 3, and QEMU.

### Build & Run Command
```bash
python build.py && qemu-system-x86_64 -drive format=raw,file=pyther_os.img

```

## Author & Credits

* **Developer:** Arsh
* **GitHub:** [OfficialArshYT](https://github.com/OfficialArshYT)

* **YouTube:** [@OfficialArsh.](https://www.youtube.com/@OfficialArsh.)
## License

This project is licensed under the MIT License - see the [LICENSE](https://www.google.com/search?q=MIT-LICENSE) file for details.
