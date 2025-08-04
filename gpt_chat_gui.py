# Free AI GUI Application - No API Required

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog
import threading
import requests
import json
import csv
import os
import webbrowser
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import re
import time
import platform
import subprocess

# Try to import pyperclip for clipboard functionality
try:
    import pyperclip
except ImportError:
    pyperclip = None

# Try to import transformers for local AI
try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

# Free Hugging Face API endpoint (no key required for basic use)
FREE_API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"

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

class AutomationProgressDialog:
    """Progress dialog to show during automation to prevent user interference"""
    def __init__(self, parent, ticker):
        self.ticker = ticker
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Automating AI Assistant...")
        self.dialog.geometry("450x220")
        self.dialog.configure(bg="#1a1a1a")
        
        # HARD FOCUS - Stay on top of EVERYTHING including Chrome
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.attributes('-topmost', True)
        self.dialog.lift()
        self.dialog.focus_force()
        
        # Make it even more prominent
        self.dialog.attributes('-alpha', 0.98)  # Slight transparency to show it's special
        self.dialog.resizable(False, False)
        
        # Center the dialog on screen (not just relative to parent)
        screen_width = self.dialog.winfo_screenwidth()
        screen_height = self.dialog.winfo_screenheight()
        x = (screen_width - 450) // 2
        y = (screen_height - 220) // 2
        self.dialog.geometry(f"450x220+{x}+{y}")
        
        # Prevent user from closing during automation
        self.dialog.protocol("WM_DELETE_WINDOW", lambda: None)
        
        # Force focus repeatedly to ensure it stays on top
        self.dialog.after(100, self.maintain_focus)
        self.dialog.after(500, self.maintain_focus)
        self.dialog.after(1000, self.maintain_focus)
        
        self.setup_ui()
        
    def maintain_focus(self):
        """Aggressively maintain focus over all windows including browsers"""
        try:
            self.dialog.lift()
            self.dialog.focus_force()
            self.dialog.attributes('-topmost', True)
        except:
            pass  # Dialog might be destroyed
        
    def setup_ui(self):
        # Main frame with more prominent styling
        main_frame = tk.Frame(self.dialog, bg="#1a1a1a")
        main_frame.pack(expand=True, fill='both', padx=25, pady=25)
        
        # Bold title with border
        title_frame = tk.Frame(main_frame, bg="#333333", relief="raised", bd=2)
        title_frame.pack(fill='x', pady=(0, 15))
        
        title_label = tk.Label(title_frame, 
                              text="🤖 AUTOMATING AI ASSISTANT INPUT", 
                              font=("Helvetica", 16, "bold"),
                              fg="#00ff00",
                              bg="#333333",
                              pady=8)
        title_label.pack()
        
        # Prominent ticker display
        ticker_frame = tk.Frame(main_frame, bg="#444444", relief="sunken", bd=2)
        ticker_frame.pack(fill='x', pady=10)
        
        ticker_label = tk.Label(ticker_frame,
                               text=f"📊 TICKER: {self.ticker}",
                               font=("Helvetica", 14, "bold"),
                               fg="#ffff00",
                               bg="#444444",
                               pady=5)
        ticker_label.pack()
        
        # Status label
        self.status_label = tk.Label(main_frame,
                                    text="🌐 Opening AI Assistant in your browser...",
                                    font=("Helvetica", 11),
                                    fg="#ffffff",
                                    bg="#1a1a1a",
                                    wraplength=380)
        self.status_label.pack(pady=8)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate', length=350)
        self.progress.pack(pady=10)
        self.progress.start(15)  # Faster animation
        
        # Prominent warning
        warning_frame = tk.Frame(main_frame, bg="#cc3300", relief="raised", bd=1)
        warning_frame.pack(fill='x', pady=(10, 0))
        
        warning_label = tk.Label(warning_frame,
                                text="⚠️ PLEASE DON'T CLICK IN YOUR BROWSER",
                                font=("Helvetica", 10, "bold"),
                                fg="#ffffff",
                                bg="#cc3300",
                                pady=3)
        warning_label.pack()
        
        # Keep dialog on top continuously
        self.dialog.after(2000, self.maintain_focus)
        self.dialog.after(4000, self.maintain_focus)
        self.dialog.after(6000, self.maintain_focus)
        
    def update_status(self, message):
        """Update the status message and maintain hard focus"""
        try:
            self.status_label.config(text=message)
            self.dialog.update()
            # Reassert dominance over all windows
            self.maintain_focus()
        except:
            pass  # Dialog might be destroyed
        
    def close(self):
        """Close the progress dialog"""
        self.progress.stop()
        self.dialog.grab_release()
        self.dialog.destroy()

class StockAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Analyzer - AI Powered v0.17")
        self.root.geometry("800x700")
        self.root.configure(bg="#f0f0f0")
        
        # Make window always on top and give it focus
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.focus_force()
        
        # After window is created, allow it to be moved behind other windows again
        self.root.after(100, lambda: self.root.attributes('-topmost', False))
        
        # AI model storage
        self.ai_model = None
        self.model_type = "api"  # "api" or "local"
        
        # Stock data for autocomplete
        self.stock_data = self.load_stock_data()
        self.suggestion_listbox = None
        self.current_suggestions = []  # Store current suggestions for selection
        self.typing_new_ticker = False  # Flag to track if user is entering new ticker
        
        self.setup_gui()
        self.setup_ai_model()
    
    def setup_gui(self):
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="📈 Stock Analyzer - AI Powered v0.17", 
                               font=("Arial", 24, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 30))
        
        # Question/Input section - more compact
        input_frame = ttk.LabelFrame(main_frame, text="🔍 Stock Search - Type ticker or company name", padding="10")
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        input_frame.columnconfigure(0, weight=1)
        input_frame.columnconfigure(1, weight=0)
        
        self.question_input = tk.Text(input_frame, height=1, 
                                     font=("Arial", 16), wrap=tk.WORD,
                                     relief="solid", borderwidth=1,
                                     bg="#ffffff",
                                     fg="#000000")
        self.question_input.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        self.question_input.insert("1.0", "Type ticker or company name (e.g., AAPL, Apple, Microsoft)")
        self.question_input.bind("<FocusIn>", self.clear_placeholder)
        self.question_input.bind("<KeyRelease>", self.on_key_release)
        self.question_input.bind("<Return>", self.on_enter_key)
        self.question_input.bind("<Button-1>", self.hide_suggestions)
        self.question_input.bind("<Double-Button-1>", self.select_all_text)
        
        # Analyze Stock Button - positioned to the right of input
        self.run_button = ttk.Button(input_frame, text="📊 ANALYZE STOCK", 
                                    command=self.run_gpt, 
                                    style="Accent.TButton")
        self.run_button.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Create main content area for stock analysis results
        content_frame = ttk.Frame(main_frame)
        content_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(0, weight=1)  # Analysis area gets all available space
        
        # Results display section (main area)
        results_frame = ttk.LabelFrame(content_frame, text="Stock Analysis Results", padding="15")
        results_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(3, weight=1)  # Changed to 3 to accommodate stock info header
        
        # Font size controls
        font_control_frame = ttk.Frame(results_frame)
        font_control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        font_control_frame.columnconfigure(0, weight=1)
        
        # Font size variable
        self.font_size = tk.IntVar(value=14)  # Start with size 14
        
        # Font size label and buttons
        font_label = ttk.Label(font_control_frame, text="Font Size:", font=("Arial", 10))
        font_label.grid(row=0, column=0, sticky=tk.W)
        
        # Font size buttons with different sizes of "A" - improved visibility
        small_btn = ttk.Button(font_control_frame, text="A", 
                              command=lambda: self.change_font_size(12),
                              width=4)
        small_btn.grid(row=0, column=1, padx=(10, 3))
        small_btn.configure(style="SmallFont.TButton")
        
        medium_btn = ttk.Button(font_control_frame, text="A", 
                               command=lambda: self.change_font_size(14),
                               width=4)
        medium_btn.grid(row=0, column=2, padx=3)
        medium_btn.configure(style="MediumFont.TButton")
        
        large_btn = ttk.Button(font_control_frame, text="A", 
                              command=lambda: self.change_font_size(16),
                              width=4)
        large_btn.grid(row=0, column=3, padx=3)
        large_btn.configure(style="LargeFont.TButton")
        
        xlarge_btn = ttk.Button(font_control_frame, text="A", 
                               command=lambda: self.change_font_size(18),
                               width=4)
        xlarge_btn.grid(row=0, column=4, padx=(3, 0))
        xlarge_btn.configure(style="XLargeFont.TButton")
        
        # Stock info header - displays ticker, company name, and price
        self.stock_info_frame = ttk.Frame(results_frame)
        self.stock_info_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(10, 10))
        self.stock_info_frame.columnconfigure(0, weight=1)
        
        self.stock_info_label = ttk.Label(self.stock_info_frame, text="", 
                                         font=("Arial", 12, "bold"))
        self.stock_info_label.grid(row=0, column=0, sticky=tk.W)
        
        self.results_display = scrolledtext.ScrolledText(results_frame, 
                                                        font=("Arial", self.font_size.get()), 
                                                        wrap=tk.WORD, 
                                                        state=tk.DISABLED,
                                                        bg="#ffffff",
                                                        fg="#000000",
                                                        height=20)
        self.results_display.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Ensure proper scrolling behavior
        self.results_display.vbar.config(command=self.results_display.yview)
        self.results_display.config(yscrollcommand=self.results_display.vbar.set)
        
        # Configure text styling with variable fonts
        self.update_text_styles()
        
        # STICKY BOTTOM: AI Assistant Section - moved to main_frame for sticky behavior
        ai_header_frame = ttk.LabelFrame(main_frame, text="🤖 AI Assistants", padding="10")
        ai_header_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        ai_header_frame.columnconfigure(0, weight=0)  # Stock Ticker Research section
        ai_header_frame.columnconfigure(1, weight=0)  # Research Links section
        ai_header_frame.columnconfigure(2, weight=1)  # Allow text to expand
        ai_header_frame.columnconfigure(3, weight=0)  # Description text
        ai_header_frame.rowconfigure(0, weight=0)  # Headers
        ai_header_frame.rowconfigure(1, weight=0)  # Buttons
        ai_header_frame.rowconfigure(2, weight=0)  # Second button row
        
        # Stock Ticker Research Section
        stock_research_label = ttk.Label(ai_header_frame, 
                                        text="Stock Ticker Research", 
                                        font=("Arial", 12, "bold"),
                                        foreground="#0099ff")
        stock_research_label.grid(row=0, column=0, padx=(0, 20), pady=(0, 5), sticky=tk.W)
        
        self.ai_button = ttk.Button(ai_header_frame, text="Stock Predictor", 
                                   command=self.open_stock_predictor,
                                   style="AI.TButton")
        self.ai_button.grid(row=1, column=0, padx=(0, 20), pady=(0, 5), sticky=tk.W)
        
        self.investing_button = ttk.Button(ai_header_frame, text="Smarter Investing", 
                                         command=self.open_smarter_investing,
                                         style="AI.TButton")
        self.investing_button.grid(row=2, column=0, padx=(0, 20), pady=(0, 5), sticky=tk.W)
        
        # Research Links Section
        research_links_label = ttk.Label(ai_header_frame, 
                                        text="Research Links", 
                                        font=("Arial", 12, "bold"),
                                        foreground="#0099ff")
        research_links_label.grid(row=0, column=1, padx=(0, 20), pady=(0, 5), sticky=tk.W)
        
        self.dividend_button = ttk.Button(ai_header_frame, text="Dividend Sniper", 
                                        command=self.open_dividend_sniper,
                                        style="AI.TButton")
        self.dividend_button.grid(row=1, column=1, padx=(0, 20), pady=(0, 5), sticky=tk.W)

        # New Stock Screener Buttons
        self.buyhold_screener_button = ttk.Button(ai_header_frame, text="Buy & Hold Value Screener", 
                                        command=lambda: webbrowser.open("https://finviz.com/screener.ashx?v=121&f=cap_microover,fa_curratio_o1.5,fa_estltgrowth_o10,fa_peg_o1,fa_roe_o15,ta_beta_o1.5,ta_sma20_pa&ft=4&o=-forwardpe"),
                                        style="AI.TButton")
        self.buyhold_screener_button.grid(row=2, column=1, padx=(0, 20), pady=(0, 5), sticky=tk.W)
        
        # Add tooltip for Buy & Hold Value Screener
        self.create_tooltip(self.buyhold_screener_button, 
                           "Focused on low PEG, strong ROE, reasonable debt, and growth potential. This is literally tailored for long-term holds. Low volatility, strong balance sheets.")

        self.dividend_growth_button = ttk.Button(ai_header_frame, text="Undervalued Dividend Growth", 
                                        command=lambda: webbrowser.open("https://finviz.com/screener.ashx?v=111&f=cap_largeover,fa_div_pos,fa_epsyoy1_o5,fa_estltgrowth_o5,fa_payoutratio_u50,fa_pe_u20,fa_peg_low&ft=4&o=-pe"),
                                        style="AI.TButton")
        self.dividend_growth_button.grid(row=3, column=1, padx=(0, 20), pady=(0, 5), sticky=tk.W)
        
        # Add tooltip for Undervalued Dividend Growth
        self.create_tooltip(self.dividend_growth_button, 
                           "Great for beginners who want steady income + long-term upside. You get dividends, low PE, growth estimates, and low payout ratios (dividends are sustainable).")

        self.bullish_growth_button = ttk.Button(ai_header_frame, text="Consistent Growth on a Bullish Trend", 
                                        command=lambda: webbrowser.open("https://finviz.com/screener.ashx?v=141&f=fa_eps5years_pos,fa_epsqoq_o20,fa_epsyoy_o25,fa_epsyoy1_o15,fa_estltgrowth_pos,fa_roe_o15,sh_instown_o10,sh_price_o15,ta_highlow52w_a90h,ta_rsi_nos50&ft=4&o=-perfytd"),
                                        style="AI.TButton")
        self.bullish_growth_button.grid(row=4, column=1, padx=(0, 20), pady=(0, 5), sticky=tk.W)
        
        # Add tooltip for Consistent Growth on a Bullish Trend
        self.create_tooltip(self.bullish_growth_button, 
                           "Combo of fundamentals + technicals. If you want stronger long-term confidence plus uptrend support, this one's for you.")
        
        # AI Assistant description text - positioned to the right of all sections
        ai_header_label = ttk.Label(ai_header_frame, 
                                   text="Launch specialized AI Assistants for advanced analysis.\nStock Ticker Research: Automated ticker input with AI analysis.\nResearch Links: General research tools and screeners.", 
                                   font=("Arial", 10, "italic"),
                                   foreground="#000000",
                                   justify=tk.LEFT,
                                   wraplength=280)
        ai_header_label.grid(row=0, column=3, rowspan=3, sticky=(tk.W, tk.N), padx=(20, 0), pady=(5, 0))
        
        # Configure button styles for better readability
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Arial", 14, "bold"))
        style.configure("AI.TButton", font=("Arial", 12, "bold"), foreground="#10a37f")
        style.configure("Theme.TButton", font=("Arial", 12, "bold"), foreground="#666666")
        
        # Configure font size button styles with better visibility
        style.configure("SmallFont.TButton", font=("Arial", 12), foreground="#2c3e50", background="#ecf0f1")
        style.configure("MediumFont.TButton", font=("Arial", 14, "bold"), foreground="#2c3e50", background="#bdc3c7")
        style.configure("LargeFont.TButton", font=("Arial", 16, "bold"), foreground="#2c3e50", background="#95a5a6")
        style.configure("XLargeFont.TButton", font=("Arial", 18, "bold"), foreground="#2c3e50", background="#7f8c8d")
        
        # Status bar - positioned at the very bottom
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                                   relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Configure main frame row weights for sticky bottom behavior
        main_frame.rowconfigure(0, weight=0)  # Header section (fixed)
        main_frame.rowconfigure(1, weight=0)  # Input section (fixed)
        main_frame.rowconfigure(2, weight=1)  # Content area (expandable)
        main_frame.rowconfigure(3, weight=0)  # AI Assistant section (sticky bottom)
        main_frame.rowconfigure(4, weight=0)  # Status bar (bottom)
        
        # Initial display
        self.display_message("Welcome to Stock Analyzer! Enter a stock symbol (e.g., AAPL, TSLA) or ask stock analysis questions.", "info")
        self.update_status("Ready - Click 'ANALYZE STOCK' to start!")
    
    def create_tooltip(self, widget, text):
        """Create a tooltip that appears on hover"""
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            # Create tooltip with attractive styling
            label = tk.Label(tooltip, text=text, 
                           background="#2c3e50", 
                           foreground="#ffffff",
                           font=("Arial", 10),
                           relief="solid", 
                           borderwidth=1,
                           wraplength=300,
                           justify="left",
                           padx=8, 
                           pady=6)
            label.pack()
            
            # Store tooltip reference
            widget.tooltip = tooltip
            
            # Auto-hide after 10 seconds
            tooltip.after(10000, lambda: tooltip.destroy() if tooltip.winfo_exists() else None)
        
        def hide_tooltip(event):
            if hasattr(widget, 'tooltip'):
                try:
                    widget.tooltip.destroy()
                except:
                    pass
        
        # Bind hover events
        widget.bind("<Enter>", show_tooltip)
        widget.bind("<Leave>", hide_tooltip)
    
    def setup_ai_model(self):
        """Setup free AI model"""
        if TRANSFORMERS_AVAILABLE:
            try:
                # Try to load a small local model
                self.update_status("Loading AI model...")
                threading.Thread(target=self._load_local_model, daemon=True).start()
            except Exception as e:
                self.model_type = "api"
                self.update_status("Using free online AI")
        else:
            self.model_type = "api"
            self.update_status("Using free online AI (install transformers for local AI)")
    
    def load_stock_data(self):
        """Load stock data from CSV file"""
        stock_data = []
        csv_path = os.path.join(os.path.dirname(__file__), "stock_data.csv")
        
        try:
            with open(csv_path, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    stock_data.append({
                        'ticker': row['ticker'].upper(),
                        'company': row['company_name']
                    })
        except FileNotFoundError:
            self.update_status("Stock data file not found")
        except Exception as e:
            self.update_status(f"Error loading stock data: {str(e)}")
        
        return stock_data
    
    def _load_local_model(self):
        """Load local AI model in background"""
        try:
            # Load a smaller, faster model
            self.ai_model = pipeline("text-generation", 
                                   model="microsoft/DialoGPT-small",
                                   device=-1)  # Use CPU
            self.model_type = "local"
            self.root.after(0, lambda: self.update_status("✅ Local AI model loaded!"))
        except Exception as e:
            self.model_type = "api"
            self.root.after(0, lambda: self.update_status("Using free online AI"))
    
    def clear_placeholder(self, event):
        """Clear placeholder text and auto-clear previous ticker when user clicks in input"""
        current_text = self.question_input.get("1.0", tk.END).strip()
        
        if current_text == "Type ticker or company name (e.g., AAPL, Apple, Microsoft)":
            # Clear placeholder text
            self.question_input.delete("1.0", tk.END)
        elif not self.typing_new_ticker:
            # Auto-clear any existing ticker/content when user clicks to enter new one
            self.question_input.delete("1.0", tk.END)
        
        # Set flag that user is now typing a new ticker
        self.typing_new_ticker = True
    
    def select_all_text(self, event):
        """Select all text in the input box when double-clicked"""
        # Clear placeholder text first if it's there
        current_text = self.question_input.get("1.0", tk.END).strip()
        if current_text == "Enter stock symbol (e.g., AAPL, TSLA) or company name...":
            self.question_input.delete("1.0", tk.END)
            return
        
        # Select all text in the input box
        self.question_input.tag_add(tk.SEL, "1.0", tk.END)
        self.question_input.mark_set(tk.INSERT, "1.0")
        self.question_input.see(tk.INSERT)
        
        # Set flag that user is now typing a new ticker
        self.typing_new_ticker = True
        
        # Hide any suggestions
        self.hide_suggestions()
        
        # Return "break" to prevent default double-click behavior
        return "break"
    
    def on_key_release(self, event):
        """Handle key release events for autocomplete and uppercase conversion"""
        # Hide suggestions on certain keys
        if event.keysym in ['Return', 'Tab', 'Escape']:
            self.hide_suggestions()
            return
        
        current_pos = self.question_input.index(tk.INSERT)
        content = self.question_input.get("1.0", tk.END)
        
        # Don't process placeholder text
        if content.strip() == "Enter stock symbol (e.g., AAPL, TSLA) or company name...":
            return
        
        # Convert to uppercase
        upper_content = content.upper()
        
        # Only update if there's a change to avoid cursor jumping
        if content != upper_content:
            self.question_input.delete("1.0", tk.END)
            self.question_input.insert("1.0", upper_content)
            self.question_input.mark_set(tk.INSERT, current_pos)
        
        # Show suggestions based on current input
        self.show_suggestions()
    
    def show_suggestions(self):
        """Show stock ticker and company name suggestions with Finviz-style search"""
        content = self.question_input.get("1.0", tk.END).strip()
        
        if len(content) < 1 or content.upper() == "TYPE TICKER OR COMPANY NAME (E.G., AAPL, APPLE, MICROSOFT)":
            self.hide_suggestions()
            return
        
        # Use the advanced search function similar to web app
        matches = self.search_stocks(content, max_results=8)
        
        if matches:
            self.display_suggestions(matches)
        else:
            self.hide_suggestions()
    
    def search_stocks(self, query, max_results=8):
        """
        Advanced stock search with Finviz-style prioritization
        Returns filtered results with match types and smart ranking
        """
        if not query or len(query) < 1:
            return []
        
        query = query.upper().strip()
        results = []
        
        # Exact ticker matches first (highest priority)
        for stock in self.stock_data:
            if stock['ticker'].upper() == query:
                results.append({
                    'display': f"{stock['ticker']} - {stock['company']}",
                    'ticker': stock['ticker'],
                    'company': stock['company'],
                    'match_type': 'exact_ticker',
                    'icon': '🎯'
                })
        
        # Company name exact word matches (e.g., "APPLE" should find "Apple Inc")
        if len(results) < max_results:
            for stock in self.stock_data:
                if stock['ticker'].upper() not in [r['ticker'].upper() for r in results]:
                    company_words = stock['company'].upper().split()
                    if any(word == query for word in company_words):
                        results.append({
                            'display': f"{stock['ticker']} - {stock['company']}",
                            'ticker': stock['ticker'],
                            'company': stock['company'],
                            'match_type': 'company_exact_word',
                            'icon': '🎯'
                        })
                        if len(results) >= max_results:
                            break
        
        # Ticker starts with query
        if len(results) < max_results:
            for stock in self.stock_data:
                if (stock['ticker'].upper().startswith(query) and 
                    stock['ticker'].upper() not in [r['ticker'].upper() for r in results]):
                    results.append({
                        'display': f"{stock['ticker']} - {stock['company']}",
                        'ticker': stock['ticker'],
                        'company': stock['company'],
                        'match_type': 'ticker_starts',
                        'icon': '📈'
                    })
                    if len(results) >= max_results:
                        break
        
        # Company name contains query
        if len(results) < max_results:
            for stock in self.stock_data:
                if (query in stock['company'].upper() and 
                    stock['ticker'].upper() not in [r['ticker'].upper() for r in results]):
                    results.append({
                        'display': f"{stock['ticker']} - {stock['company']}",
                        'ticker': stock['ticker'],
                        'company': stock['company'],
                        'match_type': 'company_contains',
                        'icon': '🏢'
                    })
                    if len(results) >= max_results:
                        break
        
        # Ticker contains query (partial matches)
        if len(results) < max_results:
            for stock in self.stock_data:
                if (query in stock['ticker'].upper() and 
                    stock['ticker'].upper() not in [r['ticker'].upper() for r in results]):
                    results.append({
                        'display': f"{stock['ticker']} - {stock['company']}",
                        'ticker': stock['ticker'],
                        'company': stock['company'],
                        'match_type': 'ticker_contains',
                        'icon': '📊'
                    })
                    if len(results) >= max_results:
                        break
        
        return results
    
    def display_suggestions(self, suggestions):
        """Display enhanced suggestion dropdown with Finviz-style formatting"""
        if self.suggestion_listbox:
            self.suggestion_listbox.destroy()
        
        # Create suggestion listbox with enhanced styling
        max_height = min(len(suggestions), 6)  # Show up to 6 suggestions at once
        self.suggestion_listbox = tk.Listbox(self.root, 
                                           height=max_height,
                                           font=("Arial", 11), 
                                           bg="#ffffff",           # White background
                                           fg="#2c3e50",           # Dark blue text
                                           selectbackground="#007acc",  # Blue selection
                                           selectforeground="#ffffff",  # White text when selected
                                           highlightthickness=1,
                                           highlightcolor="#007acc",
                                           relief="solid",
                                           borderwidth=1,
                                           activestyle="dotbox")    # Better selection style
        
        # Add enhanced suggestions with icons and formatting
        for suggestion in suggestions:
            icon = suggestion.get('icon', '📊')
            ticker = suggestion['ticker']
            company = suggestion['company']
            
            # Truncate company name if too long for better display
            if len(company) > 40:
                company = company[:37] + "..."
            
            # Format based on match type for better visual hierarchy
            if suggestion['match_type'] in ['exact_ticker', 'company_exact_word']:
                # Highlight exact matches
                display_text = f"{icon} {ticker} - {company} ★"
            else:
                display_text = f"{icon} {ticker} - {company}"
            
            self.suggestion_listbox.insert(tk.END, display_text)
        
        # Position the listbox below the input with better positioning
        input_x = self.question_input.winfo_rootx()
        input_y = self.question_input.winfo_rooty() + self.question_input.winfo_height()
        input_width = max(self.question_input.winfo_width(), 400)  # Minimum width for readability
        
        # Calculate position relative to root window
        rel_x = input_x - self.root.winfo_rootx()
        rel_y = input_y - self.root.winfo_rooty()
        
        self.suggestion_listbox.place(x=rel_x, y=rel_y, width=input_width)
        
        # Bind enhanced selection events
        self.suggestion_listbox.bind("<Double-Button-1>", self.on_suggestion_select)
        self.suggestion_listbox.bind("<Return>", self.on_suggestion_select)
        self.suggestion_listbox.bind("<Button-1>", self.on_suggestion_click)
        
        # Store suggestions data for selection handling
        self.current_suggestions = suggestions
    
    def hide_suggestions(self, event=None):
        """Hide suggestion dropdown"""
        if self.suggestion_listbox:
            self.suggestion_listbox.destroy()
            self.suggestion_listbox = None
    
    def on_suggestion_select(self, event):
        """Handle suggestion selection (double-click or Enter)"""
        try:
            selection_index = self.suggestion_listbox.curselection()[0]
            selected_suggestion = self.current_suggestions[selection_index]
            ticker = selected_suggestion['ticker']
            
            # Clear input and insert selected ticker
            self.question_input.delete("1.0", tk.END)
            self.question_input.insert("1.0", ticker)
            
            # Hide suggestions
            self.hide_suggestions()
            
            # Reset typing flag since user selected from suggestions
            self.typing_new_ticker = False
            
            # Focus back to input
            self.question_input.focus_set()
            
            # Auto-analyze if it's an exact match (like the web app)
            if selected_suggestion['match_type'] in ['exact_ticker', 'company_exact_word']:
                self.root.after(100, self.run_gpt)  # Small delay to ensure UI updates
                
        except (IndexError, AttributeError):
            # Handle case where no selection or suggestions data is missing
            pass
    
    def on_suggestion_click(self, event):
        """Handle single click on suggestion (select but don't auto-run)"""
        try:
            selection_index = self.suggestion_listbox.curselection()[0]
            selected_suggestion = self.current_suggestions[selection_index]
            ticker = selected_suggestion['ticker']
            
            # Clear input and insert selected ticker
            self.question_input.delete("1.0", tk.END)
            self.question_input.insert("1.0", ticker)
            
            # Hide suggestions
            self.hide_suggestions()
            
            # Reset typing flag since user selected from suggestions
            self.typing_new_ticker = False
            
            # Focus back to input
            self.question_input.focus_set()
            
        except (IndexError, AttributeError):
            # Handle case where no selection or suggestions data is missing
            pass
    
    def on_enter_key(self, event):
        """Execute analysis when Enter key is pressed"""
        # Prevent default behavior (new line) and execute the button
        self.run_gpt()
        return "break"  # This prevents the default Enter behavior
    
    def open_stock_predictor(self):
        """Open your custom Stock Predictor AI Assistant and automatically input the ticker"""
        question = self.question_input.get("1.0", tk.END).strip()
        
        # Clear placeholder text if present
        if question == "Enter stock symbol (e.g., AAPL, TSLA) or company name...":
            question = ""
        
        # Extract ticker from the question (look for stock symbols)
        import re
        ticker = ""
        if question:
            # Find potential stock tickers (1-5 letter combinations, uppercase, with optional dots)
            ticker_matches = re.findall(r'\b[A-Z]{1,5}(?:\.[A-Z])?\b', question.upper())
            if ticker_matches:
                ticker = self.find_ticker_from_company_name(ticker_matches[0])
            else:
                # If no clear ticker, try to resolve the whole question as company name
                ticker = self.find_ticker_from_company_name(question.strip())
        
        print(f"🔍 Debug - Original question: '{question}'")  # Debug
        print(f"🔍 Debug - Extracted ticker: '{ticker}'")  # Debug
        
        # Your custom Stock Predictor AI Assistant URL
        custom_ai_url = "https://chatgpt.com/g/g-686c5fc3dd948191a0ff9c14cecda1b4-stock-predictor-prompt-gpt"
        
        try:
            if ticker:
                # Show progress dialog during automation
                progress_dialog = AutomationProgressDialog(self.root, ticker)
                
                def run_automation():
                    """Run automation in separate thread to prevent UI blocking"""
                    try:
                        progress_dialog.update_status("🌐 Opening AI Assistant in your browser...")
                        
                        # Use automation to enter ticker + "STOCK TICKER"
                        ticker_with_text = f"{ticker} STOCK TICKER"
                        success = self.use_existing_browser_with_progress(custom_ai_url, ticker_with_text, progress_dialog)
                        
                        # Schedule UI updates on main thread
                        self.root.after(0, lambda: self.automation_completed(success, ticker, custom_ai_url, progress_dialog))
                        
                    except Exception as e:
                        # Schedule error handling on main thread
                        self.root.after(0, lambda: self.automation_error(str(e), ticker, custom_ai_url, progress_dialog))
                
                # Start automation in background thread
                automation_thread = threading.Thread(target=run_automation, daemon=True)
                automation_thread.start()
            else:
                # No ticker found, just open the AI Assistant
                webbrowser.open(custom_ai_url)
                self.update_status("🚀 Stock Predictor AI opened - Enter any ticker for analysis!")

                
        except Exception as e:
            self.update_status(f"❌ Error: {str(e)}")
            # Fallback to manual method
            if ticker:
                self.fallback_ai_method(custom_ai_url, ticker)
            else:
                webbrowser.open(custom_ai_url)
    
    def automation_completed(self, success, ticker, url, progress_dialog):
        """Handle Stock Predictor automation completion on main thread"""
        progress_dialog.close()
        
        if success == True:
            # Just update the status bar, don't show message
            self.update_status(f"✅ Stock Predictor AI automated for {ticker} - Check your browser!")
        elif success == "clipboard":
            # Clipboard method was used
            self.update_status(f"📋 {ticker} copied to clipboard - Paste in Stock Predictor AI!")
        else:
            # Automation failed, use manual fallback
            self.update_status(f"🔄 Automation failed, using manual method...")
            self.fallback_ai_method(url, ticker)
    
    def automation_error(self, error, ticker, url, progress_dialog):
        """Handle Stock Predictor automation error on main thread"""
        progress_dialog.close()
        self.update_status(f"❌ Error: {error}")
        # Fallback to manual method
        self.fallback_ai_method(url, ticker)

    def automate_gpt_input(self, url, ticker):
        """Automate the AI Assistant input using browser automation with improved reliability"""
        try:
            # Try to import selenium for browser automation
            from selenium import webdriver
            from selenium.webdriver.common.by import By
            from selenium.webdriver.common.keys import Keys
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.chrome.service import Service
            from selenium.webdriver.common.action_chains import ActionChains
            import time
            
            print(f"🤖 Starting AI Assistant automation for: {ticker}")
            
            # Try to use existing browser window first
            try:
                return self.try_applescript_automation(url, ticker)
            except Exception as e:
                print(f"AppleScript failed, trying Selenium: {e}")
            
            # Try to use webdriver-manager for automatic driver management
            try:
                from webdriver_manager.chrome import ChromeDriverManager
                service = Service(ChromeDriverManager().install())
            except ImportError:
                # Fallback to system ChromeDriver
                service = None
            
            # Set up Chrome options for better compatibility
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--allow-running-insecure-content")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Create the driver
            if service:
                driver = webdriver.Chrome(service=service, options=chrome_options)
            else:
                driver = webdriver.Chrome(options=chrome_options)
            
            # Execute script to hide webdriver property
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print(f"🌐 Opening URL: {url}")
            driver.get(url)
            
            # Wait longer for AI Assistant to fully load
            print("⏳ Waiting for page to load...")
            time.sleep(8)  # Increased wait time
            
            # Check if the page loaded properly
            current_url = driver.current_url.lower()
            if "chatgpt" not in current_url and "openai" not in current_url:
                print(f"⚠️ Warning: URL might have redirected. Current URL: {driver.current_url}")
            
            # Wait for the page to load and find the input field with longer timeout
            wait = WebDriverWait(driver, 45)  # Increased timeout
            
            # Updated selectors for current ChatGPT interface (2024/2025)
            input_selectors = [
                # Most common current selectors
                "textarea[placeholder*='Message']",
                "textarea[data-testid='textbox']",
                "div[contenteditable='true'][data-testid='textbox']",
                "textarea[placeholder*='Ask']",
                "textarea[id*='prompt']",
                "#prompt-textarea",
                
                # Fallback selectors
                "div[contenteditable='true']",
                "textarea",
                "[data-testid='textbox']",
                "div[role='textbox']",
                "textarea[role='textbox']",
                
                # Additional modern selectors
                "textarea[placeholder*='Type a message']",
                "textarea[placeholder*='Send a message']",
                "div[contenteditable='true'][role='textbox']"
            ]
            
            input_element = None
            for i, selector in enumerate(input_selectors):
                try:
                    print(f"🔍 Trying selector {i+1}/{len(input_selectors)}: {selector}")
                    
                    # Wait a bit between attempts
                    time.sleep(3)
                    
                    # Check if window is still open
                    if len(driver.window_handles) == 0:
                        print("❌ Browser window was closed")
                        return False
                    
                    # Try to find the element
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        for element in elements:
                            if element.is_displayed() and element.is_enabled():
                                # Check if element is actually in viewport
                                location = element.location
                                size = element.size
                                if location['y'] >= 0 and size['height'] > 0:
                                    input_element = element
                                    print(f"✅ Found valid input field with selector: {selector}")
                                    break
                        if input_element:
                            break
                    
                except Exception as e:
                    print(f"❌ Selector {selector} failed: {str(e)[:100]}")
                    continue
            
            if input_element:
                try:
                    print("🎯 Found input field, attempting to enter ticker...")
                    
                    # Scroll to element and ensure it's visible
                    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", input_element)
                    time.sleep(3)
                    
                    # Use ActionChains for more reliable interaction
                    actions = ActionChains(driver)
                    
                    # Click the input field to focus it
                    actions.move_to_element(input_element).click().perform()
                    time.sleep(2)
                    
                    # Clear any existing content with multiple methods
                    try:
                        input_element.clear()
                        time.sleep(1)
                        # Select all and delete as backup
                        actions.key_down(Keys.COMMAND).send_keys('a').key_up(Keys.COMMAND).send_keys(Keys.DELETE).perform()
                        time.sleep(1)
                    except:
                        pass
                    
                    # Type the ticker with more realistic timing
                    ticker_text = f"{ticker} stock analysis"
                    print(f"⌨️ Entering: {ticker_text}")
                    
                    for char in ticker_text:
                        input_element.send_keys(char)
                        time.sleep(0.1)  # Human-like typing speed
                    
                    time.sleep(2)
                    
                    # Submit the form
                    print("📤 Submitting ticker...")
                    input_element.send_keys(Keys.RETURN)
                    
                    print("✅ Automation successful! Browser will stay open for results.")
                    self.update_status(f"✅ Successfully automated {ticker} input to AI Assistant!")
                    
                    # Don't close the driver - let user see results
                    return True
                    
                except Exception as e:
                    print(f"❌ Error during input automation: {e}")
                    try:
                        driver.quit()
                    except:
                        pass
                    return False
            else:
                print("❌ Could not find input field with any selector")
                try:
                    driver.quit()
                except:
                    pass
                return False
                
        except ImportError as e:
            print(f"❌ Selenium not available: {e}")
            # Selenium not installed, try alternative method
            return self.try_applescript_automation(url, ticker)
        except Exception as e:
            print(f"❌ Browser automation error: {e}")
            try:
                if 'driver' in locals():
                    driver.quit()
            except:
                pass
            return False
    
    def try_applescript_automation(self, url, ticker):
        """Try AppleScript automation on macOS as fallback - Enhanced for better reliability"""
        try:
            import subprocess
            import time
            
            print("🍎 Trying enhanced AppleScript automation...")
            
            # Open the URL first
            webbrowser.open(url)
            time.sleep(6)  # Wait longer for page to load
            
            # Enhanced AppleScript with better browser detection and input methods
            ticker_with_context = f"{ticker} stock analysis"
            
            # Build AppleScript without f-string to avoid brace issues
            applescript = '''
            tell application "System Events"
                -- Wait for page to fully load
                delay 6
                
                -- Find and activate any available browser
                set browserActivated to false
                set browserName to ""
                
                -- Try different browsers in order of preference
                set browserList to {"Google Chrome", "Safari", "Microsoft Edge", "Firefox", "Arc"}
                
                repeat with browserApp in browserList
                    try
                        tell application browserApp to activate
                        set browserActivated to true
                        set browserName to browserApp
                        exit repeat
                    on error
                        -- Browser not available, try next one
                    end try
                end repeat
                
                if not browserActivated then
                    error "No supported browser found"
                end if
                
                delay 3
                
                -- Multiple methods to find and interact with the input field
                set success to false
                
                -- Method 1: Smart click positioning (works well with ChatGPT layout)
                try
                    -- Get the frontmost window bounds
                    set frontApp to first application process whose frontmost is true
                    set frontWindow to front window of frontApp
                    set windowBounds to bounds of frontWindow
                    
                    -- Calculate click position in bottom area of window
                    set windowWidth to (item 3 of windowBounds) - (item 1 of windowBounds)
                    set windowHeight to (item 4 of windowBounds) - (item 2 of windowBounds)
                    set centerX to (item 1 of windowBounds) + (windowWidth / 2)
                    set inputY to (item 2 of windowBounds) + (windowHeight * 0.85)
                    
                    -- Click in the input area
                    click at {centerX, inputY}
                    delay 2
                    
                    -- Clear any existing content and type ticker
                    keystroke "a" using command down
                    delay 0.5
                    keystroke "TICKER_PLACEHOLDER"
                    delay 2
                    
                    -- Submit
                    key code 36  -- Return key
                    set success to true
                on error
                    -- Method 1 failed, try Method 2
                end try
                
                -- Method 2: Tab navigation if click method fails
                if not success then
                    try
                        -- Use tab navigation to find input field
                        repeat 8 times
                            key code 48  -- Tab key
                            delay 0.4
                        end repeat
                        
                        -- Try typing in the focused element
                        keystroke "TICKER_PLACEHOLDER"
                        delay 2
                        key code 36  -- Return
                        set success to true
                    on error
                        -- Method 2 failed, try Method 3
                    end try
                end if
                
                -- Method 3: Alternative click positions
                if not success then
                    try
                        -- Try clicking in different areas of the bottom region
                        set frontApp to first application process whose frontmost is true
                        set frontWindow to front window of frontApp
                        set windowBounds to bounds of frontWindow
                        set centerX to (item 1 of windowBounds) + ((item 3 of windowBounds) - (item 1 of windowBounds)) / 2
                        set bottomY to (item 2 of windowBounds) + ((item 4 of windowBounds) - (item 2 of windowBounds)) * 0.9
                        
                        click at {centerX, bottomY}
                        delay 2
                        
                        -- Clear and type
                        keystroke "a" using command down
                        delay 0.5
                        keystroke "TICKER_PLACEHOLDER"
                        delay 2
                        key code 36  -- Return
                        set success to true
                    on error
                        -- All methods failed
                    end try
                end if
                
                return success
            end tell
            '''
            
            # Replace placeholder with actual ticker text
            applescript = applescript.replace("TICKER_PLACEHOLDER", ticker_with_context)
            
            # Execute AppleScript with longer timeout
            result = subprocess.run(['osascript', '-e', applescript], 
                                  capture_output=True, text=True, timeout=45)
            
            if result.returncode == 0 and "true" in result.stdout:
                print("✅ Enhanced AppleScript automation successful!")
                self.update_status(f"✅ Successfully automated {ticker} input to AI Assistant!")
                return True
            else:
                print(f"❌ AppleScript failed: {result.stderr}")
                return False
            
        except subprocess.TimeoutExpired:
            print("❌ AppleScript automation timed out")
            return False
        except Exception as e:
            print(f"❌ AppleScript automation error: {e}")
            return False
    
    def fallback_ai_method(self, url, ticker):
        """Enhanced fallback method - copy to clipboard and open browser with clear instructions"""
        ticker_with_text = f"{ticker} stock analysis and price prediction"
        try:
            import pyperclip
            pyperclip.copy(ticker_with_text)
            clipboard_success = True
        except ImportError:
            clipboard_success = False
        
        # Open the AI Assistant in browser
        webbrowser.open(url)
        
        # Just update status bar, don't show detailed message
        if clipboard_success:
            self.update_status(f"🌐 AI Assistant opened - '{ticker}' copied to clipboard!")
        else:
            self.update_status(f"🌐 AI Assistant opened - Type '{ticker} stock analysis' in browser!")
        
        return True  # Always return True for fallback method
    
    def open_dividend_sniper(self):
        """Open your custom Dividend Sniper AI Assistant"""
        # Your custom Dividend Sniper AI Assistant URL
        dividend_ai_url = "https://chatgpt.com/g/g-6878fe277c5c819180211289d9e16148-high-yield-dividend-sniper"
        
        # The suggested query to use
        suggested_query = "Find and analyze the top 5 U.S. high-yield dividend stocks that meet your safety criteria."
        
        try:
            # Copy the suggested query to clipboard
            try:
                import pyperclip
                pyperclip.copy(suggested_query)
                clipboard_success = True
            except ImportError:
                clipboard_success = False
            
            # Simply open the Dividend Sniper GPT URL
            webbrowser.open(dividend_ai_url)
            
            # Just update status bar, don't show message
            if clipboard_success:
                self.update_status("💰 Dividend Sniper AI opened - Query copied to clipboard!")
            else:
                self.update_status("💰 Dividend Sniper AI opened - Check your browser!")
                
        except Exception as e:
            self.update_status(f"❌ Could not open browser: {str(e)}")
            messagebox.showerror("Browser Error", f"Could not open browser.\n\nPlease manually visit:\n{dividend_ai_url}")
            messagebox.showinfo("Suggested Query", f"Query to use: {suggested_query}")
    
    def open_smarter_investing(self):
        """Open the 9 Prompt for Smarter Investing AI Assistant and automatically input the ticker"""
        # Get the current ticker from input
        question = self.question_input.get("1.0", tk.END).strip()
        
        if not question or question == "Enter stock symbol (e.g., AAPL, TSLA) or company name...":
            # No ticker provided, just open the AI assistant
            investing_url = "https://chatgpt.com/g/g-687b911701a08191aadd69c345a67d17-9-prompts-for-smarter-investing"
            webbrowser.open(investing_url)
            self.update_status("💡 Smarter Investing AI opened - Check your browser!")
            return
        
        # Convert stock tickers to uppercase automatically
        ticker_input = self._format_stock_input(question)
        ticker = self._get_best_ticker_match(ticker_input)
        
        if ticker:
            # Create progress dialog
            def run_automation():
                try:
                    progress_dialog = AutomationProgressDialog(self.root, ticker)
                    
                    # Update status
                    self.root.after(0, lambda: self.update_status(f"🤖 Automating 9 Prompt for Smarter Investing with {ticker}..."))
                    
                    # Your 9 Prompt for Smarter Investing AI Assistant URL  
                    investing_url = "https://chatgpt.com/g/g-687b911701a08191aadd69c345a67d17-9-prompts-for-smarter-investing"
                    
                    # Wait for browser to open
                    self.root.after(0, lambda: progress_dialog.update_status("🌐 Opening AI Assistant in your browser..."))
                    
                    # Use automation to enter ticker + "STOCK TICKER"
                    ticker_with_text = f"{ticker} STOCK TICKER"
                    success = self.use_existing_browser_with_progress(investing_url, ticker_with_text, progress_dialog)
                    
                    # Return to main thread for completion
                    self.root.after(0, lambda: self.investing_automation_completed(success, ticker, investing_url, progress_dialog))
                    
                except Exception as e:
                    # Handle errors on main thread
                    self.root.after(0, lambda: self.investing_automation_error(str(e), ticker, investing_url, progress_dialog))
            
            # Run automation in background thread
            thread = threading.Thread(target=run_automation)
            thread.daemon = True
            thread.start()
        else:
            # No ticker found, just open the AI Assistant
            investing_url = "https://chatgpt.com/g/g-687b911701a08191aadd69c345a67d17-9-prompts-for-smarter-investing"
            webbrowser.open(investing_url)
            self.update_status("💡 Smarter Investing AI opened - No ticker detected from input!")

    def investing_automation_completed(self, success, ticker, url, progress_dialog):
        """Handle investing AI assistant automation completion on main thread"""
        progress_dialog.close()
        
        if success == True:
            # Just update the status bar, don't show message
            self.update_status(f"✅ Smarter Investing AI automated for {ticker} - Check your browser!")
        elif success == "clipboard":
            # Clipboard method was used
            self.update_status(f"📋 {ticker} copied to clipboard - Paste in Smarter Investing AI!")
        else:
            # Automation failed, use manual fallback
            self.update_status(f"🔄 Automation failed, using manual method...")
            self.investing_fallback_method(url, ticker)
    
    def investing_automation_error(self, error, ticker, url, progress_dialog):
        """Handle investing AI assistant automation error on main thread"""
        progress_dialog.close()
        self.update_status(f"❌ Error: {error}")
        # Fallback to manual method
        self.fallback_ai_method(url, ticker)
    
    def _get_best_ticker_match(self, input_text):
        """Get the best ticker match from input text"""
        # First try direct ticker match (1-5 letter uppercase, with optional dots)
        ticker_matches = re.findall(r'\b[A-Z]{1,5}(?:\.[A-Z])?\b', input_text.upper())
        if ticker_matches:
            potential_ticker = ticker_matches[0]
            # Check if it's a valid ticker in our database
            for stock in self.stock_data:
                if stock['ticker'] == potential_ticker:
                    return potential_ticker
            # If not found in database, still return it as it might be valid
            return potential_ticker
        
        # If no direct ticker match, try company name resolution
        return self.find_ticker_from_company_name(input_text.strip())
    
    def use_existing_browser_with_progress(self, url, ticker_text, progress_dialog):
        """Use existing browser window with progress updates - RESTORED WORKING VERSION"""
        try:
            import subprocess
            import time
            
            progress_dialog.update_status("🌐 Opening AI Assistant in your browser...")
            print(f"🌐 Using existing browser window...")
            print(f"🎯 Ticker to enter: '{ticker_text}'")  # Debug output
            
            # First, open the URL (this will use existing browser or open new tab)
            webbrowser.open(url)
            time.sleep(4)  # Wait for ChatGPT to load
            
            progress_dialog.update_status("🤖 Attempting to input ticker automatically...")
            
            # Use AppleScript to type in the existing browser - RESTORED WORKING VERSION
            applescript_template = '''
            tell application "System Events"
                -- Wait for page to load completely
                delay 4
                
                -- Try to activate the browser (works for Chrome, Safari, Firefox, etc)
                set browserActivated to false
                try
                    tell application "Google Chrome" to activate
                    set browserActivated to true
                on error
                    try
                        tell application "Safari" to activate
                        set browserActivated to true
                    on error
                        try
                            tell application "Firefox" to activate
                            set browserActivated to true
                        on error
                            try
                                tell application "Microsoft Edge" to activate
                                set browserActivated to true
                            end try
                        end try
                    end try
                end try
                
                if not browserActivated then error "No browser found"
                
                delay 2
                
                -- Try multiple methods to find the input field
                set inputFound to false
                
                -- Method 1: Simple click and type (most reliable for ChatGPT)
                try
                    -- Click in the bottom area where ChatGPT input typically is
                    tell application "System Events"
                        -- Get the frontmost window
                        set frontWindow to front window of (first application process whose frontmost is true)
                        set windowBounds to bounds of frontWindow
                        
                        -- Calculate click position (bottom center of window)
                        set windowWidth to (item 3 of windowBounds) - (item 1 of windowBounds)
                        set windowHeight to (item 4 of windowBounds) - (item 2 of windowBounds)
                        set clickX to (item 1 of windowBounds) + (windowWidth / 2)
                        set clickY to (item 2 of windowBounds) + (windowHeight * 0.85)
                        
                        -- Click to focus the input area
                        click at {clickX, clickY}
                        delay 1.5
                        
                        -- Clear any existing content and type ticker
                        keystroke "a" using command down
                        delay 0.5
                        keystroke "TICKER_PLACEHOLDER"
                        delay 1
                        key code 36  -- Return key
                        set inputFound to true
                    end tell
                on error
                    -- Method 2: Try Tab navigation if direct click fails
                    try
                        -- Press Tab several times to find the input field
                        repeat 3 times
                            key code 48  -- Tab key
                            delay 0.3
                        end repeat
                        
                        -- Clear any existing content and type ticker
                        keystroke "a" using command down
                        delay 0.5
                        keystroke "TICKER_PLACEHOLDER"
                        delay 1
                        key code 36  -- Return
                        set inputFound to true
                    on error
                        -- Method 3: Simple keystroke approach (assume focus is already correct)
                        try
                            keystroke "TICKER_PLACEHOLDER"
                            delay 1
                            key code 36  -- Return
                            set inputFound to true
                        end try
                    end try
                end try
                
                if inputFound then
                    return "success"
                else
                    return "failed"
                end if
                
            end tell
            '''
            
            # Replace the placeholder with the actual ticker
            applescript = applescript_template.replace("TICKER_PLACEHOLDER", ticker_text)
            
            progress_dialog.update_status("🍎 Using working AppleScript automation...")
            
            # Execute AppleScript with longer timeout
            result = subprocess.run(['osascript', '-e', applescript], 
                                  capture_output=True, text=True, timeout=20)
            
            if result.returncode == 0 and "success" in result.stdout:
                print("✅ Successfully automated ticker input!")
                progress_dialog.update_status("✅ Automation successful!")
                time.sleep(2)
                return True
            else:
                print(f"❌ AppleScript automation didn't work as expected")
                print(f"stdout: {result.stdout}")
                print(f"stderr: {result.stderr}")
                # Try clipboard fallback
                progress_dialog.update_status("📋 Using clipboard method...")
                try:
                    import pyperclip
                    pyperclip.copy(ticker_text)
                    progress_dialog.update_status("✅ Ticker copied to clipboard!")
                    time.sleep(1)
                    return "clipboard"
                except ImportError:
                    pass
                return False
            
        except subprocess.TimeoutExpired:
            print("❌ AppleScript automation timed out")
            progress_dialog.update_status("⏰ Automation timed out...")
            return False
        except Exception as e:
            print(f"❌ AppleScript automation error: {e}")
            return False
    
    def run_gpt(self):
        """Main function to run Stock Analysis AI"""
        question = self.question_input.get("1.0", tk.END).strip()
        
        if not question or question == "Type ticker or company name (e.g., AAPL, Apple, Microsoft)":
            messagebox.showwarning("No Input", "Please enter a stock symbol or company name!")
            return
        
        # Reset typing flag after analysis
        self.typing_new_ticker = False
        
        # Convert stock tickers to uppercase automatically
        question = self._format_stock_input(question)
        
        # Disable button and show loading
        self.run_button.config(state="disabled", text="🔄 Analyzing...")
        self.update_status("Running stock analysis...")
        
        # Clear previous results
        self.results_display.config(state=tk.NORMAL)
        self.results_display.delete("1.0", tk.END)
        self.results_display.config(state=tk.DISABLED)
        
        # Run AI in separate thread
        if self.model_type == "local" and self.ai_model:
            thread = threading.Thread(target=self._call_local_ai, args=(question,))
        else:
            thread = threading.Thread(target=self._call_stock_analyzer_api, args=(question,))
        thread.daemon = True
        thread.start()
    
    def _format_stock_input(self, input_text):
        """Clean and format stock ticker input using advanced validation"""
        # First, try to clean the entire input as a potential ticker
        cleaned_ticker = clean_ticker(input_text)
        
        # If it's a valid ticker, return it
        if validate_ticker(cleaned_ticker):
            return cleaned_ticker
        
        # Otherwise, look for potential tickers in the text and clean them
        words = input_text.split()
        for i, word in enumerate(words):
            cleaned_word = clean_ticker(word)
            if validate_ticker(cleaned_word):
                words[i] = cleaned_word
        
        return ' '.join(words)
    
    def _call_local_ai(self, question):
        """Call local AI model"""
        try:
            # Use local transformers model
            response = self.ai_model(question, max_length=200, num_return_sequences=1)
            ai_response = response[0]['generated_text']
            
            # Clean up the response
            if question in ai_response:
                ai_response = ai_response.replace(question, "").strip()
            
            self.root.after(0, self._display_ai_response, ai_response, None)
            
        except Exception as e:
            error_msg = f"Error with local AI: {str(e)}"
            self.root.after(0, self._display_ai_response, None, error_msg)
    
    def _call_stock_analyzer_api(self, question):
        """Call stock analysis with enhanced real data analysis"""
        try:
            print(f"Debug: Analyzing question: {question}")  # Debug output
            
            # Always use comprehensive real data analysis for better reliability
            fallback_response = self._create_comprehensive_analysis(question)
            self.root.after(0, self._display_ai_response, fallback_response, None)
            
        except Exception as e:
            print(f"Debug: Exception occurred: {str(e)}")  # Debug output
            # Ensure we always provide some analysis
            fallback_response = self._create_comprehensive_analysis(question)
            self.root.after(0, self._display_ai_response, fallback_response, None)
    
    def _create_comprehensive_analysis(self, question):
        """Create a comprehensive stock analysis using real data from yfinance"""
        import re
        import yfinance as yf
        from datetime import datetime
        
        # Extract ticker for analysis - improved company name resolution
        ticker_matches = re.findall(r'\b[A-Z]{1,5}(?:\.[A-Z])?\b', question.upper())
        
        if ticker_matches:
            # First try the regex match
            potential_ticker = ticker_matches[0]
            ticker = self.find_ticker_from_company_name(potential_ticker)
        else:
            # If no clear ticker pattern, try to resolve the whole input as a company name
            ticker = self.find_ticker_from_company_name(question.strip())
        
        # Final cleanup
        ticker = ticker.upper().strip()
        
        # Get company name and show header immediately
        company_name = self.get_company_name_from_ticker(ticker)
        self.root.after(0, self.display_analysis_header, ticker, company_name)
        
        try:
            # Fetch real stock data
            stock = yf.Ticker(ticker)
            info = stock.info
            hist = stock.history(period="1y")
            
            if hist.empty:
                return f"❌ Could not fetch data for ticker: {ticker}. Please check the symbol and try again."
            
            # Calculate technical indicators
            current_price = hist['Close'].iloc[-1]
            sma_9 = hist['Close'].rolling(window=9).mean().iloc[-1]
            sma_50 = hist['Close'].rolling(window=50).mean().iloc[-1]
            sma_200 = hist['Close'].rolling(window=200).mean().iloc[-1]
            
            # RSI calculation
            delta = hist['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs)).iloc[-1]
            
            # MACD calculation
            exp1 = hist['Close'].ewm(span=12).mean()
            exp2 = hist['Close'].ewm(span=26).mean()
            macd_line = exp1 - exp2
            signal_line = macd_line.ewm(span=9).mean()
            macd_current = macd_line.iloc[-1]
            signal_current = signal_line.iloc[-1]
            
            # Ichimoku Cloud calculation
            high_9 = hist['High'].rolling(window=9).max()
            low_9 = hist['Low'].rolling(window=9).min()
            tenkan_sen = ((high_9 + low_9) / 2).iloc[-1]
            
            high_26 = hist['High'].rolling(window=26).max()
            low_26 = hist['Low'].rolling(window=26).min()
            kijun_sen = ((high_26 + low_26) / 2).iloc[-1]
            
            # Determine cloud position (current price vs cloud)
            high_52 = hist['High'].rolling(window=52).max()
            low_52 = hist['Low'].rolling(window=52).min()
            senkou_span_b = ((high_52 + low_52) / 2).iloc[-27] if len(hist) > 27 else None
            senkou_span_a = ((tenkan_sen + kijun_sen) / 2)
            
            # Cloud signal
            ichimoku_signal = "NEUTRAL"
            if senkou_span_b is not None:
                if current_price > max(senkou_span_a, senkou_span_b):
                    ichimoku_signal = "BULLISH"
                elif current_price < min(senkou_span_a, senkou_span_b):
                    ichimoku_signal = "BEARISH"
            
            # Volume analysis
            avg_volume = hist['Volume'].mean()
            current_volume = hist['Volume'].iloc[-1]
            volume_ratio = current_volume / avg_volume
            
            # Price levels
            year_high = hist['High'].max()
            year_low = hist['Low'].min()
            price_change_1y = ((current_price - hist['Close'].iloc[0]) / hist['Close'].iloc[0]) * 100
            
            # Get company name for display
            company_name = self.get_company_name_from_ticker(ticker)
            
            # Calculate intrinsic value
            intrinsic_value = self.calculate_intrinsic_value(ticker)
            
            # Update the stock info header with intrinsic value
            self.root.after(0, lambda: self.update_stock_info_header(ticker, company_name, current_price, intrinsic_value))
            
            formatted = f"📊 COMPREHENSIVE STOCK ANALYSIS: {ticker} ({company_name})\n"
            formatted += f"{'='*60}\n\n"
            
            # Add company and industry overview
            sector = info.get('sector', 'N/A')
            industry = info.get('industry', 'N/A')
            formatted += self.get_industry_insights(ticker, sector, industry, company_name)
            
            formatted += f"Query: {question}\n"
            formatted += f"Current Price: ${current_price:.2f}\n"
            formatted += f"52-Week Range: ${year_low:.2f} - ${year_high:.2f}\n"
            formatted += f"1-Year Performance: {price_change_1y:+.2f}%\n"
            formatted += f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
            
            # 1. MARKET TREND ALIGNMENT
            formatted += f"🔍 **1. MARKET TREND ALIGNMENT**\n"
            sector = info.get('sector', 'N/A')
            industry = info.get('industry', 'N/A')
            formatted += f"• Sector: {sector}\n"
            formatted += f"• Industry: {industry}\n"
            
            if current_price > sma_200:
                formatted += f"• Long-term trend: BULLISH (Price above 200-day MA: ${sma_200:.2f})\n"
            else:
                formatted += f"• Long-term trend: BEARISH (Price below 200-day MA: ${sma_200:.2f})\n"
            
            if current_price > sma_50:
                formatted += f"• Short-term trend: BULLISH (Price above 50-day MA: ${sma_50:.2f})\n"
            else:
                formatted += f"• Short-term trend: BEARISH (Price below 50-day MA: ${sma_50:.2f})\n"
            
            if current_price > sma_9:
                formatted += f"• Very short-term trend: BULLISH (Price above 9-day MA: ${sma_9:.2f})\n"
            else:
                formatted += f"• Very short-term trend: BEARISH (Price below 9-day MA: ${sma_9:.2f})\n"
            formatted += f"\n"
            
            # 2. TECHNICAL ANALYSIS
            formatted += f"📈 **2. TECHNICAL OVERVIEW & MOMENTUM**\n"
            formatted += f"• RSI (14-day): {rsi:.1f} "
            if rsi > 70:
                formatted += f"(OVERBOUGHT)\n"
            elif rsi < 30:
                formatted += f"(OVERSOLD)\n"
            else:
                formatted += f"(NEUTRAL)\n"
            
            formatted += f"• MACD: {macd_current:.3f}, Signal: {signal_current:.3f}\n"
            if macd_current > signal_current:
                formatted += f"• MACD Signal: BULLISH (MACD above signal line)\n"
            else:
                formatted += f"• MACD Signal: BEARISH (MACD below signal line)\n"
            
            formatted += f"• Ichimoku Cloud: {ichimoku_signal}\n"
            formatted += f"• Tenkan-sen (9): ${tenkan_sen:.2f}\n"
            formatted += f"• Kijun-sen (26): ${kijun_sen:.2f}\n"
            if current_price > tenkan_sen and current_price > kijun_sen:
                formatted += f"• Price above both Ichimoku lines: BULLISH\n"
            elif current_price < tenkan_sen and current_price < kijun_sen:
                formatted += f"• Price below both Ichimoku lines: BEARISH\n"
            else:
                formatted += f"• Mixed Ichimoku signals: NEUTRAL\n"
            
            formatted += f"• 9-day MA: ${sma_9:.2f}\n"
            formatted += f"• 50-day MA: ${sma_50:.2f}\n"
            formatted += f"• 200-day MA: ${sma_200:.2f}\n"
            formatted += f"• Volume vs Avg: {volume_ratio:.1f}x (Current: {current_volume:,.0f})\n\n"
            
            # 3. VALUATION & FUNDAMENTALS
            formatted += f"💰 **3. VALUATION & FUNDAMENTALS**\n"
            pe_ratio = info.get('forwardPE', info.get('trailingPE', 'N/A'))
            market_cap = info.get('marketCap', 'N/A')
            revenue = info.get('totalRevenue', 'N/A')
            
            formatted += f"• Market Cap: ${market_cap:,.0f}\n" if market_cap != 'N/A' else f"• Market Cap: N/A\n"
            formatted += f"• P/E Ratio: {pe_ratio:.2f}\n" if pe_ratio != 'N/A' else f"• P/E Ratio: N/A\n"
            formatted += f"• Annual Revenue: ${revenue:,.0f}\n" if revenue != 'N/A' else f"• Annual Revenue: N/A\n"
            
            # Valuation assessment
            if pe_ratio != 'N/A' and pe_ratio < 15:
                formatted += f"• Valuation Assessment: UNDERVALUED (Low P/E)\n"
            elif pe_ratio != 'N/A' and pe_ratio > 25:
                formatted += f"• Valuation Assessment: OVERVALUED (High P/E)\n"
            else:
                formatted += f"• Valuation Assessment: FAIRLY VALUED\n"
            formatted += f"\n"
            
            # 4. BUY/SELL/HOLD RECOMMENDATION
            formatted += f"🎯 **4. BUY/SELL/HOLD RECOMMENDATION**\n"
            
            # Score calculation
            signals = []
            if rsi < 30: signals.append("Oversold RSI")
            if rsi > 70: signals.append("Overbought RSI") 
            if current_price > sma_9: signals.append("Above 9-day MA")
            if current_price > sma_50: signals.append("Above 50-day MA")
            if current_price > sma_200: signals.append("Above 200-day MA")
            if macd_current > signal_current: signals.append("MACD Bullish")
            if ichimoku_signal == "BULLISH": signals.append("Ichimoku Bullish")
            if ichimoku_signal == "BEARISH": signals.append("Ichimoku Bearish")
            if volume_ratio > 1.5: signals.append("High Volume")
            
            bullish_signals = sum(1 for s in signals if s in ["Oversold RSI", "Above 9-day MA", "Above 50-day MA", "Above 200-day MA", "MACD Bullish", "Ichimoku Bullish", "High Volume"])
            bearish_signals = sum(1 for s in signals if s in ["Overbought RSI", "Ichimoku Bearish"])
            
            if bullish_signals >= 3:
                recommendation = "BUY"
                formatted += f"• Recommendation: **{recommendation}** ({bullish_signals} bullish signals)\n"
            elif bearish_signals >= 2:
                recommendation = "SELL"
                formatted += f"• Recommendation: **{recommendation}** ({bearish_signals} bearish signals)\n"
            else:
                recommendation = "HOLD"
                formatted += f"• Recommendation: **{recommendation}** (Mixed signals)\n"
            
            formatted += f"• Entry Point: Consider ${current_price*0.95:.2f} - ${current_price*1.05:.2f}\n"
            formatted += f"• Stop Loss: ${current_price*0.90:.2f} (10% below current)\n"
            formatted += f"• Target Price: ${current_price*1.20:.2f} (20% above current)\n\n"
            
            # SUMMARY
            formatted += f"📋 **SUMMARY & ACTION PLAN**\n"
            formatted += f"• Overall Assessment: {recommendation} based on technical and fundamental analysis\n"
            formatted += f"• Key Monitors: Volume, {sector} sector performance, earnings reports\n"
            formatted += f"• Reassessment: Weekly technical review, quarterly fundamental review\n\n"
            
            formatted += f"🔗 **For Advanced AI Analysis**: Use the 'Stock Predictor' button to get detailed,\n"
            formatted += f"real-time analysis using your custom Stock Predictor AI Assistant with current market data.\n\n"
            
            formatted += f"⚠️ **Disclaimer**: This analysis is for educational purposes only.\n"
            formatted += f"Always consult with financial advisors and conduct your own research before making investment decisions.\n"
            formatted += f"Past performance does not guarantee future results.\n\n"
            formatted += f"{'='*60}\n"
            formatted += f"🏁 END OF ANALYSIS - Stock Analyzer v0.15 🏁\n"
            formatted += f"{'='*60}\n"
            formatted += f"\n\n\n------- SCROLL DOWN TO SEE COMPLETE ANALYSIS -------\n\n"
            
            return formatted
            
        except Exception as e:
            # Still update the stock info header even if there's an error
            company_name = self.get_company_name_from_ticker(ticker)
            self.root.after(0, lambda: self.update_stock_info_header(ticker, company_name))
            
            return f"❌ Error fetching data for {ticker} ({company_name}): {str(e)}\n\nPlease check the ticker symbol and try again."
    
    def find_ticker_from_company_name(self, company_input):
        """Find ticker from company name input"""
        company_input = company_input.upper().strip()
        
        # First, check if it's already a ticker
        for stock in self.stock_data:
            if stock['ticker'] == company_input:
                return company_input
        
        # If not, search for company name matches
        best_match = ""
        best_score = 0
        
        for stock in self.stock_data:
            company_name = stock['company'].upper()
            ticker = stock['ticker']
            
            # Exact match
            if company_name == company_input:
                return ticker
                
            # Partial match - check if input words are in company name
            input_words = company_input.split()
            company_words = company_name.split()
            
            matches = sum(1 for word in input_words if any(w.startswith(word) for w in company_words))
            score = matches / len(input_words) if input_words else 0
            
            if score > best_score and score > 0.5:  # At least 50% match
                best_score = score
                best_match = ticker
        
        # Return best match or the original input if no good match found
        return best_match if best_match else company_input
    
    def calculate_intrinsic_value(self, ticker):
        """Calculate intrinsic value using multiple valuation methods"""
        try:
            import yfinance as yf
            
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Get key financial metrics
            current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
            forward_pe = info.get('forwardPE', 0)
            trailing_pe = info.get('trailingPE', 0)
            book_value = info.get('bookValue', 0)
            dividend_yield = info.get('dividendYield', 0)
            dividend_rate = info.get('dividendRate', 0)
            
            # Method 1: P/E based valuation
            pe_based_value = 0
            if forward_pe and forward_pe > 0:
                # Use a conservative P/E of 15 for fair value estimation
                fair_pe = min(15, forward_pe * 0.8)  # Be conservative
                earnings_per_share = current_price / forward_pe if forward_pe > 0 else 0
                pe_based_value = earnings_per_share * fair_pe
            elif trailing_pe and trailing_pe > 0:
                fair_pe = min(15, trailing_pe * 0.8)
                earnings_per_share = current_price / trailing_pe if trailing_pe > 0 else 0
                pe_based_value = earnings_per_share * fair_pe
            
            # Method 2: Book Value based (for asset-heavy companies)
            book_value_based = book_value * 1.2 if book_value > 0 else 0 # 20% premium to book
            
            # Method 3: Dividend Discount Model (for dividend-paying stocks)
            dividend_based_value = 0
            if dividend_rate and dividend_rate > 0:
                # Assume 8% required return and 3% growth
                required_return = 0.08
                growth_rate = 0.03
                if required_return > growth_rate:
                    dividend_based_value = dividend_rate / (required_return - growth_rate)
            
            # Method 4: Simple DCF approximation
            dcf_value = 0
            if forward_pe and forward_pe > 0:
                # Very simplified DCF using P/E as proxy
                earnings_per_share = current_price / forward_pe
                # Assume 5% growth for 5 years, then 2% perpetual
                dcf_value = earnings_per_share * 12  # Conservative multiplier
            
            # Calculate weighted average (prioritize methods that returned values)
            values = []
            weights = []
            
            if pe_based_value > 0:
                values.append(pe_based_value)
                weights.append(0.4)  # 40% weight
            
            if book_value_based > 0:
                values.append(book_value_based)
                weights.append(0.2)  # 20% weight
                
            if dividend_based_value > 0:
                values.append(dividend_based_value)
                weights.append(0.2)  # 20% weight
                
            if dcf_value > 0:
                values.append(dcf_value)
                weights.append(0.2)  # 20% weight
            
            if values:
                # Normalize weights
                total_weight = sum(weights)
                normalized_weights = [w/total_weight for w in weights]
                
                # Calculate weighted average
                intrinsic_value = sum(v * w for v, w in zip(values, normalized_weights))
                
                # Sanity checks to prevent unrealistic values
                if intrinsic_value > current_price * 3:   # Max 3x current price
                    intrinsic_value = current_price * 1.5  # Cap at 50% premium
                elif intrinsic_value < current_price * 0.3:  # Min 30% of current price
                    intrinsic_value = current_price * 0.8  # Set to 20% discount
                
                return round(intrinsic_value, 2)
            else:
                # If no valuation methods worked, return current price as estimate
                return current_price
                
        except Exception as e:
            print(f"Error calculating intrinsic value for {ticker}: {e}")
            # Return None to indicate calculation failed
            return None

    def get_value_assessment(self, current_price, intrinsic_value):
        """Assess if stock is undervalued, fairly valued, or overvalued"""
        if not intrinsic_value or intrinsic_value <= 0:
            return "Unable to assess"
        
        ratio = current_price / intrinsic_value
        
        if ratio < 0.9:  # Current price is less than 90% of intrinsic value
            return "Undervalued"
        elif ratio > 1.1:  # Current price is more than 110% of intrinsic value
            return "Overvalued"
        else:
            return "Fairly Valued"

    def get_company_name_from_ticker(self, ticker):
        """Get company name from ticker"""
        ticker = ticker.upper()
        for stock in self.stock_data:
            if stock['ticker'] == ticker:
                return stock['company']
        return f"Unknown Company ({ticker})"
    
    def get_industry_insights(self, ticker, sector, industry, company_name):
        """Get industry and company insights"""
        insights = f"💼 **COMPANY & INDUSTRY OVERVIEW**\n"
        insights += f"Company: {company_name}\n"
        insights += f"Sector: {sector}\n"
        insights += f"Industry: {industry}\n\n"
        
        # Add sector-specific insights
        if sector == "Technology":
            insights += "🔬 Technology Sector: Focus on innovation, R&D spending, and market disruption potential.\n"
        elif sector == "Healthcare":
            insights += "🏥 Healthcare Sector: Monitor regulatory approvals, drug pipelines, and demographic trends.\n"
        elif sector == "Financial Services":
            insights += "🏦 Financial Sector: Interest rate sensitivity, credit quality, and regulatory environment are key.\n"
        elif sector == "Energy":
            insights += "⚡ Energy Sector: Commodity price exposure, production costs, and renewable transition trends.\n"
        elif sector == "Consumer Defensive":
            insights += "🛒 Consumer Defensive: Stable demand, dividend yields, and inflation impact considerations.\n"
        
        insights += "\n"
        return insights
    
    def display_analysis_header(self, ticker, company_name):
        """Display analysis header immediately"""
        self.results_display.config(state=tk.NORMAL)
        header_text = f"📊 COMPREHENSIVE STOCK ANALYSIS: {ticker} ({company_name})\n"
        header_text += f"{'='*60}\n\n"
        header_text += "🔄 Analyzing... Please wait while we gather data...\n\n"
        self.results_display.insert(tk.END, header_text)
        self.results_display.config(state=tk.DISABLED)
        
        # Stay at the top - don't scroll
        self.results_display.see("1.0")
        self.results_display.update_idletasks()
    
    def update_stock_info_header(self, ticker, company_name, price=None, intrinsic_value=None):
        """Update the stock info header with ticker/company/price on top, and intrinsic value below"""
        from datetime import datetime
        header_lines = []
        # Top line: Ticker, Company, Price
        top_line = f"{ticker} | {company_name}"
        if price is not None:
            top_line += f" | ${price:.2f}"
        header_lines.append(top_line)
        # Second line: Intrinsic Value (with breakdown if available)
        if intrinsic_value and isinstance(intrinsic_value, dict):
            iv = intrinsic_value.get('intrinsic_value', None)
            dcf = intrinsic_value.get('dcf_value', None)
            pe = intrinsic_value.get('pe_value', None)
            bv = intrinsic_value.get('book_value', None)
            ddm = intrinsic_value.get('dividend_value', None)
            methods = intrinsic_value.get('methods_used', 0)
            if iv:
                iv_line = f"Intrinsic Value: ${iv:.2f} "
                # Value assessment
                if price and iv > 0:
                    if price < iv * 0.85:
                        iv_line += "(Undervalued)"
                    elif price > iv * 1.15:
                        iv_line += "(Overvalued)"
                    else:
                        iv_line += "(Fair Value)"
                header_lines.append(iv_line)
                # Breakdown
                breakdown = []
                if dcf: breakdown.append(f"DCF: ${dcf:.2f}")
                if pe: breakdown.append(f"P/E: ${pe:.2f}")
                if bv: breakdown.append(f"Book: ${bv:.2f}")
                if ddm: breakdown.append(f"DDM: ${ddm:.2f}")
                if breakdown:
                    header_lines.append("Breakdown: " + ", ".join(breakdown))
        elif isinstance(intrinsic_value, (int, float)) and intrinsic_value > 0:
            iv_line = f"Intrinsic Value: ${intrinsic_value:.2f} "
            if price and intrinsic_value > 0:
                if price < intrinsic_value * 0.85:
                    iv_line += "(Undervalued)"
                elif price > intrinsic_value * 1.15:
                    iv_line += "(Overvalued)"
                else:
                    iv_line += "(Fair Value)"
            header_lines.append(iv_line)
        # Add time
        header_lines.append(datetime.now().strftime('%H:%M:%S'))
        # Set label text with line breaks for separation
        header_text = "\n".join(header_lines)
        
        # Update the label with new text
        self.stock_info_label.config(text=header_text)
    
    def _display_ai_response(self, response, error):
        """Display AI response in the GUI"""
        if error:
            self.display_message(error, "error")
            self.update_status("❌ Error occurred")
        else:
            self.display_complete_analysis(response, "response")
            self.update_status("✅ Analysis complete")
        
        # Re-enable button
        self.run_button.config(state="normal", text="📊 ANALYZE STOCK")
    
    def display_complete_analysis(self, message, tag="response"):
        """Display the complete analysis and allow proper scrolling"""
        self.results_display.config(state=tk.NORMAL)
        # Clear the loading message and replace with full analysis
        self.results_display.delete("1.0", tk.END)
        self.results_display.insert(tk.END, message + "\n\n\n\n\n", tag)
        self.results_display.config(state=tk.DISABLED)
        
        # Start at the top so user can read from beginning, but ensure scrolling works
        self.results_display.see("1.0")
        self.results_display.update_idletasks()
        
        # Force scrollbar update to ensure proper scrolling
        self.results_display.after(100, lambda: self.results_display.see(tk.END))
        self.results_display.after(150, lambda: self.results_display.see("1.0"))
    
    def display_message(self, message, tag="response", preserve_content=False):
        """Display a message in the results area
        Args:
            message: The message to display
            tag: The tag for styling the message
            preserve_content: If True, append to existing content instead of clearing
        """
        self.results_display.config(state=tk.NORMAL)
        
        if not preserve_content:
            # Clear previous content (default behavior for stock analysis)
            self.results_display.delete("1.0", tk.END)
        else:
            # Append to existing content (for button messages)
            if self.results_display.get("1.0", tk.END).strip():
                self.results_display.insert(tk.END, "\n" + "="*50 + "\n\n", "info")
        
        self.results_display.insert(tk.END, message + "\n\n", tag)
        self.results_display.config(state=tk.DISABLED)
        
        # Always scroll to the bottom to show new content
        self.results_display.see(tk.END)
        self.results_display.update_idletasks()
    
    def update_status(self, status):
        """Update status bar"""
        self.status_var.set(status)

    def change_font_size(self, size):
        """Change font size of the results display"""
        self.font_size.set(size)
        self.results_display.config(font=("Arial", size))
        self.update_text_styles()
    
    def update_text_styles(self):
        """Update text styles for the results display"""
        current_size = self.font_size.get()
        
        # Configure text tags with proper styling
        self.results_display.tag_configure("response", 
                                          font=("Arial", current_size),
                                          foreground="#000000")
        self.results_display.tag_configure("error", 
                                          font=("Arial", current_size),
                                          foreground="#e74c3c")
        self.results_display.tag_configure("success", 
                                          font=("Arial", current_size),
                                          foreground="#27ae60")
        self.results_display.tag_configure("info", 
                                          font=("Arial", current_size),
                                          foreground="#3498db")

# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = StockAnalyzerGUI(root)
    root.mainloop()
