#!/usr/bin/env python3
"""
Test script for the new Finviz-style search functionality
Tests the search_stocks function with various queries
"""

import pandas as pd
import re

def clean_ticker(ticker_input):
    """Clean and validate ticker input"""
    if not ticker_input:
        return ""
    
    cleaned = re.sub(r'\s+', '', str(ticker_input).upper())
    cleaned = re.sub(r'[^A-Z0-9.-]', '', cleaned)
    cleaned = cleaned.strip('.-')
    
    if cleaned and cleaned[0].isdigit():
        return ""
    
    if len(cleaned) > 10:
        cleaned = cleaned[:10]
    
    return cleaned

def validate_ticker(ticker):
    """Basic ticker validation"""
    if not ticker:
        return False
    
    if not re.match(r'^[A-Z0-9.-]+$', ticker):
        return False
    
    if not ticker[0].isalpha():
        return False
    
    if len(ticker) < 1 or len(ticker) > 8:
        return False
    
    if len(ticker) > 1 and ticker[1:].isdigit() and len(ticker) > 5:
        return False
    
    return True

def load_test_stock_data():
    """Load test stock data"""
    default_stocks = [
        ['AAPL', 'Apple Inc'],
        ['MSFT', 'Microsoft Corporation'],
        ['GOOGL', 'Alphabet Inc Class A'],
        ['AMZN', 'Amazon.com Inc'],
        ['TSLA', 'Tesla Inc'],
        ['NVDA', 'NVIDIA Corporation'],
        ['META', 'Meta Platforms Inc'],
        ['BRK.A', 'Berkshire Hathaway Inc Class A'],
        ['BRK.B', 'Berkshire Hathaway Inc Class B'],
        ['JPM', 'JPMorgan Chase & Co'],
        ['JNJ', 'Johnson & Johnson'],
        ['V', 'Visa Inc'],
        ['PG', 'Procter & Gamble Co'],
        ['UNH', 'UnitedHealth Group Inc'],
        ['HD', 'Home Depot Inc'],
        ['MA', 'Mastercard Inc'],
        ['BAC', 'Bank of America Corp'],
        ['ABBV', 'AbbVie Inc'],
        ['AVGO', 'Broadcom Inc'],
        ['XOM', 'Exxon Mobil Corp'],
        ['WMT', 'Walmart Inc'],
        ['LLY', 'Eli Lilly and Co'],
        ['KO', 'Coca-Cola Co'],
        ['COST', 'Costco Wholesale Corp'],
        ['PEP', 'PepsiCo Inc'],
        ['TMO', 'Thermo Fisher Scientific Inc'],
        ['ABT', 'Abbott Laboratories'],
        ['ACN', 'Accenture PLC'],
        ['VZ', 'Verizon Communications Inc'],
        ['T', 'AT&T Inc'],
        ['NFLX', 'Netflix Inc'],
        ['CRM', 'Salesforce Inc'],
        ['ADBE', 'Adobe Inc'],
        ['TXN', 'Texas Instruments Inc'],
        ['DHR', 'Danaher Corp'],
        ['NKE', 'Nike Inc'],
        ['ORCL', 'Oracle Corp'],
        ['CVX', 'Chevron Corp'],
        ['WFC', 'Wells Fargo & Co'],
        ['AMD', 'Advanced Micro Devices Inc'],
        ['INTC', 'Intel Corp'],
        ['IBM', 'International Business Machines Corp'],
        ['SPY', 'SPDR S&P 500 ETF Trust'],
        ['QQQ', 'Invesco QQQ Trust'],
        ['VOO', 'Vanguard S&P 500 ETF'],
        ['VTI', 'Vanguard Total Stock Market ETF'],
        ['BTC-USD', 'Bitcoin USD'],
        ['ETH-USD', 'Ethereum USD']
    ]
    return pd.DataFrame(default_stocks, columns=['ticker', 'company_name'])

def search_stocks(query, stock_data, max_results=10):
    """Search stocks by ticker or company name - Finviz style"""
    if not query or len(query) < 1:
        return []
    
    query = query.upper().strip()
    results = []
    
    # Exact ticker matches first
    exact_matches = stock_data[stock_data['ticker'].str.upper() == query]
    for _, row in exact_matches.iterrows():
        results.append({
            'display': f"{row['ticker']} - {row['company_name']}",
            'ticker': row['ticker'],
            'company': row['company_name'],
            'match_type': 'exact_ticker'
        })
    
    # Ticker starts with query
    if len(results) < max_results:
        ticker_starts = stock_data[
            (stock_data['ticker'].str.upper().str.startswith(query)) & 
            (~stock_data['ticker'].str.upper().isin([r['ticker'].upper() for r in results]))
        ]
        for _, row in ticker_starts.iterrows():
            if len(results) >= max_results:
                break
            results.append({
                'display': f"{row['ticker']} - {row['company_name']}",
                'ticker': row['ticker'],
                'company': row['company_name'],
                'match_type': 'ticker_starts'
            })
    
    # Company name contains query
    if len(results) < max_results:
        company_contains = stock_data[
            (stock_data['company_name'].str.upper().str.contains(query, na=False)) &
            (~stock_data['ticker'].str.upper().isin([r['ticker'].upper() for r in results]))
        ]
        for _, row in company_contains.iterrows():
            if len(results) >= max_results:
                break
            results.append({
                'display': f"{row['ticker']} - {row['company_name']}",
                'ticker': row['ticker'],
                'company': row['company_name'],
                'match_type': 'company_contains'
            })
    
    # Ticker contains query (partial matches)
    if len(results) < max_results:
        ticker_contains = stock_data[
            (stock_data['ticker'].str.upper().str.contains(query, na=False)) &
            (~stock_data['ticker'].str.upper().isin([r['ticker'].upper() for r in results]))
        ]
        for _, row in ticker_contains.iterrows():
            if len(results) >= max_results:
                break
            results.append({
                'display': f"{row['ticker']} - {row['company_name']}",
                'ticker': row['ticker'],
                'company': row['company_name'],
                'match_type': 'ticker_contains'
            })
    
    return results[:max_results]

def test_search_functionality():
    """Test the Finviz-style search with various queries"""
    print("🔍 Testing Finviz-Style Search Functionality")
    print("=" * 60)
    
    stock_data = load_test_stock_data()
    
    test_queries = [
        "AAPL",      # Exact ticker match
        "apple",     # Company name search
        "mic",       # Partial company name
        "A",         # Single letter - should match multiple
        "tesla",     # Company name
        "BRK",       # Ticker starts with
        "bank",      # Company contains
        "ETF",       # ETF search
        "bitcoin",   # Crypto search
        "SO",        # Partial ticker (should match multiple)
    ]
    
    for query in test_queries:
        print(f"\n🔎 Query: '{query}'")
        print("-" * 40)
        
        results = search_stocks(query, stock_data, max_results=5)
        
        if results:
            for i, result in enumerate(results, 1):
                match_icon = {
                    'exact_ticker': '🎯',
                    'ticker_starts': '📈',
                    'company_contains': '🏢',
                    'ticker_contains': '📊'
                }.get(result['match_type'], '🔍')
                
                print(f"  {i}. {match_icon} {result['ticker']} - {result['company']}")
                print(f"     Match type: {result['match_type']}")
        else:
            print("  No results found")
    
    print("\n" + "=" * 60)
    print("✅ Search functionality test completed!")
    print("\n💡 This demonstrates how the new search works:")
    print("   • Exact ticker matches appear first")
    print("   • Then tickers starting with the query")
    print("   • Then company names containing the query")
    print("   • Finally partial ticker matches")
    print("   • Results are limited to prevent overwhelming the user")

if __name__ == "__main__":
    test_search_functionality()
