from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import sys

# The target html file name is an argument sent from an external source through the console command as the single input parameter
html_file_name = sys.argv[1]

# Initialize a new webdriver
driver = webdriver.Chrome()

# Open the local HTML file
driver.get(f"file:///{html_file_name}")

# Selectors found in STEP 1
job_items_selector = ".job-item"
job_title_selector = ".job-item-title"
job_url_selector = ".job-item-apply"

# Scrape job listings
job_items = driver.find_elements(By.CSS_SELECTOR, job_items_selector)
jobs = []

for job_item in job_items:
    job_title_element = job_item.find_element(By.CSS_SELECTOR, job_title_selector)
    job_url_element = job_item.find_element(By.CSS_SELECTOR, job_url_selector)
    job_title = job_title_element.text
    job_url = job_url_element.get_attribute('href')
    jobs.append({"Job-title": job_title, "URL": job_url})

driver.quit()

# Return JSON formatted output
print(json.dumps(jobs))