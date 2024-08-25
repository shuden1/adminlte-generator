from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import json
import sys

# Define the selectors
job_block_selector = ".jet-posts__item"
job_title_selector = ".entry-title a"
job_url_selector = "a"

# Read the target HTML filename from the argument sent from an external source
html_filename = sys.argv[1]

# Scrape the job listings
service = Service()
driver = webdriver.Chrome(service=service)

# Open the HTML file locally
driver.get(f"file://{html_filename}")

# Find all job listing blocks
job_blocks = driver.find_elements(By.CSS_SELECTOR, job_block_selector)

# Iterate over job listing blocks and extract job titles and associated URLs
jobs = []
for job_block in job_blocks:
    job_title_element = job_block.find_element(By.CSS_SELECTOR, job_title_selector)
    job_url_element = job_block.find_element(By.CSS_SELECTOR, job_url_selector)
    job_title = job_title_element.text
    job_url = job_url_element.get_attribute("href")
    jobs.append({"Job-title": job_title, "URL": job_url})

driver.quit()

# Return a JSON with the job listings
print(json.dumps(jobs))
