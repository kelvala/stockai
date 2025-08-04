#!/usr/bin/env python3
"""
Test script for the new Finviz-style search functionality in the GUI
"""

import csv
import os
import re

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

def load_stock_data():
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
        print("Stock data file not found")
        return []
    except Exception as e:
        print(f"Error loading stock data: {str(e)}")
        return []
    
    return stock_data

def search_stocks(query, stock_data, max_results=8):
    """
    Advanced stock search with Finviz-style prioritization
    Returns filtered results with match types and smart ranking
    """
    if not query or len(query) < 1:
        return []
    
    query = query.upper().strip()
    results = []
    
    # Exact ticker matches first (highest priority)
    for stock in stock_data:
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
        for stock in stock_data:
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
        for stock in stock_data:
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
        for stock in stock_data:
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
        for stock in stock_data:
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

def test_search_functionality():
    """Test the search functionality with various queries"""
    print("🔍 Testing GUI Search Functionality")
    print("=" * 50)
    
    # Load stock data
    stock_data = load_stock_data()
    print(f"📊 Loaded {len(stock_data)} stocks from CSV")
    
    # Test cases
    test_queries = [
        "AAPL",      # Exact ticker match
        "Apple",     # Company name exact word
        "MICRO",     # Ticker starts with
        "microsoft", # Company contains (case insensitive)
        "GOOG",      # Partial ticker
        "bank",      # Multiple company matches
        "tesla",     # Company name
        "BTC",       # Crypto ticker
    ]
    
    for query in test_queries:
        print(f"\n🔍 Query: '{query}'")
        results = search_stocks(query, stock_data, max_results=5)
        
        if results:
            for i, result in enumerate(results, 1):
                icon = result['icon']
                ticker = result['ticker']
                company = result['company'][:40] + "..." if len(result['company']) > 40 else result['company']
                match_type = result['match_type']
                print(f"  {i}. {icon} {ticker} - {company} ({match_type})")
        else:
            print("  ❌ No matches found")

if __name__ == "__main__":
    test_search_functionality()
