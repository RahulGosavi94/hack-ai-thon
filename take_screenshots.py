#!/usr/bin/env python3
"""
Script to take screenshots of each tab in the web UI
Requires: pip install selenium pillow
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Create screenshots directory
os.makedirs("screenshots", exist_ok=True)

# Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

# Initialize Chrome driver
driver = webdriver.Chrome(options=chrome_options)

try:
    # Open the web UI
    driver.get("http://localhost:5000")
    print("✓ Opened web UI at http://localhost:5000")
    
    # Wait for page to load
    time.sleep(3)
    
    # Tab data-tab attributes and names
    tabs = [
        ("Flight List", "flights"),
        ("Flight Details", "details"),
        ("Passenger Impact", "passengers"),
        ("AI Suggestions", "suggestions"),
        ("Manager Summary", "summary"),
        ("Mass Meal Issuance", "mass-meals"),
        ("Mass Rebooking", "mass-rebooking"),
    ]
    
    # Take screenshots for each tab
    for tab_name, tab_attr in tabs:
        try:
            # Click the tab using data-tab attribute
            tab_element = driver.find_element(By.CSS_SELECTOR, f'a[data-tab="{tab_attr}"]')
            tab_element.click()
            print(f"✓ Clicked {tab_name} tab")
            
            # Wait for content to load
            time.sleep(2)
            
            # Take screenshot
            screenshot_path = f"screenshots/{tab_name.replace(' ', '_').lower()}.png"
            driver.save_screenshot(screenshot_path)
            print(f"✓ Saved screenshot: {screenshot_path}")
            
        except Exception as e:
            print(f"✗ Error with {tab_name} tab: {e}")
    
    print("\n✓ All screenshots captured successfully!")
    
finally:
    driver.quit()
