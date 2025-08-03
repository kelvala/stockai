#!/usr/bin/env python3
"""Test script to verify ticker resolution and company name lookup"""

import csv
import os

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
    except Exception as e:
        print(f"Error loading stock data: {str(e)}")
    
    return stock_data

def get_company_name_from_ticker(ticker, stock_data):
    """Get company name from ticker symbol"""
    ticker_upper = ticker.upper().strip()
    
    # Search in stock data for the company name
    for stock in stock_data:
        if stock['ticker'] == ticker_upper:
            return stock['company']
    
    # If not found, return ticker as fallback
    return ticker_upper

def test_ticker_lookup():
    """Test the ticker lookup functionality"""
    stock_data = load_stock_data()
    
    # Test cases
    test_cases = ['T', 'AAPL', 'TSLA', 'MSFT', 'GOOGL', 'INVALID']
    
    print("Testing ticker to company name lookup:")
    print("-" * 50)
    
    for ticker in test_cases:
        company = get_company_name_from_ticker(ticker, stock_data)
        print(f"{ticker:8} -> {company}")
    
    print("\nTesting 'T' specifically:")
    print(f"T -> {get_company_name_from_ticker('T', stock_data)}")

if __name__ == "__main__":
    test_ticker_lookup()
