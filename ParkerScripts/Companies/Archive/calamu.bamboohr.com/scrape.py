from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import json
import sys

# Retrieve the HTML filename from the command line argument
html_filename = sys.argv[1]

# Selenium script to scrape the job listings
driver = webdriver.Chrome()
driver.get(f"file://{html_filename}")

# Use the selectors identified to find job listings
jobs_data = []

# Extract job titles and URLs
job_listings = driver.find_elements(By.CSS_SELECTOR, "ul > div > li > div[class*='MuiBox-root'] > a[class*='jss-']")
for job in job_listings:
    job_title = job.text.strip()
    job_url = job.get_attribute('href').strip()
    jobs_data.append({"Job-title": job_title, "URL": job_url})

# Close the driver after scraping is done
driver.quit()

# Output the scraped data as JSON
print(json.dumps(jobs_data))
