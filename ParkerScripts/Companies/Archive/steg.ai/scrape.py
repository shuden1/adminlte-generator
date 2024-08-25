from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import sys
import json

# Step 2: Selenium script

# Set up Chrome WebDriver
options = webdriver.ChromeOptions()
options.headless = True
driver = webdriver.Chrome(options=options)

# Accept the HTML file as a command line argument
html_file = sys.argv[1]

# Open the local HTML file
driver.get(f"file://{html_file}")

# Use SELECTORS from Step 1
job_blocks_selector = "div.flex.flex-col.md\\:flex-row.items-center.md\\:items-start.md\\:justify-center.px-4.w-full.max-w-\\[64rem\\]"
job_title_selector = "p.text-2xl.font-bold"
job_url_selector = "a[href]"

# Find job posting blocks
job_blocks = driver.find_elements(By.CSS_SELECTOR, job_blocks_selector)

# Iterate through job posting blocks and scrape job titles and URLs
job_listings = []

for job_block in job_blocks:
    job_title = job_block.find_element(By.CSS_SELECTOR, job_title_selector).text
    job_url = job_block.find_element(By.CSS_SELECTOR, job_url_selector).get_attribute('href')
    job_listings.append({"Job-title": job_title, "URL": job_url})

# Output the results
print(json.dumps(job_listings))

# Close the WebDriver
driver.quit()
