#!/usr/bin/env python3
"""
Test script to verify scrolling and text display functionality
"""

import tkinter as tk
from tkinter import scrolledtext
import time

def test_scrolling():
    """Test scrolling behavior with long text"""
    root = tk.Tk()
    root.title("Scrolling Test")
    root.geometry("600x400")
    
    # Create a scrolled text widget
    text_widget = scrolledtext.ScrolledText(root, 
                                           font=("Arial", 12), 
                                           wrap=tk.WORD, 
                                           state=tk.DISABLED,
                                           bg="#f8f9fa")
    text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def add_long_text():
        """Add long text and test scrolling"""
        long_text = """📊 COMPREHENSIVE STOCK ANALYSIS: TEST
========================================

This is a test of the scrolling functionality.
We want to make sure that when we add a lot of text,
the text widget automatically scrolls to the bottom
and shows all the content without any cutoff.

Let me add many lines to test this:

Line 1: This is a test line
Line 2: This is another test line
Line 3: Testing scrolling behavior
Line 4: Making sure content is visible
Line 5: Checking text widget configuration
Line 6: Verifying scroll position
Line 7: Testing font rendering
Line 8: Checking text wrapping
Line 9: Testing bottom padding
Line 10: Verifying complete display

📈 TECHNICAL ANALYSIS SECTION
• This section tests technical indicators
• RSI: 45.2 (NEUTRAL)
• MACD: Bullish signal detected
• Moving averages: Trending upward
• Volume: Above average

💰 VALUATION SECTION
• Market Cap: $500B
• P/E Ratio: 22.5
• Revenue Growth: 15% YoY
• Profit Margins: Strong

🎯 RECOMMENDATION
• Overall Assessment: BUY
• Entry Point: $150-155
• Stop Loss: $135
• Target Price: $180

📋 SUMMARY
• Stock shows strong fundamentals
• Technical indicators are positive
• Market conditions are favorable
• Recommended allocation: 3-5% of portfolio

⚠️ DISCLAIMER
This analysis is for educational purposes only.
Always consult with financial advisors and conduct 
your own research before making investment decisions.
Past performance does not guarantee future results.

============================================
🏁 END OF ANALYSIS - Test Version 🏁
============================================


------- SCROLL DOWN TO SEE COMPLETE ANALYSIS -------

"""
        
        text_widget.config(state=tk.NORMAL)
        text_widget.delete("1.0", tk.END)
        text_widget.insert(tk.END, long_text + "\n\n\n\n\n")
        text_widget.config(state=tk.DISABLED)
        
        # Force scrolling to the bottom
        text_widget.update_idletasks()
        text_widget.see(tk.END)
        text_widget.mark_set("insert", tk.END)
        text_widget.see("insert")
        root.update_idletasks()
        
        print("Text added and scrolled to bottom")
    
    # Add button to trigger test
    button = tk.Button(root, text="Add Long Text & Scroll", command=add_long_text)
    button.pack(pady=5)
    
    # Add text immediately
    root.after(500, add_long_text)
    
    root.mainloop()

if __name__ == "__main__":
    test_scrolling()
