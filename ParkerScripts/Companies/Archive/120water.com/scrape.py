from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import json
import sys

# STEP 1: Selectors from BeautifulSoup analysis
job_listing_selector = '.type-position'
job_title_selector = 'h3.c-loop-post_title a'

# STEP 2: Python + Selenium script
target_html_file = sys.argv[1]

# Setting up Chrome WebDriver
driver = webdriver.Chrome()
driver.get(f"file://{target_html_file}")

# Scraping job listings
job_elements = driver.find_elements(By.CSS_SELECTOR, job_listing_selector)
jobs_list = []

for job_element in job_elements:
    job_title_element = job_element.find_element(By.CSS_SELECTOR, job_title_selector)
    job_title = job_title_element.text.strip()
    job_url = job_title_element.get_attribute('href')
    jobs_list.append({"Job-title": job_title, "URL": job_url})

# Convert list to JSON format
json_output = json.dumps(jobs_list)
print(json_output)

# Close the WebDriver
driver.quit()
