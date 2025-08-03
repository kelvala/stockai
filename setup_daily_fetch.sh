#!/bin/bash
"""
Daily Ticker Fetch Automation Script
Sets up cron job to run ticker fetching daily at 6 AM
"""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/fetch_comprehensive_tickers.py"
LOG_FILE="$SCRIPT_DIR/daily_ticker_fetch.log"

# Function to set up daily cron job
setup_daily_cron() {
    echo "🕐 Setting up daily ticker fetch cron job..."
    
    # Create cron job entry (runs daily at 6:00 AM)
    CRON_JOB="0 6 * * * cd $SCRIPT_DIR && python3 $PYTHON_SCRIPT >> $LOG_FILE 2>&1"
    
    # Add to crontab
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    
    echo "✅ Cron job added successfully!"
    echo "📅 Will run daily at 6:00 AM"
    echo "📝 Logs will be saved to: $LOG_FILE"
    echo ""
    echo "To view current cron jobs: crontab -l"
    echo "To remove this cron job: crontab -e (then delete the line)"
}

# Function to run manually
run_manual() {
    echo "🚀 Running ticker fetch manually..."
    cd "$SCRIPT_DIR"
    python3 "$PYTHON_SCRIPT"
}

# Function to show current cron jobs
show_cron() {
    echo "📋 Current cron jobs:"
    crontab -l
}

# Function to remove cron job
remove_cron() {
    echo "🗑️ Removing ticker fetch cron job..."
    crontab -l | grep -v "fetch_comprehensive_tickers.py" | crontab -
    echo "✅ Cron job removed"
}

# Main menu
echo "📈 Stock Ticker Daily Fetch Setup"
echo "=================================="
echo ""
echo "Choose an option:"
echo "1) Set up daily automatic fetch (6 AM)"
echo "2) Run ticker fetch manually now"
echo "3) Show current cron jobs"
echo "4) Remove daily fetch cron job"
echo "5) Exit"
echo ""

read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        setup_daily_cron
        ;;
    2)
        run_manual
        ;;
    3)
        show_cron
        ;;
    4)
        remove_cron
        ;;
    5)
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac
