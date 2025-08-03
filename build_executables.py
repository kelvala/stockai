#!/usr/bin/env python3
"""
Build script for Stock Analyzer GUI v0.16
Creates standalone executables for macOS and Windows
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def install_pyinstaller():
    """Install PyInstaller if not available"""
    try:
        import PyInstaller
        print("✅ PyInstaller is already installed")
    except ImportError:
        print("📦 Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller installed successfully")

def create_spec_file():
    """Create PyInstaller spec file for better control"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

import sys

block_cipher = None

a = Analysis(
    ['gpt_chat_gui.py'],
    pathex=[],
    binaries=[],
    datas=[('stock_data.csv', '.')],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.scrolledtext',
        'tkinter.messagebox',
        'yfinance',
        'pandas',
        'numpy',
        'requests',
        'urllib3',
        'certifi',
        'charset_normalizer',
        'idna',
        'pytz',
        'dateutil',
        'six',
        'threading',
        'webbrowser',
        'subprocess',
        'os',
        'sys',
        'time',
        'datetime',
        're',
        'csv',
        'math'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'scipy',
        'IPython',
        'jupyter',
        'notebook',
        'plotly',
        'PIL',
        'cv2',
        'tensorflow',
        'torch',
        'sklearn'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='StockAnalyzer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)

# macOS app bundle
if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='Stock Analyzer.app',
        icon=None,
        bundle_identifier='com.stockanalyzer.gui',
        info_plist={
            'CFBundleName': 'Stock Analyzer',
            'CFBundleDisplayName': 'Stock Analyzer - AI Powered v0.16',
            'CFBundleVersion': '0.16.0',
            'CFBundleShortVersionString': '0.16',
            'NSHighResolutionCapable': True,
            'LSMinimumSystemVersion': '10.14.0',
        }
    )
'''
    
    with open('StockAnalyzer.spec', 'w') as f:
        f.write(spec_content)
    print("✅ Created PyInstaller spec file")

def build_executable():
    """Build the executable using PyInstaller"""
    system = platform.system()
    print(f"🔨 Building executable for {system}...")
    
    # Build command
    cmd = [
        'pyinstaller',
        '--clean',
        '--noconfirm',
        'StockAnalyzer.spec'
    ]
    
    try:
        # Run PyInstaller
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            print("✅ Build completed successfully!")
            
            # Show output location
            if system == "Darwin":  # macOS
                app_path = "dist/Stock Analyzer.app"
                exe_path = "dist/StockAnalyzer"
                if os.path.exists(app_path):
                    print(f"📱 macOS App Bundle: {app_path}")
                if os.path.exists(exe_path):
                    print(f"🖥️  macOS Executable: {exe_path}")
            else:  # Windows/Linux
                exe_path = "dist/StockAnalyzer.exe" if system == "Windows" else "dist/StockAnalyzer"
                if os.path.exists(exe_path):
                    print(f"🖥️  Executable: {exe_path}")
            
            # Show size info
            try:
                if system == "Darwin" and os.path.exists(app_path):
                    size = get_folder_size(app_path)
                    print(f"📊 App Bundle Size: {size:.1f} MB")
                elif os.path.exists(exe_path.replace('.exe', '') if system != "Windows" else exe_path):
                    size = os.path.getsize(exe_path.replace('.exe', '') if system != "Windows" else exe_path) / (1024*1024)
                    print(f"📊 Executable Size: {size:.1f} MB")
            except:
                pass
                
        else:
            print("❌ Build failed!")
            print("Error output:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Build error: {e}")
        return False
        
    return True

def get_folder_size(folder_path):
    """Calculate folder size in MB"""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                total_size += os.path.getsize(filepath)
            except (OSError, FileNotFoundError):
                pass
    return total_size / (1024 * 1024)

def cleanup_build_files():
    """Clean up build artifacts"""
    import shutil
    
    cleanup_dirs = ['build', '__pycache__']
    cleanup_files = ['StockAnalyzer.spec']
    
    for directory in cleanup_dirs:
        if os.path.exists(directory):
            shutil.rmtree(directory)
            print(f"🧹 Cleaned up {directory}/")
    
    for file in cleanup_files:
        if os.path.exists(file):
            os.remove(file)
            print(f"🧹 Cleaned up {file}")

def create_distribution_info():
    """Create distribution information file"""
    system = platform.system()
    arch = platform.machine()
    
    info_content = f"""# Stock Analyzer v0.16 - Distribution Information

## Build Information
- **Version**: 0.16
- **Built on**: {system} {arch}
- **Python Version**: {sys.version}
- **Build Date**: {subprocess.check_output(['date'], text=True).strip() if system != 'Windows' else 'Windows Build'}

## Executable Locations
"""
    
    if system == "Darwin":
        info_content += """
- **macOS App Bundle**: `dist/Stock Analyzer.app`
- **macOS Executable**: `dist/StockAnalyzer`

## Installation Instructions

### macOS
1. Copy `Stock Analyzer.app` to your Applications folder
2. Right-click and select "Open" the first time (security requirement)
3. The app will launch and be available in your Applications

### Running from Terminal
```bash
./dist/StockAnalyzer
```
"""
    else:
        info_content += """
- **Windows Executable**: `dist/StockAnalyzer.exe`

## Installation Instructions

### Windows
1. Copy `StockAnalyzer.exe` to desired location
2. Double-click to run
3. Windows may show security warning - click "More info" then "Run anyway"

### Running from Command Line
```cmd
dist\\StockAnalyzer.exe
```
"""
    
    info_content += """
## Features
- ✅ AI-Powered Stock Analysis
- ✅ Real-time Stock Data via yfinance
- ✅ Intrinsic Value Calculations
- ✅ Technical Analysis (RSI, MACD, Moving Averages)
- ✅ AI Assistant Integration (Stock Predictor, Smarter Investing, Dividend Sniper)
- ✅ Finviz Screener Integration
- ✅ Autocomplete for Stock Tickers
- ✅ Clean, Modern GUI

## Requirements
- **No Python installation required** - Fully standalone executable
- **Internet connection** for stock data and AI Assistant features
- **Modern OS**: macOS 10.14+ or Windows 10+

## Troubleshooting
- If the app doesn't start, try running from terminal to see error messages
- Ensure internet connection for stock data fetching
- For macOS: Allow app in System Preferences > Security & Privacy if blocked

## Support
For issues or questions, check the project repository or documentation.
"""
    
    with open('DISTRIBUTION_INFO.md', 'w') as f:
        f.write(info_content)
    print("✅ Created distribution information file")

def main():
    """Main build process"""
    print("🚀 Stock Analyzer v0.16 - Executable Builder")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('gpt_chat_gui.py'):
        print("❌ Error: gpt_chat_gui.py not found in current directory")
        print("Please run this script from the GPT-Stock-Analyzer directory")
        return
    
    if not os.path.exists('stock_data.csv'):
        print("❌ Error: stock_data.csv not found")
        print("This file is required for the executable to work properly")
        return
    
    # Install PyInstaller
    install_pyinstaller()
    
    # Create spec file
    create_spec_file()
    
    # Build executable
    success = build_executable()
    
    if success:
        # Create distribution info
        create_distribution_info()
        
        print("\n🎉 Build completed successfully!")
        print("=" * 50)
        
        system = platform.system()
        if system == "Darwin":
            print("📱 macOS App Bundle created: dist/Stock Analyzer.app")
            print("🖥️  macOS Executable created: dist/StockAnalyzer")
            print("\n💡 To distribute:")
            print("   - Share the entire 'Stock Analyzer.app' folder for GUI experience")
            print("   - Or share just 'StockAnalyzer' executable for command-line use")
        else:
            exe_name = "StockAnalyzer.exe" if system == "Windows" else "StockAnalyzer"
            print(f"🖥️  Executable created: dist/{exe_name}")
            print(f"\n💡 To distribute: Share the 'dist/{exe_name}' file")
        
        print("\n📖 See DISTRIBUTION_INFO.md for detailed installation instructions")
        
        # Ask about cleanup
        response = input("\n🧹 Clean up build files? (y/n): ").lower()
        if response == 'y':
            cleanup_build_files()
            print("✅ Build files cleaned up")
    else:
        print("❌ Build failed. Check error messages above.")

if __name__ == "__main__":
    main()
