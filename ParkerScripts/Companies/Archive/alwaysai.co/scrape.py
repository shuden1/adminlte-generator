from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import sys
import json

# Initialize Selenium WebDriver
driver = webdriver.Chrome()

# Read the target HTML file name from the console command argument
target_html_file = sys.argv[1]

# Open the local HTML file with WebDriver
driver.get(f"file:///{target_html_file}")

# Define the CSS selectors based on the structure identified in the HTML file provided earlier
job_block_selector = '.holder__type__job_listings .border-b-2.border-gray-200'

# Locate job listing blocks
job_blocks = driver.find_elements(By.CSS_SELECTOR, job_block_selector)

# Prepare a list to store job data
jobs_data = []

# Iterate over each job block to extract the required information
for job_block in job_blocks:
    # Extract job title text
    job_title = job_block.find_element(By.CSS_SELECTOR, 'h2').text.strip()
    # Prepare URL; as per previous analysis, actual job URL details are not available (hence set as None)
    job_url = None  # No URL available in the provided HTML structure
    # Append job information to the list
    jobs_data.append({"Job-title": job_title, "URL": job_url})

# Close WebDriver
driver.quit()

# Return job data as JSON output
jobs_json = json.dumps(jobs_data)
print(jobs_json)
