# Free GPT GUI Application - No API Required

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog
import threading
import requests
import json
import csv
import os
import webbrowser

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
        self.root.title("Stock Analyzer - AI Powered")
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
        title_label = ttk.Label(main_frame, text="📈 Stock Analyzer - AI Powered", 
                               font=("Arial", 24, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 30))
        
        # Question/Input section
        input_frame = ttk.LabelFrame(main_frame, text="Ask Stock Analysis Questions", padding="15")
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        input_frame.columnconfigure(0, weight=1)
        
        self.question_input = scrolledtext.ScrolledText(input_frame, height=4, 
                                                       font=("Arial", 11), wrap=tk.WORD)
        self.question_input.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        self.question_input.insert("1.0", "Enter stock symbol (e.g., AAPL) or ask stock analysis questions...")
        self.question_input.bind("<FocusIn>", self.clear_placeholder)
        self.question_input.bind("<KeyRelease>", self.on_key_release)
        self.question_input.bind("<Return>", self.on_enter_key)
        self.question_input.bind("<Button-1>", self.hide_suggestions)
        
        # Big Run GPT Button
        self.run_button = ttk.Button(input_frame, text="� ANALYZE STOCK", 
                                    command=self.run_gpt, 
                                    style="Accent.TButton")
        self.run_button.grid(row=1, column=0, pady=5)
        
        # Configure button style for larger appearance
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Arial", 14, "bold"))
        
        # Results display section
        results_frame = ttk.LabelFrame(main_frame, text="Stock Analysis Results", padding="15")
        results_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        self.results_display = scrolledtext.ScrolledText(results_frame, 
                                                        font=("Arial", 11), 
                                                        wrap=tk.WORD, 
                                                        state=tk.DISABLED,
                                                        bg="#f8f9fa")
        self.results_display.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure text styling
        self.results_display.tag_configure("response", font=("Arial", 11), foreground="#2c3e50")
        self.results_display.tag_configure("error", font=("Arial", 11), foreground="red")
        self.results_display.tag_configure("info", foreground="blue", 
                                          font=("Arial", 10, "italic"))
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                                   relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Configure main frame row weights
        main_frame.rowconfigure(2, weight=1)
        
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
    
    def prompt_for_api_key(self):
        """Not needed for free version"""
        pass
    
    def set_api_key(self, api_key):
        """Not needed for free version"""
        pass
    
    def clear_placeholder(self, event):
        """Clear placeholder text when user clicks in input"""
        current_text = self.question_input.get("1.0", tk.END).strip()
        if current_text == "Enter stock symbol (e.g., AAPL) or ask stock analysis questions...":
            self.question_input.delete("1.0", tk.END)
    
    def on_key_release(self, event):
        """Handle key release events for autocomplete and uppercase conversion"""
        # Hide suggestions on certain keys
        if event.keysym in ['Return', 'Tab', 'Escape']:
            self.hide_suggestions()
            return
        
        current_pos = self.question_input.index(tk.INSERT)
        content = self.question_input.get("1.0", tk.END)
        
        # Don't process placeholder text
        if content.strip() == "Enter stock symbol (e.g., AAPL) or ask stock analysis questions...":
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
        
        if len(content) < 1 or content == "Enter stock symbol (e.g., AAPL) or ask stock analysis questions...".upper():
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
        
        # Focus back to input
        self.question_input.focus_set()
    
    def on_enter_key(self, event):
        """Execute analysis when Enter key is pressed"""
        # Prevent default behavior (new line) and execute the button
        self.run_gpt()
        return "break"  # This prevents the default Enter behavior
    
    def open_chatgpt_browser(self):
        """Open ChatGPT in browser with the current question"""
        question = self.question_input.get("1.0", tk.END).strip()
        
        # Clear placeholder text if present
        if question == "Enter stock symbol (e.g., AAPL) or ask stock analysis questions...":
            question = ""
        
        # Format question for ChatGPT
        if question:
            # URL encode the question for ChatGPT
            import urllib.parse
            encoded_question = urllib.parse.quote(f"Analyze this stock: {question}")
            # Open ChatGPT with the question pre-filled (if your custom GPT supports it)
            chatgpt_url = f"https://chat.openai.com/?q={encoded_question}"
        else:
            # Open your custom GPT directly - replace this URL with your custom GPT link
            chatgpt_url = "https://chat.openai.com/"
        
        try:
            webbrowser.open(chatgpt_url)
            self.update_status("🌐 Opened ChatGPT in browser")
            self.display_message(f"Opening ChatGPT in browser with query: {question if question else 'Ready for your stock questions!'}", "info")
        except Exception as e:
            self.update_status(f"❌ Could not open browser: {str(e)}")
            messagebox.showerror("Browser Error", f"Could not open ChatGPT in browser: {str(e)}")
    
    def run_gpt(self):
        """Main function to run Stock Analysis AI"""
        question = self.question_input.get("1.0", tk.END).strip()
        
        if not question or question == "Enter stock symbol (e.g., AAPL) or ask stock analysis questions...":
            messagebox.showwarning("No Input", "Please enter a stock symbol or analysis question!")
            return
        
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
        """Call stock analysis API with specialized prompts"""
        try:
            print(f"Debug: Analyzing question: {question}")  # Debug output
            
            # Create a stock analysis prompt that mimics your custom GPT
            stock_prompt = self._create_stock_analysis_prompt(question)
            
            # Use Hugging Face free API with stock analysis context
            headers = {"Content-Type": "application/json"}
            data = {"inputs": stock_prompt, "parameters": {"max_length": 300, "temperature": 0.7}}
            
            print(f"Debug: Sending request to API...")  # Debug output
            
            response = requests.post(FREE_API_URL, headers=headers, json=data, timeout=30)
            
            print(f"Debug: Got response with status: {response.status_code}")  # Debug output
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    ai_response = result[0].get('generated_text', 'No response generated')
                    
                    # Clean up response
                    if stock_prompt in ai_response:
                        ai_response = ai_response.replace(stock_prompt, "").strip()
                    
                    # Format the response for stock analysis
                    formatted_response = self._format_stock_response(ai_response, question)
                    
                    self.root.after(0, self._display_ai_response, formatted_response, None)
                else:
                    self.root.after(0, self._display_ai_response, None, "No valid response from AI")
            elif response.status_code == 503:
                # Service temporarily unavailable, provide a fallback response
                fallback_response = self._create_fallback_analysis(question)
                self.root.after(0, self._display_ai_response, fallback_response, None)
            else:
                error_msg = f"API Error: {response.status_code} - {response.text}"
                self.root.after(0, self._display_ai_response, None, error_msg)
                
        except requests.exceptions.Timeout:
            fallback_response = self._create_fallback_analysis(question)
            self.root.after(0, self._display_ai_response, fallback_response, None)
        except Exception as e:
            print(f"Debug: Exception occurred: {str(e)}")  # Debug output
            fallback_response = self._create_fallback_analysis(question)
            self.root.after(0, self._display_ai_response, fallback_response, None)
    
    def _create_fallback_analysis(self, question):
        """Create a fallback analysis when API is unavailable"""
        formatted = f"📊 STOCK ANALYSIS RESULTS\n"
        formatted += f"{'='*50}\n\n"
        formatted += f"Query: {question}\n\n"
        formatted += f"Analysis:\n"
        formatted += f"Stock analysis for {question}:\n\n"
        formatted += f"• Market Position: Based on current market trends\n"
        formatted += f"• Technical Indicators: Review recent price movements and volume\n"
        formatted += f"• Fundamental Analysis: Consider company financials and industry position\n"
        formatted += f"• Risk Assessment: Evaluate market volatility and sector-specific risks\n"
        formatted += f"• Recommendation: Conduct thorough research before making investment decisions\n\n"
        formatted += f"Note: This is a basic analysis template. For detailed insights, please try again when the AI service is available.\n\n"
        formatted += f"⚠️ Disclaimer: This is AI-generated analysis for educational purposes only. Always consult with financial advisors before making investment decisions."
        return formatted
    
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
            self.display_message(response, "response")
            self.update_status("✅ AI response received")
        
        # Re-enable button
        self.run_button.config(state="normal", text="� ANALYZE STOCK")
    
    def display_message(self, message, tag="response"):
        """Display a message in the results area"""
        self.results_display.config(state=tk.NORMAL)
        self.results_display.insert(tk.END, message + "\n\n", tag)
        self.results_display.config(state=tk.DISABLED)
        self.results_display.see(tk.END)
    
    def update_status(self, status):
        """Update the status bar"""
        self.status_var.set(status)

def main():
    root = tk.Tk()
    app = StockAnalyzerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
