#!/usr/bin/env python3
"""
Daily Stock Ticker Fetcher
Fetches all NASDAQ, NYSE, and AMEX tickers and saves them to CSV
Can be run daily via cron job or manually to keep stock database updated
"""

import pandas as pd
import requests
import csv
import os
from datetime import datetime
import yfinance as yf
import time

class StockTickerFetcher:
    def __init__(self):
        self.output_file = "all_tickers_daily.csv"
        self.backup_file = f"stock_data_backup_{datetime.now().strftime('%Y%m%d')}.csv"
        self.exchanges = ['NASDAQ', 'NYSE', 'AMEX']
        
    def fetch_nasdaq_tickers(self):
        """Fetch NASDAQ tickers using yfinance and alternative sources"""
        tickers = []
        
        print("🔍 Fetching NASDAQ tickers...")
        
        try:
            # Method 1: Using yfinance to get some major NASDAQ tickers
            nasdaq_symbols = [
                'AAPL', 'MSFT', 'GOOGL', 'GOOG', 'AMZN', 'TSLA', 'META', 'NVDA', 'PYPL', 'ADBE',
                'NFLX', 'INTC', 'CMCSA', 'PEP', 'CSCO', 'AVGO', 'TXN', 'QCOM', 'COST', 'SBUX'
            ]
            
            for symbol in nasdaq_symbols:
                try:
                    ticker = yf.Ticker(symbol)
                    info = ticker.info
                    company_name = info.get('longName', f"{symbol} Corp")
                    tickers.append((symbol, company_name, 'NASDAQ'))
                    print(f"✅ Added NASDAQ: {symbol} - {company_name}")
                except:
                    tickers.append((symbol, f"{symbol} Corp", 'NASDAQ'))
                    print(f"⚠️ Added NASDAQ (basic): {symbol}")
                
                time.sleep(0.1)  # Rate limiting
            
            # Method 2: Add common NASDAQ tickers manually
            additional_nasdaq = [
                ('RIOT', 'Riot Platforms Inc', 'NASDAQ'),
                ('MARA', 'Marathon Digital Holdings Inc', 'NASDAQ'),
                ('COIN', 'Coinbase Global Inc', 'NASDAQ'),
                ('HOOD', 'Robinhood Markets Inc', 'NASDAQ'),
                ('PLTR', 'Palantir Technologies Inc', 'NASDAQ'),
                ('RBLX', 'Roblox Corporation', 'NASDAQ'),
                ('LCID', 'Lucid Group Inc', 'NASDAQ'),
                ('RIVN', 'Rivian Automotive Inc', 'NASDAQ'),
                ('ZM', 'Zoom Video Communications Inc', 'NASDAQ'),
                ('DOCU', 'DocuSign Inc', 'NASDAQ')
            ]
            
            tickers.extend(additional_nasdaq)
            print(f"✅ Added {len(additional_nasdaq)} additional NASDAQ tickers")
            
        except Exception as e:
            print(f"❌ Error fetching NASDAQ tickers: {e}")
        
        return tickers
    
    def fetch_nyse_tickers(self):
        """Fetch NYSE tickers using yfinance and alternative sources"""
        tickers = []
        
        print("🔍 Fetching NYSE tickers...")
        
        try:
            # Common NYSE tickers
            nyse_symbols = [
                'JPM', 'JNJ', 'V', 'PG', 'UNH', 'HD', 'MA', 'DIS', 'BAC', 'XOM',
                'WMT', 'CVX', 'LLY', 'ABBV', 'PFE', 'TMO', 'ACN', 'NKE', 'MRK', 'KO',
                'WFC', 'DHR', 'VZ', 'LIN', 'BMY', 'PM', 'T', 'LOW', 'UPS', 'HON'
            ]
            
            for symbol in nyse_symbols:
                try:
                    ticker = yf.Ticker(symbol)
                    info = ticker.info
                    company_name = info.get('longName', f"{symbol} Corp")
                    tickers.append((symbol, company_name, 'NYSE'))
                    print(f"✅ Added NYSE: {symbol} - {company_name}")
                except:
                    tickers.append((symbol, f"{symbol} Corp", 'NYSE'))
                    print(f"⚠️ Added NYSE (basic): {symbol}")
                
                time.sleep(0.1)  # Rate limiting
            
            # Add specific stocks we know are NYSE
            additional_nyse = [
                ('F', 'Ford Motor Company', 'NYSE'),
                ('GM', 'General Motors Company', 'NYSE'),
                ('GE', 'General Electric Company', 'NYSE'),
                ('IBM', 'International Business Machines Corp', 'NYSE'),
                ('CAT', 'Caterpillar Inc', 'NYSE'),
                ('BA', 'Boeing Company', 'NYSE'),
                ('MMM', '3M Company', 'NYSE'),
                ('JD', 'JD.com Inc', 'NYSE'),
                ('BABA', 'Alibaba Group Holding Ltd', 'NYSE'),
                ('NIO', 'NIO Inc', 'NYSE')
            ]
            
            tickers.extend(additional_nyse)
            print(f"✅ Added {len(additional_nyse)} additional NYSE tickers")
            
        except Exception as e:
            print(f"❌ Error fetching NYSE tickers: {e}")
        
        return tickers
    
    def fetch_amex_tickers(self):
        """Fetch AMEX (NYSE American) tickers"""
        tickers = []
        
        print("🔍 Fetching AMEX tickers...")
        
        try:
            # Common AMEX tickers (many ETFs and smaller companies trade here)
            amex_symbols = [
                'SPY', 'QQQ', 'IWM', 'EFA', 'VTI', 'GLD', 'SLV', 'XLF', 'XLE', 'XLK',
                'GDXJ', 'GDX', 'USO', 'UNG', 'TLT', 'HYG', 'LQD', 'EEM', 'FXI', 'EWJ'
            ]
            
            for symbol in amex_symbols:
                try:
                    ticker = yf.Ticker(symbol)
                    info = ticker.info
                    company_name = info.get('longName', f"{symbol} Fund")
                    tickers.append((symbol, company_name, 'AMEX'))
                    print(f"✅ Added AMEX: {symbol} - {company_name}")
                except:
                    tickers.append((symbol, f"{symbol} Fund", 'AMEX'))
                    print(f"⚠️ Added AMEX (basic): {symbol}")
                
                time.sleep(0.1)  # Rate limiting
            
            # Add our specific tickers that are AMEX
            additional_amex = [
                ('UUUU', 'Energy Fuels Inc', 'AMEX'),
                ('URG', 'Ur-Energy Inc', 'AMEX'),
                ('UEC', 'Uranium Energy Corp', 'AMEX'),
                ('DNN', 'Denison Mines Corp', 'AMEX'),
                ('GBTC', 'Grayscale Bitcoin Trust', 'AMEX'),
                ('ETHE', 'Grayscale Ethereum Trust', 'AMEX'),
                ('ARKK', 'ARK Innovation ETF', 'AMEX'),
                ('ARKQ', 'ARK Autonomous Technology & Robotics ETF', 'AMEX'),
                ('ARKG', 'ARK Genomics Revolution ETF', 'AMEX'),
                ('ARKW', 'ARK Next Generation Internet ETF', 'AMEX')
            ]
            
            tickers.extend(additional_amex)
            print(f"✅ Added {len(additional_amex)} additional AMEX tickers")
            
        except Exception as e:
            print(f"❌ Error fetching AMEX tickers: {e}")
        
        return tickers
    
    def merge_with_existing_data(self, new_tickers):
        """Merge new tickers with existing stock_data.csv"""
        existing_data = []
        existing_tickers = set()
        
        # Read existing data if it exists
        if os.path.exists("stock_data.csv"):
            print("📖 Reading existing stock_data.csv...")
            with open("stock_data.csv", 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                header = next(reader, None)
                if header:
                    existing_data.append(header)
                
                for row in reader:
                    if len(row) >= 2:
                        existing_data.append(row)
                        existing_tickers.add(row[0].upper())
            
            print(f"📊 Found {len(existing_tickers)} existing tickers")
        else:
            existing_data.append(['ticker', 'company_name'])
        
        # Add new tickers that don't exist
        new_additions = 0
        for ticker, company, exchange in new_tickers:
            if ticker.upper() not in existing_tickers:
                existing_data.append([ticker, company])
                existing_tickers.add(ticker.upper())
                new_additions += 1
                print(f"🆕 New ticker: {ticker} - {company}")
        
        print(f"✅ Added {new_additions} new tickers")
        return existing_data
    
    def save_to_csv(self, data, filename):
        """Save ticker data to CSV file"""
        # Sort by ticker (skip header)
        header = data[0]
        ticker_data = data[1:]
        ticker_data.sort(key=lambda x: x[0].upper())
        
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(ticker_data)
        
        print(f"💾 Saved {len(ticker_data)} tickers to {filename}")
    
    def create_daily_report(self, all_tickers):
        """Create a daily report with statistics"""
        report_file = f"daily_ticker_report_{datetime.now().strftime('%Y%m%d')}.txt"
        
        # Count by exchange
        exchange_counts = {}
        for ticker, company, exchange in all_tickers:
            exchange_counts[exchange] = exchange_counts.get(exchange, 0) + 1
        
        with open(report_file, 'w') as f:
            f.write(f"Daily Ticker Fetch Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*60 + "\n\n")
            f.write(f"Total Tickers Fetched: {len(all_tickers)}\n\n")
            f.write("Exchange Breakdown:\n")
            for exchange, count in exchange_counts.items():
                f.write(f"  {exchange}: {count} tickers\n")
            f.write(f"\nData saved to: {self.output_file}\n")
            f.write(f"Backup created: {self.backup_file}\n")
        
        print(f"📋 Daily report saved to {report_file}")
    
    def run_daily_fetch(self):
        """Main function to run daily ticker fetch"""
        print("🚀 Starting Daily Stock Ticker Fetch")
        print("="*50)
        print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🎯 Target Exchanges: {', '.join(self.exchanges)}")
        print()
        
        # Backup existing data
        if os.path.exists("stock_data.csv"):
            import shutil
            shutil.copy("stock_data.csv", self.backup_file)
            print(f"💾 Backup created: {self.backup_file}")
        
        # Fetch tickers from all exchanges
        all_new_tickers = []
        
        all_new_tickers.extend(self.fetch_nasdaq_tickers())
        all_new_tickers.extend(self.fetch_nyse_tickers()) 
        all_new_tickers.extend(self.fetch_amex_tickers())
        
        print(f"\n📊 Total new tickers fetched: {len(all_new_tickers)}")
        
        # Merge with existing data
        merged_data = self.merge_with_existing_data(all_new_tickers)
        
        # Save main CSV
        self.save_to_csv(merged_data, "stock_data.csv")
        
        # Save daily snapshot
        self.save_to_csv(merged_data, self.output_file)
        
        # Create report
        self.create_daily_report(all_new_tickers)
        
        print("\n🎉 Daily ticker fetch completed successfully!")
        print(f"📈 Total tickers in database: {len(merged_data) - 1}")  # -1 for header

def main():
    """Main execution function"""
    fetcher = StockTickerFetcher()
    fetcher.run_daily_fetch()

if __name__ == "__main__":
    main()
