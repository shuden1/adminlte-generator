from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from sys import argv
import json

# Extract the HTML file path from the input argument
html_file_path = argv[1]

# Start the WebDriver session
driver = webdriver.Chrome()
driver.get(f"file:///{html_file_path}")

# Selectors defined in STEP 1
job_listing_selector = "div.rte.scroll-trigger.animate--slide-in"
job_title_selector = "h2.zoom > a"

# List to hold job data
job_listings = []

# Identify all blocks with Job Openings
elements = driver.find_elements(By.CSS_SELECTOR, job_listing_selector)

# Extract job titles and their associated URLs
for element in elements:
    job_title_elements = element.find_elements(By.CSS_SELECTOR, job_title_selector)
    for job_title_element in job_title_elements:
        job_title = job_title_element.text
        job_url = job_title_element.get_attribute('href')
        job_listings.append({"Job-title": job_title, "URL": job_url})

# Returning JSON as a string for simplicity
print(json.dumps(job_listings))

# Clean up by quitting the driver instance
driver.quit()
