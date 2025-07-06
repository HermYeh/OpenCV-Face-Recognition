#!/usr/bin/env python3
"""
Face Recognition Launcher
Automatically chooses between GUI and headless modes
"""

import os
import sys
import subprocess

def check_display():
    """Check if display is available"""
    return 'DISPLAY' in os.environ and os.environ['DISPLAY'] != ''

def check_gui_capabilities():
    """Check if GUI can be used"""
    try:
        import tkinter
        root = tkinter.Tk()
        root.destroy()
        return True
    except:
        return False

def main():
    print("Face Recognition System Launcher")
    print("=" * 40)
    
    # Check system capabilities
    has_display = check_display()
    has_gui = check_gui_capabilities()
    
    print(f"Display available: {has_display}")
    print(f"GUI capabilities: {has_gui}")
    
    if has_display and has_gui:
        print("\nStarting GUI version...")
        try:
            import face_recognition_ui
            face_recognition_ui.main()
        except ImportError:
            print("Error: GUI module not found")
            sys.exit(1)
    else:
        print("\nStarting headless version...")
        try:
            import face_recognition_ui_headless
            face_recognition_ui_headless.main()
        except ImportError:
            print("Error: Headless module not found")
            sys.exit(1)

if __name__ == "__main__":
    main() 