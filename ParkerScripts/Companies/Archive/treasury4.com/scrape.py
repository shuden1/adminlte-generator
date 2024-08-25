from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import json
import sys

# Job Openings block selector
job_block_selector = '.css-cq05mv'

# Job title and URL selectors within the job block
job_title_selector = '.css-zepamx-Anchor.e1tt4etm0'
job_url_selector = '.css-18pvq2f-Anchor.e1tt4etm0'

# The target HTML file name should be an argument sent from an external source through the console command
target_html_file = sys.argv[1]

# Set up the Selenium Chrome WebDriver
driver = webdriver.Chrome()

# Open the local HTML file
driver.get(f"file://{target_html_file}")

# Find all job listings using the selectors defined in STEP 1
job_openings = driver.find_elements(By.CSS_SELECTOR, job_block_selector)

# Extract job titles and URLs from the listings
job_listings = []
for job in job_openings:
    title_element = job.find_element(By.CSS_SELECTOR, job_title_selector)
    link_element = job.find_element(By.CSS_SELECTOR, job_url_selector)
    title = title_element.text
    url = link_element.get_attribute('href')
    job_listings.append({"Job-title": title, "URL": url})

# Close the browser
driver.quit()

# Output the job listings in JSON format
print(json.dumps(job_listings))
