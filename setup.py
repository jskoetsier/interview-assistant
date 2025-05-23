#!/usr/bin/env python3
"""
Setup script for Network Engineer Interview Assistant
This script checks for required dependencies and installs them if needed.
"""

import sys
import subprocess
import os
import platform

def check_python_version():
    """Check if Python version is 3.6 or higher."""
    if sys.version_info < (3, 6):
        print("Error: Python 3.6 or higher is required.")
        print(f"Current Python version: {sys.version}")
        return False
    return True

def check_and_install_pyqt():
    """Check if PyQt5 is installed, and install it if not."""
    try:
        import PyQt5
        print(f"PyQt5 is already installed (version: {PyQt5.QtCore.QT_VERSION_STR})")
        return True
    except ImportError:
        print("PyQt5 is not installed. Attempting to install...")

        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt5"])
            print("PyQt5 has been successfully installed.")
            return True
        except subprocess.CalledProcessError:
            print("Error: Failed to install PyQt5. Please install it manually using:")
            print("pip install PyQt5")
            return False

def create_launcher():
    """Create a launcher script or shortcut based on the operating system."""
    system = platform.system()

    if system == "Windows":
        # Create a batch file for Windows
        with open("run_interview_assistant.bat", "w") as f:
            f.write('@echo off\n')
            f.write('python interview_assistant.py\n')
            f.write('pause\n')
        print("Created launcher: run_interview_assistant.bat")

    elif system == "Darwin":  # macOS
        # Create a shell script for macOS
        with open("run_interview_assistant.sh", "w") as f:
            f.write('#!/bin/bash\n')
            f.write('python3 "$(dirname "$0")/interview_assistant.py"\n')

        # Make it executable
        os.chmod("run_interview_assistant.sh", 0o755)
        print("Created launcher: run_interview_assistant.sh")

    elif system == "Linux":
        # Create a shell script for Linux
        with open("run_interview_assistant.sh", "w") as f:
            f.write('#!/bin/bash\n')
            f.write('python3 "$(dirname "$0")/interview_assistant.py"\n')

        # Make it executable
        os.chmod("run_interview_assistant.sh", 0o755)
        print("Created launcher: run_interview_assistant.sh")

    else:
        print(f"Unsupported operating system: {system}")
        print("Please run the application using: python interview_assistant.py")

def main():
    """Main setup function."""
    print("Setting up Network Engineer Interview Assistant...")

    # Check Python version
    if not check_python_version():
        return

    # Check and install PyQt5
    if not check_and_install_pyqt():
        return

    # Create launcher
    create_launcher()

    print("\nSetup complete!")
    print("\nTo run the application:")

    system = platform.system()
    if system == "Windows":
        print("  Double-click on run_interview_assistant.bat")
        print("  Or run: python interview_assistant.py")
    elif system in ["Darwin", "Linux"]:
        print("  Run: ./run_interview_assistant.sh")
        print("  Or run: python3 interview_assistant.py")
    else:
        print("  Run: python interview_assistant.py")

if __name__ == "__main__":
    main()
