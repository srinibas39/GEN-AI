#!/usr/bin/env python3
import sys
import json
import subprocess
import time
import webbrowser
from pathlib import Path
from fastmcp import FastMCP
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import io

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
def open_excalidraw() -> str:
    """Open Excalidraw in Chrome browser"""
    try:
        webbrowser.open('https://excalidraw.com')
        return "Excalidraw opened in browser successfully"
    except Exception as e:
        return f"Error opening Excalidraw: {str(e)}"

@mcp.tool
def create_excalidraw_demo(a: int, b: int , op:str) -> str:
    """Open Excalidraw, press 8 to select Text tool, and type mathematical expressions"""
    try:
        # Perform calculations
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
        wait = WebDriverWait(driver, 3)
        
        # Press 8 to select Text tool
        actions = ActionChains(driver)
        actions.send_keys('8').perform()
        time.sleep(1)
        
        # Click on canvas to start typing
        actions.move_by_offset(400, 300).click().perform()
        time.sleep(1)
        
        # Type the first mathematical expression
        actions.send_keys(f"{a} {op} {b} = {addition_result}").perform()
        time.sleep(2)
        
        # Press Enter to finish first text
        actions.send_keys('\ue007').perform()  # Enter key
        time.sleep(1)
        
        
        # Take screenshot
        screenshot_path = f"/tmp/excalidraw_demo_{int(time.time())}.png"
        driver.save_screenshot(screenshot_path)
        
        driver.quit()
        
        return f"Demo completed successfully! Screenshot saved at {screenshot_path}. Created text: '{a} + {b} = {addition_result}' and '{a} * {b} = {multiplication_result}'"
        
    except Exception as e:
        return f"Error creating Excalidraw demo: {str(e)}"


@mcp.tool
def take_screenshot(url: str, filename: str = None) -> str:
    """Take a screenshot of a webpage"""
    try:
        if filename is None:
            filename = f"screenshot_{int(time.time())}.png"
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(url)
        time.sleep(2)  # Wait for page to load
        
        screenshot_path = f"/tmp/{filename}"
        driver.save_screenshot(screenshot_path)
        driver.quit()
        
        return f"Screenshot saved at {screenshot_path}"
        
    except Exception as e:
        return f"Error taking screenshot: {str(e)}"

if __name__ == "__main__":
    print("Starting Simple MCP Demo Server...", file=sys.stderr)
    mcp.run()
