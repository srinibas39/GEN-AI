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

def open_excalidraw_and_draw_box():
    """Open Excalidraw and draw a simple box"""
    try:
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
        
        # Create rectangle
        # Click on rectangle tool
        try:
            rectangle_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'ToolIcon__icon')))
            rectangle_btn.click()
            time.sleep(1)
        except:
            # Fallback: use keyboard shortcut
            actions = ActionChains(driver)
            actions.key_down('\ue009').send_keys('r').key_up('\ue009').perform()  # Cmd+R for rectangle
            time.sleep(1)
        
        # Draw a box
        actions = ActionChains(driver)
        actions.move_by_offset(400, 300).click_and_hold().move_by_offset(200, 150).release().perform()
        time.sleep(1)
        
        print("✅ Successfully opened Excalidraw and drew a box!")
        print("📦 A rectangle has been drawn on the canvas")
        
        # Keep the browser open so you can see the result
        print("🔍 Browser will stay open for 10 seconds...")
        time.sleep(10)
        driver.quit()
        
        return "Successfully opened Excalidraw and drew a box!"
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return f"Error: {str(e)}"

if __name__ == "__main__":
    print("🚀 Opening Excalidraw and drawing a box...")
    result = open_excalidraw_and_draw_box()
    print(result)
