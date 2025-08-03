#!/usr/bin/env python3
"""Test the new uranium/lithium stocks and industry insights"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from gpt_chat_gui import StockAnalyzerGUI
import tkinter as tk

def test_new_stocks():
    """Test the new uranium and lithium stocks"""
    
    root = tk.Tk()
    root.withdraw()  # Hide the window
    
    app = StockAnalyzerGUI(root)
    
    print("Testing new uranium/lithium stocks:")
    print("-" * 50)
    
    test_tickers = ['LAC', 'URNJ', 'CCJ', 'UEC', 'UUUU', 'DNN', 'URG', 'LTHM', 'ALB', 'SQM']
    
    for ticker in test_tickers:
        resolved_ticker = app.find_ticker_from_company_name(ticker)
        company_name = app.get_company_name_from_ticker(resolved_ticker)
        print(f"Ticker: {ticker:6} -> Resolved: {resolved_ticker:6} -> Company: {company_name}")
    
    print("\nTesting industry insights:")
    print("-" * 50)
    
    # Test uranium company
    insights = app.get_industry_insights('URNJ', 'Energy', 'Uranium Mining', 'Sprott Junior Uranium Miners ETF')
    print("URNJ Insights:")
    print(insights)
    
    # Test lithium company
    insights = app.get_industry_insights('LAC', 'Materials', 'Lithium Mining', 'Lithium Americas Corp')
    print("LAC Insights:")
    print(insights)
    
    # Test crypto company
    insights = app.get_industry_insights('BTCS', 'Technology', 'Blockchain', 'BTCS Inc')
    print("BTCS Insights:")
    print(insights)
    
    print("✅ Test completed!")
    
    root.destroy()

if __name__ == "__main__":
    test_new_stocks()
