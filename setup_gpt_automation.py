#!/usr/bin/env python3
"""
Install and setup browser automation for GPT integration
"""

import subprocess
import sys
import os

def install_selenium():
    """Install selenium and related dependencies"""
    print("🔧 Setting up browser automation for GPT integration...")
    
    try:
        # Install selenium
        print("📦 Installing selenium...")
        subprocess.run([sys.executable, "-m", "pip", "install", "selenium>=4.0.0"], check=True)
        print("✅ Selenium installed successfully")
        
        # Try to install webdriver-manager for automatic ChromeDriver management
        print("📦 Installing webdriver-manager...")
        subprocess.run([sys.executable, "-m", "pip", "install", "webdriver-manager"], check=True)
        print("✅ Webdriver-manager installed successfully")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Installation failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_automation():
    """Test if browser automation works"""
    print("\n🧪 Testing browser automation...")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.chrome.service import Service
        
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in background for test
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Create service with automatic driver management
        service = Service(ChromeDriverManager().install())
        
        # Create the driver
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Test basic functionality
        driver.get("https://www.google.com")
        title = driver.title
        driver.quit()
        
        print(f"✅ Browser automation test successful! (Page title: {title})")
        return True
        
    except ImportError:
        print("❌ Selenium not properly installed")
        return False
    except Exception as e:
        print(f"❌ Browser automation test failed: {e}")
        print("💡 You may need to install Chrome browser or update ChromeDriver")
        return False

def main():
    """Main setup function"""
    print("🚀 GPT Integration Setup")
    print("=" * 50)
    
    # Install dependencies
    if install_selenium():
        print("\n" + "=" * 50)
        
        # Test the setup
        if test_automation():
            print("\n🎉 GPT automation setup complete!")
            print("💡 Your Stock Analyzer can now automatically input tickers into ChatGPT!")
            print("🔗 When you click 'Stock Predictor', it will:")
            print("   1. Open your custom GPT")
            print("   2. Automatically enter the stock ticker")
            print("   3. Submit it for analysis")
        else:
            print("\n⚠️ Setup completed but automation test failed")
            print("💡 GPT integration will still work manually (copy/paste method)")
    else:
        print("\n❌ Setup failed")
        print("💡 GPT integration will use manual method (copy/paste)")
    
    print("\n🔄 You can run this script again anytime to test/fix the setup")

if __name__ == "__main__":
    main()
