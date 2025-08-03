#!/usr/bin/env python3
"""Add BTCS and cryptocurrency/blockchain related stocks to stock_data.csv"""

import csv
import os

def add_crypto_stocks():
    """Add BTCS and related cryptocurrency/blockchain stocks"""
    
    # Cryptocurrency and blockchain related stocks to add
    crypto_stocks = [
        ("BTCS", "BTCS Inc"),
        ("RIOT", "Riot Blockchain Inc"),
        ("MARA", "Marathon Digital Holdings Inc"),
        ("CLSK", "CleanSpark Inc"),
        ("HUT", "Hut 8 Mining Corp"),
        ("BITF", "Bitfarms Ltd"),
        ("CIFR", "Cipher Mining Inc"),
        ("CORZ", "Core Scientific Inc"),
        ("WULF", "TeraWulf Inc"),
        ("IREN", "Iris Energy Limited"),
        ("CAN", "Canaan Inc"),
        ("EBANG", "Ebang International Holdings Inc"),
        ("SOS", "SOS Limited"),
        ("BTBT", "Bit Digital Inc"),
        ("ANY", "Sphere 3D Corp"),
        ("DGHI", "Digihost Technology Inc"),
        ("ARBK", "Argo Blockchain plc"),
        ("GREE", "Greenidge Generation Holdings Inc"),
        ("BKKT", "Bakkt Holdings Inc"),
        ("SI", "Silvergate Capital Corp"),
        ("HOOD", "Robinhood Markets Inc"),
        ("SQ", "Block Inc"),
        ("PYPL", "PayPal Holdings Inc"),
        ("MSTR", "MicroStrategy Incorporated"),
        ("TSLA", "Tesla Inc"),  # Known for Bitcoin holdings
        ("NVDA", "NVIDIA Corporation"),  # GPU mining
        ("AMD", "Advanced Micro Devices Inc"),  # GPU mining
        ("INTC", "Intel Corporation"),  # Blockchain tech
        ("IBM", "International Business Machines Corp"),  # Blockchain solutions
        ("CRM", "Salesforce Inc"),  # Blockchain platforms
        ("ORCL", "Oracle Corporation"),  # Blockchain databases
        ("MOGO", "Mogo Inc"),
        ("FTFT", "Future FinTech Group Inc"),
        ("EBON", "Ebang International Holdings Inc"),
        ("NILE", "BitNile Holdings Inc"),
        ("GBTC", "Grayscale Bitcoin Trust"),
        ("ETHE", "Grayscale Ethereum Trust"),
        ("BITO", "ProShares Bitcoin Strategy ETF"),
        ("BITI", "ProShares Short Bitcoin Strategy ETF")
    ]
    
    csv_file = "stock_data.csv"
    
    # Read existing data
    existing_tickers = set()
    existing_data = []
    
    if os.path.exists(csv_file):
        with open(csv_file, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)  # Skip header
            existing_data.append(header)
            
            for row in reader:
                if len(row) >= 2:
                    existing_data.append(row)
                    existing_tickers.add(row[0].upper())
    
    # Add new crypto stocks that don't already exist
    new_additions = []
    for ticker, company in crypto_stocks:
        if ticker.upper() not in existing_tickers:
            existing_data.append([ticker, company])
            new_additions.append(f"{ticker} ({company})")
            print(f"✅ Added: {ticker} - {company}")
        else:
            print(f"⚠️ Already exists: {ticker}")
    
    # Sort by ticker (skip header)
    header = existing_data[0]
    data_rows = existing_data[1:]
    data_rows.sort(key=lambda x: x[0].upper())
    
    # Write back to file
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data_rows)
    
    print(f"\n📊 Added {len(new_additions)} new cryptocurrency/blockchain stocks:")
    for addition in new_additions:
        print(f"   • {addition}")
    
    print(f"\n✅ Updated {csv_file} with crypto/blockchain stocks")
    print(f"📈 Total stocks in database: {len(data_rows)}")

if __name__ == "__main__":
    add_crypto_stocks()
