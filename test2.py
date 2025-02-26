import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import logging
from selenium.webdriver.remote.remote_connection import LOGGER

# Suppress Selenium logs
LOGGER.setLevel(logging.CRITICAL)

def scrape_collectr_price():
    url = "https://app.getcollectr.com/?query=sm158"
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--enable-unsafe-swiftshader")
    options.add_argument("--log-level=3")
    options.add_argument("--silent")

    service = Service(ChromeDriverManager().install(), log_output=os.devnull)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    time.sleep(5)

    try:
        price_tag = driver.find_element(By.TAG_NAME, "h2")  # Adjust if needed
        return price_tag.text.strip() if price_tag else "N/A"
    finally:
        driver.quit()

def scrape_pricecharting_price():
    url = "https://www.pricecharting.com/search-products?type=prices&ignore-preferences=true&q=sm158&go=Go"
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--enable-unsafe-swiftshader")
    options.add_argument("--log-level=3")
    options.add_argument("--silent")

    service = Service(ChromeDriverManager().install(), log_output=os.devnull)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    time.sleep(5)

    try:
        price_tag = driver.find_element(By.CLASS_NAME, "js-price")
        return price_tag.text.strip() if price_tag else "N/A"
    finally:
        driver.quit()

# Get the prices
collectr_price = scrape_collectr_price()
pricecharting_price = scrape_pricecharting_price()

# Create DataFrame
data = {
    "Source": ["Collectr", "PriceCharting"],
    "Price": [collectr_price, pricecharting_price]
}

df = pd.DataFrame(data)

# Save to Excel file
excel_filename = "test.xlsx"
df.to_excel(excel_filename, index=False)

print(f"Data saved to {excel_filename}")
