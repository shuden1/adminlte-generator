from bs4 import BeautifulSoup
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import sys
import json

# Step 1 (Already done): Selectors
job_opening_block_selector = "ul > div"
job_title_selector = "div > a.jss-f65"
job_url_selector = "div > a.jss-f65"

# Step 2: Selenium Script
if len(sys.argv) < 2:
    raise ValueError("No target HTML file name provided")

target_html_file = sys.argv[1]

# Initialize selenium webdriver
driver = webdriver.Chrome()
driver.get(f"file://{target_html_file}")

# Find job listings
job_listings_elements = driver.find_elements(By.CSS_SELECTOR, job_opening_block_selector)
job_listings = []

for element in job_listings_elements:
    job_title_element = element.find_element(By.CSS_SELECTOR, job_title_selector)
    job_title = job_title_element.text
    job_url = job_title_element.get_attribute('href')
    job_listings.append({"Job-title": job_title, "URL": job_url})

driver.quit()

# Return the JSON
print(json.dumps(job_listings))
