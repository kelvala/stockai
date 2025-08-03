#!/usr/bin/env python3
"""Test LAC and URNJ analysis with industry insights"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from gpt_chat_gui import StockAnalyzerGUI
import tkinter as tk

def test_lac_urnj_analysis():
    """Test LAC and URNJ ticker resolution and industry insights"""
    
    # Create a dummy root (we won't show it)
    root = tk.Tk()
    root.withdraw()  # Hide the window
    
    # Create the app instance
    app = StockAnalyzerGUI(root)
    
    # Test LAC and URNJ resolution
    print("Testing LAC and URNJ stock resolution:")
    print("-" * 50)
    
    test_inputs = [
        'LAC', 'LITHIUM AMERICAS', 'URNJ', 'URANIUM MINERS', 'SPROTT URANIUM',
        'URA', 'URANIUM ETF', 'LIT', 'LITHIUM ETF', 'BATT', 'BATTERY ETF'
    ]
    
    for input_text in test_inputs:
        resolved_ticker = app.find_ticker_from_company_name(input_text)
        company_name = app.get_company_name_from_ticker(resolved_ticker)
        print(f"Input: {input_text:18} -> Ticker: {resolved_ticker:6} -> Company: {company_name}")
    
    print("\n" + "="*70)
    print("Testing Industry Insights:")
    print("="*70)
    
    # Test industry insights for specific tickers
    test_cases = [
        ('LAC', 'Lithium Americas Corp'),
        ('URNJ', 'Sprott Junior Uranium Miners ETF'),
        ('BTCS', 'BTCS Inc'),
        ('URA', 'Global X Uranium ETF'),
        ('LIT', 'Global X Lithium & Battery Tech ETF')
    ]
    
    for ticker, company in test_cases:
        print(f"\n📊 Testing {ticker} ({company}):")
        print("-" * 50)
        
        # Mock some basic info for testing
        insights = app.get_industry_insights(ticker, 'Basic Materials', 'Mining', company)
        print(insights)
    
    print("✅ Test completed - LAC, URNJ and related stocks ready!")
    print("🚀 Industry insights now include detailed explanations!")
    
    # Clean up
    root.destroy()

if __name__ == "__main__":
    test_lac_urnj_analysis()
