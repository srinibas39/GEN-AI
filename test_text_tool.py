#!/usr/bin/env python3
import time
import webbrowser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def open_excalidraw_and_type_math():
    """Open Excalidraw, press 8 to select Text tool, and type mathematical expressions"""
    try:
        # Test with 2 + 3 and 3 * 7
        a, b = 2, 3
        addition_result = a + b
        multiplication_result = a * b
        
        # Open Chrome and Excalidraw
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # Open Excalidraw
        driver.get("https://excalidraw.com")
        time.sleep(3)  # Wait for page to load
        
        # Wait for the canvas to be ready
        wait = WebDriverWait(driver, 5)
        
        # Press 8 to select Text tool
        actions = ActionChains(driver)
        actions.send_keys('8').perform()
        time.sleep(1)
        
        # Click on canvas to start typing
        actions.move_by_offset(400, 300).click().perform()
        time.sleep(1)
        
        # Type the first mathematical expression
        actions.send_keys(f"{a} + {b} = {addition_result}").perform()
        time.sleep(2)
        
        # Press Enter to finish first text
        actions.send_keys('\ue007').perform()  # Enter key
        time.sleep(1)
        
        # Press 8 again to select Text tool for second expression
        actions.send_keys('8').perform()
        time.sleep(1)
        
        # Click at a different location for second expression
        actions.move_by_offset(0, 100).click().perform()
        time.sleep(1)
        
        # Type the second mathematical expression
        actions.send_keys(f"{a} * {b} = {multiplication_result}").perform()
        time.sleep(2)
        
        # Press Enter to finish second text
        actions.send_keys('\ue007').perform()  # Enter key
        time.sleep(1)
        
        # Take screenshot
        screenshot_path = f"/tmp/excalidraw_text_{int(time.time())}.png"
        driver.save_screenshot(screenshot_path)
        
        print("✅ Successfully opened Excalidraw and typed mathematical expressions!")
        print(f"📝 Typed: '{a} + {b} = {addition_result}'")
        print(f"📝 Typed: '{a} * {b} = {multiplication_result}'")
        print(f"📸 Screenshot saved at: {screenshot_path}")
        
        # Keep the browser open for a few seconds so you can see the result
        time.sleep(5)
        driver.quit()
        
        return f"Demo completed successfully! Screenshot saved at {screenshot_path}"
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return f"Error: {str(e)}"

if __name__ == "__main__":
    print("🚀 Opening Excalidraw and typing mathematical expressions...")
    result = open_excalidraw_and_type_math()
    print(result)
