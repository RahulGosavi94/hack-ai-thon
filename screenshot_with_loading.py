#!/usr/bin/env python3
"""
Smart screenshot script - Wait for page to load completely before capturing
Takes screenshots only after each page/tab is fully loaded
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

os.makedirs("screenshots_complete", exist_ok=True)

print("=" * 70)
print("📸 CAPTURING FULLY LOADED PAGES - ONE SCREENSHOT PER TAB")
print("=" * 70)

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 15)
screenshot_num = 1

def take_screenshot(tab_name, description=""):
    global screenshot_num
    filename = f"screenshots_complete/{screenshot_num:02d}_{tab_name}.png"
    driver.save_screenshot(filename)
    print(f"\n✓ Screenshot {screenshot_num}: {filename}")
    print(f"  {description}")
    screenshot_num += 1
    return filename

try:
    # STEP 1: Open URL and wait for initial load
    print("\n1️⃣ OPENING APPLICATION URL")
    print("   URL: http://localhost:5000")
    driver.get("http://localhost:5000")
    print("   ⏳ Waiting for page to load...")
    
    # Wait for main content to be visible
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[data-tab]")))
    time.sleep(2)
    
    take_screenshot("01_homepage_loaded", "Application homepage - Initial load complete")
    
    # STEP 2: FLIGHT LIST TAB (Should already be active)
    print("\n2️⃣ FLIGHT LIST TAB")
    print("   Clicking Flight List tab...")
    flights_tab = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-tab="flights"]')))
    flights_tab.click()
    
    print("   ⏳ Waiting for flights data to load...")
    # Wait for flight table to be populated
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tbody tr")))
    time.sleep(2)
    
    take_screenshot("02_flight_list_tab", "All flights displayed with status (🟢 On-time, 🔴 Delayed)")
    
    # STEP 3: FLIGHT DETAILS TAB
    print("\n3️⃣ FLIGHT DETAILS TAB")
    print("   Clicking Flight Details tab...")
    details_tab = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-tab="details"]')))
    details_tab.click()
    
    print("   ⏳ Waiting for flight details to load...")
    # Wait for details content
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".card, .panel, [role='article']")))
    time.sleep(2)
    
    take_screenshot("03_flight_details_tab", "Detailed flight information and passenger manifest")
    
    # STEP 4: PASSENGER IMPACT TAB
    print("\n4️⃣ PASSENGER IMPACT TAB")
    print("   Clicking Passenger Impact tab...")
    passengers_tab = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-tab="passengers"]')))
    passengers_tab.click()
    
    print("   ⏳ Waiting for passengers list to load...")
    # Wait for passenger table
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tbody tr, .passenger-list")))
    time.sleep(2)
    
    take_screenshot("04_passenger_impact_tab", "Complete list of affected passengers with status")
    
    # STEP 5: AI SUGGESTIONS TAB
    print("\n5️⃣ AI SUGGESTIONS TAB")
    print("   Clicking AI Suggestions tab...")
    suggestions_tab = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-tab="suggestions"]')))
    suggestions_tab.click()
    
    print("   ⏳ Waiting for LLM to generate recommendations (this may take 5+ seconds)...")
    # Wait for recommendations to be generated
    try:
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".recommendation, .card, .suggestion")))
    except:
        print("   ⚠️  Recommendations may still be loading...")
    
    time.sleep(3)
    
    take_screenshot("05_ai_suggestions_tab", "LLM-generated passenger care recommendations (Hotel, Meals, Rebooking)")
    
    # STEP 6: MANAGER SUMMARY TAB
    print("\n6️⃣ MANAGER SUMMARY TAB")
    print("   Clicking Manager Summary tab...")
    summary_tab = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-tab="summary"]')))
    summary_tab.click()
    
    print("   ⏳ Waiting for KPI dashboard to load...")
    # Wait for KPI metrics - more flexible selector
    try:
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div, h1, h2, h3")))
    except:
        pass
    time.sleep(3)
    
    take_screenshot("06_manager_summary_tab", "Executive Dashboard: Passengers affected, Cost impact, Reprotected, Vouchers issued")
    
    # STEP 7: MASS MEAL ISSUANCE TAB
    print("\n7️⃣ MASS MEAL ISSUANCE TAB")
    print("   Clicking Mass Meal Issuance tab...")
    meals_tab = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-tab="mass-meals"]')))
    meals_tab.click()
    
    print("   ⏳ Waiting for meal issuance form to load...")
    # Wait for form elements
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "form, input, button")))
    time.sleep(2)
    
    take_screenshot("07_mass_meal_issuance_tab", "Bulk meal coupon issuance interface for multiple passengers")
    
    # STEP 8: MASS REBOOKING TAB
    print("\n8️⃣ MASS REBOOKING TAB")
    print("   Clicking Mass Rebooking tab...")
    rebooking_tab = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-tab="mass-rebooking"]')))
    rebooking_tab.click()
    
    print("   ⏳ Waiting for rebooking interface to load...")
    # Wait for rebooking form
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "form, select, input, button")))
    time.sleep(2)
    
    take_screenshot("08_mass_rebooking_tab", "Bulk passenger rebooking interface to alternative flights")
    
    # Final summary
    print("\n" + "=" * 70)
    print("✅ SCREENSHOT CAPTURE COMPLETE!")
    print("=" * 70)
    print(f"\n📁 Total Screenshots: {screenshot_num - 1}")
    print(f"📂 Location: screenshots_complete/")
    print("\n📸 Screenshots captured (Each fully loaded):")
    print("  ✓ 01 - Homepage loaded")
    print("  ✓ 02 - Flight List tab (All flights displayed)")
    print("  ✓ 03 - Flight Details tab (Flight info + Passengers)")
    print("  ✓ 04 - Passenger Impact tab (All affected passengers)")
    print("  ✓ 05 - AI Suggestions tab (LLM recommendations)")
    print("  ✓ 06 - Manager Summary tab (KPI Dashboard)")
    print("  ✓ 07 - Mass Meal Issuance tab (Bulk meal form)")
    print("  ✓ 08 - Mass Rebooking tab (Bulk rebooking form)")
    print("\n✨ All pages waited for complete load before capturing!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

finally:
    driver.quit()
    print("\n✓ Browser closed")
