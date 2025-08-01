"""
Stock Analyzer Web App
A comprehensive stock analysis tool powered by AI and real-time data
Built with Streamlit for easy web deployment
"""

import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import re
import numpy as np
import requests
from io import StringIO

# Configure Streamlit page
st.set_page_config(
    page_title="Stock Analyzer - AI-Powered Stock Research",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #0099ff;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stock-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #0099ff;
        margin: 0.5rem 0;
    }
    .ai-button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white !important;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        text-decoration: none !important;
        display: inline-block;
        margin: 0.2rem;
        font-weight: bold;
        border: none;
        cursor: pointer;
    }
    .ai-button:hover {
        background: linear-gradient(45deg, #5a6fd8, #6a42a0);
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .screener-button {
        background: linear-gradient(45deg, #11998e, #38ef7d);
        color: white !important;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        text-decoration: none !important;
        display: inline-block;
        margin: 0.2rem;
        font-weight: bold;
        border: none;
        cursor: pointer;
    }
    .screener-button:hover {
        background: linear-gradient(45deg, #0f8a7e, #32d670);
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_stock_data():
    """Load stock data from CSV or create default dataset"""
    try:
        # Try to load from GitHub or local file
        df = pd.read_csv('stock_data.csv')
        return df
    except:
        # Fallback dataset with popular stocks
        default_stocks = [
            ['AAPL', 'Apple Inc'],
            ['MSFT', 'Microsoft Corporation'],
            ['GOOGL', 'Alphabet Inc Class A'],
            ['AMZN', 'Amazon.com Inc'],
            ['TSLA', 'Tesla Inc'],
            ['META', 'Meta Platforms Inc'],
            ['NVDA', 'NVIDIA Corporation'],
            ['JPM', 'JPMorgan Chase & Co'],
            ['JNJ', 'Johnson & Johnson'],
            ['V', 'Visa Inc'],
            ['PG', 'Procter & Gamble Co'],
            ['UNH', 'UnitedHealth Group Inc'],
            ['HD', 'Home Depot Inc'],
            ['MA', 'Mastercard Inc'],
            ['DIS', 'Walt Disney Co'],
            ['BAC', 'Bank of America Corp'],
            ['XOM', 'Exxon Mobil Corporation'],
            ['WMT', 'Walmart Inc'],
            ['CVX', 'Chevron Corporation'],
            ['LLY', 'Eli Lilly and Company']
        ]
        return pd.DataFrame(default_stocks, columns=['ticker', 'company_name'])

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_stock_data(ticker):
    """Fetch comprehensive stock data using yfinance"""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        hist = stock.history(period="1y")
        
        if hist.empty:
            return None
            
        # Don't cache the stock object itself, just the data we need
        return {
            'info': dict(info),  # Convert to regular dict
            'history': hist,
            'current_price': float(hist['Close'].iloc[-1]),
            'company_name': info.get('longName', f"{ticker} Corp")
        }
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {str(e)}")
        return None

def calculate_technical_indicators(hist):
    """Calculate technical indicators"""
    # Moving averages
    hist['SMA_50'] = hist['Close'].rolling(window=50).mean()
    hist['SMA_200'] = hist['Close'].rolling(window=200).mean()
    
    # RSI
    delta = hist['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    hist['RSI'] = 100 - (100 / (1 + rs))
    
    # MACD
    exp1 = hist['Close'].ewm(span=12).mean()
    exp2 = hist['Close'].ewm(span=26).mean()
    hist['MACD'] = exp1 - exp2
    hist['MACD_Signal'] = hist['MACD'].ewm(span=9).mean()
    
    # Bollinger Bands
    hist['BB_Middle'] = hist['Close'].rolling(window=20).mean()
    bb_std = hist['Close'].rolling(window=20).std()
    hist['BB_Upper'] = hist['BB_Middle'] + (bb_std * 2)
    hist['BB_Lower'] = hist['BB_Middle'] - (bb_std * 2)
    
    return hist

def calculate_intrinsic_value(info, current_price):
    """Calculate intrinsic value using multiple methods"""
    try:
        # Method 1: P/E based valuation
        forward_pe = info.get('forwardPE', 0)
        trailing_pe = info.get('trailingPE', 0)
        
        pe_based_value = 0
        if forward_pe and forward_pe > 0:
            fair_pe = min(15, forward_pe * 0.8)
            earnings_per_share = current_price / forward_pe
            pe_based_value = earnings_per_share * fair_pe
        elif trailing_pe and trailing_pe > 0:
            fair_pe = min(15, trailing_pe * 0.8)
            earnings_per_share = current_price / trailing_pe
            pe_based_value = earnings_per_share * fair_pe
        
        # Method 2: Book Value based
        book_value = info.get('bookValue', 0)
        book_value_based = book_value * 1.2 if book_value > 0 else 0
        
        # Method 3: Dividend Discount Model
        dividend_rate = info.get('dividendRate', 0)
        dividend_based_value = 0
        if dividend_rate and dividend_rate > 0:
            required_return = 0.08
            growth_rate = 0.03
            if required_return > growth_rate:
                dividend_based_value = dividend_rate / (required_return - growth_rate)
        
        # Calculate weighted average
        values = []
        weights = []
        
        if pe_based_value > 0:
            values.append(pe_based_value)
            weights.append(0.5)
        if book_value_based > 0:
            values.append(book_value_based)
            weights.append(0.3)
        if dividend_based_value > 0:
            values.append(dividend_based_value)
            weights.append(0.2)
        
        if values:
            total_weight = sum(weights)
            normalized_weights = [w/total_weight for w in weights]
            intrinsic_value = sum(v * w for v, w in zip(values, normalized_weights))
            
            # Sanity checks
            if intrinsic_value > current_price * 3:
                intrinsic_value = current_price * 1.5
            elif intrinsic_value < current_price * 0.3:
                intrinsic_value = current_price * 0.8
                
            return round(intrinsic_value, 2)
        else:
            return current_price
    except:
        return current_price

def get_recommendation(hist, info, current_price, intrinsic_value):
    """Generate buy/sell/hold recommendation"""
    try:
        # Get latest values
        rsi = hist['RSI'].iloc[-1]
        sma_50 = hist['SMA_50'].iloc[-1]
        sma_200 = hist['SMA_200'].iloc[-1]
        macd = hist['MACD'].iloc[-1]
        macd_signal = hist['MACD_Signal'].iloc[-1]
        
        # Score calculation
        score = 0
        signals = []
        
        # RSI signals
        if rsi < 30:
            score += 2
            signals.append("Oversold RSI")
        elif rsi > 70:
            score -= 2
            signals.append("Overbought RSI")
        
        # Moving average signals
        if current_price > sma_50:
            score += 1
            signals.append("Above 50-day MA")
        if current_price > sma_200:
            score += 1
            signals.append("Above 200-day MA")
        
        # MACD signal
        if macd > macd_signal:
            score += 1
            signals.append("MACD Bullish")
        
        # Valuation signal
        if intrinsic_value and current_price < intrinsic_value * 0.9:
            score += 2
            signals.append("Undervalued")
        elif intrinsic_value and current_price > intrinsic_value * 1.1:
            score -= 2
            signals.append("Overvalued")
        
        # Generate recommendation
        if score >= 3:
            recommendation = "🟢 BUY"
            color = "green"
        elif score <= -2:
            recommendation = "🔴 SELL"
            color = "red"
        else:
            recommendation = "🟡 HOLD"
            color = "orange"
        
        return recommendation, color, signals, score
    except:
        return "🟡 HOLD", "orange", ["Insufficient data"], 0

def create_price_chart(hist, ticker):
    """Create interactive price chart with technical indicators"""
    fig = go.Figure()
    
    # Candlestick chart
    fig.add_trace(go.Candlestick(
        x=hist.index,
        open=hist['Open'],
        high=hist['High'],
        low=hist['Low'],
        close=hist['Close'],
        name=ticker
    ))
    
    # Add moving averages
    fig.add_trace(go.Scatter(
        x=hist.index, y=hist['SMA_50'],
        line=dict(color='blue', width=1),
        name='50-day MA'
    ))
    
    fig.add_trace(go.Scatter(
        x=hist.index, y=hist['SMA_200'],
        line=dict(color='red', width=1),
        name='200-day MA'
    ))
    
    # Add Bollinger Bands
    fig.add_trace(go.Scatter(
        x=hist.index, y=hist['BB_Upper'],
        line=dict(color='gray', width=1, dash='dash'),
        name='BB Upper'
    ))
    
    fig.add_trace(go.Scatter(
        x=hist.index, y=hist['BB_Lower'],
        line=dict(color='gray', width=1, dash='dash'),
        name='BB Lower',
        fill='tonexty',
        fillcolor='rgba(128,128,128,0.1)'
    ))
    
    fig.update_layout(
        title=f"{ticker} - Price Chart with Technical Indicators",
        yaxis_title="Price ($)",
        xaxis_title="Date",
        height=500,
        xaxis_rangeslider_visible=False
    )
    
    return fig

def create_indicators_chart(hist):
    """Create RSI and MACD charts"""
    fig = go.Figure()
    
    # RSI subplot
    fig.add_trace(go.Scatter(
        x=hist.index, y=hist['RSI'],
        line=dict(color='purple'),
        name='RSI'
    ))
    
    # Add RSI levels
    fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Overbought")
    fig.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Oversold")
    
    fig.update_layout(
        title="RSI (Relative Strength Index)",
        yaxis_title="RSI",
        xaxis_title="Date",
        height=300,
        yaxis=dict(range=[0, 100])
    )
    
    return fig

def create_macd_chart(hist):
    """Create MACD chart"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=hist.index, y=hist['MACD'],
        line=dict(color='blue'),
        name='MACD'
    ))
    
    fig.add_trace(go.Scatter(
        x=hist.index, y=hist['MACD_Signal'],
        line=dict(color='red'),
        name='Signal'
    ))
    
    # MACD histogram
    histogram = hist['MACD'] - hist['MACD_Signal']
    colors = ['green' if x >= 0 else 'red' for x in histogram]
    
    fig.add_trace(go.Bar(
        x=hist.index, y=histogram,
        marker_color=colors,
        name='Histogram',
        opacity=0.6
    ))
    
    fig.update_layout(
        title="MACD (Moving Average Convergence Divergence)",
        yaxis_title="MACD",
        xaxis_title="Date",
        height=300
    )
    
    return fig

# Main Streamlit App
def main():
    # Header
    st.markdown('<h1 class="main-header">📊 Stock Analyzer</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">AI-Powered Stock Research & Analysis Tool</p>', unsafe_allow_html=True)
    
    # Load stock data
    stock_data = load_stock_data()
    
    # Sidebar
    with st.sidebar:
        st.header("🔍 Stock Selection")
        
        # Stock ticker input with autocomplete
        ticker_options = stock_data['ticker'].tolist()
        company_options = [f"{row['ticker']} - {row['company_name']}" for _, row in stock_data.iterrows()]
        
        selected_option = st.selectbox(
            "Select or type a stock ticker:",
            options=company_options,
            index=0,
            help="Choose from popular stocks or type your own ticker"
        )
        
        # Extract ticker from selection
        ticker = selected_option.split(' - ')[0] if selected_option else 'AAPL'
        
        # Manual ticker input
        manual_ticker = st.text_input(
            "Or enter a ticker manually:",
            value="",
            help="Enter stock symbol (e.g., AAPL, TSLA)",
            placeholder="e.g., AAPL"
        ).upper()
        
        if manual_ticker:
            ticker = manual_ticker
        
        st.markdown("---")
        
        # AI Assistant Links
        st.header("🤖 AI Assistants")
        
        if ticker:
            # Get company name for context
            try:
                temp_stock = yf.Ticker(ticker)
                company_name = temp_stock.info.get('longName', ticker)
            except:
                company_name = ticker
            
            # Simple, reliable copy solution
            analysis_text = f"Analyze {ticker} ({company_name}) stock ticker for smart investing decisions"
            
            # Display the text clearly
            st.write(f"**Copy this text for AI Assistant:**")
            
            # Use a text input that's easy to copy from
            st.text_input(
                "📋 Select all and copy (Ctrl+A, then Ctrl+C):",
                value=analysis_text,
                key=f"copy_text_{ticker}",
                help="Click in the box, select all (Ctrl+A), then copy (Ctrl+C)"
            )
            
            st.info("💡 **Instructions:** Copy the text above, then click an AI Assistant button below and paste it!")
            
            ai_assistants = [
                ("📈 Stock Predictor", "https://chatgpt.com/g/g-686c5fc3dd948191a0ff9c14cecda1b4-stock-predictor-prompt-gpt"),
                ("💡 Smarter Investing", "https://chatgpt.com/g/g-687b911701a08191aadd69c345a67d17-9-prompts-for-smarter-investing"),
                ("💰 Dividend Sniper", "https://chatgpt.com/g/g-6878fe277c5c819180211289d9e16148-high-yield-dividend-sniper")
            ]
        else:
            ai_assistants = [
                ("📈 Stock Predictor", "https://chatgpt.com/g/g-686c5fc3dd948191a0ff9c14cecda1b4-stock-predictor-prompt-gpt"),
                ("💡 Smarter Investing", "https://chatgpt.com/g/g-687b911701a08191aadd69c345a67d17-9-prompts-for-smarter-investing"),
                ("💰 Dividend Sniper", "https://chatgpt.com/g/g-6878fe277c5c819180211289d9e16148-high-yield-dividend-sniper")
            ]
        
        for name, url in ai_assistants:
            st.markdown(f'''
            <a href="{url}" target="_blank" class="ai-button" style="color: white !important; text-decoration: none !important;">
                {name}
            </a>
            ''', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Stock Screeners - Using popular free screener websites
        st.header("💎 Stock Screeners")
        
        screeners = [
            ("🎯 Value Screener", "https://finviz.com/screener.ashx?v=111&f=fa_pe_low,fa_pb_low"),
            ("📊 Dividend Screener", "https://finviz.com/screener.ashx?v=111&f=fa_div_high"),
            ("🚀 Growth Screener", "https://finviz.com/screener.ashx?v=111&f=fa_sales5years_pos,fa_salesqoq_pos")
        ]
        
        for name, url in screeners:
            st.markdown(f'''
            <a href="{url}" target="_blank" class="screener-button" style="color: white !important; text-decoration: none !important;">
                {name}
            </a>
            ''', unsafe_allow_html=True)
    
    # Main content
    if ticker:
        # Fetch stock data
        with st.spinner(f'Fetching data for {ticker}...'):
            stock_data_obj = get_stock_data(ticker)
        
        if stock_data_obj:
            info = stock_data_obj['info']
            hist = stock_data_obj['history']
            current_price = stock_data_obj['current_price']
            company_name = stock_data_obj['company_name']
            
            # Calculate technical indicators
            hist = calculate_technical_indicators(hist)
            
            # Calculate intrinsic value
            intrinsic_value = calculate_intrinsic_value(info, current_price)
            
            # Get recommendation
            recommendation, rec_color, signals, score = get_recommendation(hist, info, current_price, intrinsic_value)
            
            # Stock header card
            st.markdown(f"""
            <div class="stock-card">
                <h2>{ticker} - {company_name}</h2>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h3>${current_price:.2f}</h3>
                        <p>Current Price</p>
                    </div>
                    <div>
                        <h3>${intrinsic_value:.2f}</h3>
                        <p>Intrinsic Value</p>
                    </div>
                    <div>
                        <h3 style="color: {rec_color};">{recommendation}</h3>
                        <p>Recommendation</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Metrics row
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Market Cap",
                    f"${info.get('marketCap', 0):,.0f}" if info.get('marketCap') else "N/A"
                )
            
            with col2:
                st.metric(
                    "P/E Ratio",
                    f"{info.get('forwardPE', info.get('trailingPE', 'N/A')):.2f}" if info.get('forwardPE') or info.get('trailingPE') else "N/A"
                )
            
            with col3:
                year_change = ((current_price - hist['Close'].iloc[0]) / hist['Close'].iloc[0]) * 100
                st.metric(
                    "1-Year Change",
                    f"{year_change:+.2f}%"
                )
            
            with col4:
                rsi = hist['RSI'].iloc[-1]
                st.metric(
                    "RSI (14)",
                    f"{rsi:.1f}"
                )
            
            # Charts
            st.header("📊 Technical Analysis")
            
            # Price chart
            price_chart = create_price_chart(hist, ticker)
            st.plotly_chart(price_chart, use_container_width=True)
            
            # Indicator charts
            col1, col2 = st.columns(2)
            
            with col1:
                rsi_chart = create_indicators_chart(hist)
                st.plotly_chart(rsi_chart, use_container_width=True)
            
            with col2:
                macd_chart = create_macd_chart(hist)
                st.plotly_chart(macd_chart, use_container_width=True)
            
            # Analysis section
            st.header("📋 Detailed Analysis")
            
            # Company info
            with st.expander("📈 Company Information", expanded=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Sector:** {info.get('sector', 'N/A')}")
                    st.write(f"**Industry:** {info.get('industry', 'N/A')}")
                    st.write(f"**Employees:** {info.get('fullTimeEmployees', 'N/A'):,}" if info.get('fullTimeEmployees') else "**Employees:** N/A")
                
                with col2:
                    st.write(f"**52-Week High:** ${hist['High'].max():.2f}")
                    st.write(f"**52-Week Low:** ${hist['Low'].min():.2f}")
                    st.write(f"**Average Volume:** {hist['Volume'].mean():,.0f}")
                
                if info.get('longBusinessSummary'):
                    st.write("**Business Summary:**")
                    st.write(info['longBusinessSummary'][:500] + "..." if len(info['longBusinessSummary']) > 500 else info['longBusinessSummary'])
            
            # Technical signals
            with st.expander("🔍 Technical Signals", expanded=True):
                st.write(f"**Recommendation Score:** {score}")
                st.write("**Active Signals:**")
                for signal in signals:
                    st.write(f"• {signal}")
                
                # Support and resistance levels
                st.write("**Key Levels:**")
                st.write(f"• **Resistance:** ${hist['High'].rolling(20).max().iloc[-1]:.2f}")
                st.write(f"• **Support:** ${hist['Low'].rolling(20).min().iloc[-1]:.2f}")
            
            # Valuation analysis
            with st.expander("💰 Valuation Analysis", expanded=True):
                valuation_ratio = current_price / intrinsic_value if intrinsic_value > 0 else 1
                
                if valuation_ratio < 0.9:
                    valuation_status = "🟢 Undervalued"
                elif valuation_ratio > 1.1:
                    valuation_status = "🔴 Overvalued"
                else:
                    valuation_status = "🟡 Fairly Valued"
                
                st.write(f"**Valuation Status:** {valuation_status}")
                st.write(f"**Price to Intrinsic Value Ratio:** {valuation_ratio:.2f}")
                
                # Financial metrics
                if info.get('totalRevenue'):
                    st.write(f"**Annual Revenue:** ${info['totalRevenue']:,.0f}")
                if info.get('totalDebt'):
                    st.write(f"**Total Debt:** ${info['totalDebt']:,.0f}")
                if info.get('freeCashflow'):
                    st.write(f"**Free Cash Flow:** ${info['freeCashflow']:,.0f}")
        
        else:
            st.error(f"Could not fetch data for ticker: {ticker}. Please check the symbol and try again.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <p><strong>Stock Analyzer v0.16</strong> - AI-Powered Stock Research Tool</p>
        <p>⚠️ <strong>Disclaimer:</strong> This analysis is for educational purposes only. 
        Always consult with financial advisors and conduct your own research before making investment decisions.</p>
        <p>Data provided by Yahoo Finance • Built with Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
