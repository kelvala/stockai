#!/usr/bin/env python3
"""
Update stock_data.csv with real company names for better search testing
"""

import csv
import os

# Common stock tickers and their real company names
real_company_names = {
    'AAPL': 'Apple Inc',
    'MSFT': 'Microsoft Corporation',
    'GOOGL': 'Alphabet Inc Class A',
    'GOOG': 'Alphabet Inc Class C',
    'AMZN': 'Amazon.com Inc',
    'TSLA': 'Tesla Inc',
    'NVDA': 'NVIDIA Corporation',
    'META': 'Meta Platforms Inc',
    'BRK.A': 'Berkshire Hathaway Inc Class A',
    'BRK.B': 'Berkshire Hathaway Inc Class B',
    'JPM': 'JPMorgan Chase & Co',
    'JNJ': 'Johnson & Johnson',
    'V': 'Visa Inc',
    'PG': 'Procter & Gamble Co',
    'UNH': 'UnitedHealth Group Inc',
    'HD': 'Home Depot Inc',
    'MA': 'Mastercard Inc',
    'BAC': 'Bank of America Corp',
    'ABBV': 'AbbVie Inc',
    'AVGO': 'Broadcom Inc',
    'XOM': 'Exxon Mobil Corp',
    'WMT': 'Walmart Inc',
    'LLY': 'Eli Lilly and Co',
    'KO': 'Coca-Cola Co',
    'COST': 'Costco Wholesale Corp',
    'PEP': 'PepsiCo Inc',
    'TMO': 'Thermo Fisher Scientific Inc',
    'ABT': 'Abbott Laboratories',
    'ACN': 'Accenture PLC',
    'VZ': 'Verizon Communications Inc',
    'T': 'AT&T Inc',
    'NFLX': 'Netflix Inc',
    'CRM': 'Salesforce Inc',
    'ADBE': 'Adobe Inc',
    'TXN': 'Texas Instruments Inc',
    'DHR': 'Danaher Corp',
    'NKE': 'Nike Inc',
    'ORCL': 'Oracle Corp',
    'CVX': 'Chevron Corp',
    'WFC': 'Wells Fargo & Co',
    'AMD': 'Advanced Micro Devices Inc',
    'INTC': 'Intel Corp',
    'IBM': 'International Business Machines Corp',
    'SPY': 'SPDR S&P 500 ETF Trust',
    'QQQ': 'Invesco QQQ Trust',
    'VOO': 'Vanguard S&P 500 ETF',
    'VTI': 'Vanguard Total Stock Market ETF',
    'BTC-USD': 'Bitcoin USD',
    'ETH-USD': 'Ethereum USD',
    'AAL': 'American Airlines Group Inc',
    'MSTR': 'MicroStrategy Inc',
    'GBTC': 'Grayscale Bitcoin Trust',
    'BTCS': 'BTCS Inc'
}

def update_stock_data():
    """Update the stock_data.csv with real company names"""
    csv_path = 'stock_data.csv'
    
    # Read current data
    rows = []
    try:
        with open(csv_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                ticker = row['ticker']
                # Use real company name if available, otherwise keep existing
                if ticker in real_company_names:
                    row['company_name'] = real_company_names[ticker]
                rows.append(row)
    except FileNotFoundError:
        print(f"File {csv_path} not found")
        return
    
    # Write updated data
    with open(csv_path, 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['ticker', 'company_name']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"✅ Updated {len(rows)} rows in stock_data.csv")
    print(f"📊 Updated {len(real_company_names)} tickers with real company names")

if __name__ == "__main__":
    update_stock_data()
