#!/usr/bin/env python3
"""Add lithium and uranium mining stocks to stock_data.csv"""

import csv
import os

def add_uranium_lithium_stocks():
    """Add comprehensive lithium and uranium mining stocks"""
    
    # Lithium and Uranium related stocks to add
    mining_stocks = [
        # Lithium Companies
        ("ALB", "Albemarle Corporation"),
        ("SQM", "Sociedad Quimica y Minera de Chile SA"),
        ("FMC", "FMC Corporation"),
        ("LTHM", "Livent Corporation"),
        ("LAC", "Lithium Americas Corp"),  # Already exists
        ("LTBR", "Lightbridge Corporation"),
        ("LIACF", "Lithium Ionic Corp"),
        ("LILIF", "Lithium Chile Inc"),
        ("PELL", "Piedmont Lithium Inc"),
        ("SGML", "Sigma Lithium Corporation"),
        ("ARVL", "Arrival"),
        ("LIT", "Global X Lithium & Battery Tech ETF"),
        
        # Uranium Companies  
        ("CCJ", "Cameco Corporation"),
        ("SRUUF", "Sprott Physical Uranium Trust"),
        ("UEC", "Uranium Energy Corp"),
        ("UUUU", "Energy Fuels Inc"),  # Already exists
        ("DNN", "Denison Mines Corp"),
        ("PALAF", "Paladin Energy Ltd"),
        ("NXE", "NexGen Energy Ltd"),
        ("UROY", "Uranium Royalty Corp"),
        ("LEU", "Centrus Energy Corp"),
        ("URG", "Ur-Energy Inc"),
        ("LTBR", "Lightbridge Corporation"),
        ("URNM", "North Shore Global Uranium Mining ETF"),
        ("URNJ", "Sprott Junior Uranium Miners ETF"),  # Already exists
        ("URA", "Global X Uranium ETF"),
        
        # Rare Earth & Critical Minerals
        ("REE", "Rare Element Resources Ltd"),
        ("MP", "MP Materials Corp"),
        ("LYNAS", "Lynas Rare Earths Limited"),
        ("REMX", "VanEck Rare Earth/Strategic Metals ETF"),
        ("VAL", "Valaris Limited"),
        ("NEM", "Newmont Corporation"),
        ("GOLD", "Barrick Gold Corporation"),
        ("AEM", "Agnico Eagle Mines Limited"),
        ("KGC", "Kinross Gold Corporation"),
        ("IAG", "Iamgold Corporation"),
        ("CDE", "Coeur Mining Inc"),
        ("HL", "Hecla Mining Company"),
        ("PAAS", "Pan American Silver Corp"),
        ("AG", "First Majestic Silver Corp"),
        ("EXK", "Endeavour Silver Corp"),
        
        # Battery Technology Related
        ("BATT", "Amplify Lithium & Battery Technology ETF"),
        ("ILIT", "iShares Lithium Miners and Producers ETF"),
        ("KBAT", "KraneShares Battery Metals & Technology ETF"),
        ("DRIV", "Global X Autonomous & Electric Vehicles ETF"),
        ("GRID", "First Trust NASDAQ Clean Edge Smart Grid Infrastructure Index Fund"),
        
        # Mining Equipment & Services
        ("CAT", "Caterpillar Inc"),
        ("DE", "Deere & Company"),
        ("TEX", "Terex Corporation"),
        ("JOY", "Komatsu Ltd"),
        
        # Related Energy/Clean Tech
        ("ENPH", "Enphase Energy Inc"),
        ("SEDG", "SolarEdge Technologies Inc"),
        ("FSLR", "First Solar Inc"),
        ("SPWR", "SunPower Corporation"),
        ("RUN", "Sunrun Inc"),
        ("NEE", "NextEra Energy Inc"),
        ("BEP", "Brookfield Renewable Partners LP"),
        ("CWEN", "Clearway Energy Inc")
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
    
    # Add new mining stocks that don't already exist
    new_additions = []
    for ticker, company in mining_stocks:
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
    
    print(f"\n📊 Added {len(new_additions)} new lithium/uranium/mining stocks:")
    for addition in new_additions[:15]:  # Show first 15
        print(f"   • {addition}")
    if len(new_additions) > 15:
        print(f"   ... and {len(new_additions) - 15} more")
    
    print(f"\n✅ Updated {csv_file} with lithium/uranium mining stocks")
    print(f"📈 Total stocks in database: {len(data_rows)}")

if __name__ == "__main__":
    add_uranium_lithium_stocks()
