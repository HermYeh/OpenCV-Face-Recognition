#!/usr/bin/env python3
"""
Test script for spread keyboard layout: keys spread across full screen width
"""

import tkinter as tk
from tkinter import messagebox
from integrated_keyboard import show_integrated_keyboard

def test_spread_keyboard():
    """Test the spread keyboard layout"""
    root = tk.Tk()
    root.title("Spread Keyboard Test")
    root.geometry("1000x600")
    root.configure(bg='#2c3e50')
    
    # Instructions
    instruction = tk.Label(root, 
                          text="Spread Keyboard Test:\n\n" +
                               "• Keys spread across full screen width\n" +
                               "• Optimized for 800px screen width\n" +
                               "• Dynamic button sizing based on row length\n" +
                               "• Touch-friendly large buttons\n" +
                               "• Press ESC to close window\n" +
                               "• Click 'Done' on keyboard or 'Confirm' to proceed\n\n" +
                               "Keyboard Layout:\n" +
                               "┌─────────────────────────────────────┐\n" +
                               "│           Input Area                 │ ← Top section\n" +
                               "│  [Enter Name] [Confirm] [Cancel]    │\n" +
                               "└─────────────────────────────────────┘\n" +
                               "│                                     │\n" +
                               "│           Spread Keyboard            │ ← Bottom section\n" +
                               "│  [1][2][3][4][5][6][7][8][9][0]   │ ← Full width\n" +
                               "│  [Q][W][E][R][T][Y][U][I][O][P]   │ ← Full width\n" +
                               "│  [A][S][D][F][G][H][J][K][L]      │ ← Full width\n" +
                               "│  [Z][X][C][V][B][N][M][Space][Backspace][Clear] │ ← Full width\n" +
                               "└─────────────────────────────────────┘",
                          font=('Arial', 10),
                          fg='white', bg='#2c3e50',
                          justify=tk.LEFT)
    instruction.pack(pady=20)
    
    def show_keyboard():
        result = show_integrated_keyboard(root)
        print(f"Spread keyboard result: {result}")
        if result:
            messagebox.showinfo("Result", f"Name entered: {result}")
        else:
            messagebox.showinfo("Result", "No name entered or cancelled")
    
    # Test button
    btn = tk.Button(root, text="Show Spread Keyboard", 
                   command=show_keyboard,
                   font=('Arial', 12, 'bold'),
                   bg='#27ae60', fg='white',
                   width=25, height=2)
    btn.pack(pady=20)
    
    # Additional info
    info = tk.Label(root, 
                   text="Key Features:\n" +
                        "• 800px wide window optimized for screen width\n" +
                        "• Dynamic button sizing based on row length\n" +
                        "• Function keys (Space, Backspace, Clear) are double width\n" +
                        "• All buttons expand to fill available space\n" +
                        "• Perfect for touchscreen devices",
                   font=('Arial', 9),
                   fg='#ecf0f1', bg='#2c3e50',
                   justify=tk.LEFT)
    info.pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    test_spread_keyboard() 