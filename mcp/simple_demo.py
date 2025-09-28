#!/usr/bin/env python3
import sys
import json
import time
import webbrowser
from pathlib import Path
from fastmcp import FastMCP
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import os

# Create a simple MCP server
mcp = FastMCP("Simple Demo")

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers together"""
    return a + b

@mcp.tool
def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    return a - b

@mcp.tool  
def multiply(a: int, b: int) -> int:
    """Multiply two numbers together"""
    return a * b

@mcp.tool
def divison(a:int , b: int) -> int:
    """Divides Two numbers"""
    return a/b



@mcp.tool
def create_excalidraw_square(a: int, b: int , op:str , res:int , name:str) -> str:
    """Open Excalidraw, select shape tool, and draw a square."""
    try:
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        # Launch driver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Bypass detection
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        # Open Excalidraw
        driver.get("https://excalidraw.com")
        time.sleep(3)  # Wait for the site to load fully

        # Click somewhere on the canvas to focus
        actions = ActionChains(driver)
        actions.move_by_offset(300, 300).click().perform()
        time.sleep(1)

        # Press '2' to select rectangle tool (or '8' if you want text tool)
        actions.send_keys('2').perform()
        time.sleep(1)

        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, '[data-testid="color-top-pick-\\#b2f2bb"]').click()

        # Draw a square by click-drag
        actions.click_and_hold().move_by_offset(200, 200).release().perform()

        actions.send_keys("8").perform()
        time.sleep(1)

        actions.move_by_offset(-100, -100).click().perform()
        time.sleep(1)
        actions.send_keys(f"🔥 Hi {name}\n, {a} {op} {b} = {res}").perform()

        time.sleep(1)

      # Take screenshot
        filename = "excalidraw_message.png"
        screenshot_path = f"/tmp/{filename}"
        driver.save_screenshot(screenshot_path)


        # Open screenshot
        if os.path.exists(screenshot_path):
            webbrowser.open(f"file://{screenshot_path}")

        time.sleep(2)
        driver.quit()


        return "✅ Square created successfully on Excalidraw!"

    except Exception as e:
        return f"❌ Error creating Excalidraw demo: {str(e)}"




if __name__ == "__main__":
    print("Starting Simple MCP Demo Server...", file=sys.stderr)
    mcp.run()
