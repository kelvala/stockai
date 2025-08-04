#!/usr/bin/env python3
"""
Add missing uranium and energy stocks to stock_data.csv
Ensures comprehensive uranium sector coverage
"""

import csv
import os
from datetime import datetime
import shutil

def add_uranium_stocks():
    """Add comprehensive uranium and energy stocks"""
    
    print("⚛️ Adding comprehensive uranium and energy stocks...")
    
    # Comprehensive uranium/energy stocks list
    uranium_stocks = [
        # US Uranium Stocks
        ("UUUU", "Energy Fuels Inc"),
        ("UEC", "Uranium Energy Corp"),
        ("LEU", "Centrus Energy Corp"),
        ("LTBR", "Lightbridge Corp"),
        ("URG", "Ur-Energy Inc"),
        ("BWXT", "BWX Technologies Inc"),
        ("SMR", "NuScale Power Corp"),
        
        # Canadian Uranium Stocks
        ("CCJ", "Cameco Corp"),
        ("DNN", "Denison Mines Corp"),
        ("FCU.TO", "Fission Uranium Corp"),
        ("NXE.TO", "NexGen Energy Ltd"),
        ("GLO.TO", "Global Atomic Corp"),
        ("EU.TO", "Encavis AG"),
        ("CVV.TO", "Cameco Corporation"),
        ("URC.TO", "Uranium Royalty Corp"),
        ("UUUU", "Energy Fuels Inc"),
        
        # International Uranium Stocks
        ("PALAF", "Paladin Energy Ltd"),
        ("BQSSF", "Boss Energy Ltd"),
        ("BANNF", "Bannerman Energy Ltd"),
        ("PENMF", "Peninsula Energy Ltd"),
        ("DYLLF", "Deep Yellow Ltd"),
        ("ELVUF", "Elevate Uranium Ltd"),
        
        # Uranium ETFs and Trusts
        ("URA", "Global X Uranium ETF"),
        ("URNM", "North Shore Global Uranium Mining ETF"),
        ("URNJ", "Sprott Junior Uranium Miners ETF"),
        ("SRUUF", "Sprott Physical Uranium Trust"),
        ("UPC.TO", "Uranium Participation Corp"),
        
        # Nuclear Energy Companies
        ("NLR", "VanEck Nuclear Energy ETF"),
        ("PKN", "Invesco Nuclear Energy ETF"),
        ("NEE", "NextEra Energy Inc"),
        ("EXC", "Exelon Corp"),
        ("CEG", "Constellation Energy Corp"),
        ("VST", "Vistra Corp"),
        ("CNP", "CenterPoint Energy Inc"),
        
        # Related Energy/Mining
        ("REMX", "VanEck Rare Earth/Strategic Metals ETF"),
        ("LIT", "Global X Lithium & Battery Tech ETF"),
        ("COPX", "Global X Copper Miners ETF"),
        ("SIL", "Global X Silver Miners ETF"),
        ("GDX", "VanEck Gold Miners ETF"),
        ("PICK", "iShares MSCI Global Metals & Mining Producers ETF"),
        
        # Additional Uranium Related
        ("UROY", "Uranium Royalty Corp"),
        ("UUUU", "Energy Fuels Inc"),  # Ensure this is definitely there
    ]
    
    # Read existing stock data
    existing_tickers = set()
    stock_data = []
    
    if os.path.exists('stock_data.csv'):
        print("📋 Reading existing stock data...")
        with open('stock_data.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader, None)
            for row in reader:
                if len(row) >= 2:
                    ticker, company = row[0].strip().upper(), row[1].strip()
                    existing_tickers.add(ticker)
                    stock_data.append((ticker, company))
    
    # Add new uranium stocks that don't exist
    new_additions = 0
    for ticker, company in uranium_stocks:
        ticker_clean = ticker.upper().strip()
        if ticker_clean not in existing_tickers:
            stock_data.append((ticker_clean, company))
            existing_tickers.add(ticker_clean)
            new_additions += 1
            print(f"  ✅ Added: {ticker_clean} - {company}")
    
    # Sort by ticker for better organization
    stock_data.sort(key=lambda x: x[0])
    
    # Create backup of existing file
    if os.path.exists('stock_data.csv'):
        backup_name = f"stock_data_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        shutil.copy('stock_data.csv', backup_name)
        print(f"📦 Backup created: {backup_name}")
    
    # Write updated stock data
    print("💾 Saving updated stock data...")
    with open('stock_data.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['ticker', 'company_name'])
        writer.writerows(stock_data)
    
    print(f"🎉 SUCCESS!")
    print(f"   📊 Total tickers: {len(stock_data)}")
    print(f"   ➕ New additions: {new_additions}")
    print(f"   ⚛️ Uranium sector coverage enhanced!")
    
    # Verify UUUU was added/exists
    if any(ticker == 'UUUU' for ticker, _ in stock_data):
        print("   ✅ UUUU (Energy Fuels Inc) confirmed in database!")
    
    return True

if __name__ == "__main__":
    add_uranium_stocks()
