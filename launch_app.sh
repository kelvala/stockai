#!/bin/bash

# Stock Analyzer v0.10 - Launcher Script
# This script launches the Stock Analyzer app

echo "🚀 Starting Stock Analyzer v0.10..."
echo "📈 AI-Powered Stock Analysis Tool"
echo ""

# Check if the executable exists
if [ -f "dist/StockAnalyzer" ]; then
    echo "✅ Found executable, launching..."
    ./dist/StockAnalyzer
elif [ -d "dist/StockAnalyzer.app" ]; then
    echo "✅ Found app bundle, launching..."
    open "dist/StockAnalyzer.app"
else
    echo "❌ Executable not found!"
    echo "Please run 'python3 build_standalone.py' first to build the app."
    exit 1
fi
