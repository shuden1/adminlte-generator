from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import json
import sys

# The target HTML file name is an argument sent from an external source
target_html_file = sys.argv[1]

# Set up ChromeDriver without any additional path adjustments
driver = webdriver.Chrome()

# Open the local HTML file using file:// protocol
driver.get(f"file://{target_html_file}")

# Scrape all job listings, using the selectors defined in step 1
job_openings_selector = '.job-listing, .opening'
job_title_selector = 'h2, h3, h4, h5, h6'
url_selector = 'a'

job_openings = []

# Find elements representing job openings
job_blocks = driver.find_elements(By.CSS_SELECTOR, job_openings_selector)
for job_block in job_blocks:
    # Find the job title within the job block
    job_title_element = job_block.find_element(By.CSS_SELECTOR, job_title_selector)
    job_title = job_title_element.text

    # Find the URL associated with the job title
    url_element = job_block.find_element(By.CSS_SELECTOR, url_selector)
    job_url = url_element.get_attribute('href')

    job_openings.append({"Job-title": job_title, "URL": job_url})

# Quit the driver
driver.quit()

# Output the scraped job listings as JSON
print(json.dumps(job_openings, ensure_ascii=False))
