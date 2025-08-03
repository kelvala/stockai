#!/usr/bin/env python3
"""Test scrolling in the analysis display"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from gpt_chat_gui import StockAnalyzerGUI
import tkinter as tk

def test_scrolling():
    """Test that scrolling works properly"""
    
    # Create a dummy root (we won't show it)
    root = tk.Tk()
    root.withdraw()  # Hide the window
    
    # Create the app instance
    app = StockAnalyzerGUI(root)
    
    # Test long message that requires scrolling
    long_message = "📊 COMPREHENSIVE STOCK ANALYSIS: TEST\n" + "="*60 + "\n\n"
    
    # Add many lines to test scrolling
    for i in range(50):
        long_message += f"Line {i+1}: This is a test line to check scrolling functionality.\n"
    
    long_message += "\n" + "="*60 + "\n"
    long_message += "END OF ANALYSIS - You should be able to scroll to see this!"
    
    # Display the message
    app.display_message(long_message, "response")
    
    print("Long message displayed. Check that scrolling works in the GUI.")
    print("The text should scroll to the bottom automatically.")
    
    # Don't destroy root immediately - let user test
    input("Press Enter to continue...")
    
    # Clean up
    root.destroy()

if __name__ == "__main__":
    test_scrolling()
