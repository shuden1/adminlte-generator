from selenium import webdriver
from selenium.webdriver.common.by import By
import sys
import json

# Read the filename from command line argument
filename = sys.argv[1]

# Initialize ChromeDriver
driver = webdriver.Chrome()

# Open the local HTML file
file_path = f"file:///{filename}"
driver.get(file_path)

# Selectors from STEP 1
job_block_selector = ".eael-grid-post-holder"
job_title_selector = ".eael-entry-title a"

# Find all job listing elements
job_listings = driver.find_elements(By.CSS_SELECTOR, job_block_selector)

# Extract job titles and associated URLs
jobs_json = []
for job_listing in job_listings:
    title_element = job_listing.find_element(By.CSS_SELECTOR, job_title_selector)
    job_title = title_element.text
    job_url = title_element.get_attribute('href')
    jobs_json.append({"Job-title": job_title, "URL": job_url})

driver.quit()

# Return the JSON output
print(json.dumps(jobs_json))