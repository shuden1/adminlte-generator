import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import json

# The target HTML file name is provided as a command-line argument
html_file_path = sys.argv[1]

# Set up the Chrome WebDriver
driver = webdriver.Chrome()

# Open the local HTML file in Chrome
driver.get(f'file:///{html_file_path}')

# The following selectors are based on the provided HTML structure
job_listings_selector = '.job_detail .job-title a'

# Find job listing elements
job_listings = driver.find_elements(By.CSS_SELECTOR, job_listings_selector)

# Extract job titles and URLs from the elements
jobs = []
for listing in job_listings:
    job_title = listing.text.strip()
    job_url = listing.get_attribute('href').strip()
    jobs.append({"Job-title": job_title, "URL": job_url})

# Close the WebDriver
driver.quit()

# Output the job listings as JSON
print(json.dumps(jobs))
