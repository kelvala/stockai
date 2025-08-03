#!/usr/bin/env python3
"""
Enhanced script to add even MORE US stock tickers
"""

import csv
import os

def add_more_comprehensive_tickers():
    """Add even more comprehensive US stock tickers"""
    
    # Read existing tickers
    existing_tickers = set()
    csv_path = "stock_data.csv"
    
    try:
        with open(csv_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                existing_tickers.add(row['ticker'].upper())
    except FileNotFoundError:
        pass
    
    print(f"📊 Found {len(existing_tickers)} existing tickers")
    
    # Massive additional ticker list (real US stocks)
    additional_tickers = [
        # Major tech stocks not yet included
        {'ticker': 'CRM', 'company_name': 'Salesforce Inc'},
        {'ticker': 'SHOP', 'company_name': 'Shopify Inc'},
        {'ticker': 'SQ', 'company_name': 'Block Inc'},
        {'ticker': 'ROKU', 'company_name': 'Roku Inc'},
        {'ticker': 'DOCU', 'company_name': 'DocuSign Inc'},
        {'ticker': 'ZM', 'company_name': 'Zoom Video Communications Inc'},
        {'ticker': 'SNOW', 'company_name': 'Snowflake Inc'},
        {'ticker': 'CRWD', 'company_name': 'CrowdStrike Holdings Inc'},
        {'ticker': 'DDOG', 'company_name': 'Datadog Inc'},
        {'ticker': 'NET', 'company_name': 'Cloudflare Inc'},
        {'ticker': 'OKTA', 'company_name': 'Okta Inc'},
        {'ticker': 'TWLO', 'company_name': 'Twilio Inc'},
        {'ticker': 'ZS', 'company_name': 'Zscaler Inc'},
        {'ticker': 'WORK', 'company_name': 'Slack Technologies Inc'},
        {'ticker': 'SPLK', 'company_name': 'Splunk Inc'},
        
        # Biotech and Healthcare
        {'ticker': 'MRNA', 'company_name': 'Moderna Inc'},
        {'ticker': 'BNTX', 'company_name': 'BioNTech SE'},
        {'ticker': 'PFE', 'company_name': 'Pfizer Inc'},
        {'ticker': 'JNJ', 'company_name': 'Johnson & Johnson'},
        {'ticker': 'ABBV', 'company_name': 'AbbVie Inc'},
        {'ticker': 'LLY', 'company_name': 'Eli Lilly and Company'},
        {'ticker': 'UNH', 'company_name': 'UnitedHealth Group Inc'},
        {'ticker': 'TMO', 'company_name': 'Thermo Fisher Scientific Inc'},
        {'ticker': 'DHR', 'company_name': 'Danaher Corporation'},
        {'ticker': 'ABT', 'company_name': 'Abbott Laboratories'},
        {'ticker': 'ISRG', 'company_name': 'Intuitive Surgical Inc'},
        {'ticker': 'SYK', 'company_name': 'Stryker Corporation'},
        {'ticker': 'BSX', 'company_name': 'Boston Scientific Corporation'},
        {'ticker': 'MDT', 'company_name': 'Medtronic plc'},
        {'ticker': 'CI', 'company_name': 'Cigna Corporation'},
        {'ticker': 'CVS', 'company_name': 'CVS Health Corporation'},
        {'ticker': 'ANTM', 'company_name': 'Anthem Inc'},
        {'ticker': 'HUM', 'company_name': 'Humana Inc'},
        {'ticker': 'CNC', 'company_name': 'Centene Corporation'},
        {'ticker': 'WBA', 'company_name': 'Walgreens Boots Alliance Inc'},
        
        # Financial services
        {'ticker': 'BRK.A', 'company_name': 'Berkshire Hathaway Inc Class A'},
        {'ticker': 'BRK.B', 'company_name': 'Berkshire Hathaway Inc Class B'},
        {'ticker': 'JPM', 'company_name': 'JPMorgan Chase & Co'},
        {'ticker': 'BAC', 'company_name': 'Bank of America Corporation'},
        {'ticker': 'WFC', 'company_name': 'Wells Fargo & Company'},
        {'ticker': 'C', 'company_name': 'Citigroup Inc'},
        {'ticker': 'GS', 'company_name': 'Goldman Sachs Group Inc'},
        {'ticker': 'MS', 'company_name': 'Morgan Stanley'},
        {'ticker': 'BLK', 'company_name': 'BlackRock Inc'},
        {'ticker': 'SCHW', 'company_name': 'Charles Schwab Corporation'},
        {'ticker': 'AXP', 'company_name': 'American Express Company'},
        {'ticker': 'V', 'company_name': 'Visa Inc'},
        {'ticker': 'MA', 'company_name': 'Mastercard Incorporated'},
        {'ticker': 'PYPL', 'company_name': 'PayPal Holdings Inc'},
        {'ticker': 'COF', 'company_name': 'Capital One Financial Corporation'},
        {'ticker': 'USB', 'company_name': 'U.S. Bancorp'},
        {'ticker': 'PNC', 'company_name': 'PNC Financial Services Group Inc'},
        {'ticker': 'TFC', 'company_name': 'Truist Financial Corporation'},
        {'ticker': 'KEY', 'company_name': 'KeyCorp'},
        {'ticker': 'RF', 'company_name': 'Regions Financial Corporation'},
        
        # Electric vehicles and clean energy
        {'ticker': 'TSLA', 'company_name': 'Tesla Inc'},
        {'ticker': 'NIO', 'company_name': 'NIO Inc'},
        {'ticker': 'XPEV', 'company_name': 'XPeng Inc'},
        {'ticker': 'LI', 'company_name': 'Li Auto Inc'},
        {'ticker': 'LCID', 'company_name': 'Lucid Group Inc'},
        {'ticker': 'RIVN', 'company_name': 'Rivian Automotive Inc'},
        {'ticker': 'F', 'company_name': 'Ford Motor Company'},
        {'ticker': 'GM', 'company_name': 'General Motors Company'},
        {'ticker': 'NKLA', 'company_name': 'Nikola Corporation'},
        {'ticker': 'QS', 'company_name': 'QuantumScape Corporation'},
        {'ticker': 'ENPH', 'company_name': 'Enphase Energy Inc'},
        {'ticker': 'SEDG', 'company_name': 'SolarEdge Technologies Inc'},
        {'ticker': 'FSLR', 'company_name': 'First Solar Inc'},
        {'ticker': 'SPWR', 'company_name': 'SunPower Corporation'},
        {'ticker': 'RUN', 'company_name': 'Sunrun Inc'},
        
        # Airlines and Travel
        {'ticker': 'DAL', 'company_name': 'Delta Air Lines Inc'},
        {'ticker': 'AAL', 'company_name': 'American Airlines Group Inc'},
        {'ticker': 'UAL', 'company_name': 'United Airlines Holdings Inc'},
        {'ticker': 'LUV', 'company_name': 'Southwest Airlines Co'},
        {'ticker': 'ALK', 'company_name': 'Alaska Air Group Inc'},
        {'ticker': 'JBLU', 'company_name': 'JetBlue Airways Corporation'},
        {'ticker': 'SAVE', 'company_name': 'Spirit Airlines Inc'},
        {'ticker': 'HA', 'company_name': 'Hawaiian Holdings Inc'},
        {'ticker': 'SKYW', 'company_name': 'SkyWest Inc'},
        {'ticker': 'UBER', 'company_name': 'Uber Technologies Inc'},
        {'ticker': 'LYFT', 'company_name': 'Lyft Inc'},
        {'ticker': 'ABNB', 'company_name': 'Airbnb Inc'},
        {'ticker': 'BKNG', 'company_name': 'Booking Holdings Inc'},
        {'ticker': 'EXPE', 'company_name': 'Expedia Group Inc'},
        {'ticker': 'TRIP', 'company_name': 'TripAdvisor Inc'},
        
        # Retail and Consumer
        {'ticker': 'AMZN', 'company_name': 'Amazon.com Inc'},
        {'ticker': 'WMT', 'company_name': 'Walmart Inc'},
        {'ticker': 'COST', 'company_name': 'Costco Wholesale Corporation'},
        {'ticker': 'TGT', 'company_name': 'Target Corporation'},
        {'ticker': 'HD', 'company_name': 'Home Depot Inc'},
        {'ticker': 'LOW', 'company_name': 'Lowe\'s Companies Inc'},
        {'ticker': 'TJX', 'company_name': 'TJX Companies Inc'},
        {'ticker': 'SBUX', 'company_name': 'Starbucks Corporation'},
        {'ticker': 'MCD', 'company_name': 'McDonald\'s Corporation'},
        {'ticker': 'NKE', 'company_name': 'Nike Inc'},
        {'ticker': 'LULU', 'company_name': 'Lululemon Athletica Inc'},
        {'ticker': 'ULTA', 'company_name': 'Ulta Beauty Inc'},
        {'ticker': 'BBY', 'company_name': 'Best Buy Co Inc'},
        {'ticker': 'M', 'company_name': 'Macy\'s Inc'},
        {'ticker': 'JWN', 'company_name': 'Nordstrom Inc'},
        {'ticker': 'GPS', 'company_name': 'Gap Inc'},
        {'ticker': 'ANF', 'company_name': 'Abercrombie & Fitch Co'},
        {'ticker': 'AEO', 'company_name': 'American Eagle Outfitters Inc'},
        
        # Media and Entertainment
        {'ticker': 'DIS', 'company_name': 'Walt Disney Company'},
        {'ticker': 'NFLX', 'company_name': 'Netflix Inc'},
        {'ticker': 'CMCSA', 'company_name': 'Comcast Corporation'},
        {'ticker': 'T', 'company_name': 'AT&T Inc'},
        {'ticker': 'VZ', 'company_name': 'Verizon Communications Inc'},
        {'ticker': 'TMUS', 'company_name': 'T-Mobile US Inc'},
        {'ticker': 'CHTR', 'company_name': 'Charter Communications Inc'},
        {'ticker': 'WBD', 'company_name': 'Warner Bros Discovery Inc'},
        {'ticker': 'PARA', 'company_name': 'Paramount Global'},
        {'ticker': 'FOX', 'company_name': 'Fox Corporation'},
        {'ticker': 'FOXA', 'company_name': 'Fox Corporation Class A'},
        {'ticker': 'LYV', 'company_name': 'Live Nation Entertainment Inc'},
        {'ticker': 'SPOT', 'company_name': 'Spotify Technology SA'},
        {'ticker': 'ROKU', 'company_name': 'Roku Inc'},
        
        # Food and Beverage
        {'ticker': 'KO', 'company_name': 'Coca-Cola Company'},
        {'ticker': 'PEP', 'company_name': 'PepsiCo Inc'},
        {'ticker': 'MDLZ', 'company_name': 'Mondelez International Inc'},
        {'ticker': 'GIS', 'company_name': 'General Mills Inc'},
        {'ticker': 'K', 'company_name': 'Kellogg Company'},
        {'ticker': 'CPB', 'company_name': 'Campbell Soup Company'},
        {'ticker': 'HSY', 'company_name': 'Hershey Company'},
        {'ticker': 'TSN', 'company_name': 'Tyson Foods Inc'},
        {'ticker': 'HRL', 'company_name': 'Hormel Foods Corporation'},
        {'ticker': 'CAG', 'company_name': 'Conagra Brands Inc'},
        {'ticker': 'KHC', 'company_name': 'Kraft Heinz Company'},
        {'ticker': 'SJM', 'company_name': 'J.M. Smucker Company'},
        {'ticker': 'KR', 'company_name': 'Kroger Co'},
        
        # Industrial and Manufacturing
        {'ticker': 'BA', 'company_name': 'Boeing Company'},
        {'ticker': 'HON', 'company_name': 'Honeywell International Inc'},
        {'ticker': 'UNP', 'company_name': 'Union Pacific Corporation'},
        {'ticker': 'UPS', 'company_name': 'United Parcel Service Inc'},
        {'ticker': 'FDX', 'company_name': 'FedEx Corporation'},
        {'ticker': 'CSX', 'company_name': 'CSX Corporation'},
        {'ticker': 'NSC', 'company_name': 'Norfolk Southern Corporation'},
        {'ticker': 'KSU', 'company_name': 'Kansas City Southern'},
        {'ticker': 'CAT', 'company_name': 'Caterpillar Inc'},
        {'ticker': 'DE', 'company_name': 'Deere & Company'},
        {'ticker': 'MMM', 'company_name': '3M Company'},
        {'ticker': 'GE', 'company_name': 'General Electric Company'},
        {'ticker': 'EMR', 'company_name': 'Emerson Electric Co'},
        {'ticker': 'ITW', 'company_name': 'Illinois Tool Works Inc'},
        {'ticker': 'PH', 'company_name': 'Parker-Hannifin Corporation'},
        {'ticker': 'ROK', 'company_name': 'Rockwell Automation Inc'},
        {'ticker': 'ETN', 'company_name': 'Eaton Corporation plc'},
        
        # Semiconductors
        {'ticker': 'NVDA', 'company_name': 'NVIDIA Corporation'},
        {'ticker': 'AMD', 'company_name': 'Advanced Micro Devices Inc'},
        {'ticker': 'INTC', 'company_name': 'Intel Corporation'},
        {'ticker': 'QCOM', 'company_name': 'QUALCOMM Incorporated'},
        {'ticker': 'AVGO', 'company_name': 'Broadcom Inc'},
        {'ticker': 'TXN', 'company_name': 'Texas Instruments Incorporated'},
        {'ticker': 'ADI', 'company_name': 'Analog Devices Inc'},
        {'ticker': 'MRVL', 'company_name': 'Marvell Technology Inc'},
        {'ticker': 'LRCX', 'company_name': 'Lam Research Corporation'},
        {'ticker': 'AMAT', 'company_name': 'Applied Materials Inc'},
        {'ticker': 'KLAC', 'company_name': 'KLA Corporation'},
        {'ticker': 'ASML', 'company_name': 'ASML Holding NV'},
        {'ticker': 'TSM', 'company_name': 'Taiwan Semiconductor Manufacturing Company'},
        {'ticker': 'MU', 'company_name': 'Micron Technology Inc'},
        {'ticker': 'WDC', 'company_name': 'Western Digital Corporation'},
        {'ticker': 'STX', 'company_name': 'Seagate Technology Holdings plc'},
        
        # Popular smaller caps and growth stocks
        {'ticker': 'ARKK', 'company_name': 'ARK Innovation ETF'},
        {'ticker': 'ARKG', 'company_name': 'ARK Genomics Revolution ETF'},
        {'ticker': 'ARKQ', 'company_name': 'ARK Autonomous Technology & Robotics ETF'},
        {'ticker': 'ARKW', 'company_name': 'ARK Next Generation Internet ETF'},
        {'ticker': 'ARKF', 'company_name': 'ARK Fintech Innovation ETF'},
        {'ticker': 'SPCE', 'company_name': 'Virgin Galactic Holdings Inc'},
        {'ticker': 'PLTR', 'company_name': 'Palantir Technologies Inc'},
        {'ticker': 'WISH', 'company_name': 'ContextLogic Inc'},
        {'ticker': 'CLOV', 'company_name': 'Clover Health Investments Corp'},
        {'ticker': 'SOFI', 'company_name': 'SoFi Technologies Inc'},
        {'ticker': 'HOOD', 'company_name': 'Robinhood Markets Inc'},
        {'ticker': 'RBLX', 'company_name': 'Roblox Corporation'},
        {'ticker': 'U', 'company_name': 'Unity Software Inc'},
        {'ticker': 'PATH', 'company_name': 'UiPath Inc'},
        {'ticker': 'OPEN', 'company_name': 'Opendoor Technologies Inc'},
        {'ticker': 'PINS', 'company_name': 'Pinterest Inc'},
        {'ticker': 'SNAP', 'company_name': 'Snap Inc'},
        {'ticker': 'TWTR', 'company_name': 'Twitter Inc'},
        {'ticker': 'UPST', 'company_name': 'Upstart Holdings Inc'},
        {'ticker': 'AFRM', 'company_name': 'Affirm Holdings Inc'},
        
        # Small letter tickers that might be missed
        {'ticker': 'A', 'company_name': 'Agilent Technologies Inc'},
        {'ticker': 'B', 'company_name': 'Barnes Group Inc'},
        {'ticker': 'C', 'company_name': 'Citigroup Inc'},
        {'ticker': 'D', 'company_name': 'Dominion Energy Inc'},
        {'ticker': 'E', 'company_name': 'Eni S.p.A.'},
        {'ticker': 'F', 'company_name': 'Ford Motor Company'},
        {'ticker': 'G', 'company_name': 'Genpact Limited'},
        {'ticker': 'H', 'company_name': 'Hyatt Hotels Corporation'},
        {'ticker': 'I', 'company_name': 'Intelsat S.A.'},
        {'ticker': 'J', 'company_name': 'Jacobs Engineering Group Inc'},
        {'ticker': 'K', 'company_name': 'Kellogg Company'},
        {'ticker': 'L', 'company_name': 'Loews Corporation'},
        {'ticker': 'M', 'company_name': 'Macy\'s Inc'},
        {'ticker': 'N', 'company_name': 'NetSuite Inc'},
        {'ticker': 'O', 'company_name': 'Realty Income Corporation'},
        {'ticker': 'P', 'company_name': 'Pandora Media Inc'},
        {'ticker': 'Q', 'company_name': 'Quintiles IMS Holdings Inc'},
        {'ticker': 'R', 'company_name': 'Ryder System Inc'},
        {'ticker': 'S', 'company_name': 'Sprint Corporation'},
        {'ticker': 'T', 'company_name': 'AT&T Inc'},
        {'ticker': 'U', 'company_name': 'Unity Software Inc'},
        {'ticker': 'V', 'company_name': 'Visa Inc'},
        {'ticker': 'W', 'company_name': 'Wayfair Inc'},
        {'ticker': 'X', 'company_name': 'United States Steel Corporation'},
        {'ticker': 'Y', 'company_name': 'Alleghany Corporation'},
        {'ticker': 'Z', 'company_name': 'Zillow Group Inc'},
    ]
    
    # Remove duplicates
    new_tickers = []
    for ticker_data in additional_tickers:
        if ticker_data['ticker'] not in existing_tickers:
            new_tickers.append(ticker_data)
            existing_tickers.add(ticker_data['ticker'])
    
    print(f"🚀 Adding {len(new_tickers)} additional tickers")
    
    # Append to existing CSV
    if new_tickers:
        with open(csv_path, 'a', newline='', encoding='utf-8') as file:
            fieldnames = ['ticker', 'company_name']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            for ticker_data in new_tickers:
                writer.writerow({
                    'ticker': ticker_data['ticker'],
                    'company_name': ticker_data['company_name']
                })
    
    # Read and sort the entire file
    all_data = []
    with open(csv_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            all_data.append({
                'ticker': row['ticker'].upper().strip(),
                'company_name': row['company_name'].strip()
            })
    
    # Remove any duplicates that might have crept in
    seen = set()
    unique_data = []
    for item in all_data:
        if item['ticker'] not in seen:
            seen.add(item['ticker'])
            unique_data.append(item)
    
    # Sort by ticker
    unique_data.sort(key=lambda x: x['ticker'])
    
    # Rewrite the file sorted and deduplicated
    with open(csv_path, 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['ticker', 'company_name']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        writer.writeheader()
        for item in unique_data:
            writer.writerow(item)
    
    print(f"✅ Final count: {len(unique_data)} unique tickers")
    print("🎉 Stock data file updated with comprehensive US ticker list!")

if __name__ == "__main__":
    add_more_comprehensive_tickers()
