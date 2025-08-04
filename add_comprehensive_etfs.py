#!/usr/bin/env python3
"""
Add comprehensive ETF and commodity fund coverage to stock_data.csv
Includes all major commodity ETFs, sector ETFs, international ETFs, and specialized funds
"""

import csv
import os
from datetime import datetime
import shutil

def add_comprehensive_etfs():
    """Add comprehensive ETF coverage including commodity funds like CPER"""
    
    print("📈 Adding comprehensive ETF and commodity fund coverage...")
    
    # Comprehensive ETF list organized by category
    comprehensive_etfs = [
        # COMMODITY ETFs (Missing from current database)
        ("CPER", "United States Copper Index Fund"),
        ("JJC", "iPath Series B Bloomberg Copper Subindex Total Return ETN"),
        ("COPX", "Global X Copper Miners ETF"),
        ("JJN", "iPath Series B Bloomberg Nickel Subindex Total Return ETN"),
        ("JJT", "iPath Series B Bloomberg Tin Subindex Total Return ETN"),
        ("JJU", "iPath Series B Bloomberg Aluminum Subindex Total Return ETN"),
        ("PALL", "ETFS Physical Palladium Shares"),
        ("PPLT", "ETFS Physical Platinum Shares"),
        ("GLD", "SPDR Gold Shares"),
        ("IAU", "iShares Gold Trust"),
        ("SLV", "iShares Silver Trust"),
        ("SIVR", "ETFS Physical Silver Shares"),
        ("DBA", "Invesco DB Agriculture Fund"),
        ("CORN", "Teucrium Corn Fund"),
        ("WEAT", "Teucrium Wheat Fund"),
        ("SOYB", "Teucrium Soybean Fund"),
        ("CANE", "Teucrium Sugar Fund"),
        ("COW", "iPath Series B Bloomberg Livestock Subindex Total Return ETN"),
        ("USO", "United States Oil Fund"),
        ("UCO", "ProShares Ultra Bloomberg Crude Oil"),
        ("SCO", "ProShares UltraShort Bloomberg Crude Oil"),
        ("UNG", "United States Natural Gas Fund"),
        ("KOLD", "ProShares UltraShort Bloomberg Natural Gas"),
        ("BOIL", "ProShares Ultra Bloomberg Natural Gas"),
        ("DJP", "iPath Series B Bloomberg Commodity Index Total Return ETN"),
        ("GSG", "iShares S&P GSCI Commodity-Indexed Trust"),
        ("PDBC", "Invesco Optimum Yield Diversified Commodity Strategy No K-1 ETF"),
        ("BCI", "abrdn Bloomberg All Commodity Strategy K-1 Free ETF"),
        
        # URANIUM & NUCLEAR ETFs
        ("URA", "Global X Uranium ETF"),
        ("URNJ", "Sprott Junior Uranium Miners ETF"),
        ("URNM", "Sprott Uranium Miners ETF"),
        ("NLR", "VanEck Nuclear Energy ETF"),
        ("PKN", "Invesco Nuclear Energy ETF"),
        
        # LITHIUM & BATTERY ETFs
        ("LIT", "Global X Lithium & Battery Tech ETF"),
        ("BATT", "Amplify Lithium & Battery Technology ETF"),
        ("KBAT", "KraneShares Battery Metals & Technology ETF"),
        ("LTHM", "Livent Corporation"),  # Pure-play lithium
        ("ALB", "Albemarle Corporation"),  # Lithium producer
        ("SQM", "Sociedad Quimica y Minera de Chile S.A."),  # Lithium
        
        # RENEWABLE ENERGY ETFs
        ("ICLN", "iShares Global Clean Energy ETF"),
        ("QCLN", "First Trust NASDAQ Clean Edge Green Energy Index Fund"),
        ("PBW", "Invesco WilderHill Clean Energy ETF"),
        ("ERTH", "Invesco MSCI Sustainable Future ETF"),
        ("GRID", "First Trust NASDAQ Clean Edge Smart Grid Infrastructure Index Fund"),
        ("FAN", "First Trust Global Wind Energy ETF"),
        ("TAN", "Invesco Solar ETF"),
        ("SUNW", "Sunworks Inc"),
        
        # SEMICONDUCTOR ETFs
        ("SMH", "VanEck Semiconductor ETF"),
        ("SOXX", "iShares Semiconductor ETF"),
        ("PSI", "Invesco Dynamic Semiconductors ETF"),
        ("SOXL", "Direxion Daily Semiconductor Bull 3X Shares"),
        ("SOXS", "Direxion Daily Semiconductor Bear 3X Shares"),
        
        # TECHNOLOGY SECTOR ETFs
        ("XLK", "Technology Select Sector SPDR Fund"),
        ("VGT", "Vanguard Information Technology ETF"),
        ("FTEC", "Fidelity MSCI Information Technology Index ETF"),
        ("IYW", "iShares U.S. Technology ETF"),
        ("IGV", "iShares Expanded Tech-Software Sector ETF"),
        ("KWEB", "KraneShares CSI China Internet ETF"),
        ("CIBR", "First Trust NASDAQ Cybersecurity ETF"),
        ("HACK", "ETFMG Prime Cyber Security ETF"),
        ("ROBO", "ROBO Global Robotics and Automation Index ETF"),
        ("BOTZ", "Global X Robotics & Artificial Intelligence ETF"),
        ("ARKK", "ARK Innovation ETF"),
        ("ARKQ", "ARK Autonomous Technology & Robotics ETF"),
        ("ARKW", "ARK Next Generation Internet ETF"),
        ("ARKG", "ARK Genomic Revolution ETF"),
        ("ARKF", "ARK Fintech Innovation ETF"),
        
        # FINANCIAL SECTOR ETFs
        ("XLF", "Financial Select Sector SPDR Fund"),
        ("VFH", "Vanguard Financials ETF"),
        ("FNCL", "Fidelity MSCI Financials Index ETF"),
        ("IYF", "iShares U.S. Financials ETF"),
        ("KRE", "SPDR S&P Regional Banking ETF"),
        ("KBE", "SPDR S&P Bank ETF"),
        ("IAI", "iShares U.S. Broker-Dealers & Securities Exchanges ETF"),
        ("IEZ", "iShares U.S. Oil Equipment & Services ETF"),
        
        # ENERGY SECTOR ETFs
        ("XLE", "Energy Select Sector SPDR Fund"),
        ("VDE", "Vanguard Energy ETF"),
        ("FENY", "Fidelity MSCI Energy Index ETF"),
        ("IYE", "iShares U.S. Energy ETF"),
        ("XOP", "SPDR S&P Oil & Gas Exploration & Production ETF"),
        ("OIH", "VanEck Oil Services ETF"),
        ("PXJ", "Invesco Dynamic Energy Exploration & Production ETF"),
        ("GUSH", "Direxion Daily S&P Oil & Gas Exp. & Prod. Bull 2X Shares"),
        ("DRIP", "Direxion Daily S&P Oil & Gas Exp. & Prod. Bear 2X Shares"),
        
        # HEALTHCARE ETFs
        ("XLV", "Health Care Select Sector SPDR Fund"),
        ("VHT", "Vanguard Health Care ETF"),
        ("FHLC", "Fidelity MSCI Health Care Index ETF"),
        ("IYH", "iShares U.S. Healthcare ETF"),
        ("XBI", "SPDR S&P Biotech ETF"),
        ("IBB", "iShares Biotechnology ETF"),
        ("ARKG", "ARK Genomic Revolution ETF"),
        ("GNOM", "Global X Genomics & Biotechnology ETF"),
        
        # REAL ESTATE ETFs
        ("XLRE", "Real Estate Select Sector SPDR Fund"),
        ("VNQ", "Vanguard Real Estate ETF"),
        ("FREL", "Fidelity MSCI Real Estate Index ETF"),
        ("IYR", "iShares U.S. Real Estate ETF"),
        ("REM", "iShares Mortgage Real Estate ETF"),
        ("MORT", "VanEck Mortgage REIT Income ETF"),
        
        # UTILITIES ETFs
        ("XLU", "Utilities Select Sector SPDR Fund"),
        ("VPU", "Vanguard Utilities ETF"),
        ("FUTY", "Fidelity MSCI Utilities Index ETF"),
        ("IDU", "iShares U.S. Utilities ETF"),
        
        # MATERIALS ETFs
        ("XLB", "Materials Select Sector SPDR Fund"),
        ("VAW", "Vanguard Materials ETF"),
        ("FMAT", "Fidelity MSCI Materials Index ETF"),
        ("IYM", "iShares U.S. Basic Materials ETF"),
        
        # INDUSTRIAL ETFs
        ("XLI", "Industrial Select Sector SPDR Fund"),
        ("VIS", "Vanguard Industrials ETF"),
        ("FIDU", "Fidelity MSCI Industrials Index ETF"),
        ("IYJ", "iShares U.S. Industrials ETF"),
        
        # CONSUMER ETFs
        ("XLY", "Consumer Discretionary Select Sector SPDR Fund"),
        ("XLP", "Consumer Staples Select Sector SPDR Fund"),
        ("VCR", "Vanguard Consumer Discretionary ETF"),
        ("VDC", "Vanguard Consumer Staples ETF"),
        ("FDIS", "Fidelity MSCI Consumer Discretionary Index ETF"),
        ("FSTA", "Fidelity MSCI Consumer Staples Index ETF"),
        ("IYC", "iShares U.S. Consumer Discretionary ETF"),
        ("IYK", "iShares U.S. Consumer Staples ETF"),
        
        # INTERNATIONAL ETFs
        ("EFA", "iShares MSCI EAFE ETF"),
        ("EEM", "iShares MSCI Emerging Markets ETF"),
        ("IEFA", "iShares Core MSCI EAFE IMI Index ETF"),
        ("IEMG", "iShares Core MSCI Emerging Markets IMI Index ETF"),
        ("VEA", "Vanguard FTSE Developed Markets ETF"),
        ("VWO", "Vanguard FTSE Emerging Markets ETF"),
        ("FTIHX", "Fidelity Total International Index Fund"),
        ("FXNAX", "Fidelity U.S. Sustainability Index Fund"),
        ("FEZ", "SPDR EURO STOXX 50 ETF"),
        ("EWJ", "iShares MSCI Japan ETF"),
        ("EWZ", "iShares MSCI Brazil ETF"),
        ("INDA", "iShares MSCI India ETF"),
        ("FXI", "iShares China Large-Cap ETF"),
        ("MCHI", "iShares MSCI China ETF"),
        ("EWY", "iShares MSCI South Korea ETF"),
        ("EWT", "iShares MSCI Taiwan ETF"),
        ("RSX", "VanEck Russia ETF"),
        ("EWU", "iShares MSCI United Kingdom ETF"),
        ("EWG", "iShares MSCI Germany ETF"),
        ("EWC", "iShares MSCI Canada ETF"),
        
        # CRYPTOCURRENCY ETFs
        ("BITO", "ProShares Bitcoin Strategy ETF"),
        ("BITI", "ProShares Short Bitcoin Strategy ETF"),
        ("GBTC", "Grayscale Bitcoin Trust"),
        ("ETHE", "Grayscale Ethereum Trust"),
        ("GDLC", "Grayscale Digital Large Cap Fund"),
        ("BKCH", "Global X Blockchain ETF"),
        ("BLOK", "Amplify Transformational Data Sharing ETF"),
        ("LEGR", "First Trust Indxx Innovative Transaction & Process ETF"),
        
        # BROAD MARKET ETFs
        ("SPY", "SPDR S&P 500 ETF Trust"),
        ("QQQ", "Invesco QQQ Trust"),
        ("IWM", "iShares Russell 2000 ETF"),
        ("VTI", "Vanguard Total Stock Market ETF"),
        ("VOO", "Vanguard S&P 500 ETF"),
        ("VEA", "Vanguard FTSE Developed Markets ETF"),
        ("VWO", "Vanguard FTSE Emerging Markets ETF"),
        ("BND", "Vanguard Total Bond Market ETF"),
        ("AGG", "iShares Core U.S. Aggregate Bond ETF"),
        ("LQD", "iShares iBoxx $ Investment Grade Corporate Bond ETF"),
        ("HYG", "iShares iBoxx $ High Yield Corporate Bond ETF"),
        ("TLT", "iShares 20+ Year Treasury Bond ETF"),
        ("IEF", "iShares 7-10 Year Treasury Bond ETF"),
        ("SHY", "iShares 1-3 Year Treasury Bond ETF"),
        
        # VOLATILITY & INVERSE ETFs
        ("VIX", "CBOE Volatility Index"),
        ("VXX", "iPath Series B S&P 500 VIX Short-Term Futures ETN"),
        ("UVXY", "ProShares Ultra VIX Short-Term Futures ETF"),
        ("SVXY", "ProShares Short VIX Short-Term Futures ETF"),
        ("SQQQ", "ProShares UltraPro Short QQQ"),
        ("TQQQ", "ProShares UltraPro QQQ"),
        ("SPXS", "Direxion Daily S&P 500 Bear 3X Shares"),
        ("SPXL", "Direxion Daily S&P 500 Bull 3X Shares"),
        ("TNA", "Direxion Daily Small Cap Bull 3X Shares"),
        ("TZA", "Direxion Daily Small Cap Bear 3X Shares"),
        
        # DIVIDEND ETFs
        ("VYM", "Vanguard High Dividend Yield ETF"),
        ("SCHD", "Schwab US Dividend Equity ETF"),
        ("HDV", "iShares Core High Dividend ETF"),
        ("DVY", "iShares Select Dividend ETF"),
        ("VIG", "Vanguard Dividend Appreciation ETF"),
        ("DGRO", "iShares Core Dividend Growth ETF"),
        ("NOBL", "ProShares S&P 500 Dividend Aristocrats ETF"),
        ("RDVY", "First Trust Rising Dividend Achievers ETF"),
        
        # GROWTH & VALUE ETFs
        ("VUG", "Vanguard Growth ETF"),
        ("VTV", "Vanguard Value ETF"),
        ("IVV", "iShares Core S&P 500 ETF"),
        ("IVW", "iShares Core S&P U.S. Growth ETF"),
        ("IVE", "iShares Core S&P U.S. Value ETF"),
        ("MGK", "Vanguard Mega Cap Growth ETF"),
        ("MGV", "Vanguard Mega Cap Value ETF"),
        
        # SMALL CAP ETFs
        ("IWM", "iShares Russell 2000 ETF"),
        ("VB", "Vanguard Small-Cap ETF"),
        ("VTWO", "Vanguard Russell 2000 ETF"),
        ("SCHA", "Schwab U.S. Small-Cap ETF"),
        ("IJR", "iShares Core S&P Small-Cap ETF"),
        
        # MID CAP ETFs
        ("MDY", "SPDR S&P MidCap 400 ETF Trust"),
        ("VO", "Vanguard Mid-Cap ETF"),
        ("IJH", "iShares Core S&P Mid-Cap ETF"),
        ("SCHM", "Schwab U.S. Mid-Cap ETF"),
        
        # SPECIALTY & THEMATIC ETFs
        ("MOON", "Direxion Moonshot Innovators ETF"),
        ("SPACE", "Procure Space ETF"),
        ("UFO", "Procure Space ETF"),
        ("JETS", "U.S. Global Jets ETF"),
        ("AWAY", "ETFMG Travel Tech ETF"),
        ("GAMR", "Wedbush ETFMG Video Game Tech ETF"),
        ("ESPO", "VanEck Video Gaming and eSports ETF"),
        ("HERO", "Global X Video Games & Esports ETF"),
        ("DRIV", "Global X Autonomous & Electric Vehicles ETF"),
        ("IDRV", "iShares Self-Driving EV and Tech ETF"),
        ("LIT", "Global X Lithium & Battery Tech ETF"),
        ("REMX", "VanEck Rare Earth/Strategic Metals ETF"),
        ("PICK", "iShares MSCI Global Metals & Mining Producers ETF"),
        ("SIL", "Global X Silver Miners ETF"),
        ("GDX", "VanEck Gold Miners ETF"),
        ("GDXJ", "VanEck Junior Gold Miners ETF"),
        ("RING", "iShares MSCI Global Gold Miners ETF"),
        ("GLTR", "ETFS Physical Precious Metals Basket Shares"),
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
    
    # Add new ETFs that don't exist
    new_additions = 0
    for ticker, company in comprehensive_etfs:
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
    print(f"   📈 CPER and other commodity ETFs are now included!")
    
    # Verify CPER was added
    if any(ticker == 'CPER' for ticker, _ in stock_data):
        print("   ✅ CPER (United States Copper Index Fund) confirmed added!")
    
    return True

if __name__ == "__main__":
    add_comprehensive_etfs()
