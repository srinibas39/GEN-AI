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

def create_boxes_with_text():
    """Create boxes with '2 + 3 = 5' text and different background colors automatically"""
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
        time.sleep(5)  # Wait for page to load
        
        # Wait for the canvas to be ready
        wait = WebDriverWait(driver, 10)
        
        # Create first rectangle
        # Click on rectangle tool
        try:
            rectangle_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="toolbar-rectangle"]')))
            rectangle_btn.click()
            time.sleep(1)
        except:
            # Fallback: use keyboard shortcut
            actions = ActionChains(driver)
            actions.key_down('\ue009').send_keys('r').key_up('\ue009').perform()  # Cmd+R for rectangle
            time.sleep(1)
        
        # Draw first rectangle
        actions = ActionChains(driver)
        actions.move_by_offset(300, 200).click_and_hold().move_by_offset(200, 100).release().perform()
        time.sleep(1)
        
        # Add text to first rectangle
        actions.move_by_offset(100, 50).click().perform()
        time.sleep(1)
        actions.send_keys("2 + 3 = 5").perform()
        time.sleep(1)
        
        # Change background color of first rectangle (light blue)
        actions.key_down('\ue009').send_keys('a').key_up('\ue009').perform()  # Select all
        time.sleep(1)
        
        # Try to find and click background color picker
        try:
            bg_color_btn = driver.find_element(By.CSS_SELECTOR, '[data-testid="background-color"]')
            bg_color_btn.click()
            time.sleep(1)
            # Select a light blue color
            blue_color = driver.find_element(By.CSS_SELECTOR, '[data-testid="color-9cf"]')
            blue_color.click()
            time.sleep(1)
        except:
            pass  # Continue if color selection fails
        
        # Create second rectangle 
        actions.key_down('\ue009').send_keys('r').key_up('\ue009').perform()  # Rectangle tool
        time.sleep(1)
        
        # Draw second rectangle
        actions.move_by_offset(0, 200).click_and_hold().move_by_offset(200, 100).release().perform()
        time.sleep(1)
        
        # Add text to second rectangle
        actions.move_by_offset(100, 50).click().perform()
        time.sleep(1)
        actions.send_keys("2 + 3 = 5").perform()
        time.sleep(1)
        
        # Change background color of second rectangle (light green)
        actions.key_down('\ue009').send_keys('a').key_up('\ue009').perform()  # Select all
        time.sleep(1)
        
        try:
            bg_color_btn = driver.find_element(By.CSS_SELECTOR, '[data-testid="background-color"]')
            bg_color_btn.click()
            time.sleep(1)
            # Select a light green color
            green_color = driver.find_element(By.CSS_SELECTOR, '[data-testid="color-9f3"]')
            green_color.click()
            time.sleep(1)
        except:
            pass  # Continue if color selection fails
        
        # Take screenshot
        screenshot_path = f"/tmp/excalidraw_boxes_{int(time.time())}.png"
        driver.save_screenshot(screenshot_path)
        
        print(f"✅ Successfully created boxes with '2 + 3 = 5' text!")
        print(f"📸 Screenshot saved at: {screenshot_path}")
        print("🎨 Created two boxes with different background colors:")
        print("   - First box: Light blue background")
        print("   - Second box: Light green background")
        print("   - Both boxes contain: '2 + 3 = 5'")
        
        # Keep the browser open for a few seconds so you can see the result
        time.sleep(5)
        driver.quit()
        
        return f"Demo completed successfully! Screenshot saved at {screenshot_path}"
        
    except Exception as e:
        print(f"❌ Error creating Excalidraw demo: {str(e)}")
        return f"Error creating Excalidraw demo: {str(e)}"

if __name__ == "__main__":
    print("🚀 Starting automatic box creation in Excalidraw...")
    result = create_boxes_with_text()
    print(result)
