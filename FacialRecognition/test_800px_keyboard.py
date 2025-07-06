#!/usr/bin/env python3
"""
Test script for 800px screen width keyboard layout
"""

import tkinter as tk
from tkinter import messagebox
from integrated_keyboard import show_integrated_keyboard

def test_800px_keyboard():
    """Test the keyboard layout optimized for 800px screen width"""
    root = tk.Tk()
    root.title("800px Keyboard Test")
    root.geometry("800x600")
    root.configure(bg='#2c3e50')
    
    # Instructions
    instruction = tk.Label(root, 
                          text="800px Screen Keyboard Test:\n\n" +
                               "• Optimized for 800px screen width\n" +
                               "• Keys spread across available space\n" +
                               "• Dynamic button sizing for optimal touch targets\n" +
                               "• Press ESC to close window\n" +
                               "• Click 'Done' on keyboard or 'Confirm' to proceed\n\n" +
                               "Button Sizing (800px width):\n" +
                               "• Row 1 (10 keys): ~10px each\n" +
                               "• Row 2 (10 keys): ~10px each\n" +
                               "• Row 3 (9 keys): ~11px each\n" +
                               "• Row 4 (10 keys): ~10px each (function keys double)\n\n" +
                               "Layout:\n" +
                               "┌─────────────────────────────────────┐\n" +
                               "│           Input Area                 │\n" +
                               "└─────────────────────────────────────┘\n" +
                               "│           Spread Keyboard            │\n" +
                               "│  [1][2][3][4][5][6][7][8][9][0]   │\n" +
                               "│  [Q][W][E][R][T][Y][U][I][O][P]   │\n" +
                               "│  [A][S][D][F][G][H][J][K][L]      │\n" +
                               "│  [Z][X][C][V][B][N][M][Space][Backspace][Clear] │\n" +
                               "└─────────────────────────────────────┘",
                          font=('Arial', 9),
                          fg='white', bg='#2c3e50',
                          justify=tk.LEFT)
    instruction.pack(pady=20)
    
    def show_keyboard():
        result = show_integrated_keyboard(root)
        print(f"800px keyboard result: {result}")
        if result:
            messagebox.showinfo("Result", f"Name entered: {result}")
        else:
            messagebox.showinfo("Result", "No name entered or cancelled")
    
    # Test button
    btn = tk.Button(root, text="Show 800px Keyboard", 
                   command=show_keyboard,
                   font=('Arial', 12, 'bold'),
                   bg='#27ae60', fg='white',
                   width=25, height=2)
    btn.pack(pady=20)
    
    # Screen info
    screen_info = tk.Label(root, 
                          text=f"Current Screen Width: {root.winfo_screenwidth()}px\n" +
                               f"Current Screen Height: {root.winfo_screenheight()}px\n" +
                               f"Window Width: 800px\n" +
                               f"Window Height: 500px",
                          font=('Arial', 9),
                          fg='#ecf0f1', bg='#2c3e50')
    screen_info.pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    test_800px_keyboard() 