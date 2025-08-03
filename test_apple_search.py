#!/usr/bin/env python3
"""
Test the improved search functionality with "APPLE" case
"""

import pandas as pd
import re

def load_test_stock_data():
    """Load test stock data"""
    default_stocks = [
        ['AAPL', 'Apple Inc'],
        ['MSFT', 'Microsoft Corporation'],
        ['GOOGL', 'Alphabet Inc Class A'],
        ['AMZN', 'Amazon.com Inc'],
        ['TSLA', 'Tesla Inc'],
        ['NVDA', 'NVIDIA Corporation'],
    ]
    return pd.DataFrame(default_stocks, columns=['ticker', 'company_name'])

def search_stocks(query, stock_data, max_results=10):
    """Search stocks by ticker or company name - improved version"""
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
    
    # Company name exact word matches (e.g., "APPLE" should find "Apple Inc")
    if len(results) < max_results:
        try:
            company_exact_word = stock_data[
                (stock_data['company_name'].str.upper().str.contains(r'\b' + query + r'\b', na=False, regex=True)) &
                (~stock_data['ticker'].str.upper().isin([r['ticker'].upper() for r in results]))
            ]
            for _, row in company_exact_word.iterrows():
                if len(results) >= max_results:
                    break
                results.append({
                    'display': f"{row['ticker']} - {row['company_name']}",
                    'ticker': row['ticker'],
                    'company': row['company_name'],
                    'match_type': 'company_exact_word'
                })
        except:
            # Fallback to simple contains if regex fails
            pass
    
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
    
    return results[:max_results]

def test_apple_search():
    """Test the APPLE search case specifically"""
    print("🧪 Testing 'APPLE' Search Case")
    print("=" * 40)
    
    stock_data = load_test_stock_data()
    
    # Test the problematic case
    query = "APPLE"
    results = search_stocks(query, stock_data, max_results=5)
    
    print(f"Query: '{query}'")
    print(f"Results found: {len(results)}")
    
    if results:
        for i, result in enumerate(results, 1):
            print(f"  {i}. {result['ticker']} - {result['company']}")
            print(f"     Match type: {result['match_type']}")
    else:
        print("  No results found")
    
    print("\n" + "=" * 40)
    
    # Test other variations
    test_queries = ["apple", "AAPL", "Apple Inc", "microsoft", "MICRO"]
    
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        results = search_stocks(query, stock_data, max_results=2)
        if results:
            for result in results:
                print(f"  → {result['ticker']} ({result['match_type']})")
        else:
            print("  → No results")

if __name__ == "__main__":
    test_apple_search()
