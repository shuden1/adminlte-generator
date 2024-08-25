import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import json

# Get the target HTML file name from command line argument
target_html = sys.argv[1]

# Set up the Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--disable-gpu')
options.add_argument('--headless')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=options)

# Open the local HTML file
driver.get(f"file:///{target_html}")

# Scrape job listings using the selectors
job_listings = []
# Find job blocks by a consistent attribute observed in the myfiles_browser tool
for job_block in driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="job-card"]'):
    # Find job title and URL within each job block
    title_elem = job_block.find_element(By.CSS_SELECTOR, 'h3.sc-bwzfXH')
    job_title = title_elem.text.strip()
    job_url = title_elem.find_element(By.TAG_NAME, 'a').get_attribute('href')
    job_listings.append({"Job-title": job_title, "URL": job_url})

# Quit the WebDriver
driver.quit()

# Return the JSON result
print(json.dumps(job_listings, indent=2))
