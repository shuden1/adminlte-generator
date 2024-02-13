from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import sys

# Getting the HTML file name from the command line argument
target_html_file_name = sys.argv[1]

# Selectors defined from STEP 1
job_block_selector = '.wixui-repeater__item'
job_title_selector = '.comp-lfvpri2m3 .wixui-rich-text__text'
job_url_selector = '.comp-lfvpri2p3 a'

# Selenium Script
driver = webdriver.Chrome()
driver.get(f"file://{target_html_file_name}")

# Scraping job listings
job_listings = []
job_blocks = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
for job_block in job_blocks:
    job_title = job_block.find_element(By.CSS_SELECTOR, job_title_selector).text
    job_url = job_block.find_element(By.CSS_SELECTOR, job_url_selector).get_attribute('href')
    job_listings.append({"Job-title": job_title, "URL": job_url})

# Returning a JSON
print(json.dumps(job_listings))

# Cleanup: close the driver
driver.close()