def main():
    os_clear()
    
    running = True
    pause = ' '
    editing = True
    
    while running:
        os_clear()
        
        # Header Box
        os_draw_box(0, 0, 80, 2, 31)
        os_print("                         PYTHER OS SYSTEM INTERFACE                            \n")
        
        # Main Menu
        os_print("\n Select a Tool / Test Below:\n\n")
        os_print("  [1] Calculator Tool\n")
        os_print("  [2] Text Notepad / Buffer Test\n")
        os_print("  [3] GUI & Color Palette Test\n")
        os_print("  [4] Info & Developer Guide\n")
        os_print("  [5] Shutdown / Exit System\n\n")
        
        os_print("Enter Choice (1-5): ")
        choice = os_read_int()
        
        # ----------------------------------------------------
        # TOOL 1: EXTENDED CALCULATOR
        # ----------------------------------------------------
        if choice == 1:
            os_clear()
            os_draw_box(0, 0, 80, 2, 79)
            os_print("=== CALCULATOR TOOL ===\n\n")
            
            os_print("Enter First Digit (0-9): ")
            num1 = os_read_int()
            
            os_print("Enter Operator (+, -, *, /, ^): ")
            op = os_read_char()
            os_print_char(op)
            os_print("\n")
            
            os_print("Enter Second Digit (0-9): ")
            num2 = os_read_int()
            
            result = 0
            if op == '+':
                result = num1 + num2
            if op == '-':
                result = num1 - num2
            if op == '*':
                result = num1 * num2
            if op == '/':
                if num2 == 0:
                    result = 0
                else:
                    result = num1 / num2
            if op == '^':
                result = 1
                count = 0
                while count < num2:
                    result = result * num1
                    count = count + 1
                
            os_print("\nResult: ")
            os_print_int(result)
            os_print("\n\nPress any key to return to menu...")
            pause = os_read_char()

        # ----------------------------------------------------
        # TOOL 2: NOTEPAD / TEXT BUFFER
        # ----------------------------------------------------
        if choice == 2:
            os_clear()
            os_draw_box(0, 0, 80, 2, 47)
            os_print("=== NOTEPAD / BUFFER TEST ===\n")
            os_print("Type characters below. Press '`' (backtick) to quit to menu.\n\n")
            
            editing = True
            while editing:
                ch = os_read_char()
                if ch == '`':
                    editing = False
                elif ch == '\b':
                    os_backspace()
                else:
                    os_print_char(ch)

        # ----------------------------------------------------
        # TOOL 3: GUI BOXES & COLOR DEMO
        # ----------------------------------------------------
        if choice == 3:
            os_clear()
            os_print("=== GRAPHICAL / VGA PALETTE TEST ===\n\n")
            
            os_draw_box(4, 5, 20, 5, 31)   # Blue Box
            os_draw_box(4, 30, 20, 5, 47)  # Green Box
            os_draw_box(4, 55, 20, 5, 79)  # Red Box
            
            os_print("\n\n\n\n\n\n\n")
            os_print("  [Blue Box]        [Green Box]       [Red Box]\n\n")
            
            os_draw_box(13, 0, 80, 4, 111) 
            os_print("\n  Extended driver VGA text-mode UI rendered successfully!\n\n")
            os_print("Press any key to return to main menu...")
            pause = os_read_char()

        # ----------------------------------------------------
        # TOOL 4: INFO & DEVELOPER GUIDE
        # ----------------------------------------------------
        if choice == 4:
            os_clear()
            os_draw_box(0, 0, 80, 2, 31)
            os_print("=== PYTHER OS DEVELOPER GUIDE ===\n\n")
            
            os_print("HOW PYTHER WORKS:\n")
            os_print(" Write your kernel logic in Python syntax inside kernel.py.\n")
            os_print(" Running build.py transpiles your Python AST directly into bare-metal C.\n\n")
            
            os_print("BARE-METAL API KEYWORDS & REPLACEMENTS:\n")
            os_print(" * print()        -> os_print(\"text\") or os_print_char(ch)\n")
            os_print(" * print(number) -> os_print_int(num)\n")
            os_print(" * input()        -> os_read_char() or os_read_int()\n")
            os_print(" * clear screen   -> os_clear()\n")
            os_print(" * draw box/UI    -> os_draw_box(row, col, width, height, color)\n")
            os_print(" * delete char    -> os_backspace()\n\n")
            
            os_print("CONTROL FLOW SUPPORT:\n")
            os_print(" * standard 'if' / 'else' conditions work natively.\n")
            os_print(" * 'while' loops work natively (use variable = 0 to break loops).\n")
            os_print(" * Math: +, -, *, /, and ^ (power loop) are fully supported.\n\n")
            
            os_print("Press any key to return to menu...")
            pause = os_read_char()

        # ----------------------------------------------------
        # TOOL 5: SHUTDOWN
        # ----------------------------------------------------
        if choice == 5:
            running = False

    os_clear()
    os_print("==========================================\n")
    os_print("    PYTHER OS HALTED. SAFE TO TURN OFF.   \n")
    os_print("==========================================\n")