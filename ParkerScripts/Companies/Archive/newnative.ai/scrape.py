from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import json
import sys

# Get arguments from external source
html_file_name = sys.argv[1]

# Start Chrome WebDriver
driver = webdriver.Chrome()

# Function to parse job listings
def parse_job_listings(driver, job_listing_selector, job_title_selector, job_link_selector):
    driver.get(f"file://{html_file_name}")
    job_listings = driver.find_elements(By.CSS_SELECTOR, job_listing_selector)
    job_data = []
    for job_listing in job_listings:
        job_title_element = job_listing.find_element(By.CSS_SELECTOR, job_title_selector)
        job_title = job_title_element.text
        job_link = job_listing.find_element(By.CSS_SELECTOR, job_link_selector).get_attribute('href')
        job_data.append({"Job-title": job_title, "URL": job_link})
    return job_data

# Define the necessary selectors based on BeautifulSoup analysis
job_listing_selector = "article.relative.flex.flex-col.w-full.border-b"
job_title_selector = "div.flex.items-center.justify-between h2"
job_link_selector = "a.mb-2.group.rounded-lg"

# Extract job data and output as JSON
job_listings_data = parse_job_listings(driver, job_listing_selector, job_title_selector, job_link_selector)
print(json.dumps(job_listings_data))

# Clean up
driver.quit()
