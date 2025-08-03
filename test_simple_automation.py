#!/usr/bin/env python3
"""
Test specific automation issue
"""

import subprocess
import time
import webbrowser

def test_simple_automation():
    """Test the simple automation approach"""
    print("🧪 Testing Simple Automation")
    print("=" * 40)
    
    # Test data
    test_url = "https://chatgpt.com/g/g-686c5fc3dd948191a0ff9c14cecda1b4-stock-predictor-prompt-gpt"
    test_ticker = "AAPL"
    
    print(f"Opening URL: {test_url}")
    webbrowser.open(test_url)
    time.sleep(5)  # Wait for page to load
    
    print(f"Attempting to enter ticker: {test_ticker}")
    
    # Simple, direct AppleScript
    applescript = f'''
    tell application "System Events"
        delay 3
        
        -- Try to activate browser
        try
            tell application "Google Chrome" to activate
        on error
            try
                tell application "Safari" to activate
            end try
        end try
        
        delay 2
        
        -- Simple approach: click bottom center and type
        try
            set frontWindow to front window of (first application process whose frontmost is true)
            set windowBounds to bounds of frontWindow
            
            -- Calculate bottom center
            set windowWidth to (item 3 of windowBounds) - (item 1 of windowBounds)
            set windowHeight to (item 4 of windowBounds) - (item 2 of windowBounds)
            set clickX to (item 1 of windowBounds) + (windowWidth / 2)
            set clickY to (item 2 of windowBounds) + (windowHeight * 0.85)
            
            -- Click and type
            click at {{clickX, clickY}}
            delay 1
            
            -- Select all and replace
            keystroke "a" using command down
            delay 0.5
            keystroke "{test_ticker}"
            delay 1
            key code 36  -- Enter
            
            return "success"
        on error e
            return "error: " & e
        end try
    end tell
    '''
    
    try:
        result = subprocess.run(['osascript', '-e', applescript], 
                              capture_output=True, text=True, timeout=20)
        
        print(f"AppleScript result: {result.stdout.strip()}")
        if result.stderr:
            print(f"AppleScript errors: {result.stderr}")
            
        if result.returncode == 0:
            print("✅ Automation completed")
        else:
            print("❌ Automation failed")
            
    except Exception as e:
        print(f"❌ Error running AppleScript: {e}")

if __name__ == "__main__":
    response = input("This will open ChatGPT and try to enter 'AAPL'. Continue? (y/n): ")
    if response.lower() == 'y':
        test_simple_automation()
    else:
        print("Test cancelled")
