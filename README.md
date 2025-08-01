# 📈 Stock Analyzer - AI Powered v0.14

A modern Python GUI application that provides AI-powered stock analysis and market insights using advanced AI assistants.

## ✨ Features

- **Stock Analysis Interface**: Clean, user-friendly tkinter-based interface designed for stock analysis
- **AI-Powered Insights**: Advanced AI analysis using custom AI assistants for stocks, market trends, and investment recommendations
- **AI Assistant Integration**: Direct integration with specialized AI assistants:
  - 🌐 **Stock Predictor**: Advanced stock analysis and predictions
  - 💰 **Dividend Sniper**: High-yield dividend stock recommendations  
  - 💡 **Smarter Investing**: 9-prompt investing framework analysis
- **Automated Browser Integration**: Automatically opens AI assistants and inputs stock tickers
- **Real-time Analysis**: Threaded API calls for responsive stock analysis
- **Professional Results**: Formatted analysis results with disclaimers and risk assessments
- **Free to Use**: No API keys required - uses free AI models
- **Error Handling**: Comprehensive error handling and user feedback

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- Internet connection (for AI analysis)

### Installation

1. **Install dependencies:**
   ```bash
   pip install requests
   ```

2. **Run the application:**
   ```bash
   python3 gpt_chat_gui.py
   ```

## 🎯 How to Use

### **Stock Analysis:**
1. **Enter Stock Symbol**: Type a stock symbol like "AAPL", "TSLA", "GOOGL"
2. **Ask Analysis Questions**: Ask questions like:
   - "Analyze AAPL stock"
   - "What's the outlook for Tesla?"
   - "Should I buy Microsoft stock?"
   - "Compare Apple vs Google stocks"
3. **Click "ANALYZE STOCK"**: Get comprehensive AI analysis
4. **Review Results**: See formatted analysis with recommendations

### **Example Queries:**
- `AAPL` - Get analysis for Apple Inc.
- `What's the market outlook for tech stocks?`
- `Analyze Tesla's recent performance`
- `Compare AMZN and GOOGL for long-term investment`

## 🛠️ Features Overview

### Analysis Interface
- **Large input area** for stock symbols and questions
- **Professional results display** with formatted analysis
- **Status updates** showing analysis progress
- **Always-on-top focus** for easy access

### AI Integration
- **Specialized stock analysis prompts** 
- **Comprehensive analysis** including technical and fundamental factors
- **Risk assessment** and investment recommendations
- **Market trend analysis**

### Professional Output
- **Formatted results** with clear sections
- **Investment disclaimers** for responsible analysis
- **Error handling** for invalid symbols or network issues

## 🔧 Technical Details

- **Framework**: tkinter (built-in Python GUI framework)
- **AI Model**: OpenAI GPT-3.5-turbo
- **Threading**: Prevents GUI freezing during API calls
- **File Format**: JSON for chat history storage

## 🔐 Security Notes

- API keys are stored locally in `config.json`
- Consider using environment variables for production
- API key input field uses password masking
- No chat data is sent to external servers (except OpenAI)

## 📝 Example Usage

```python
# Run the application
python gpt_chat_gui.py

# The GUI will open with:
# 1. API key configuration section
# 2. Chat conversation area
# 3. Message input area
# 4. Control buttons (Send, Clear, Save, Load)
```

## 🎨 Interface Preview

```
┌─────────────────────────────────────────┐
│          🤖 GPT Chat Assistant          │
├─────────────────────────────────────────┤
│ API Key: [••••••••••••] [Set API Key]  │
│ Status: ✅ Ready to chat!               │
├─────────────────────────────────────────┤
│                                         │
│ [Conversation Area]                     │
│ You: Hello, how are you?                │
│ GPT: I'm doing well, thank you!...     │
│                                         │
├─────────────────────────────────────────┤
│ Your Message:                           │
│ [Text Input Area]                       │
│                              [Send]     │
│                              [Clear]    │
│                              [Save]     │
│                              [Load]     │
└─────────────────────────────────────────┘
```

## 🤝 Contributing

Feel free to fork this project and submit pull requests for improvements!

## 📄 License

This project is open source and available under the MIT License.
