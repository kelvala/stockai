# Free GPT GUI Application - No API Required

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

# Try to import transformers for local AI
try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

# Free Hugging Face API endpoint (no key required for basic use)
FREE_API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"

class StockAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Analyzer - AI Powered v0.12")
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
        title_label = ttk.Label(main_frame, text="📈 Stock Analyzer - AI Powered v0.12", 
                               font=("Arial", 24, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 30))
        
        # Question/Input section - more compact
        input_frame = ttk.LabelFrame(main_frame, text="Enter Stock Symbol or Company Name", padding="10")
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        input_frame.columnconfigure(0, weight=1)
        input_frame.columnconfigure(1, weight=0)
        
        self.question_input = tk.Text(input_frame, height=2, 
                                     font=("Arial", 12), wrap=tk.WORD,
                                     relief="solid", borderwidth=1)
        self.question_input.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        self.question_input.insert("1.0", "Enter stock symbol (e.g., AAPL, TSLA) or company name...")
        self.question_input.bind("<FocusIn>", self.clear_placeholder)
        self.question_input.bind("<KeyRelease>", self.on_key_release)
        self.question_input.bind("<Return>", self.on_enter_key)
        self.question_input.bind("<Button-1>", self.hide_suggestions)
        
        # Analyze Stock Button - positioned to the right of input
        self.run_button = ttk.Button(input_frame, text="📊 ANALYZE\nSTOCK", 
                                    command=self.run_gpt, 
                                    style="Accent.TButton")
        self.run_button.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Create main content area instead of resizable paned window
        content_frame = ttk.Frame(main_frame)
        content_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(0, weight=1)  # Analysis area gets most space
        content_frame.rowconfigure(1, weight=0)  # ChatGPT area stays fixed
        
        # Results display section (main area)
        results_frame = ttk.LabelFrame(content_frame, text="Stock Analysis Results", padding="15")
        results_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
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
                                         font=("Arial", 12, "bold"),
                                         foreground="#ffffff",  # Bright white text
                                         background="#2c3e50")  # Dark background for contrast
        self.stock_info_label.grid(row=0, column=0, sticky=tk.W)
        
        self.results_display = scrolledtext.ScrolledText(results_frame, 
                                                        font=("Arial", self.font_size.get()), 
                                                        wrap=tk.WORD, 
                                                        state=tk.DISABLED,
                                                        bg="#f8f9fa")
        self.results_display.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure text styling with variable fonts
        self.update_text_styles()
        
        # ChatGPT Section Header (fixed bottom section)
        chatgpt_header_frame = ttk.LabelFrame(content_frame, text="🤖 ChatGPT AI Assistants", padding="10")
        chatgpt_header_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 0))
        chatgpt_header_frame.columnconfigure(0, weight=0)  # Don't expand buttons
        chatgpt_header_frame.columnconfigure(1, weight=1)  # Allow text to expand
        chatgpt_header_frame.rowconfigure(0, weight=0)  # Keep buttons at fixed height
        chatgpt_header_frame.rowconfigure(1, weight=0)  # Keep buttons at fixed height
        
        # ChatGPT Browser Buttons - stacked in upper left corner for visibility
        self.chatgpt_button = ttk.Button(chatgpt_header_frame, text="🌐 Stock Predictor", 
                                        command=self.open_chatgpt_browser,
                                        style="ChatGPT.TButton")
        self.chatgpt_button.grid(row=0, column=0, padx=(0, 15), pady=(0, 5), sticky=tk.W)
        
        self.dividend_button = ttk.Button(chatgpt_header_frame, text="💰 Dividend Sniper", 
                                        command=self.open_dividend_sniper,
                                        style="Dividend.TButton")
        self.dividend_button.grid(row=1, column=0, padx=(0, 15), pady=(0, 5), sticky=tk.W)
        
        # ChatGPT header text - positioned to the right of buttons
        chatgpt_header_label = ttk.Label(chatgpt_header_frame, 
                                        text="Launch specialized GPTs for advanced analysis.\nClick buttons to open custom GPTs with automation.", 
                                        font=("Arial", 11, "italic"),
                                        foreground="#555555",
                                        justify=tk.LEFT)
        chatgpt_header_label.grid(row=0, column=1, rowspan=2, sticky=(tk.W, tk.N), padx=(0, 0), pady=(5, 0))
        
        # Configure button styles for better readability
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Arial", 14, "bold"))
        style.configure("ChatGPT.TButton", font=("Arial", 12, "bold"), foreground="#10a37f")
        style.configure("Dividend.TButton", font=("Arial", 12, "bold"), foreground="#10a37f")
        
        # Configure font size button styles with better visibility
        style.configure("SmallFont.TButton", font=("Arial", 12), foreground="#2c3e50", background="#ecf0f1")
        style.configure("MediumFont.TButton", font=("Arial", 14, "bold"), foreground="#2c3e50", background="#bdc3c7")
        style.configure("LargeFont.TButton", font=("Arial", 16, "bold"), foreground="#2c3e50", background="#95a5a6")
        style.configure("XLargeFont.TButton", font=("Arial", 18, "bold"), foreground="#2c3e50", background="#7f8c8d")
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                                   relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Configure main frame row weights
        main_frame.rowconfigure(2, weight=1)  # Make the content frame expandable
        
        # Initial display
        self.display_message("Welcome to Stock Analyzer! Enter a stock symbol (e.g., AAPL, TSLA) or ask stock analysis questions.", "info")
        self.update_status("Ready - Click 'ANALYZE STOCK' to start!")
    
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
        
        if current_text == "Enter stock symbol (e.g., AAPL, TSLA) or company name...":
            # Clear placeholder text
            self.question_input.delete("1.0", tk.END)
        elif not self.typing_new_ticker:
            # Auto-clear any existing ticker/content when user clicks to enter new one
            self.question_input.delete("1.0", tk.END)
        
        # Set flag that user is now typing a new ticker
        self.typing_new_ticker = True
    
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
        """Show stock ticker and company name suggestions"""
        content = self.question_input.get("1.0", tk.END).strip().upper()
        
        if len(content) < 1 or content == "ENTER STOCK SYMBOL (E.G., AAPL, TSLA) OR COMPANY NAME...":
            self.hide_suggestions()
            return
        
        # Find matching stocks
        matches = []
        for stock in self.stock_data:
            ticker = stock['ticker']
            company = stock['company'].upper()
            
            # Match ticker or company name
            if ticker.startswith(content) or any(word.startswith(content) for word in company.split()):
                matches.append(f"{ticker} - {stock['company']}")
        
        if matches:
            self.display_suggestions(matches[:10])  # Limit to 10 suggestions
        else:
            self.hide_suggestions()
    
    def display_suggestions(self, suggestions):
        """Display suggestion dropdown"""
        if self.suggestion_listbox:
            self.suggestion_listbox.destroy()
        
        # Create suggestion listbox with proper colors
        self.suggestion_listbox = tk.Listbox(self.root, height=min(len(suggestions), 8), 
                                           font=("Arial", 10), 
                                           bg="#ffffff",      # White background
                                           fg="#2c3e50",      # Dark blue text
                                           selectbackground="#007acc",  # Blue selection
                                           selectforeground="#ffffff",  # White text when selected
                                           highlightthickness=1,
                                           highlightcolor="#007acc",
                                           relief="solid",
                                           borderwidth=1)
        
        # Add suggestions
        for suggestion in suggestions:
            self.suggestion_listbox.insert(tk.END, suggestion)
        
        # Position the listbox below the input
        input_x = self.question_input.winfo_rootx()
        input_y = self.question_input.winfo_rooty() + self.question_input.winfo_height()
        input_width = self.question_input.winfo_width()
        
        self.suggestion_listbox.place(x=input_x - self.root.winfo_rootx(), 
                                    y=input_y - self.root.winfo_rooty(),
                                    width=input_width)
        
        # Bind selection event
        self.suggestion_listbox.bind("<Double-Button-1>", self.on_suggestion_select)
        self.suggestion_listbox.bind("<Return>", self.on_suggestion_select)
    
    def hide_suggestions(self, event=None):
        """Hide suggestion dropdown"""
        if self.suggestion_listbox:
            self.suggestion_listbox.destroy()
            self.suggestion_listbox = None
    
    def on_suggestion_select(self, event):
        """Handle suggestion selection"""
        selection = self.suggestion_listbox.get(self.suggestion_listbox.curselection())
        ticker = selection.split(" - ")[0]
        
        # Clear input and insert selected ticker
        self.question_input.delete("1.0", tk.END)
        self.question_input.insert("1.0", ticker)
        
        # Hide suggestions
        self.hide_suggestions()
        
        # Reset typing flag since user selected from suggestions
        self.typing_new_ticker = False
        
        # Focus back to input
        self.question_input.focus_set()
    
    def on_enter_key(self, event):
        """Execute analysis when Enter key is pressed"""
        # Prevent default behavior (new line) and execute the button
        self.run_gpt()
        return "break"  # This prevents the default Enter behavior
    
    def open_chatgpt_browser(self):
        """Open your custom Stock Predictor GPT and automatically input the ticker"""
        question = self.question_input.get("1.0", tk.END).strip()
        
        # Clear placeholder text if present
        if question == "Enter stock symbol (e.g., AAPL, TSLA) or company name...":
            question = ""
        
        # Extract ticker from the question (look for stock symbols)
        import re
        ticker = ""
        if question:
            # Find potential stock tickers (1-5 letter combinations, uppercase)
            ticker_matches = re.findall(r'\b[A-Z]{1,5}\b', question.upper())
            if ticker_matches:
                ticker = self.find_ticker_from_company_name(ticker_matches[0])
            else:
                # If no clear ticker, try to resolve the whole question as company name
                ticker = self.find_ticker_from_company_name(question.strip())
        
        print(f"🔍 Debug - Original question: '{question}'")  # Debug
        print(f"🔍 Debug - Extracted ticker: '{ticker}'")  # Debug
        
        # Your custom Stock Predictor GPT URL
        custom_gpt_url = "https://chatgpt.com/g/g-686c5fc3dd948191a0ff9c14cecda1b4-stock-predictor-prompt-gpt"
        
        try:
            if ticker:
                # Use simple approach with existing browser - prioritize this method
                self.update_status(f"🤖 Automating {ticker} input...")
                success = self.use_existing_browser(custom_gpt_url, ticker)
                
                if success:
                    self.display_message(f"🚀 STOCK PREDICTOR GPT AUTOMATED!\n\n" +
                                       f"✨ Successfully used your existing browser window\n" +
                                       f"🤖 Ticker '{ticker}' has been entered and submitted!\n" +
                                       f"📊 Check your browser for the analysis results.\n\n" +
                                       f"🎯 The GPT should now be analyzing {ticker} for you!\n\n" +
                                       f"🔗 GPT Link: {custom_gpt_url}", "success")
                else:
                    # Automation failed, use manual fallback
                    self.update_status(f"🔄 Automation failed, using manual method...")
                    self.fallback_gpt_method(custom_gpt_url, ticker)
            else:
                # No ticker found, just open the GPT
                webbrowser.open(custom_gpt_url)
                self.display_message(f"🚀 STOCK PREDICTOR GPT OPENED!\n\n" +
                                   f"✨ Your custom GPT is now open in your browser!\n" +
                                   f"� Enter any stock ticker in the 'Ask anything' box for detailed predictions and analysis.\n\n" +
                                   f"� GPT Link: {custom_gpt_url}", "success")
                
        except Exception as e:
            self.update_status(f"❌ Error: {str(e)}")
            # Fallback to manual method
            if ticker:
                self.fallback_gpt_method(custom_gpt_url, ticker)
            else:
                webbrowser.open(custom_gpt_url)
    
    def automate_gpt_input(self, url, ticker):
        """Automate the GPT input using browser automation"""
        try:
            # Try to import selenium for browser automation
            from selenium import webdriver
            from selenium.webdriver.common.by import By
            from selenium.webdriver.common.keys import Keys
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.chrome.service import Service
            import time
            
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
            
            print(f"Opening URL: {url}")
            driver.get(url)
            
            # Wait longer for ChatGPT to fully load
            print("Waiting for page to load...")
            time.sleep(5)
            
            # Check if the page loaded properly
            if "chatgpt" not in driver.current_url.lower():
                print(f"Warning: URL might have redirected. Current URL: {driver.current_url}")
            
            # Wait for the page to load and find the input field with longer timeout
            wait = WebDriverWait(driver, 30)
            
            # Try different selectors for ChatGPT input field (updated for current ChatGPT)
            input_selectors = [
                "textarea[data-testid='textbox']",
                "textarea[placeholder*='Message']",
                "textarea[placeholder*='Ask']", 
                "div[contenteditable='true']",
                "#prompt-textarea",
                "textarea",
                "[data-testid='textbox']",
                "div[role='textbox']",
                "textarea[role='textbox']"
            ]
            
            input_element = None
            for i, selector in enumerate(input_selectors):
                try:
                    print(f"Trying selector {i+1}/{len(input_selectors)}: {selector}")
                    
                    # Wait a bit between attempts
                    time.sleep(2)
                    
                    # Check if window is still open
                    if len(driver.window_handles) == 0:
                        print("Browser window was closed")
                        return False
                    
                    input_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                    
                    # Additional checks
                    if input_element and input_element.is_displayed() and input_element.is_enabled():
                        print(f"✅ Found input field with selector: {selector}")
                        break
                    else:
                        print(f"Element found but not ready: displayed={input_element.is_displayed()}, enabled={input_element.is_enabled()}")
                        input_element = None
                        
                except Exception as e:
                    print(f"Selector {selector} failed: {str(e)[:100]}")
                    continue
            
            if input_element:
                try:
                    # Scroll to element and ensure it's visible
                    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", input_element)
                    time.sleep(2)
                    
                    # Click the input field to focus it
                    driver.execute_script("arguments[0].click();", input_element)
                    time.sleep(2)
                    
                    # Clear any existing content
                    driver.execute_script("arguments[0].value = '';", input_element)
                    input_element.clear()
                    time.sleep(1)
                    
                    # Type the ticker
                    print(f"Entering ticker: {ticker}")
                    input_element.send_keys(ticker)
                    time.sleep(2)
                    
                    # Submit the form
                    print("Submitting ticker...")
                    input_element.send_keys(Keys.RETURN)
                    
                    self.update_status(f"✅ Successfully automated {ticker} input to GPT!")
                    
                    # Keep browser open for user to see results
                    print("✅ Automation successful! Browser will stay open for results.")
                    
                    # Don't close the driver - let user see results
                    return True
                    
                except Exception as e:
                    print(f"Error during input automation: {e}")
                    driver.quit()
                    return False
            else:
                print("❌ Could not find input field with any selector")
                driver.quit()
                return False
                
        except ImportError as e:
            print(f"Selenium not available: {e}")
            # Selenium not installed, try alternative method
            return self.try_applescript_automation(url, ticker)
        except Exception as e:
            print(f"Browser automation error: {e}")
            try:
                if 'driver' in locals():
                    driver.quit()
            except:
                pass
            return False
    
    def try_applescript_automation(self, url, ticker):
        """Try AppleScript automation on macOS as fallback"""
        try:
            import subprocess
            import time
            
            print("🍎 Trying AppleScript automation...")
            
            # Open the URL first
            webbrowser.open(url)
            time.sleep(5)  # Wait longer for page to load
            
            # Enhanced AppleScript to find and interact with ChatGPT
            applescript = f'''
            tell application "System Events"
                -- Wait for page to fully load
                delay 5
                
                -- Try multiple methods to find the input field
                try
                    -- Method 1: Look for text area by accessibility
                    tell application "Google Chrome" to activate
                    delay 2
                    
                    -- Try clicking in the general area where input should be
                    click at {{800, 600}}
                    delay 1
                    
                    -- Clear any existing text and type ticker
                    keystroke "a" using command down
                    delay 0.5
                    keystroke "{ticker}"
                    delay 1
                    key code 36  -- Return key
                    
                    return true
                on error
                    -- Method 2: Use Tab navigation
                    try
                        key code 48  -- Tab key multiple times to find input
                        delay 0.5
                        key code 48  -- Tab
                        delay 0.5
                        key code 48  -- Tab
                        delay 0.5
                        
                        keystroke "{ticker}"
                        delay 1
                        key code 36  -- Return
                        
                        return true
                    on error
                        return false
                    end try
                end try
            end tell
            '''
            
            # Execute AppleScript
            result = subprocess.run(['osascript', '-e', applescript], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print("✅ AppleScript automation successful!")
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
    
    def fallback_gpt_method(self, url, ticker):
        """Fallback method - copy to clipboard and open browser with clear instructions"""
        try:
            import pyperclip
            pyperclip.copy(ticker)
            clipboard_success = True
        except ImportError:
            clipboard_success = False
        
        webbrowser.open(url)
        self.update_status("🌐 Opened Stock Predictor GPT!")
        
        if clipboard_success:
            self.display_message(f"🚀 STOCK PREDICTOR GPT OPENED!\n\n" +
                               f"✨ Your Stock Predictor GPT is now open in your browser!\n" +
                               f"📋 Ticker '{ticker}' has been copied to your clipboard!\n\n" +
                               f"💡 Quick Steps:\n" +
                               f"   1. Look for the input box at the bottom of the ChatGPT page\n" +
                               f"   2. Click in the input box\n" +
                               f"   3. Paste '{ticker}' (Cmd+V on Mac, Ctrl+V on PC)\n" +
                               f"   4. Press Enter to get detailed analysis\n\n" +
                               f"🎯 Alternative: Just type '{ticker}' directly in the input box\n\n" +
                               f"🔗 GPT Link: {url}", "success")
        else:
            self.display_message(f"🚀 STOCK PREDICTOR GPT OPENED!\n\n" +
                               f"✨ Your Stock Predictor GPT is now open in your browser!\n\n" +
                               f"💡 To analyze {ticker}:\n" +
                               f"   1. Look for the input box at the bottom of the ChatGPT page\n" +
                               f"   2. Click in the input box\n" +
                               f"   3. Type '{ticker}' and press Enter\n\n" +
                               f"🎯 The GPT will provide detailed analysis and predictions!\n\n" +
                               f"🔗 GPT Link: {url}", "success")
    
    def open_dividend_sniper(self):
        """Open your custom Dividend Sniper GPT"""
        # Your custom Dividend Sniper GPT URL
        dividend_gpt_url = "https://chatgpt.com/g/g-6878fe277c5c819180211289d9e16148-high-yield-dividend-sniper"
        
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
            webbrowser.open(dividend_gpt_url)
            self.update_status("🌐 Opened Dividend Sniper GPT!")
            
            # Show results in the main display
            self.display_message(f"💰 DIVIDEND SNIPER GPT OPENED!\n\n" +
                               f"✨ Your High-Yield Dividend Sniper GPT is now open in your browser!\n" +
                               f"📋 Suggested query copied to clipboard!\n\n" +
                               f"� To get dividend analysis:\n" +
                               f"   1. Look for the 'Ask anything' input box\n" +
                               f"   2. Paste the query (Cmd+V) or ask your own question\n" +
                               f"   3. Press Enter to get dividend recommendations\n\n" +
                               f"🔗 Suggested Query: {suggested_query}\n\n" +
                               f"🔗 GPT Link: {dividend_gpt_url}", "success")
                
        except Exception as e:
            self.update_status(f"❌ Could not open browser: {str(e)}")
            messagebox.showerror("Browser Error", f"Could not open browser.\n\nPlease manually visit:\n{dividend_gpt_url}")
            messagebox.showinfo("Suggested Query", f"Query to use: {suggested_query}")
    
    def run_gpt(self):
        """Main function to run Stock Analysis AI"""
        question = self.question_input.get("1.0", tk.END).strip()
        
        if not question or question == "Enter stock symbol (e.g., AAPL, TSLA) or company name...":
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
        """Convert stock tickers to uppercase and format input"""
        import re
        
        # Find potential stock tickers (3-5 letter combinations)
        def uppercase_ticker(match):
            return match.group().upper()
        
        # Convert potential stock tickers to uppercase
        formatted = re.sub(r'\b[A-Za-z]{1,5}\b', uppercase_ticker, input_text)
        
        return formatted
    
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
        # Extract ticker for analysis - improved company name resolution
        import re
        ticker_matches = re.findall(r'\b[A-Z]{1,5}\b', question.upper())
        
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
            
            # Update the stock info header
            self.root.after(0, lambda: self.update_stock_info_header(ticker, company_name, current_price))
            
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
            if current_price > sma_50: signals.append("Above 50-day MA")
            if current_price > sma_200: signals.append("Above 200-day MA")
            if macd_current > signal_current: signals.append("MACD Bullish")
            if volume_ratio > 1.5: signals.append("High Volume")
            
            bullish_signals = sum(1 for s in signals if s in ["Oversold RSI", "Above 50-day MA", "Above 200-day MA", "MACD Bullish", "High Volume"])
            bearish_signals = sum(1 for s in signals if s in ["Overbought RSI"])
            
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
            formatted += f"real-time analysis using your custom Stock Predictor GPT with current market data.\n\n"
            
            formatted += f"⚠️ **Disclaimer**: This analysis is for educational purposes only.\n"
            formatted += f"Always consult with financial advisors and conduct your own research before making investment decisions.\n"
            formatted += f"Past performance does not guarantee future results.\n\n"
            formatted += f"{'='*60}\n"
            formatted += f"🏁 END OF ANALYSIS - Stock Analyzer v0.12 🏁\n"
            formatted += f"{'='*60}\n"
            formatted += f"\n\n\n------- SCROLL DOWN TO SEE COMPLETE ANALYSIS -------\n\n"
            
            return formatted
            
        except Exception as e:
            # Still update the stock info header even if there's an error
            company_name = self.get_company_name_from_ticker(ticker)
            self.root.after(0, lambda: self.update_stock_info_header(ticker, company_name))
            
            return f"❌ Error fetching data for {ticker} ({company_name}): {str(e)}\n\nPlease check the ticker symbol and try again."
    
    def _create_stock_analysis_prompt(self, user_input):
        """Create a specialized prompt for stock analysis"""
        return f"""Stock Analysis Request: {user_input}

Please provide a comprehensive stock analysis including:
- Market outlook and trends
- Technical analysis indicators
- Fundamental analysis factors
- Risk assessment
- Investment recommendations

Analysis:"""
    
    def _format_stock_response(self, response, original_question):
        """Format the AI response for stock analysis"""
        formatted = f"📊 STOCK ANALYSIS RESULTS\n"
        formatted += f"{'='*50}\n\n"
        formatted += f"Query: {original_question}\n\n"
        formatted += f"Analysis:\n{response}\n\n"
        formatted += f"⚠️ Disclaimer: This is AI-generated analysis for educational purposes only. Always consult with financial advisors before making investment decisions."
        return formatted
    
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
    
    def display_analysis_header(self, ticker, company_name):
        """Display the analysis header immediately at the top"""
        self.results_display.config(state=tk.NORMAL)
        header_text = f"📊 COMPREHENSIVE STOCK ANALYSIS: {ticker} ({company_name})\n"
        header_text += f"{'='*60}\n\n"
        header_text += "🔄 Analyzing... Please wait while we gather data...\n\n"
        self.results_display.insert(tk.END, header_text)
        self.results_display.config(state=tk.DISABLED)
        
        # Stay at the top - don't scroll
        self.results_display.see("1.0")
        self.results_display.update_idletasks()
    
    def display_complete_analysis(self, message, tag="response"):
        """Display the complete analysis and stay at the top"""
        self.results_display.config(state=tk.NORMAL)
        # Clear the loading message and replace with full analysis
        self.results_display.delete("1.0", tk.END)
        self.results_display.insert(tk.END, message + "\n\n\n\n\n", tag)
        self.results_display.config(state=tk.DISABLED)
        
        # Stay at the top so user can read from beginning
        self.results_display.see("1.0")
        self.results_display.update_idletasks()
        
        # DO NOT auto-scroll to bottom - let user read from the top
    
    def change_font_size(self, new_size):
        """Change the font size of the results display"""
        self.font_size.set(new_size)
        
        # Update the main font
        current_font = self.results_display.cget("font")
        new_font = ("Arial", new_size)
        self.results_display.configure(font=new_font)
        
        # Update all text tag styles
        self.update_text_styles()
        
        # Update status
        self.update_status(f"Font size changed to {new_size}pt")
    
    def update_text_styles(self):
        """Update text styling with current font size"""
        size = self.font_size.get()
        
        # Configure text styling with variable fonts
        self.results_display.tag_configure("response", font=("Arial", size), foreground="#2c3e50")
        self.results_display.tag_configure("error", font=("Arial", size), foreground="red")
        self.results_display.tag_configure("info", foreground="blue", 
                                          font=("Arial", max(10, size-2), "italic"))
        self.results_display.tag_configure("success", foreground="#10a37f", 
                                          font=("Arial", size, "bold"))

    def display_message(self, message, tag="response"):
        """Display a message in the results area"""
        self.results_display.config(state=tk.NORMAL)
        self.results_display.insert(tk.END, message + "\n\n\n\n\n", tag)  # Extra padding to prevent cutoff
        self.results_display.config(state=tk.DISABLED)
        
        # Use the helper function to ensure bottom visibility
        self.ensure_bottom_visible()
    
    def ensure_bottom_visible(self):
        """Ensure the bottom of the text is visible with multiple scroll attempts"""
        # Multiple attempts to ensure proper scrolling
        for i in range(3):
            self.results_display.see(tk.END)
            self.results_display.mark_set("insert", tk.END)
            self.results_display.see("insert")
            self.results_display.update_idletasks()
            self.root.update_idletasks()
    
    def update_status(self, status):
        """Update the status bar"""
        self.status_var.set(status)
    
    def find_ticker_from_company_name(self, input_text):
        """Find the actual ticker from company name or partial company name"""
        input_upper = input_text.upper().strip()
        
        # First, check if it's already a valid ticker
        for stock in self.stock_data:
            if stock['ticker'] == input_upper:
                return input_upper
        
        # Then check if it matches a company name
        best_match = None
        best_score = 0
        
        for stock in self.stock_data:
            company_upper = stock['company'].upper()
            
            # Exact company name match
            if company_upper == input_upper:
                return stock['ticker']
            
            # Check if input is contained in company name
            if input_upper in company_upper:
                # Score based on how much of the company name matches
                score = len(input_upper) / len(company_upper)
                if score > best_score:
                    best_score = score
                    best_match = stock['ticker']
            
            # Check if company name words start with input
            company_words = company_upper.split()
            for word in company_words:
                if word.startswith(input_upper) and len(input_upper) >= 3:
                    score = len(input_upper) / len(word)
                    if score > best_score:
                        best_score = score
                        best_match = stock['ticker']
        
        # Return best match if we found a decent one
        if best_match and best_score > 0.3:
            return best_match
        
        # Common company name mappings for popular stocks
        company_mappings = {
            'TESLA': 'TSLA',
            'APPLE': 'AAPL',
            'MICROSOFT': 'MSFT',
            'AMAZON': 'AMZN',
            'GOOGLE': 'GOOGL',
            'ALPHABET': 'GOOGL',
            'META': 'META',
            'FACEBOOK': 'META',
            'NVIDIA': 'NVDA',
            'NETFLIX': 'NFLX',
            'DISNEY': 'DIS',
            'MCDONALDS': 'MCD',
            'STARBUCKS': 'SBUX',
            'WALMART': 'WMT',
            'TARGET': 'TGT',
            'COSTCO': 'COST',
            'BOEING': 'BA',
            'CATERPILLAR': 'CAT',
            'JOHNSON': 'JNJ',  # Johnson & Johnson
            'PFIZER': 'PFE',
            'COCA COLA': 'KO',
            'PEPSI': 'PEP',
            'WILLIAMS': 'WMB',  # Williams Companies
            'EXXON': 'XOM',
            'CHEVRON': 'CVX',
            'FORD': 'F',
            'GENERAL MOTORS': 'GM',
            'UBER': 'UBER',
            'LYFT': 'LYFT',
            'AIRBNB': 'ABNB',
            'SPOTIFY': 'SPOT',
            'ZOOM': 'ZM',
            'SLACK': 'WORK',
            'PALANTIR': 'PLTR',
            'SNOWFLAKE': 'SNOW',
            'GAMESTOP': 'GME',
            'AMC': 'AMC',
            'BLACKBERRY': 'BB',
            'NOKIA': 'NOK',
            'AT&T': 'T',
            'ATT': 'T',
            'T-MOBILE': 'TMUS',
            'TMOBILE': 'TMUS',
            'T MOBILE': 'TMUS',
            'ENERGY FUELS': 'UUUU',
            'ENERGY': 'UUUU',
            'ENERGY FUELS': 'UUUU',
            'URANIUM': 'UUUU'
        }
        
        if input_upper in company_mappings:
            return company_mappings[input_upper]
        
        # If no match found, return original input
        return input_text

    def get_company_name_from_ticker(self, ticker):
        """Get company name from ticker symbol"""
        ticker_upper = ticker.upper().strip()
        
        # Search in stock data for the company name
        for stock in self.stock_data:
            if stock['ticker'] == ticker_upper:
                return stock['company']
        
        # If not found, return ticker as fallback
        return ticker_upper

    def update_stock_info_header(self, ticker, company_name, current_price=None):
        """Update the stock info header with ticker, company name, and price"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if current_price:
            info_text = f"📊 {ticker} ({company_name}) - ${current_price:.2f} | Updated: {timestamp}"
        else:
            info_text = f"📊 {ticker} ({company_name}) | Updated: {timestamp}"
        
        self.stock_info_label.config(text=info_text)
    
    def get_industry_insights(self, ticker, sector, industry, company_name):
        """Get industry-specific insights and company overview"""
        # Industry-specific insights based on common patterns
        insights = {
            'uranium': {
                'overview': "☢️ The uranium industry focuses on mining and processing uranium for nuclear energy. Companies benefit from growing global nuclear energy demand, carbon reduction initiatives, and potential nuclear renaissance driven by clean energy needs.",
                'key_factors': "Key factors: Nuclear energy policy, uranium spot prices, mining regulations, geopolitical stability, reactor construction"
            },
            'uranium_etf': {
                'overview': "📊 Uranium mining ETFs provide diversified exposure to uranium mining companies and the nuclear fuel cycle. These funds benefit from uranium price increases and nuclear energy sector growth.",
                'key_factors': "Key factors: Uranium commodity prices, nuclear policy, mining company performance, fund management fees"
            },
            'lithium': {
                'overview': "⚡ The lithium industry is crucial for battery technology, electric vehicles, and energy storage. Companies benefit from the global transition to clean energy, massive EV adoption, and grid-scale energy storage demand.",
                'key_factors': "Key factors: EV demand growth, battery technology advances, lithium carbonate prices, mining capacity expansion"
            },
            'lithium_etf': {
                'overview': "🔋 Lithium & battery ETFs provide exposure to companies involved in lithium mining, battery production, and EV supply chains. Growth tied to electric vehicle adoption and renewable energy storage.",
                'key_factors': "Key factors: EV market growth, lithium prices, battery technology, supply chain dynamics"
            },
            'crypto': {
                'overview': "₿ Cryptocurrency and blockchain companies operate in digital asset services, crypto mining, and blockchain technology development. Highly volatile sector tied to crypto market sentiment and regulatory developments.",
                'key_factors': "Key factors: Bitcoin/crypto prices, regulatory environment, institutional adoption, mining difficulty, energy costs"
            },
            'solar': {
                'overview': "☀️ Solar energy companies design, manufacture, and install solar power systems. Growth driven by renewable energy mandates, declining solar costs, and government incentives.",
                'key_factors': "Key factors: Government incentives, solar panel costs, energy policy, grid modernization, competition"
            },
            'tech': {
                'overview': "💻 Technology companies develop software, hardware, and digital services. Growth driven by digital transformation, AI adoption, and innovation cycles.",
                'key_factors': "Key factors: Innovation pace, market competition, regulatory changes, consumer demand, AI trends"
            },
            'mining': {
                'overview': "⛏️ Mining companies extract and process natural resources including precious metals, industrial metals, and energy materials. Performance tied to commodity cycles and global economic demand.",
                'key_factors': "Key factors: Commodity prices, mining costs, environmental regulations, geopolitical risks, demand cycles"
            }
        }
        
        # Determine industry category with specific ticker recognition
        ticker_upper = ticker.upper()
        company_lower = company_name.lower()
        industry_lower = industry.lower() if industry != 'N/A' else ''
        sector_lower = sector.lower() if sector != 'N/A' else ''
        
        # Specific ticker patterns
        if ticker_upper in ['URNJ', 'URNM', 'URA'] or 'uranium' in company_lower:
            if 'etf' in company_lower or ticker_upper in ['URNJ', 'URNM', 'URA']:
                category = 'uranium_etf'
            else:
                category = 'uranium'
        elif ticker_upper in ['LAC'] or any(word in ticker_upper or word in company_lower for word in ['LITHIUM AMERICAS']):
            category = 'lithium'
        elif ticker_upper in ['LIT', 'BATT', 'ILIT', 'KBAT'] or ('lithium' in company_lower and 'etf' in company_lower):
            category = 'lithium_etf'
        elif any(word in ticker_upper or word in company_lower or word in industry_lower for word in ['URANIUM', 'NUCLEAR', 'ENERGY FUELS', 'CAMECO', 'NEXGEN', 'DENISON', 'CENTRUS']):
            category = 'uranium'
        elif any(word in ticker_upper or word in company_lower or word in industry_lower for word in ['LITHIUM', 'LIVENT', 'ALBEMARLE', 'SQM', 'PIEDMONT']):
            category = 'lithium'
        elif any(word in ticker_upper or word in company_lower or word in industry_lower for word in ['CRYPTO', 'BITCOIN', 'BLOCKCHAIN', 'BTCS', 'COIN', 'DIGITAL ASSET', 'MINING']):
            category = 'crypto'
        elif any(word in ticker_upper or word in company_lower or word in industry_lower for word in ['SOLAR', 'SUNPOWER', 'ENPHASE', 'SOLAREDGE', 'FIRST SOLAR']):
            category = 'solar'
        elif any(word in sector_lower or word in industry_lower for word in ['mining', 'metals', 'materials']):
            category = 'mining'
        elif sector_lower == 'technology':
            category = 'tech'
        else:
            # Generic overview
            return f"🏢 **COMPANY & INDUSTRY OVERVIEW**\n• Company: {company_name}\n• Sector: {sector}\n• Industry: {industry}\n\n"
        
        insight = insights[category]
        return f"🏢 **COMPANY & INDUSTRY OVERVIEW**\n• Company: {company_name}\n• {insight['overview']}\n• {insight['key_factors']}\n\n"
    
    def use_existing_browser(self, url, ticker):
        """Use AppleScript to work with existing browser window - much simpler!"""
        try:
            import subprocess
            import time
            
            print(f"🌐 Using existing browser window...")
            print(f"🎯 Ticker to enter: '{ticker}'")  # Debug output
            
            # First, open the URL (this will use existing browser or open new tab)
            webbrowser.open(url)
            time.sleep(4)  # Wait longer for ChatGPT to load
            
            # Use AppleScript to type in the existing browser
            # Construct the script with proper string handling
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
                        key code 36  -- Return key
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
            applescript = applescript_template.replace("TICKER_PLACEHOLDER", ticker)
            
            # Execute AppleScript with longer timeout
            result = subprocess.run(['osascript', '-e', applescript], 
                                  capture_output=True, text=True, timeout=20)
            
            if result.returncode == 0 and "success" in result.stdout:
                print("✅ Successfully automated ticker input!")
                self.update_status(f"✅ Entered {ticker} in existing browser")
                return True
            else:
                print(f"❌ AppleScript automation didn't work as expected")
                print(f"stdout: {result.stdout}")
                print(f"stderr: {result.stderr}")
                return False
            
        except subprocess.TimeoutExpired:
            print("❌ AppleScript automation timed out")
            return False
        except Exception as e:
            print(f"❌ Browser automation error: {e}")
            return False
    
    def simple_clipboard_method(self, url, ticker):
        """Simple fallback - copy ticker and open URL"""
        try:
            import pyperclip
            pyperclip.copy(ticker)
            clipboard_success = True
        except ImportError:
            clipboard_success = False
        
        webbrowser.open(url)
        self.update_status("🌐 Opened Stock Predictor GPT!")
        
        if clipboard_success:
            self.display_message(f"🚀 STOCK PREDICTOR GPT OPENED!\n\n" +
                               f"✨ Your Stock Predictor GPT is now open!\n" +
                               f"📋 Ticker '{ticker}' copied to clipboard!\n\n" +
                               f"💡 Quick steps:\n" +
                               f"   1. Click in the ChatGPT input box\n" +
                               f"   2. Press Cmd+V to paste '{ticker}'\n" +
                               f"   3. Press Enter for analysis\n\n" +
                               f"🔗 GPT Link: {url}", "success")
        else:
            self.display_message(f"🚀 STOCK PREDICTOR GPT OPENED!\n\n" +
                               f"✨ Your Stock Predictor GPT is now open!\n" +
                               f"💡 Just type '{ticker}' in the input box and press Enter!\n\n" +
                               f"🔗 GPT Link: {url}", "success")
    
    # ...existing code...
def main():
    root = tk.Tk()
    app = StockAnalyzerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
