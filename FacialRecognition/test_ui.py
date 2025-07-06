#!/usr/bin/env python3
"""
Test script for Face Recognition UI components
"""

import tkinter as tk
from tkinter import messagebox
import os

def test_ui_components():
    """Test basic UI components"""
    root = tk.Tk()
    root.title("UI Test")
    root.geometry("400x300")
    
    # Test basic UI creation
    label = tk.Label(root, text="UI Test - All components working", font=('Arial', 14))
    label.pack(pady=20)
    
    # Test button
    def test_button():
        messagebox.showinfo("Test", "Button click works!")
    
    button = tk.Button(root, text="Test Button", command=test_button)
    button.pack(pady=10)
    
    # Test file existence
    files_to_check = [
        'haarcascade_frontalface_default.xml',
        'face_recognition_ui.py',
        'requirements.txt'
    ]
    
    status_text = "File Status:\n"
    for file in files_to_check:
        if os.path.exists(file):
            status_text += f"✓ {file}\n"
        else:
            status_text += f"✗ {file}\n"
    
    status_label = tk.Label(root, text=status_text, font=('Arial', 10))
    status_label.pack(pady=10)
    
    # Test directory creation
    test_dirs = ['dataset', 'trainer']
    dir_status = "Directory Status:\n"
    for dir_name in test_dirs:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            dir_status += f"✓ Created {dir_name}/\n"
        else:
            dir_status += f"✓ {dir_name}/ exists\n"
    
    dir_label = tk.Label(root, text=dir_status, font=('Arial', 10))
    dir_label.pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    test_ui_components() 