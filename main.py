

import requests

"""For Scrapper"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import logging
from selenium.webdriver.remote.remote_connection import LOGGER
import time
import os

import pandas as pd

at = "wdFlFT72nG6CFayWqU54b_ON9otv_N7eMz5haRgI3IzIKPJPswPFQJ_HlG0Ru76tY7uy9WX2f6M4CL9j4wrzQ0W27DzrN6yaIy8r33z1oLlPc18NVE6ZbS3fCH37bAWzYUfNSmjHphdCaj8jUn5vUVdvXyQSbTW_YY6hP6LgEfFKWigThJ-NtWKeTolt5kGgGaDxg-6ZpNlGKo5lDqs-NJccqCo1GmIiyE76weu_umGpHpwGH94bHSR4QTdG6kSia-p0l4pDbzeUIFJHe_ZK7z79YFvKKfHtQzGJXmXPYQVUX8yQ"

print("Loading web scrapper...")
# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in the background (no GUI)
options.add_argument("--disable-gpu")  
options.add_argument("--disable-software-rasterizer")  
options.add_argument("--enable-unsafe-swiftshader")  
options.add_argument("--log-level=3")  # Suppress Chrome logs
options.add_argument("--silent") 
options.add_argument("--no-sandbox")
service = Service(ChromeDriverManager().install(), log_output=os.devnull)

LOGGER.setLevel(logging.CRITICAL)

driver = webdriver.Chrome(service=service, options=options)

def scrape_price_collectr(url):
    # Open the website
    driver.get(url)

    # Wait for JavaScript to load
    time.sleep(5)  # Adjust wait time if needed

    try:
        # Locate the price tag (modify this selector if needed)
        price_tag = driver.find_element(By.CSS_SELECTOR, "h2.text-lg.font-extrabold")

        if price_tag:
            return price_tag.text.strip()
        else:
            return "Price not found"
    except:
        pass

def scrape_price_pricechart(url):
    # Open the website
    driver.get(url)

    # Wait for JavaScript to load the price
    time.sleep(5)  # Increase wait time if needed

    try:
        # Locate the price using the class name
        price_tag = driver.find_element(By.CLASS_NAME, "js-price")

        if price_tag:
            return price_tag.text.strip()
        else:
            return "Price not found"
    except:
        pass

def add_to_inv(data):
    df = pd.DataFrame(data)

    # Path to your Excel file
    file_path = 'card_inv.xlsx'

    # Use pandas ExcelWriter with mode='a' to append the data
    with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
        try:
        # Attempt to read the existing sheet
            existing_df = pd.read_excel(file_path, sheet_name='Sheet1')
            startrow = existing_df.shape[0]  # Find the current last row
        except ValueError:
            # If the sheet does not exist, start from the top
            startrow = 0
        df.to_excel(writer, sheet_name='Sheet1', index=False, header=startrow == 0, startrow=writer.sheets['Sheet1'].max_row)
    print("Data added")


time.sleep(10)
os.system('cls')
print("Scrapper Loaded...")

while True:
    bqn = input("Enter the Cert Number: ")
    if bqn == 'q': break 

    r= requests.get(f"https://api.psacard.com/publicapi/cert/GetByCertNumber/{bqn}", headers={"Accept": "application/json",
                                                                                            "authorization": "bearer {}".format(at)})

    out = r.json()['PSACert']

    cardnum = out["CardNumber"]

    print(f"{out['Year']} - {out['Subject']} - {out['CardGrade'].split()[-1]}")
    price_collectr=scrape_price_collectr(f'https://app.getcollectr.com/?query={cardnum}')
    price_pricechart=scrape_price_pricechart(f'https://www.pricecharting.com/search-products?type=prices&q={cardnum}')
    print(f"price\nCollectr: {price_collectr}\nPriceChart: {price_pricechart}")

    data = {
        "name":[out["Subject"]],
        "year":[out["Year"]],
        "num":[cardnum],
        "grade":[out["CardGrade"]],
        "collectr":[price_collectr],
        "pricechart":[price_pricechart],
        "CertNumber":[bqn]
    }
    add_to_inv(data)
