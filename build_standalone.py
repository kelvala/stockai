#!/usr/bin/env python3
"""
Comprehensive build script for Stock Analyzer standalone executable
Supports multiple build methods: PyInstaller, cx_Freeze, and auto-py-to-exe
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

class ExecutableBuilder:
    def __init__(self):
        self.app_name = "StockAnalyzer"
        self.version = "0.12"
        self.main_script = "gpt_chat_gui.py"
        self.required_files = ["stock_data.csv", "requirements.txt", "README.md"]
        
    def check_dependencies(self):
        """Check if all required files exist"""
        print("Checking dependencies...")
        missing_files = []
        
        for file in self.required_files:
            if not os.path.exists(file):
                missing_files.append(file)
        
        if missing_files:
            print(f"❌ Missing files: {', '.join(missing_files)}")
            return False
        
        print("✅ All required files found")
        return True
    
    def install_build_tools(self):
        """Install required build tools"""
        tools = ['pyinstaller', 'cx-freeze']
        
        for tool in tools:
            try:
                print(f"Installing {tool}...")
                subprocess.run([sys.executable, "-m", "pip", "install", tool], 
                             check=True, capture_output=True)
                print(f"✅ {tool} installed successfully")
            except subprocess.CalledProcessError:
                print(f"❌ Failed to install {tool}")
    
    def build_with_pyinstaller(self):
        """Build using PyInstaller"""
        print("\n" + "="*50)
        print("Building with PyInstaller...")
        print("="*50)
        
        try:
            # Clean previous builds
            if os.path.exists("dist"):
                shutil.rmtree("dist")
            if os.path.exists("build"):
                shutil.rmtree("build")
            
            # Build command
            cmd = [
                "pyinstaller",
                "--onefile",
                "--windowed",
                "--name", self.app_name,
                "--add-data", "stock_data.csv:.",
                "--add-data", "README.md:.",
                "--add-data", "requirements.txt:.",
                "--distpath", "dist",
                "--workpath", "build",
                "--specpath", ".",
                self.main_script
            ]
            
            print(f"Running: {' '.join(cmd)}")
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            
            if os.path.exists(f"dist/{self.app_name}"):
                print("✅ PyInstaller build successful!")
                print(f"📁 Executable location: dist/{self.app_name}")
                return True
            else:
                print("❌ PyInstaller build failed - executable not found")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"❌ PyInstaller build failed: {e}")
            if e.stdout:
                print("STDOUT:", e.stdout)
            if e.stderr:
                print("STDERR:", e.stderr)
            return False
    
    def build_with_cx_freeze(self):
        """Build using cx_Freeze"""
        print("\n" + "="*50)
        print("Building with cx_Freeze...")
        print("="*50)
        
        try:
            # Clean previous builds
            if os.path.exists("build"):
                shutil.rmtree("build")
            
            cmd = [sys.executable, "setup_cx_freeze.py", "build"]
            
            print(f"Running: {' '.join(cmd)}")
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            
            if os.path.exists("build/StockAnalyzer"):
                print("✅ cx_Freeze build successful!")
                print("📁 Executable location: build/StockAnalyzer/")
                return True
            else:
                print("❌ cx_Freeze build failed - executable not found")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"❌ cx_Freeze build failed: {e}")
            return False
    
    def create_app_bundle_macos(self):
        """Create a macOS app bundle"""
        print("\n" + "="*50)
        print("Creating macOS App Bundle...")
        print("="*50)
        
        try:
            app_name = f"{self.app_name}.app"
            app_path = f"dist/{app_name}"
            
            # Create app bundle structure
            os.makedirs(f"{app_path}/Contents/MacOS", exist_ok=True)
            os.makedirs(f"{app_path}/Contents/Resources", exist_ok=True)
            
            # Copy executable
            if os.path.exists(f"dist/{self.app_name}"):
                shutil.copy2(f"dist/{self.app_name}", f"{app_path}/Contents/MacOS/")
                os.chmod(f"{app_path}/Contents/MacOS/{self.app_name}", 0o755)
            
            # Copy resources
            for file in self.required_files:
                if os.path.exists(file):
                    shutil.copy2(file, f"{app_path}/Contents/Resources/")
            
            # Create Info.plist
            plist_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>
    <string>{self.app_name}</string>
    <key>CFBundleDisplayName</key>
    <string>Stock Analyzer</string>
    <key>CFBundleIdentifier</key>
    <string>com.stockanalyzer.app</string>
    <key>CFBundleVersion</key>
    <string>{self.version}</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleExecutable</key>
    <string>{self.app_name}</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.9</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>'''
            
            with open(f"{app_path}/Contents/Info.plist", "w") as f:
                f.write(plist_content)
            
            print(f"✅ macOS App Bundle created: {app_path}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to create macOS App Bundle: {e}")
            return False
    
    def build(self):
        """Main build function"""
        print(f"Stock Analyzer v{self.version} - Executable Builder")
        print("=" * 60)
        
        # Check dependencies
        if not self.check_dependencies():
            return False
        
        # Install build tools
        self.install_build_tools()
        
        # Try PyInstaller first
        if self.build_with_pyinstaller():
            # If on macOS, create app bundle
            if sys.platform == "darwin":
                self.create_app_bundle_macos()
            
            print("\n" + "="*60)
            print("🎉 BUILD SUCCESSFUL!")
            print("="*60)
            print("Your standalone executable is ready!")
            
            if sys.platform == "darwin":
                print(f"📁 App Bundle: dist/{self.app_name}.app")
                print(f"📁 Executable: dist/{self.app_name}")
            else:
                print(f"📁 Executable: dist/{self.app_name}")
            
            print("\nYou can now distribute this to other computers!")
            print("No Python installation required on target machines.")
            
            return True
        
        # Try cx_Freeze as fallback
        elif self.build_with_cx_freeze():
            print("\n" + "="*60)
            print("🎉 BUILD SUCCESSFUL (cx_Freeze)!")
            print("="*60)
            print("Your standalone executable is ready!")
            print(f"📁 Executable folder: build/StockAnalyzer/")
            return True
        
        else:
            print("\n" + "="*60)
            print("❌ BUILD FAILED")
            print("="*60)
            print("All build methods failed. Please check the errors above.")
            return False

def main():
    builder = ExecutableBuilder()
    success = builder.build()
    
    if success:
        print("\n✅ Ready to distribute!")
    else:
        print("\n❌ Build failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
