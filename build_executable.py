#!/usr/bin/env python3
"""
Setup script to create a standalone executable for Stock Analyzer
"""

import os
import sys
import subprocess
import shutil

def check_pyinstaller():
    """Check if PyInstaller is installed"""
    try:
        import PyInstaller
        return True
    except ImportError:
        return False

def install_pyinstaller():
    """Install PyInstaller"""
    print("Installing PyInstaller...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    print("PyInstaller installed successfully!")

def create_executable():
    """Create the standalone executable"""
    print("Creating standalone executable...")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",  # Create a single executable file
        "--windowed",  # No console window (GUI only)
        "--name", "StockAnalyzer",
        "--icon", "app.ico" if os.path.exists("app.ico") else None,
        "--add-data", "stock_data.csv:.",  # Include the CSV file
        "gpt_chat_gui.py"
    ]
    
    # Remove None values from command
    cmd = [c for c in cmd if c is not None]
    
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
    
    print("Executable created successfully!")
    print("You can find it in the 'dist' folder")

def main():
    """Main setup function"""
    print("Stock Analyzer - Standalone Executable Builder")
    print("=" * 50)
    
    # Check if PyInstaller is installed
    if not check_pyinstaller():
        print("PyInstaller not found. Installing...")
        install_pyinstaller()
    
    # Create executable
    create_executable()
    
    print("\nBuild complete!")
    print("The standalone executable is in the 'dist' folder.")
    print("You can distribute the 'StockAnalyzer' executable to other computers.")

if __name__ == "__main__":
    main()
