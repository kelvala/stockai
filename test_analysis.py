#!/usr/bin/env python3
"""Test script to verify the comprehensive analysis functionality"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from gpt_chat_gui import StockAnalyzerGUI
import tkinter as tk
from datetime import datetime

def test_analysis_functionality():
    """Test the analysis functionality without running the GUI"""
    
    # Create a dummy root (we won't show it)
    root = tk.Tk()
    root.withdraw()  # Hide the window
    
    # Create the app instance
    app = StockAnalyzerGUI(root)
    
    # Test ticker resolution
    print("Testing ticker resolution:")
    print("-" * 40)
    
    test_inputs = ['T', 'AT&T', 'TMUS', 'T-MOBILE', 'TMOBILE', 'UUUU', 'ENERGY FUELS', 'AAPL', 'TESLA', 'MSFT']
    
    for input_text in test_inputs:
        resolved_ticker = app.find_ticker_from_company_name(input_text)
        company_name = app.get_company_name_from_ticker(resolved_ticker)
        print(f"Input: {input_text:8} -> Ticker: {resolved_ticker:6} -> Company: {company_name}")
    
    # Test the analysis header format
    print("\nTesting analysis header format:")
    print("-" * 40)
    
    ticker = 'T'
    company_name = app.get_company_name_from_ticker(ticker)
    current_price = 23.45  # Example price
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Show what the analysis header would look like
    print(f"Analysis header: 📊 COMPREHENSIVE STOCK ANALYSIS: {ticker} ({company_name})")
    print(f"Stock info header: 📊 {ticker} ({company_name}) - ${current_price:.2f} | Updated: {timestamp}")
    
    print("\nTest completed successfully!")
    
    # Clean up
    root.destroy()

if __name__ == "__main__":
    test_analysis_functionality()
