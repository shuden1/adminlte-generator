from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import sys

# Step 1
job_block_selector = ".positions-container .position"
job_title_selector = "h2"
job_url_selector = "a"

# Step 2
target_html_file = sys.argv[1]

# Initialize web driver
driver = webdriver.Chrome()
driver.get(f"file://{target_html_file}")

# Find job listings based on selectors
job_listings = []
job_blocks = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
for job_block in job_blocks:
    title_element = job_block.find_element(By.CSS_SELECTOR, job_title_selector)
    link_element = job_block.find_element(By.CSS_SELECTOR, job_url_selector)
    job_listing = {
        "Job-title": title_element.text,
        "URL": link_element.get_attribute('href')
    }
    job_listings.append(job_listing)

driver.quit()

# Convert the list of dictionaries to JSON format
json_output = json.dumps(job_listings)
print(json_output)