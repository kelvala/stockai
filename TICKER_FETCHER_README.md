# Daily Stock Ticker Fetcher

A comprehensive Python system to automatically fetch and update stock tickers from NASDAQ, NYSE, and AMEX exchanges daily.

## 📁 Files

### Core Scripts
- **`fetch_daily_tickers.py`** - Main daily fetcher using yfinance and manual ticker lists
- **`fetch_comprehensive_tickers.py`** - Advanced fetcher using SEC EDGAR and multiple APIs
- **`setup_daily_fetch.sh`** - Automation script to set up daily cron jobs

### Output Files
- **`stock_data.csv`** - Main ticker database used by Stock Analyzer
- **`all_tickers_daily.csv`** - Daily snapshot of fetched tickers
- **`comprehensive_tickers.csv`** - Output from comprehensive fetcher
- **`daily_ticker_report_YYYYMMDD.txt`** - Daily fetch reports
- **`stock_data_backup_YYYYMMDD.csv`** - Automatic backups

## 🚀 Quick Start

### Option 1: Manual Daily Fetch
```bash
# Run the daily fetcher manually
python3 fetch_daily_tickers.py
```

### Option 2: Comprehensive Fetch (More Tickers)
```bash
# Fetch from multiple sources including SEC EDGAR
python3 fetch_comprehensive_tickers.py
```

### Option 3: Set Up Automated Daily Fetch
```bash
# Interactive setup for daily automation
./setup_daily_fetch.sh
```

## 📊 Features

### Daily Fetcher (`fetch_daily_tickers.py`)
- ✅ Fetches major NASDAQ tickers (AAPL, MSFT, GOOGL, etc.)
- ✅ Fetches major NYSE tickers (JPM, JNJ, V, etc.)
- ✅ Fetches popular AMEX tickers and ETFs (SPY, QQQ, GLD, etc.)
- ✅ Uses yfinance for real company names
- ✅ Merges with existing data without duplicates
- ✅ Creates automatic backups
- ✅ Generates daily reports
- ✅ Rate limiting to avoid API issues

### Comprehensive Fetcher (`fetch_comprehensive_tickers.py`)
- 🏛️ Uses SEC EDGAR database (official government source)
- 📊 NASDAQ stock screener API
- 🟡 Yahoo Finance popular ticker lists
- 📈 Comprehensive ETF coverage
- 🧹 Advanced data cleaning and deduplication
- 📋 Detailed reporting

### Automation System (`setup_daily_fetch.sh`)
- 🕐 Sets up daily cron job (6:00 AM)
- 📝 Configures logging
- 🔧 Easy management (add/remove/view cron jobs)
- 🚀 Manual execution option

## 📈 Data Sources

### Free APIs Used
1. **SEC EDGAR Database** - Official US government company filings
2. **NASDAQ Screener API** - Real-time ticker data
3. **Yahoo Finance** - Company information and validation
4. **Manual Curated Lists** - Popular stocks by category

### Ticker Categories
- **NASDAQ**: Tech stocks, biotech, growth companies
- **NYSE**: Blue chips, established companies, international stocks
- **AMEX**: ETFs, smaller companies, specialty funds
- **ETFs**: Sector funds, commodity funds, international funds
- **Crypto-Related**: COIN, MSTR, RIOT, MARA, BTCS, etc.
- **EV Stocks**: TSLA, NIO, LCID, RIVN, etc.
- **Uranium**: CCJ, UUUU, UEC, URNJ, URA, etc.
- **Lithium**: LAC, ALB, SQM, LIT, etc.

## 🔧 Setup Instructions

### Prerequisites
```bash
pip install yfinance pandas requests
```

### Basic Setup
1. Download the scripts to your Stock Analyzer directory
2. Make the setup script executable: `chmod +x setup_daily_fetch.sh`
3. Run: `./setup_daily_fetch.sh`
4. Choose option 1 to set up daily automation

### Manual Configuration
To set up the cron job manually:
```bash
# Edit crontab
crontab -e

# Add this line (runs daily at 6 AM):
0 6 * * * cd /path/to/GPT-Stock-Analyzer && python3 fetch_daily_tickers.py >> daily_ticker_fetch.log 2>&1
```

## 📊 Output Format

The CSV files use this format:
```csv
ticker,company_name
AAPL,Apple Inc.
MSFT,Microsoft Corporation
GOOGL,Alphabet Inc.
```

## 📋 Daily Reports

Each run generates a report with:
- Total tickers fetched
- Exchange breakdown
- New additions
- File locations
- Timestamps

## 🛡️ Rate Limiting & Ethics

- ✅ Respects API rate limits
- ✅ Uses appropriate User-Agent headers
- ✅ Implements delays between requests
- ✅ Uses only public, free data sources
- ✅ Educational/personal use only

## 🔄 Integration with Stock Analyzer

The fetched tickers automatically update `stock_data.csv`, which is used by:
- Stock Analyzer GUI autocomplete
- Ticker resolution (company name → ticker)
- Industry categorization
- Analysis features

## 📅 Scheduling Options

### Daily (Recommended)
```bash
0 6 * * * /path/to/script  # 6:00 AM daily
```

### Weekly
```bash
0 6 * * 1 /path/to/script  # 6:00 AM every Monday
```

### Monthly
```bash
0 6 1 * * /path/to/script  # 6:00 AM first day of month
```

## 🧹 Maintenance

### View Logs
```bash
tail -f daily_ticker_fetch.log
```

### Manual Cleanup
```bash
# Remove old backup files (older than 30 days)
find . -name "stock_data_backup_*.csv" -mtime +30 -delete

# Remove old reports (older than 30 days)
find . -name "daily_ticker_report_*.txt" -mtime +30 -delete
```

### Check Cron Job Status
```bash
crontab -l  # List current cron jobs
```

## 📈 Performance

- **Daily Fetcher**: ~100-200 tickers, runs in 2-3 minutes
- **Comprehensive Fetcher**: 1000+ tickers, runs in 5-10 minutes
- **Database Size**: Typically 700-1500 unique tickers
- **Update Frequency**: Daily recommended, weekly acceptable

## 🚨 Troubleshooting

### Common Issues

**Script fails with network error:**
```bash
# Check internet connection
ping google.com

# Run with verbose output
python3 -v fetch_daily_tickers.py
```

**Cron job not running:**
```bash
# Check cron service
sudo systemctl status cron  # Linux
sudo launchctl list | grep cron  # macOS

# Check cron logs
tail -f /var/log/cron  # Linux
tail -f /var/log/system.log | grep cron  # macOS
```

**Permission errors:**
```bash
# Make scripts executable
chmod +x *.sh
chmod +x *.py

# Check file permissions
ls -la *.csv
```

## 📞 Support

For issues with the ticker fetcher:
1. Check the daily report files for error details
2. Verify internet connection and API access
3. Check log files for specific error messages
4. Ensure sufficient disk space for CSV files

---

**Last Updated**: July 18, 2025  
**Compatible with**: Stock Analyzer v0.12+
