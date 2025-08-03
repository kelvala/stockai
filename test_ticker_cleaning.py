#!/usr/bin/env python3
"""
Test script for ticker cleaning functionality
Tests various ticker input scenarios to ensure proper cleaning and validation
"""

import re

def clean_ticker(ticker_input):
    """
    Clean and validate ticker input
    - Remove spaces and extra whitespace
    - Convert to uppercase
    - Remove invalid characters
    - Handle common ticker formats (class shares, etc.)
    """
    if not ticker_input:
        return ""
    
    # Remove all whitespace and convert to uppercase
    cleaned = re.sub(r'\s+', '', str(ticker_input).upper())
    
    # Remove any characters that aren't letters, numbers, dots, or hyphens
    cleaned = re.sub(r'[^A-Z0-9.-]', '', cleaned)
    
    # Handle common ticker formats
    # Remove leading/trailing dots or hyphens
    cleaned = cleaned.strip('.-')
    
    # If ticker starts with numbers, it's likely invalid - return empty
    if cleaned and cleaned[0].isdigit():
        return ""
    
    # Validate length (most tickers are 1-5 characters, some with class designations can be longer)
    if len(cleaned) > 10:
        cleaned = cleaned[:10]
    
    return cleaned

def validate_ticker(ticker):
    """
    Basic ticker validation
    Returns True if ticker appears to be in valid format
    """
    if not ticker:
        return False
    
    # Basic format check: 1-10 characters, letters/numbers/dots/hyphens only
    if not re.match(r'^[A-Z0-9.-]+$', ticker):
        return False
    
    # Must start with a letter
    if not ticker[0].isalpha():
        return False
    
    # Length check - be more conservative with very long tickers
    if len(ticker) < 1 or len(ticker) > 8:
        return False
    
    # Additional validation: shouldn't be all numbers after the first letter
    if len(ticker) > 1 and ticker[1:].isdigit() and len(ticker) > 5:
        return False
    
    return True

def test_ticker_cleaning():
    """Test various ticker input scenarios"""
    test_cases = [
        # (input, expected_cleaned, expected_valid, description)
        ("aapl", "AAPL", True, "Simple lowercase ticker"),
        ("AAPL", "AAPL", True, "Simple uppercase ticker"),
        ("  aapl  ", "AAPL", True, "Ticker with spaces"),
        ("a a p l", "AAPL", True, "Ticker with internal spaces"),
        ("brk.a", "BRK.A", True, "Class A shares"),
        ("BRK-A", "BRK-A", True, "Class A shares with hyphen"),
        ("  brk . a  ", "BRK.A", True, "Class A shares with spaces"),
        ("tsla!", "TSLA", True, "Ticker with invalid character"),
        ("goog@l", "GOOGL", True, "Ticker with invalid character in middle"),
        ("123abc", "", False, "Ticker starting with number"),
        ("", "", False, "Empty ticker"),
        ("   ", "", False, "Only spaces"),
        ("a", "A", True, "Single character ticker"),
        ("abcdefghijklmnop", "ABCDEFGHIJ", False, "Very long ticker (truncated)"),
        ("t", "T", True, "Single letter ticker"),
        ("spy", "SPY", True, "Common ETF ticker"),
        ("VOO", "VOO", True, "Another ETF ticker"),
        ("BTC-USD", "BTC-USD", True, "Crypto ticker"),
        (".AAPL.", "AAPL", True, "Ticker with leading/trailing dots"),
        ("-MSFT-", "MSFT", True, "Ticker with leading/trailing hyphens"),
    ]
    
    print("🧪 Testing Ticker Cleaning Function")
    print("=" * 50)
    
    passed = 0
    failed = 0
    
    for input_ticker, expected_cleaned, expected_valid, description in test_cases:
        cleaned = clean_ticker(input_ticker)
        is_valid = validate_ticker(cleaned)
        
        # Check if results match expectations
        clean_ok = cleaned == expected_cleaned
        valid_ok = is_valid == expected_valid
        
        if clean_ok and valid_ok:
            status = "✅ PASS"
            passed += 1
        else:
            status = "❌ FAIL"
            failed += 1
        
        print(f"{status} | {description}")
        print(f"     Input: '{input_ticker}' → Cleaned: '{cleaned}' → Valid: {is_valid}")
        
        if not clean_ok:
            print(f"     Expected cleaned: '{expected_cleaned}', got: '{cleaned}'")
        if not valid_ok:
            print(f"     Expected valid: {expected_valid}, got: {is_valid}")
        print()
    
    print("=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed!")
    else:
        print(f"⚠️  {failed} tests failed")

if __name__ == "__main__":
    test_ticker_cleaning()
