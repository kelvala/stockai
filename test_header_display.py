#!/usr/bin/env python3
"""Test the header display functionality"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from gpt_chat_gui import StockAnalyzerGUI
import tkinter as tk
import time

def test_header_display():
    """Test that the header displays immediately at the top"""
    
    root = tk.Tk()
    root.geometry("800x600")
    
    app = StockAnalyzerGUI(root)
    
    def simulate_analysis():
        """Simulate the analysis process"""
        print("Testing header display...")
        
        # Test showing header immediately
        app.display_analysis_header("AAPL", "Apple Inc")
        print("✅ Header displayed at top")
        
        # Wait a moment to simulate processing
        root.after(2000, show_complete_analysis)
    
    def show_complete_analysis():
        """Show the complete analysis"""
        sample_analysis = """📊 COMPREHENSIVE STOCK ANALYSIS: AAPL (Apple Inc)
============================================================

Query: AAPL
Current Price: $195.50
52-Week Range: $164.08 - $199.62
1-Year Performance: +15.25%
Analysis Date: 2025-07-17 23:30

🔍 **1. MARKET TREND ALIGNMENT**
• Sector: Technology
• Industry: Consumer Electronics
• Long-term trend: BULLISH (Price above 200-day MA: $180.25)
• Short-term trend: BULLISH (Price above 50-day MA: $188.75)

📈 **2. TECHNICAL OVERVIEW & MOMENTUM**
• RSI (14-day): 58.5 (NEUTRAL)
• MACD: 2.450, Signal: 1.850
• MACD Signal: BULLISH (MACD above signal line)
• 50-day MA: $188.75
• 200-day MA: $180.25
• Volume vs Avg: 1.2x (Current: 85,000,000)

💰 **3. VALUATION & FUNDAMENTALS**
• Market Cap: $3,024,000,000,000
• P/E Ratio: 28.50
• Annual Revenue: $394,328,000,000
• Valuation Assessment: OVERVALUED (High P/E)

🎯 **4. BUY/SELL/HOLD RECOMMENDATION**
• Recommendation: **HOLD** (Mixed signals)
• Entry Point: Consider $185.73 - $205.28
• Stop Loss: $175.95 (10% below current)
• Target Price: $234.60 (20% above current)

📋 **SUMMARY & ACTION PLAN**
• Overall Assessment: HOLD based on technical and fundamental analysis
• Key Monitors: Volume, Technology sector performance, earnings reports
• Reassessment: Weekly technical review, quarterly fundamental review

🔗 **For Advanced AI Analysis**: Use the 'Stock Predictor' button to get detailed,
real-time analysis using your custom Stock Predictor GPT with current market data.

⚠️ **Disclaimer**: This analysis is for educational purposes only.
Always consult with financial advisors and conduct your own research before making investment decisions.
Past performance does not guarantee future results.

============================================================
🏁 END OF ANALYSIS - Stock Analyzer v0.11 🏁
============================================================


------- SCROLL DOWN TO SEE COMPLETE ANALYSIS -------"""
        
        app.display_complete_analysis(sample_analysis)
        print("✅ Complete analysis displayed (starts at top)")
        
        root.after(1000, lambda: print("✅ Test completed - check that display starts at top!"))
    
    # Start the test
    root.after(500, simulate_analysis)
    
    root.mainloop()

if __name__ == "__main__":
    test_header_display()
