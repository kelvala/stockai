# -*- mode: python ; coding: utf-8 -*-

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
