from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import json
import sys

# Extract the target HTML file name from command line argument
target_html_file = sys.argv[1]

# Initialize the WebDriver
driver = webdriver.Chrome()

# Open the target HTML file using the `file://` protocol
driver.get(f"file://{target_html_file}")

# Selectors for Job Openings blocks
job_opening_selector = '.job-board-list-wrapper .jobs-list'

# Selectors for job titles and their associated URLs within Job Openings blocks
job_title_selector = 'h2'

# Scrape job listings using the defined selectors
job_listings = []

# Find job opening blocks
job_opening_blocks = driver.find_elements(By.CSS_SELECTOR, job_opening_selector)
for job_block in job_opening_blocks:
    job_titles = job_block.find_elements(By.CSS_SELECTOR, job_title_selector)

    # Extract job titles and URLs if available
    for title_element in job_titles:
        title_text = title_element.text
        if title_text.lower() != "there are no open positions at this time.":
            anchor = title_element.find_element(By.XPATH, ".//a")
            job_listings.append({
                "Job-title": title_text,
                "URL": anchor.get_attribute('href') if anchor else None
            })

# Output the job listings as JSON
print(json.dumps(job_listings))

# Clean up by closing the WebDriver
driver.quit()
