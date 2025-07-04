#!/usr/bin/env python3
"""
Face Recognition System Launcher
Run this script to start the face recognition UI application.
"""

import os
import sys
import subprocess

def check_dependencies():
    """Check if required packages are installed."""
    try:
        import cv2
        import numpy
        import PIL
        import tkinter
        print("✓ All dependencies are installed.")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        return False

def install_dependencies():
    """Install required packages."""
    print("\nInstalling dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("\n✓ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("\n✗ Failed to install dependencies.")
        print("Please run: pip install -r requirements.txt")
        return False

def main():
    print("=" * 50)
    print("Face Recognition System")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("\nDependencies are missing.")
        response = input("Would you like to install them now? (y/n): ").lower()
        if response == 'y':
            if not install_dependencies():
                sys.exit(1)
        else:
            print("\nPlease install dependencies manually:")
            print("  pip install -r requirements.txt")
            sys.exit(1)
    
    # Run the face recognition UI
    print("\nStarting Face Recognition UI...")
    try:
        import face_recognition_ui
        # The UI will start automatically when imported
    except Exception as e:
        print(f"\nError starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()