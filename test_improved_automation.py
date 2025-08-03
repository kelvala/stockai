#!/usr/bin/env python3
"""
Test the improved GPT automation system
"""

import sys
import os
import tkinter as tk

# Add the current directory to sys.path to import our module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import our main application
from gpt_chat_gui import StockAnalyzerGUI

def test_automation():
    """Test the improved automation features"""
    print("🧪 Testing Improved GPT Automation System")
    print("=" * 50)
    
    # Create the main window
    root = tk.Tk()
    app = StockAnalyzerGUI(root)
    
    print("\n🔧 Testing automation methods...")
    
    # Test the new use_existing_browser method
    test_url = "https://chatgpt.com/g/g-686c5fc3dd948191a0ff9c14cecda1b4-stock-predictor-prompt-gpt"
    test_ticker = "AAPL"
    
    print(f"\n🍎 Testing AppleScript automation with {test_ticker}...")
    
    # Test if AppleScript works
    try:
        import subprocess
        
        # Simple test to see if AppleScript is available
        test_script = '''
        tell application "System Events"
            return "AppleScript works"
        end tell
        '''
        
        result = subprocess.run(['osascript', '-e', test_script], 
                              capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            print("✅ AppleScript is available and working")
            
            # Test browser automation (this will actually open a browser)
            print(f"\n🌐 Testing browser automation with {test_ticker}...")
            print("⚠️  This will open your browser - close it manually after the test")
            
            # Ask user if they want to proceed
            response = input("\nProceed with browser test? (y/n): ").strip().lower()
            if response == 'y':
                success = app.use_existing_browser(test_url, test_ticker)
                print(f"Automation result: {'✅ Success' if success else '❌ Failed'}")
            else:
                print("Skipping browser test")
                
        else:
            print("❌ AppleScript test failed:")
            print(f"Error: {result.stderr}")
            
    except Exception as e:
        print(f"❌ AppleScript test error: {e}")
    
    # Test clipboard functionality
    print(f"\n📋 Testing clipboard functionality...")
    try:
        import pyperclip
        pyperclip.copy(test_ticker)
        copied = pyperclip.paste()
        if copied == test_ticker:
            print("✅ Clipboard functionality works")
        else:
            print(f"❌ Clipboard test failed: expected '{test_ticker}', got '{copied}'")
    except ImportError:
        print("❌ pyperclip not available - clipboard fallback won't work")
    except Exception as e:
        print(f"❌ Clipboard error: {e}")
    
    # Test the full automation flow
    print(f"\n🔄 Testing full automation flow...")
    try:
        # Simulate the Stock Predictor button click
        app.entry.insert(0, test_ticker)
        
        print("Testing Stock Predictor automation (this will open browser)...")
        response = input("Proceed with full automation test? (y/n): ").strip().lower()
        if response == 'y':
            app.open_stock_predictor()
        else:
            print("Skipping full automation test")
            
    except Exception as e:
        print(f"❌ Full automation test error: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Automation testing complete!")
    print("\nKey improvements made:")
    print("• Enhanced AppleScript with multiple fallback methods")
    print("• Better browser detection (Chrome, Safari, Firefox, Edge)")
    print("• Tab navigation for more reliable input field detection")
    print("• Dynamic screen size calculation for click coordinates")
    print("• Better error handling and user feedback")
    print("• Clearer manual fallback instructions")
    
    # Don't start the GUI mainloop for testing
    root.destroy()

if __name__ == "__main__":
    test_automation()
