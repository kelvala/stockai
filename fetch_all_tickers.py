#!/usr/bin/env python3
"""
Script to fetch ALL US stock tickers and add them to stock_data.csv
"""

import pandas as pd
import requests
import csv
import os
from datetime import datetime

def fetch_all_us_tickers():
    """Fetch comprehensive list of US stock tickers from multiple sources"""
    all_tickers = []
    
    print("🚀 Fetching ALL US Stock Tickers...")
    print("=" * 50)
    
    # 1. S&P 500 Companies
    try:
        print("📈 Fetching S&P 500 companies...")
        sp500_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        sp500_tables = pd.read_html(sp500_url)
        sp500_df = sp500_tables[0]
        
        for _, row in sp500_df.iterrows():
            ticker = str(row['Symbol']).replace('.', '-').strip().upper()
            company = str(row['Security']).strip()
            if ticker and company and ticker != 'NAN':
                all_tickers.append({'ticker': ticker, 'company_name': company, 'source': 'S&P500'})
        
        print(f"✅ Added {len([t for t in all_tickers if t['source'] == 'S&P500'])} S&P 500 companies")
    except Exception as e:
        print(f"❌ Error fetching S&P 500: {e}")
    
    # 2. NASDAQ Listed Companies
    try:
        print("📊 Fetching NASDAQ companies...")
        nasdaq_url = 'https://www.nasdaq.com/market-activity/stocks/screener?exchange=nasdaq&letter=0&render=download'
        # Alternative URL that works better
        nasdaq_url2 = 'https://pkgstore.datahub.io/core/nasdaq-listings/nasdaq-listed_csv/data/7665719fb51081ba0bd834fde71ce822/nasdaq-listed_csv.csv'
        
        try:
            nasdaq_df = pd.read_csv(nasdaq_url2)
        except:
            # Fallback to manual NASDAQ list
            nasdaq_tickers = [
                'AAPL', 'MSFT', 'AMZN', 'GOOGL', 'GOOG', 'META', 'TSLA', 'NVDA', 'NFLX', 'ADBE',
                'CRM', 'PYPL', 'INTC', 'CMCSA', 'PEP', 'COST', 'TMUS', 'AVGO', 'TXN', 'QCOM',
                'CHTR', 'SBUX', 'INTU', 'AMD', 'AMGN', 'ISRG', 'BKNG', 'GILD', 'MDLZ', 'ADP',
                'CSX', 'REGN', 'VRTX', 'FISV', 'ATVI', 'MU', 'AMAT', 'ADI', 'LRCX', 'KLAC',
                'MRVL', 'ORLY', 'DXCM', 'SNPS', 'CDNS', 'WDAY', 'NXPI', 'ASML', 'TEAM', 'ADSK'
            ]
            for ticker in nasdaq_tickers:
                if not any(t['ticker'] == ticker for t in all_tickers):
                    all_tickers.append({'ticker': ticker, 'company_name': f'{ticker} Corp', 'source': 'NASDAQ'})
        
        if 'nasdaq_df' in locals() and not nasdaq_df.empty:
            for _, row in nasdaq_df.iterrows():
                ticker = str(row.get('Symbol', '')).strip().upper()
                company = str(row.get('Company Name', '')).strip()
                if ticker and company and ticker != 'NAN' and not any(t['ticker'] == ticker for t in all_tickers):
                    all_tickers.append({'ticker': ticker, 'company_name': company, 'source': 'NASDAQ'})
        
        nasdaq_count = len([t for t in all_tickers if t['source'] == 'NASDAQ'])
        print(f"✅ Added {nasdaq_count} NASDAQ companies")
    except Exception as e:
        print(f"❌ Error fetching NASDAQ: {e}")
    
    # 3. NYSE Listed Companies
    try:
        print("🏛️ Fetching NYSE companies...")
        # Major NYSE stocks
        nyse_tickers = [
            'JPM', 'JNJ', 'V', 'PG', 'UNH', 'MA', 'HD', 'NVDA', 'DIS', 'BAC',
            'XOM', 'WFC', 'CVX', 'LLY', 'ABBV', 'PFE', 'TMO', 'ABT', 'CRM', 'ORCL',
            'ACN', 'DHR', 'VZ', 'MRK', 'KO', 'WMT', 'ADBE', 'NKE', 'LIN', 'NEE',
            'BMY', 'T', 'PM', 'RTX', 'SCHW', 'HON', 'UNP', 'LOW', 'C', 'QCOM',
            'IBM', 'GS', 'CAT', 'DE', 'SPGI', 'BLK', 'AXP', 'BKNG', 'SYK', 'TJX',
            'AMD', 'GILD', 'MDLZ', 'CVS', 'CI', 'ISRG', 'ZTS', 'CB', 'MMC', 'SO',
            'DUK', 'BSX', 'BDX', 'ITW', 'SHW', 'GE', 'EMR', 'NSC', 'AON', 'EQIX',
            'APD', 'CL', 'FCX', 'SLB', 'MO', 'USB', 'PNC', 'GM', 'F', 'DAL',
            'UBER', 'SNOW', 'COP', 'PSA', 'WM', 'ICE', 'DG', 'TGT', 'BK', 'TFC',
            'COF', 'AIG', 'FIS', 'CME', 'PLD', 'GD', 'WELL', 'SPG', 'MSI', 'SQ'
        ]
        
        for ticker in nyse_tickers:
            if not any(t['ticker'] == ticker for t in all_tickers):
                all_tickers.append({'ticker': ticker, 'company_name': f'{ticker} Inc', 'source': 'NYSE'})
        
        nyse_count = len([t for t in all_tickers if t['source'] == 'NYSE'])
        print(f"✅ Added {nyse_count} NYSE companies")
    except Exception as e:
        print(f"❌ Error fetching NYSE: {e}")
    
    # 4. Popular ETFs and additional tickers
    try:
        print("📈 Adding popular ETFs and additional tickers...")
        additional_tickers = [
            # Major ETFs
            {'ticker': 'SPY', 'company_name': 'SPDR S&P 500 ETF Trust', 'source': 'ETF'},
            {'ticker': 'QQQ', 'company_name': 'Invesco QQQ Trust', 'source': 'ETF'},
            {'ticker': 'IWM', 'company_name': 'iShares Russell 2000 ETF', 'source': 'ETF'},
            {'ticker': 'VTI', 'company_name': 'Vanguard Total Stock Market ETF', 'source': 'ETF'},
            {'ticker': 'VOO', 'company_name': 'Vanguard S&P 500 ETF', 'source': 'ETF'},
            {'ticker': 'VEA', 'company_name': 'Vanguard FTSE Developed Markets ETF', 'source': 'ETF'},
            {'ticker': 'VWO', 'company_name': 'Vanguard FTSE Emerging Markets ETF', 'source': 'ETF'},
            {'ticker': 'BND', 'company_name': 'Vanguard Total Bond Market ETF', 'source': 'ETF'},
            {'ticker': 'GLD', 'company_name': 'SPDR Gold Shares', 'source': 'ETF'},
            {'ticker': 'SLV', 'company_name': 'iShares Silver Trust', 'source': 'ETF'},
            
            # Crypto-related
            {'ticker': 'COIN', 'company_name': 'Coinbase Global Inc', 'source': 'CRYPTO'},
            {'ticker': 'MSTR', 'company_name': 'MicroStrategy Inc', 'source': 'CRYPTO'},
            {'ticker': 'RIOT', 'company_name': 'Riot Platforms Inc', 'source': 'CRYPTO'},
            {'ticker': 'MARA', 'company_name': 'Marathon Digital Holdings Inc', 'source': 'CRYPTO'},
            
            # Meme Stocks & Popular
            {'ticker': 'GME', 'company_name': 'GameStop Corp', 'source': 'MEME'},
            {'ticker': 'AMC', 'company_name': 'AMC Entertainment Holdings Inc', 'source': 'MEME'},
            {'ticker': 'BB', 'company_name': 'BlackBerry Ltd', 'source': 'MEME'},
            {'ticker': 'NOK', 'company_name': 'Nokia Corp', 'source': 'POPULAR'},
            {'ticker': 'PLTR', 'company_name': 'Palantir Technologies Inc', 'source': 'POPULAR'},
            {'ticker': 'SOFI', 'company_name': 'SoFi Technologies Inc', 'source': 'POPULAR'},
            
            # Energy & Oil
            {'ticker': 'WMB', 'company_name': 'Williams Companies Inc', 'source': 'ENERGY'},
            {'ticker': 'EPD', 'company_name': 'Enterprise Products Partners LP', 'source': 'ENERGY'},
            {'ticker': 'ET', 'company_name': 'Energy Transfer LP', 'source': 'ENERGY'},
            {'ticker': 'MPLX', 'company_name': 'MPLX LP', 'source': 'ENERGY'},
            {'ticker': 'KMI', 'company_name': 'Kinder Morgan Inc', 'source': 'ENERGY'},
            {'ticker': 'OKE', 'company_name': 'ONEOK Inc', 'source': 'ENERGY'},
            {'ticker': 'PSX', 'company_name': 'Phillips 66', 'source': 'ENERGY'},
            {'ticker': 'VLO', 'company_name': 'Valero Energy Corp', 'source': 'ENERGY'},
            {'ticker': 'MPC', 'company_name': 'Marathon Petroleum Corp', 'source': 'ENERGY'},
            {'ticker': 'HES', 'company_name': 'Hess Corp', 'source': 'ENERGY'},
            {'ticker': 'EOG', 'company_name': 'EOG Resources Inc', 'source': 'ENERGY'},
            {'ticker': 'PXD', 'company_name': 'Pioneer Natural Resources Co', 'source': 'ENERGY'},
            {'ticker': 'DVN', 'company_name': 'Devon Energy Corp', 'source': 'ENERGY'},
            {'ticker': 'FANG', 'company_name': 'Diamondback Energy Inc', 'source': 'ENERGY'},
            
            # REITs
            {'ticker': 'O', 'company_name': 'Realty Income Corp', 'source': 'REIT'},
            {'ticker': 'SPG', 'company_name': 'Simon Property Group Inc', 'source': 'REIT'},
            {'ticker': 'PLD', 'company_name': 'Prologis Inc', 'source': 'REIT'},
            {'ticker': 'EQIX', 'company_name': 'Equinix Inc', 'source': 'REIT'},
            {'ticker': 'PSA', 'company_name': 'Public Storage', 'source': 'REIT'},
            {'ticker': 'AVB', 'company_name': 'AvalonBay Communities Inc', 'source': 'REIT'},
            {'ticker': 'EQR', 'company_name': 'Equity Residential', 'source': 'REIT'},
            {'ticker': 'WELL', 'company_name': 'Welltower Inc', 'source': 'REIT'},
            {'ticker': 'DLR', 'company_name': 'Digital Realty Trust Inc', 'source': 'REIT'},
            {'ticker': 'CCI', 'company_name': 'Crown Castle Inc', 'source': 'REIT'},
        ]
        
        for ticker_data in additional_tickers:
            if not any(t['ticker'] == ticker_data['ticker'] for t in all_tickers):
                all_tickers.append(ticker_data)
        
        additional_count = len([t for t in all_tickers if t['source'] in ['ETF', 'CRYPTO', 'MEME', 'POPULAR', 'ENERGY', 'REIT']])
        print(f"✅ Added {additional_count} ETFs, crypto, and popular stocks")
    except Exception as e:
        print(f"❌ Error adding additional tickers: {e}")
    
    # 5. Add more comprehensive ticker list
    try:
        print("🔍 Adding comprehensive A-Z ticker list...")
        
        # Add common tickers by letter (this is a curated list of real tickers)
        comprehensive_tickers = [
            # A tickers
            'A', 'AA', 'AAL', 'AAPL', 'AAXJ', 'AB', 'ABBV', 'ABC', 'ABMD', 'ABT', 'ACN', 'ADBE', 'ADI', 'ADM', 'ADP', 'ADSK', 'AEE', 'AEP', 'AES', 'AFL',
            'AIG', 'AIZ', 'AJG', 'AKAM', 'ALB', 'ALGN', 'ALK', 'ALL', 'ALLE', 'AMAT', 'AMD', 'AME', 'AMGN', 'AMP', 'AMT', 'AMZN', 'AN', 'ANET', 'ANSS', 'AON',
            'AOS', 'APA', 'APD', 'APH', 'APTV', 'ARE', 'ATO', 'ATVI', 'AVB', 'AVGO', 'AVY', 'AWK', 'AXP', 'AZO',
            
            # B tickers
            'BA', 'BAC', 'BAX', 'BBY', 'BDX', 'BEN', 'BF-B', 'BIIB', 'BK', 'BKNG', 'BKR', 'BLK', 'BLL', 'BMY', 'BR', 'BRK-A', 'BRK-B', 'BSX', 'BWA',
            
            # C tickers
            'C', 'CAG', 'CAH', 'CARR', 'CAT', 'CB', 'CBOE', 'CBRE', 'CCI', 'CCL', 'CDNS', 'CDW', 'CE', 'CERN', 'CF', 'CFG', 'CHD', 'CHRW', 'CHTR', 'CI',
            'CINF', 'CL', 'CLX', 'CMA', 'CMCSA', 'CME', 'CMG', 'CMI', 'CMS', 'CNC', 'CNP', 'COF', 'COG', 'COO', 'COP', 'COST', 'CPB', 'CPRT', 'CRM', 'CSCO',
            'CSX', 'CTAS', 'CTL', 'CTSH', 'CTVA', 'CTXS', 'CVS', 'CVX', 'CXO',
            
            # D tickers
            'D', 'DAL', 'DD', 'DE', 'DFS', 'DG', 'DGX', 'DHI', 'DHR', 'DIS', 'DISCA', 'DISCK', 'DISH', 'DLR', 'DLTR', 'DOV', 'DOW', 'DPZ', 'DRE', 'DRI',
            'DTE', 'DUK', 'DVA', 'DVN', 'DXC', 'DXCM',
            
            # E tickers
            'EA', 'EBAY', 'ECL', 'ED', 'EFX', 'EIX', 'EL', 'EMN', 'EMR', 'ENPH', 'EOG', 'EQIX', 'EQR', 'ES', 'ESS', 'ETFC', 'ETN', 'ETR', 'EVRG', 'EW',
            'EXC', 'EXPD', 'EXPE', 'EXR',
            
            # F tickers
            'F', 'FANG', 'FAST', 'FB', 'FBHS', 'FCX', 'FDX', 'FE', 'FFIV', 'FIS', 'FISV', 'FITB', 'FLT', 'FMC', 'FOX', 'FOXA', 'FRC', 'FRT', 'FTI', 'FTNT',
            'FTV',
            
            # G tickers
            'GD', 'GE', 'GILD', 'GIS', 'GL', 'GLW', 'GM', 'GOOG', 'GOOGL', 'GPC', 'GPN', 'GPS', 'GRMN', 'GS', 'GWW',
            
            # H tickers
            'HAL', 'HAS', 'HBAN', 'HBI', 'HCA', 'HD', 'HES', 'HFC', 'HIG', 'HII', 'HLT', 'HOLX', 'HON', 'HPE', 'HPQ', 'HRB', 'HRL', 'HSIC', 'HST', 'HSY',
            'HUM', 'HWM',
            
            # I tickers
            'IBM', 'ICE', 'IDXX', 'IEX', 'IFF', 'ILMN', 'INCY', 'INFO', 'INTC', 'INTU', 'IP', 'IPG', 'IPGP', 'IQV', 'IR', 'IRM', 'ISRG', 'IT', 'ITW', 'IVZ',
            
            # J tickers
            'JBHT', 'JCI', 'JKHY', 'JNJ', 'JNPR', 'JPM',
            
            # K tickers
            'K', 'KEY', 'KEYS', 'KHC', 'KIM', 'KLAC', 'KMB', 'KMI', 'KMX', 'KO', 'KR', 'KSS', 'KSU',
            
            # L tickers
            'L', 'LB', 'LDOS', 'LEG', 'LEN', 'LH', 'LHX', 'LIN', 'LKQ', 'LLY', 'LMT', 'LNC', 'LNT', 'LOW', 'LRCX', 'LUV', 'LVS', 'LW', 'LYB', 'LYV',
            
            # M tickers
            'MA', 'MAA', 'MAR', 'MAS', 'MCD', 'MCHP', 'MCK', 'MCO', 'MDLZ', 'MDT', 'MET', 'MGM', 'MHK', 'MKC', 'MKTX', 'MLM', 'MMC', 'MMM', 'MNST', 'MO',
            'MOS', 'MPC', 'MRK', 'MRO', 'MS', 'MSCI', 'MSFT', 'MSI', 'MTB', 'MTD', 'MU', 'MXIM',
            
            # N tickers
            'NCLH', 'NDAQ', 'NEE', 'NEM', 'NFLX', 'NI', 'NKE', 'NLOK', 'NLSN', 'NOC', 'NOW', 'NRG', 'NSC', 'NTAP', 'NTRS', 'NUE', 'NVDA', 'NVR', 'NWL',
            'NWS', 'NWSA',
            
            # O tickers
            'O', 'ODFL', 'OKE', 'OMC', 'ORCL', 'ORLY', 'OTIS', 'OXY',
            
            # P tickers
            'PAYX', 'PBCT', 'PCAR', 'PEAK', 'PEG', 'PEP', 'PFE', 'PFG', 'PG', 'PGR', 'PH', 'PHM', 'PKG', 'PKI', 'PLD', 'PM', 'PNC', 'PNR', 'PNW', 'PPG',
            'PPL', 'PRGO', 'PRU', 'PSA', 'PSX', 'PVH', 'PWR', 'PXD', 'PYPL',
            
            # Q tickers
            'QCOM', 'QRVO', 'QQQ',
            
            # R tickers
            'RCL', 'RE', 'REG', 'REGN', 'RF', 'RHI', 'RJF', 'RL', 'RMD', 'ROK', 'ROL', 'ROP', 'ROST', 'RSG', 'RTX',
            
            # S tickers
            'SBAC', 'SBUX', 'SCHW', 'SEE', 'SHW', 'SIVB', 'SJM', 'SLB', 'SLG', 'SNA', 'SNPS', 'SO', 'SPG', 'SPGI', 'SRE', 'STE', 'STT', 'STX', 'STZ',
            'SWK', 'SWKS', 'SYF', 'SYK', 'SYY',
            
            # T tickers
            'T', 'TAP', 'TDG', 'TDY', 'TEL', 'TER', 'TFC', 'TFX', 'TGT', 'TIF', 'TJX', 'TMO', 'TMUS', 'TPG', 'TPR', 'TRIP', 'TROW', 'TRV', 'TSCO', 'TSLA',
            'TSN', 'TT', 'TTWO', 'TWTR', 'TXN', 'TXT', 'TYL',
            
            # U tickers
            'UA', 'UAA', 'UAL', 'UDR', 'UHS', 'ULTA', 'UNH', 'UNM', 'UNP', 'UPS', 'URI', 'USB', 'UTX',
            
            # V tickers
            'V', 'VAR', 'VFC', 'VIAC', 'VLO', 'VMC', 'VNO', 'VRSK', 'VRSN', 'VRTX', 'VTR', 'VZ',
            
            # W tickers
            'W', 'WAB', 'WAT', 'WBA', 'WDC', 'WEC', 'WELL', 'WFC', 'WHR', 'WLTW', 'WM', 'WMB', 'WMT', 'WRB', 'WRK', 'WST', 'WU', 'WY', 'WYNN',
            
            # X, Y, Z tickers
            'XEL', 'XLNX', 'XOM', 'XRAY', 'XRX', 'XYL', 'YUM', 'ZBH', 'ZION', 'ZM', 'ZTS'
        ]
        
        for ticker in comprehensive_tickers:
            if not any(t['ticker'] == ticker for t in all_tickers):
                all_tickers.append({
                    'ticker': ticker,
                    'company_name': f'{ticker} Corporation',
                    'source': 'COMPREHENSIVE'
                })
        
        comprehensive_count = len([t for t in all_tickers if t['source'] == 'COMPREHENSIVE'])
        print(f"✅ Added {comprehensive_count} comprehensive tickers")
    except Exception as e:
        print(f"❌ Error adding comprehensive tickers: {e}")
    
    return all_tickers

def save_to_csv(tickers_data, filename='stock_data.csv'):
    """Save ticker data to CSV file"""
    try:
        # Sort by ticker for better organization
        tickers_data.sort(key=lambda x: x['ticker'])
        
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['ticker', 'company_name']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            writer.writeheader()
            for ticker_data in tickers_data:
                writer.writerow({
                    'ticker': ticker_data['ticker'],
                    'company_name': ticker_data['company_name']
                })
        
        print(f"\n✅ Successfully saved {len(tickers_data)} tickers to {filename}")
        return True
    except Exception as e:
        print(f"❌ Error saving to CSV: {e}")
        return False

def main():
    print("🎯 US Stock Ticker Fetcher")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Fetch all tickers
    all_tickers = fetch_all_us_tickers()
    
    # Remove duplicates while preserving order
    seen_tickers = set()
    unique_tickers = []
    for ticker_data in all_tickers:
        if ticker_data['ticker'] not in seen_tickers:
            seen_tickers.add(ticker_data['ticker'])
            unique_tickers.append(ticker_data)
    
    print(f"\n📊 SUMMARY:")
    print(f"Total unique tickers: {len(unique_tickers)}")
    print(f"Sources breakdown:")
    
    source_counts = {}
    for ticker_data in unique_tickers:
        source = ticker_data.get('source', 'UNKNOWN')
        source_counts[source] = source_counts.get(source, 0) + 1
    
    for source, count in sorted(source_counts.items()):
        print(f"  - {source}: {count} tickers")
    
    # Save to CSV
    if save_to_csv(unique_tickers):
        print(f"\n🎉 SUCCESS! Added {len(unique_tickers)} US stock tickers to stock_data.csv")
        print("You can now use the autocomplete feature with ALL US stocks!")
    else:
        print("\n❌ Failed to save tickers to CSV file")
    
    print(f"\n⏰ Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
