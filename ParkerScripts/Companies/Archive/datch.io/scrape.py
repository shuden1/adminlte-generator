from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import json
import sys

# The HTML file name to parse is provided as an argument from the console
html_file = sys.argv[1]

# Step1: Define selectors for job blocks, job titles and URLs
job_block_selector = '.about-jobs_collection-item'
job_title_selector = '.jobs-item_title'
job_url_selector = 'a.jobs-item_link-wrapper'

# Step 2: Selenium script to scrape job listings
def get_job_listings(html_file):
    # Initialize Chrome WebDriver
    driver = webdriver.Chrome()
    driver.get(f"file://{html_file}")

    # Scrape job listings
    job_listings = []
    job_blocks = driver.find_elements(By.CSS_SELECTOR, job_block_selector)

    for job_block in job_blocks:
        job_title_element = job_block.find_element(By.CSS_SELECTOR, job_title_selector)
        job_url_element = job_block.find_element(By.CSS_SELECTOR, job_url_selector)

        job_title = job_title_element.text
        job_url = job_url_element.get_attribute('href')

        job_listings.append({"Job-title": job_title, "URL": job_url})

    # Close the WebDriver session
    driver.quit()

    # Return job listings in JSON format
    return json.dumps(job_listings)

# Make sure this script does not run when imported
if __name__ == "__main__":
    job_listings_json = get_job_listings(html_file)
    print(job_listings_json)
