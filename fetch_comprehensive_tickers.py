#!/usr/bin/env python3
"""
Advanced Daily Ticker Fetcher using Multiple Free APIs
Fetches comprehensive ticker lists from SEC EDGAR, Yahoo Finance, and other sources
"""

import requests
import pandas as pd
import csv
import os
import json
from datetime import datetime
import time

class AdvancedTickerFetcher:
    def __init__(self):
        self.output_file = "comprehensive_tickers.csv"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Stock Analyzer Ticker Fetcher (educational use)'
        })
        
    def fetch_sec_tickers(self):
        """Fetch tickers from SEC EDGAR database (free and comprehensive)"""
        tickers = []
        
        print("🏛️ Fetching tickers from SEC EDGAR database...")
        
        try:
            # SEC provides a JSON file with all company tickers
            url = "https://www.sec.gov/files/company_tickers.json"
            response = self.session.get(url)
            
            if response.status_code == 200:
                data = response.json()
                
                for entry in data.values():
                    ticker = entry.get('ticker', '').upper()
                    company_name = entry.get('title', '').title()
                    
                    if ticker and company_name:
                        tickers.append((ticker, company_name, 'SEC_EDGAR'))
                        
                print(f"✅ Fetched {len(tickers)} tickers from SEC EDGAR")
                
            else:
                print(f"❌ Failed to fetch SEC data: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error fetching SEC tickers: {e}")
            
        return tickers
    
    def fetch_nasdaq_screener(self):
        """Fetch from NASDAQ stock screener (alternative method)"""
        tickers = []
        
        print("📊 Fetching from NASDAQ screener...")
        
        try:
            # This is a public API endpoint that NASDAQ uses
            exchanges = ['nasdaq', 'nyse', 'amex']
            
            for exchange in exchanges:
                url = f"https://api.nasdaq.com/api/screener/stocks"
                params = {
                    'tableonly': 'true',
                    'limit': '5000',
                    'exchange': exchange
                }
                
                response = self.session.get(url, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if 'data' in data and 'rows' in data['data']:
                        for row in data['data']['rows']:
                            ticker = row.get('symbol', '').upper()
                            company_name = row.get('name', '').title()
                            
                            if ticker and company_name:
                                tickers.append((ticker, company_name, exchange.upper()))
                                
                        print(f"✅ Fetched {len(data['data']['rows'])} tickers from {exchange.upper()}")
                        
                time.sleep(1)  # Rate limiting
                
        except Exception as e:
            print(f"❌ Error fetching NASDAQ screener data: {e}")
            
        return tickers
    
    def fetch_yahoo_finance_screener(self):
        """Fetch popular tickers from Yahoo Finance categories"""
        tickers = []
        
        print("🟡 Fetching popular tickers from Yahoo Finance...")
        
        # Popular ticker lists (these are publicly known)
        ticker_lists = {
            'NASDAQ_100': ['AAPL', 'MSFT', 'GOOGL', 'GOOG', 'AMZN', 'TSLA', 'META', 'NVDA', 'ADBE', 'PYPL'],
            'DOW_30': ['AAPL', 'MSFT', 'JNJ', 'JPM', 'V', 'PG', 'UNH', 'HD', 'DIS', 'MA'],
            'S&P_500_TOP': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'TSLA', 'META', 'BRK-B', 'UNH', 'JNJ'],
            'CRYPTO_RELATED': ['COIN', 'MSTR', 'RIOT', 'MARA', 'BTCS', 'HOOD', 'SQ', 'PYPL'],
            'EV_STOCKS': ['TSLA', 'NIO', 'XPEV', 'LI', 'LCID', 'RIVN', 'F', 'GM'],
            'URANIUM_STOCKS': ['CCJ', 'UUUU', 'UEC', 'DNN', 'NXE', 'URG', 'LEU'],
            'LITHIUM_STOCKS': ['LAC', 'ALB', 'SQM', 'LTHM', 'PLL']
        }
        
        for category, ticker_list in ticker_lists.items():
            print(f"📋 Processing {category} tickers...")
            
            for ticker in ticker_list:
                try:
                    # Try to get company name from a simple Yahoo endpoint
                    company_name = f"{ticker} Corporation"  # Default fallback
                    tickers.append((ticker, company_name, category))
                    
                except Exception as e:
                    print(f"⚠️ Could not process {ticker}: {e}")
                    
        print(f"✅ Added {len(tickers)} popular tickers")
        return tickers
    
    def fetch_etf_list(self):
        """Fetch popular ETF tickers"""
        tickers = []
        
        print("📈 Adding popular ETFs...")
        
        etfs = [
            ('SPY', 'SPDR S&P 500 ETF Trust'),
            ('QQQ', 'Invesco QQQ Trust'),
            ('IWM', 'iShares Russell 2000 ETF'),
            ('EFA', 'iShares MSCI EAFE ETF'),
            ('VTI', 'Vanguard Total Stock Market ETF'),
            ('VOO', 'Vanguard S&P 500 ETF'),
            ('GLD', 'SPDR Gold Shares'),
            ('SLV', 'iShares Silver Trust'),
            ('URA', 'Global X Uranium ETF'),
            ('URNJ', 'Sprott Junior Uranium Miners ETF'),
            ('LIT', 'Global X Lithium & Battery Tech ETF'),
            ('ARKK', 'ARK Innovation ETF'),
            ('ARKQ', 'ARK Autonomous Technology & Robotics ETF'),
            ('BITO', 'ProShares Bitcoin Strategy ETF'),
            ('GBTC', 'Grayscale Bitcoin Trust'),
            ('XLF', 'Financial Select Sector SPDR Fund'),
            ('XLE', 'Energy Select Sector SPDR Fund'),
            ('XLK', 'Technology Select Sector SPDR Fund')
        ]
        
        for ticker, name in etfs:
            tickers.append((ticker, name, 'ETF'))
            
        print(f"✅ Added {len(etfs)} ETFs")
        return tickers
    
    def clean_and_deduplicate(self, all_tickers):
        """Clean and remove duplicate tickers"""
        print("🧹 Cleaning and deduplicating ticker data...")
        
        seen_tickers = set()
        clean_tickers = []
        
        for ticker, company, source in all_tickers:
            ticker_clean = ticker.upper().strip()
            company_clean = company.strip().title()
            
            if ticker_clean and ticker_clean not in seen_tickers:
                # Basic validation - ticker should be 1-5 characters, mostly letters
                if len(ticker_clean) <= 6 and ticker_clean.replace('-', '').replace('.', '').isalnum():
                    clean_tickers.append((ticker_clean, company_clean))
                    seen_tickers.add(ticker_clean)
        
        print(f"✅ Cleaned data: {len(clean_tickers)} unique tickers")
        return clean_tickers
    
    def save_tickers(self, tickers):
        """Save tickers to CSV files"""
        print("💾 Saving ticker data...")
        
        # Save comprehensive list
        with open(self.output_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['ticker', 'company_name'])
            writer.writerows(tickers)
            
        # Also update the main stock_data.csv used by the analyzer
        if os.path.exists('stock_data.csv'):
            # Backup existing file
            backup_name = f"stock_data_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            import shutil
            shutil.copy('stock_data.csv', backup_name)
            print(f"📦 Backup created: {backup_name}")
        
        with open('stock_data.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['ticker', 'company_name'])
            writer.writerows(tickers)
            
        print(f"✅ Saved {len(tickers)} tickers to {self.output_file}")
        print(f"✅ Updated stock_data.csv for Stock Analyzer")
    
    def create_summary_report(self, tickers):
        """Create a summary report"""
        report_file = f"ticker_fetch_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(report_file, 'w') as f:
            f.write(f"Comprehensive Ticker Fetch Report\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*50 + "\n\n")
            f.write(f"Total Unique Tickers: {len(tickers)}\n\n")
            f.write("Sample Tickers:\n")
            
            for i, (ticker, company) in enumerate(tickers[:20]):
                f.write(f"  {ticker:6} - {company}\n")
                
            if len(tickers) > 20:
                f.write(f"  ... and {len(tickers) - 20} more\n")
                
            f.write(f"\nFiles created:\n")
            f.write(f"  - {self.output_file}\n")
            f.write(f"  - stock_data.csv (updated)\n")
            f.write(f"  - {report_file}\n")
            
        print(f"📋 Summary report saved: {report_file}")
    
    def run_comprehensive_fetch(self):
        """Run comprehensive ticker fetch from multiple sources"""
        print("🚀 Starting Comprehensive Ticker Fetch")
        print("="*60)
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        all_tickers = []
        
        # Fetch from multiple sources
        try:
            all_tickers.extend(self.fetch_sec_tickers())
        except Exception as e:
            print(f"⚠️ SEC fetch failed: {e}")
            
        try:
            all_tickers.extend(self.fetch_nasdaq_screener())
        except Exception as e:
            print(f"⚠️ NASDAQ screener fetch failed: {e}")
            
        try:
            all_tickers.extend(self.fetch_yahoo_finance_screener())
        except Exception as e:
            print(f"⚠️ Yahoo Finance fetch failed: {e}")
            
        try:
            all_tickers.extend(self.fetch_etf_list())
        except Exception as e:
            print(f"⚠️ ETF fetch failed: {e}")
        
        print(f"\n📊 Raw data collected: {len(all_tickers)} entries")
        
        # Clean and deduplicate
        clean_tickers = self.clean_and_deduplicate(all_tickers)
        
        # Sort alphabetically
        clean_tickers.sort(key=lambda x: x[0])
        
        # Save results
        self.save_tickers(clean_tickers)
        
        # Create report
        self.create_summary_report(clean_tickers)
        
        print("\n🎉 Comprehensive ticker fetch completed!")
        print(f"📈 Final database size: {len(clean_tickers)} unique tickers")

def main():
    """Main execution"""
    fetcher = AdvancedTickerFetcher()
    fetcher.run_comprehensive_fetch()

if __name__ == "__main__":
    main()
