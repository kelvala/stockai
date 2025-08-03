#!/usr/bin/env python3
"""Quick test to verify T vs T-Mobile ticker resolution"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from gpt_chat_gui import StockAnalyzerGUI
import tkinter as tk

def test_t_mobile_resolution():
    """Test T vs T-Mobile ticker resolution"""
    
    # Create a dummy root (we won't show it)
    root = tk.Tk()
    root.withdraw()  # Hide the window
    
    # Create the app instance
    app = StockAnalyzerGUI(root)
    
    print("Testing T vs T-Mobile resolution:")
    print("=" * 50)
    
    test_cases = [
        ('T', 'Should resolve to AT&T'),
        ('AT&T', 'Should resolve to AT&T'),
        ('ATT', 'Should resolve to AT&T'),
        ('TMUS', 'Should resolve to T-Mobile'),
        ('T-MOBILE', 'Should resolve to T-Mobile'),
        ('TMOBILE', 'Should resolve to T-Mobile'),
        ('T MOBILE', 'Should resolve to T-Mobile'),
    ]
    
    for input_text, expected in test_cases:
        resolved_ticker = app.find_ticker_from_company_name(input_text)
        company_name = app.get_company_name_from_ticker(resolved_ticker)
        
        print(f"Input: {input_text:10} -> Ticker: {resolved_ticker:6} -> Company: {company_name:20} | {expected}")
    
    print("\nSummary:")
    print("- T resolves to:", app.get_company_name_from_ticker('T'))
    print("- TMUS resolves to:", app.get_company_name_from_ticker('TMUS'))
    
    # Clean up
    root.destroy()

if __name__ == "__main__":
    test_t_mobile_resolution()
