#!/usr/bin/env python3
"""
Demo script showing ticker cleaning in action
"""

import re

def clean_ticker(ticker_input):
    """Clean and validate ticker input"""
    if not ticker_input:
        return ""
    
    cleaned = re.sub(r'\s+', '', str(ticker_input).upper())
    cleaned = re.sub(r'[^A-Z0-9.-]', '', cleaned)
    cleaned = cleaned.strip('.-')
    
    if cleaned and cleaned[0].isdigit():
        return ""
    
    if len(cleaned) > 10:
        cleaned = cleaned[:10]
    
    return cleaned

def validate_ticker(ticker):
    """Basic ticker validation"""
    if not ticker:
        return False
    
    if not re.match(r'^[A-Z0-9.-]+$', ticker):
        return False
    
    if not ticker[0].isalpha():
        return False
    
    if len(ticker) < 1 or len(ticker) > 8:
        return False
    
    if len(ticker) > 1 and ticker[1:].isdigit() and len(ticker) > 5:
        return False
    
    return True

def demo_ticker_cleaning():
    """Interactive demo of ticker cleaning"""
    print("🚀 Stock Analyzer - Ticker Cleaning Demo")
    print("=" * 50)
    print("This demonstrates how the web app now handles ticker input with spaces!")
    print("Try entering tickers with spaces, and see how they get cleaned automatically.")
    print("Type 'quit' to exit.\n")
    
    while True:
        user_input = input("Enter a ticker symbol (with or without spaces): ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("👋 Thanks for trying the ticker cleaning demo!")
            break
        
        if not user_input:
            print("Please enter a ticker symbol.\n")
            continue
        
        # Clean the ticker
        cleaned = clean_ticker(user_input)
        is_valid = validate_ticker(cleaned)
        
        print(f"📝 Input: '{user_input}'")
        print(f"🧹 Cleaned: '{cleaned}'")
        print(f"✅ Valid: {is_valid}")
        
        if cleaned != user_input.upper().strip():
            print(f"💡 Your input was automatically cleaned!")
        
        if not is_valid:
            print("❌ This ticker format appears to be invalid.")
        else:
            print(f"🎯 Ready to analyze: {cleaned}")
        
        print("-" * 30)

if __name__ == "__main__":
    demo_ticker_cleaning()
