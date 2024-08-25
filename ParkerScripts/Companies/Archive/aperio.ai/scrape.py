from bs4 import BeautifulSoup
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import json
import sys

# The input argument containing the filename of the target HTML file
filename = sys.argv[1]

# Selenium script to scrape job listings
driver = webdriver.Chrome()
driver.get(f"file:///{filename}")

# Extract job listings
jobs = []
job_listing_containers = driver.find_elements(By.CSS_SELECTOR, '.eut-row-inner.eut-bookmark')
for container in job_listing_containers:
    job_titles = container.find_elements(By.CSS_SELECTOR, 'h5')
    job_links = container.find_elements(By.CSS_SELECTOR, 'a.eut-btn.eut-btn-medium.eut-square.eut-bg-primary-2')
    for title, link in zip(job_titles, job_links):
        jobs.append({"Job-title": title.text.strip(), "URL": link.get_attribute('href')})

driver.quit()

# Construct the JSON output
json_output = json.dumps(jobs)
print(json_output)
