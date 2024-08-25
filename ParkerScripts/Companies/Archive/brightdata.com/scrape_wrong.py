from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import sys
import json

# Read HTML filename from console argument
html_filename = sys.argv[1]

# Initialize Selenium to use Chrome browser
driver = webdriver.Chrome()

# Open the HTML file
driver.get(f"file:///{html_filename}")

# Initialize an empty list to hold job postings
jobs = []

# Extract all job titles and URLs
for job_block in driver.find_elements(By.CSS_SELECTOR, ".title"):
    for job_link in job_block.find_elements(By.CSS_SELECTOR, "a"):
        title = job_link.text.strip()
        if title:  # Ensure the title is not empty
            # The URL is retrieved by JavaScript "onclick", extract job ID and build fragment URL
            job_id = job_link.get_attribute('onclick').split("'")[1]
            job_url = f"file:///{html_filename}#{job_id}"
            jobs.append({"Job-title": title, "URL": job_url})

# Close the browser
driver.quit()

# Convert job list to JSON and print
print(json.dumps(jobs))
