#!/usr/bin/env python3
"""
Alternative build script using cx_Freeze for creating standalone executable
"""

import sys
from cx_Freeze import setup, Executable
import os

# Dependencies are automatically detected, but some modules need help
build_exe_options = {
    "packages": [
        "tkinter", "yfinance", "pandas", "numpy", "requests", 
        "webbrowser", "csv", "json", "datetime", "threading",
        "pyperclip", "transformers", "torch"
    ],
    "excludes": ["test", "unittest"],
    "include_files": [
        ("stock_data.csv", "stock_data.csv"),
        ("README.md", "README.md"),
        ("requirements.txt", "requirements.txt")
    ],
    "build_exe": "build/StockAnalyzer"
}

# GUI applications require a different base on Windows
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Stock Analyzer",
    version="0.10",
    description="AI-Powered Stock Analysis Tool",
    options={"build_exe": build_exe_options},
    executables=[Executable("gpt_chat_gui.py", base=base, target_name="StockAnalyzer")]
)
