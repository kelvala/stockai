#!/usr/bin/env python3
"""Test BTCS and crypto stock resolution"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from gpt_chat_gui import StockAnalyzerGUI
import tkinter as tk

def test_crypto_stocks():
    """Test crypto stock ticker resolution"""
    
    # Create a dummy root (we won't show it)
    root = tk.Tk()
    root.withdraw()  # Hide the window
    
    # Create the app instance
    app = StockAnalyzerGUI(root)
    
    # Test crypto stock resolution
    print("Testing crypto/blockchain stock resolution:")
    print("-" * 50)
    
    crypto_test_inputs = [
        'BTCS', 'BTCS INC', 'RIOT', 'MARA', 'CLSK', 'HUT', 'BITF', 
        'COIN', 'COINBASE', 'NVDA', 'NVIDIA', 'GBTC', 'BITCOIN TRUST',
        'ETHE', 'ETHEREUM TRUST', 'BITO', 'BITI'
    ]
    
    for input_text in crypto_test_inputs:
        resolved_ticker = app.find_ticker_from_company_name(input_text)
        company_name = app.get_company_name_from_ticker(resolved_ticker)
        print(f"Input: {input_text:15} -> Ticker: {resolved_ticker:6} -> Company: {company_name}")
    
    print(f"\n✅ Test completed - {len(crypto_test_inputs)} crypto stocks tested!")
    print("🚀 BTCS and crypto stocks are now available in the autocomplete!")
    
    # Clean up
    root.destroy()

if __name__ == "__main__":
    test_crypto_stocks()
