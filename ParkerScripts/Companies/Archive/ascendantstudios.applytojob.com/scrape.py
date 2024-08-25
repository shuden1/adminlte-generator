from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import json
import sys

# The target HTML file name is received from the command line argument
html_file = sys.argv[1]

# Configure the ChromeDriver
driver = webdriver.Chrome()

# Open the local HTML file
driver.get(f"file://{html_file}")

# Scrape job listings using the defined selectors
job_opening_blocks = driver.find_elements(By.CSS_SELECTOR, ".jobs-list .list-group-item")
job_listings = []

for job_block in job_opening_blocks:
    job_title_element = job_block.find_element(By.CSS_SELECTOR, "a")
    job_title = job_title_element.text.strip()
    job_url = job_title_element.get_attribute("href")
    job_listings.append({"Job-title": job_title, "URL": job_url})

# Close the driver
driver.quit()

# Output the results as JSON
print(json.dumps(job_listings))
