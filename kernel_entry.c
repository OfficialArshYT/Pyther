// ==========================================
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
    os_clear();
    int running = 1;
    char pause = ' ';
    int editing = 1;
    while (1) {
        os_clear();
        os_draw_box(0, 0, 80, 2, 31);
        os_print("                         PYTHER OS SYSTEM INTERFACE                            \n");
        os_print("\n Select a Tool / Test Below:\n\n");
        os_print("  [1] Calculator Tool\n");
        os_print("  [2] Text Notepad / Buffer Test\n");
        os_print("  [3] GUI & Color Palette Test\n");
        os_print("  [4] Info & Developer Guide\n");
        os_print("  [5] Shutdown / Exit System\n\n");
        os_print("Enter Choice (1-5): ");
        int choice = os_read_int();
        if (choice == 1) {
            os_clear();
            os_draw_box(0, 0, 80, 2, 79);
            os_print("=== CALCULATOR TOOL ===\n\n");
            os_print("Enter First Digit (0-9): ");
            int num1 = os_read_int();
            os_print("Enter Operator (+, -, *, /, ^): ");
            int op = os_read_char();
            os_print_char(op);
            os_print("\n");
            os_print("Enter Second Digit (0-9): ");
            int num2 = os_read_int();
            int result = 0;
            if (op == '+') {
                result = num1 + num2;
            }
            if (op == '-') {
                result = num1 - num2;
            }
            if (op == '*') {
                result = num1 * num2;
            }
            if (op == '/') {
                if (num2 == 0) {
                    result = 0;
                } else {
                    result = num1 / num2;
                }
            }
            if (op == '^') {
                result = 1;
                int count = 0;
                while (count < num2) {
                    result = result * num1;
                    count = count + 1;
                }
            }
            os_print("\nResult: ");
            os_print_int(result);
            os_print("\n\nPress any key to return to menu...");
            pause = os_read_char();
        }
        if (choice == 2) {
            os_clear();
            os_draw_box(0, 0, 80, 2, 47);
            os_print("=== NOTEPAD / BUFFER TEST ===\n");
            os_print("Type characters below. Press '`' (backtick) to quit to menu.\n\n");
            editing = 1;
            while (1) {
                int ch = os_read_char();
                if (ch == '`') {
                    break;
                } else if (ch == '\x08') {
    os_backspace();
} else {
    os_print_char(ch);
}
            }
        }
        if (choice == 3) {
            os_clear();
            os_print("=== GRAPHICAL / VGA PALETTE TEST ===\n\n");
            os_draw_box(4, 5, 20, 5, 31);
            os_draw_box(4, 30, 20, 5, 47);
            os_draw_box(4, 55, 20, 5, 79);
            os_print("\n\n\n\n\n\n\n");
            os_print("  [Blue Box]        [Green Box]       [Red Box]\n\n");
            os_draw_box(13, 0, 80, 4, 111);
            os_print("\n  Extended driver VGA text-mode UI rendered successfully!\n\n");
            os_print("Press any key to return to main menu...");
            pause = os_read_char();
        }
        if (choice == 4) {
            os_clear();
            os_draw_box(0, 0, 80, 2, 31);
            os_print("=== PYTHER OS DEVELOPER GUIDE ===\n\n");
            os_print("HOW PYTHER WORKS:\n");
            os_print(" Write your kernel logic in Python syntax inside kernel.py.\n");
            os_print(" Running build.py transpiles your Python AST directly into bare-metal C.\n\n");
            os_print("BARE-METAL API KEYWORDS & REPLACEMENTS:\n");
            os_print(" * print()        -> os_print(\"text\") or os_print_char(ch)\n");
            os_print(" * print(number) -> os_print_int(num)\n");
            os_print(" * input()        -> os_read_char() or os_read_int()\n");
            os_print(" * clear screen   -> os_clear()\n");
            os_print(" * draw box/UI    -> os_draw_box(row, col, width, height, color)\n");
            os_print(" * delete char    -> os_backspace()\n\n");
            os_print("CONTROL FLOW SUPPORT:\n");
            os_print(" * standard 'if' / 'else' conditions work natively.\n");
            os_print(" * 'while' loops work natively (use variable = 0 to break loops).\n");
            os_print(" * Math: +, -, *, /, and ^ (power loop) are fully supported.\n\n");
            os_print("Press any key to return to menu...");
            pause = os_read_char();
        }
        if (choice == 5) {
            break;
        }
    }
    os_clear();
    os_print("==========================================\n");
    os_print("    PYTHER OS HALTED. SAFE TO TURN OFF.   \n");
    os_print("==========================================\n");

    while(1);
}
