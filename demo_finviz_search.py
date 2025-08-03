#!/usr/bin/env python3
"""
Demo script showing the new Finviz-style search in action
Interactive demonstration of search capabilities
"""

import pandas as pd
import re

# Import the search functions from our test
from test_finviz_search import search_stocks, load_test_stock_data

def interactive_search_demo():
    """Interactive demo of the Finviz-style search"""
    print("🔍 Stock Analyzer v0.17 - Finviz-Style Search Demo")
    print("=" * 60)
    print("Experience the new search just like Finviz.com!")
    print("Search by ticker symbol OR company name")
    print("Type 'quit' to exit, 'examples' for sample searches\n")
    
    stock_data = load_test_stock_data()
    
    while True:
        query = input("🔎 Search stocks: ").strip()
        
        if query.lower() in ['quit', 'exit', 'q']:
            print("👋 Thanks for trying the new search!")
            break
        
        if query.lower() in ['examples', 'help', 'demo']:
            print("\n💡 Example searches to try:")
            examples = [
                ("AAPL", "Exact ticker match"),
                ("apple", "Company name search"),
                ("mic", "Partial company name (Microsoft, AMD)"),
                ("tesla", "Company name (finds TSLA)"),
                ("A", "Ticker starts with 'A'"),
                ("bank", "Company contains 'bank'"),
                ("ETF", "Find ETFs"),
                ("BRK", "Berkshire Hathaway classes")
            ]
            for example, description in examples:
                print(f"  '{example}' - {description}")
            print()
            continue
        
        if not query:
            print("Please enter a search term.\n")
            continue
        
        # Perform search
        results = search_stocks(query, stock_data, max_results=8)
        
        print(f"\n📊 Results for '{query}':")
        print("-" * 40)
        
        if results:
            for i, result in enumerate(results, 1):
                # Match type icons
                icons = {
                    'exact_ticker': '🎯',
                    'ticker_starts': '📈', 
                    'company_contains': '🏢',
                    'ticker_contains': '📊'
                }
                icon = icons.get(result['match_type'], '🔍')
                
                # Format display
                ticker = result['ticker']
                company = result['company']
                if len(company) > 35:
                    company = company[:32] + "..."
                
                print(f"  {i}. {icon} {ticker:<8} - {company}")
                
                # Show match type for clarity
                match_desc = {
                    'exact_ticker': 'Exact ticker match',
                    'ticker_starts': 'Ticker starts with query',
                    'company_contains': 'Company name contains query',
                    'ticker_contains': 'Ticker contains query'
                }
                desc = match_desc.get(result['match_type'], 'Match')
                print(f"      └─ {desc}")
            
            print(f"\n✅ Found {len(results)} matches")
        else:
            print("  No matches found")
            print("  💡 Try:")
            print("    • Ticker symbols (AAPL, MSFT, GOOGL)")
            print("    • Company names (Apple, Microsoft, Google)")
            print("    • Partial names (bank, tech, energy)")
        
        print()

def search_comparison_demo():
    """Show side-by-side comparison of search approaches"""
    print("\n🆚 Search Comparison Demo")
    print("=" * 40)
    
    stock_data = load_test_stock_data()
    
    test_queries = ["apple", "AAPL", "mic", "bank", "A"]
    
    for query in test_queries:
        print(f"\n🔎 Query: '{query}'")
        results = search_stocks(query, stock_data, max_results=3)
        
        if results:
            for result in results:
                match_type = result['match_type'].replace('_', ' ').title()
                print(f"  • {result['ticker']} - {result['company'][:30]}...")
                print(f"    └─ {match_type}")
        else:
            print("  No results")

if __name__ == "__main__":
    print("Choose demo mode:")
    print("1. Interactive search (recommended)")
    print("2. Quick comparison demo")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == "2":
        search_comparison_demo()
    else:
        interactive_search_demo()
