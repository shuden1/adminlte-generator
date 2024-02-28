from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import sys

# Define job block and listing selectors adapted to corrections
job_block_selector = ".widget-type-rich_text"
job_title_selector = "h2 a, p a"

# Open the local html file
driver = webdriver.Chrome()
driver.get("file:///" + sys.argv[1])

# Scrape job listings
job_blocks = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
jobs = []
for job_block in job_blocks:
    job_links = job_block.find_elements(By.CSS_SELECTOR, job_title_selector)
    for job_link in job_links:
        job_title = job_link.text
        job_url = job_link.get_attribute('href')
        jobs.append({"Job-title": job_title, "URL": job_url})

# Close the driver
driver.quit()

# Print JSON result
print(json.dumps(jobs))