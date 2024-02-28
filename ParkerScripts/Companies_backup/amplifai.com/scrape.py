from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import sys

# Get the target HTML filename from command-line argument
target_html_filename = sys.argv[1]

# Start Chrome WebDriver
driver = webdriver.Chrome()

# Open the target HTML file
driver.get(f"file://{target_html_filename}")

# Define the selectors based on previous analysis
job_block_selector = '.jobs-business-unit-wrap:not(.hide)'
job_title_selector = 'h3'
job_url_selector = '.w-inline-block'

# Scrape all job listings
jobs_data = []
job_blocks = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
for job_block in job_blocks:
    job_titles = job_block.find_elements(By.CSS_SELECTOR, job_title_selector)
    job_urls = job_block.find_elements(By.CSS_SELECTOR, job_url_selector)
    
    for title, url in zip(job_titles, job_urls):
        job_data = {
            "Job-title": title.text,
            "URL": url.get_attribute('href')
        }
        jobs_data.append(job_data)

# Quit the driver
driver.quit()

# Output the JSON
print(json.dumps(jobs_data))