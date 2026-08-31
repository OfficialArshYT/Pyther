import os
import subprocess
import ast

print("==========================================")
print("    PYTHER ENGINE - FULL DRIVER CORE      ")
print("==========================================")

class PytherVisitor(ast.NodeVisitor):
    def __init__(self):
        self.c_code = []
        self.indent_level = 1
        self.declared_vars = set()

    def indent(self):
        return "    " * self.indent_level

    def visit_FunctionDef(self, node):
        if node.name == 'main':
            for stmt in node.body:
                self.visit(stmt)

    def visit_Expr(self, node):
        self.visit(node.value)

    def visit_Call(self, node):
        func_name = node.func.id
        args = []
        for arg in node.args:
            if isinstance(arg, ast.Constant):
                if isinstance(arg.value, str):
                    safe_str = arg.value.replace('\\', '\\\\').replace('\n', '\\n').replace('"', '\\"')
                    args.append(f'"{safe_str}"')
                else:
                    args.append(str(arg.value))
            elif isinstance(arg, ast.Name):
                args.append(arg.id)
        
        self.c_code.append(f"{self.indent()}{func_name}({', '.join(args)});\n")

    def visit_Assign(self, node):
        target = node.targets[0].id
        type_prefix = ""
        
        if target not in self.declared_vars:
            self.declared_vars.add(target)
            if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                if len(node.value.value) > 1:
                    type_prefix = "char* "
                else:
                    type_prefix = "char "
            else:
                type_prefix = "int "

        if isinstance(node.value, ast.Call):
            func_name = node.value.func.id
            args = []
            for arg in node.value.args:
                if isinstance(arg, ast.Constant):
                    if isinstance(arg.value, str):
                        safe_str = arg.value.replace('\\', '\\\\').replace('\n', '\\n').replace('"', '\\"')
                        args.append(f'"{safe_str}"')
                    else:
                        args.append(str(arg.value))
                elif isinstance(arg, ast.Name):
                    args.append(arg.id)
            self.c_code.append(f"{self.indent()}{type_prefix}{target} = {func_name}({', '.join(args)});\n")

        elif isinstance(node.value, ast.Constant):
            val = node.value.value
            if isinstance(val, bool):
                self.c_code.append(f"{self.indent()}{type_prefix}{target} = {1 if val else 0};\n")
            elif isinstance(val, str):
                if len(val) == 1:
                    escaped_c = repr(val)[1:-1]
                    self.c_code.append(f"{self.indent()}{type_prefix}{target} = '{escaped_c}';\n")
                else:
                    safe_str = val.replace('\\', '\\\\').replace('\n', '\\n').replace('"', '\\"')
                    self.c_code.append(f"{self.indent()}{type_prefix}{target} = \"{safe_str}\";\n")
            else:
                self.c_code.append(f"{self.indent()}{type_prefix}{target} = {val};\n")

        elif isinstance(node.value, ast.BinOp):
            left = node.value.left.id if isinstance(node.value.left, ast.Name) else str(node.value.left.value)
            right = node.value.right.id if isinstance(node.value.right, ast.Name) else str(node.value.right.value)
            
            op_symbol = '+'
            if isinstance(node.value.op, ast.Sub): op_symbol = '-'
            elif isinstance(node.value.op, ast.Mult): op_symbol = '*'
            elif isinstance(node.value.op, (ast.Div, ast.FloorDiv)): op_symbol = '/'
            
            self.c_code.append(f"{self.indent()}{type_prefix}{target} = {left} {op_symbol} {right};\n")

    def visit_While(self, node):
        if isinstance(node.test, ast.Compare):
            left = node.test.left.id
            right = node.test.comparators[0]
            right_val = right.id if isinstance(right, ast.Name) else str(right.value)
            op_symbol = '<' if isinstance(node.test.ops[0], ast.Lt) else '=='
            self.c_code.append(f"{self.indent()}while ({left} {op_symbol} {right_val}) {{\n")
        else:
            self.c_code.append(f"{self.indent()}while (1) {{\n")
            
        self.indent_level += 1
        for stmt in node.body:
            self.visit(stmt)
        self.indent_level -= 1
        self.c_code.append(f"{self.indent()}}}\n")

    def visit_If(self, node):
        left = node.test.left.id
        right = node.test.comparators[0]

        if isinstance(right, ast.Constant):
            if isinstance(right.value, str):
                escaped_c = repr(right.value)[1:-1]
                right_val = f"'{escaped_c}'"
            else:
                right_val = str(right.value)
        else:
            right_val = right.id

        self.c_code.append(f"{self.indent()}if ({left} == {right_val}) {{\n")
        self.indent_level += 1
        for stmt in node.body:
            self.visit(stmt)
        self.indent_level -= 1

        if node.orelse:
            if len(node.orelse) == 1 and isinstance(node.orelse[0], ast.If):
                self.c_code.append(f"{self.indent()}}} else ")
                saved_indent = self.indent_level
                self.indent_level = 0
                self.visit_If(node.orelse[0])
                self.indent_level = saved_indent
            else:
                self.c_code.append(f"{self.indent()}}} else {{\n")
                self.indent_level += 1
                for stmt in node.orelse:
                    self.visit(stmt)
                self.indent_level -= 1
                self.c_code.append(f"{self.indent()}}}\n")
        else:
            self.c_code.append(f"{self.indent()}}}\n")

# --- TRANSPILE KERNEL.PY ---
transpiled_user_code = ""

if os.path.exists("kernel.py"):
    with open("kernel.py", "r") as f:
        content = f.read().strip()
        if content:
            tree = ast.parse(content)
            visitor = PytherVisitor()
            visitor.visit(tree)
            transpiled_user_code = "".join(visitor.c_code)

if not transpiled_user_code.strip():
    transpiled_user_code = """
    os_print("======================================\\n");
    os_print("   PYTHER OS - READY FOR KERNEL.PY    \\n");
    os_print("======================================\\n\\n");
    os_print("No user application loaded.\\n");
    """

# Normalize loop terminations
transpiled_user_code = transpiled_user_code.replace("running = 0;\n", "break;\n")
transpiled_user_code = transpiled_user_code.replace("editing = 0;\n", "break;\n")

# --- BARE-METAL C DRIVERS ---
kernel_c_template = r"""// ==========================================
//        PYTHER ENGINE - C CORE DRIVERS
// ==========================================

static int screen_position = 0;
static int shift_pressed = 0;

static inline unsigned char inb(unsigned short port) {
    unsigned char result;
    __asm__ __volatile__("inb %1, %0" : "=a"(result) : "Nd"(port));
    return result;
}

static inline void outb(unsigned short port, unsigned char data) {
    __asm__ __volatile__("outb %0, %1" : : "a"(data), "Nd"(port));
}

void update_hardware_cursor() {
    unsigned short pos = screen_position / 2;
    outb(0x3D4, 0x0F);
    outb(0x3D5, (unsigned char)(pos & 0xFF));
    outb(0x3D4, 0x0E);
    outb(0x3D5, (unsigned char)((pos >> 8) & 0xFF));
}

void check_scroll() {
    if (screen_position >= 4000) {
        char* video_memory = (char*)0xb8000;
        for (int i = 0; i < 3840; i++) {
            video_memory[i] = video_memory[i + 160];
        }
        for (int i = 3840; i < 4000; i += 2) {
            video_memory[i] = ' ';
            video_memory[i + 1] = 0x0F;
        }
        screen_position = 3840;
    }
}

void os_clear() {
    char* video_memory = (char*)0xb8000;
    for (int i = 0; i < 4000; i += 2) {
        video_memory[i] = ' ';     
        video_memory[i+1] = 0x0F;  
    }
    screen_position = 0;
    update_hardware_cursor();
}

void os_print(char* text) {
    char* video_memory = (char*)0xb8000;
    int i = 0;
    while (text[i] != '\0') {
        check_scroll();
        if (text[i] == '\\' && text[i+1] == 'n') {
            int current_row_remainder = screen_position % 160;
            screen_position += (160 - current_row_remainder);
            i += 2; 
            check_scroll();
            continue;
        }
        if (text[i] == '\n') {
            int current_row_remainder = screen_position % 160;
            screen_position += (160 - current_row_remainder);
            i++;
            check_scroll();
            continue;
        }
        video_memory[screen_position] = text[i];
        video_memory[screen_position + 1] = 0x0F;
        screen_position += 2;
        i++;
    }
    update_hardware_cursor();
}

void os_print_char(char c) {
    char str[2] = {c, '\0'};
    os_print(str);
}

void os_print_int(int n) {
    char buf[16];
    int i = 0;
    if (n == 0) { os_print("0"); return; }
    if (n < 0) { os_print("-"); n = -n; }
    while (n > 0) {
        buf[i++] = (n % 10) + '0';
        n /= 10;
    }
    for (int j = 0; j < i / 2; j++) {
        char temp = buf[j];
        buf[j] = buf[i - 1 - j];
        buf[i - 1 - j] = temp;
    }
    buf[i] = '\0';
    os_print(buf);
}

void os_backspace() {
    if (screen_position >= 2) {
        screen_position -= 2;
        char* video_memory = (char*)0xb8000;
        video_memory[screen_position] = ' ';
        video_memory[screen_position + 1] = 0x0F;
        update_hardware_cursor();
    }
}

void os_draw_box(int row, int col, int width, int height, int color_code) {
    char* video_memory = (char*)0xb8000;
    for (int r = 0; r < height; r++) {
        for (int c = 0; c < width; c++) {
            int pos = ((row + r) * 80 + (col + c)) * 2;
            if (pos >= 0 && pos < 4000) {
                video_memory[pos] = ' ';
                video_memory[pos + 1] = (char)color_code;
            }
        }
    }
    screen_position = (row + height) * 160;
    update_hardware_cursor();
}

char os_read_char() {
    char kbd_map[128] = {
        0,  27, '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', '\b',
      '\t', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\n',
        0, 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', 39, '`',  0, '\\', 
        'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/',   0, '*',   0, ' '
    };

    char kbd_map_shift[128] = {
        0,  27, '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '\b',
      '\t', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '{', '}', '\n',
        0, 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ':', '"', '~',  0, '|', 
        'Z', 'X', 'C', 'V', 'B', 'N', 'M', '<', '>', '?',   0, '*',   0, ' '
    };

    while (inb(0x64) & 1) { inb(0x60); }

    while (1) {
        if (inb(0x64) & 0x01) {
            unsigned char scancode = inb(0x60);
            
            if (scancode == 0x2A || scancode == 0x36) { shift_pressed = 1; continue; }
            if (scancode == 0xAA || scancode == 0xB6) { shift_pressed = 0; continue; }

            if (!(scancode & 0x80)) {
                char c = shift_pressed ? kbd_map_shift[scancode] : kbd_map[scancode];
                if (c > 0) {
                    while (!(inb(0x64) & 1));
                    inb(0x60);
                    return c;
                }
            }
        }
    }
}

int os_read_int() {
    while (1) {
        char c = os_read_char();
        if (c >= '0' && c <= '9') {
            os_print_char(c);
            os_print("\n");
            return c - '0';
        }
    }
}

void pyther_start() {
    os_clear();
""" + transpiled_user_code + r"""
    while(1);
}
"""

with open("kernel_entry.c", "w") as c_file:
    c_file.write(kernel_c_template)

# --- BUILD PIPELINE ---
subprocess.run(["nasm", "-f", "bin", "boot.asm", "-o", "boot.bin"])
subprocess.run(["nasm", "-f", "elf32", "kernel_entry.asm", "-o", "kernel_entry.o"])
subprocess.run(["gcc", "-ffreestanding", "-Os", "-m32", "-c", "kernel_entry.c", "-o", "kernel_c.o"])

subprocess.run([
    "ld", "-m", "i386pe",
    "--entry=_start",
    "--image-base", "0x0",
    "-Ttext", "0x1000",
    "kernel_entry.o", "kernel_c.o",
    "-o", "kernel.tmp"
])

subprocess.run([
    "objcopy",
    "-O", "binary",
    "-j", ".text",
    "-j", ".rdata",
    "-j", ".data",
    "kernel.tmp", "kernel.bin"
])

with open("boot.bin", "rb") as f_boot, open("kernel.bin", "rb") as f_kernel:
    boot_data = f_boot.read().ljust(512, b'\x00')
    kernel_data = f_kernel.read()

full_image = (boot_data + kernel_data).ljust(102400, b'\x00')

with open("pyther_os.img", "wb") as f_out:
    f_out.write(full_image)

print("[+] Pyther Engine build complete.")