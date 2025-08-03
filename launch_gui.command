#!/bin/bash
cd "$(dirname "$0")"
echo "Starting Stock Analyzer v0.14..."
echo "Current directory: $(pwd)"
echo "Python path: $(which python3)"
echo "Python version: $(python3 --version)"
echo ""
echo "Launching GUI application..."
python3 gpt_chat_gui.py
echo ""
echo "Application finished with exit code: $?"
echo "Press Enter to close this window..."
read -n 1
